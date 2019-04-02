#!/usr/bin/env python
# coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: Actions of onedrivecmd
# Created: 09/24/2016

from __future__ import unicode_literals
from collections import OrderedDict

try:
    from static import *
    from uploader import *
    from helper_file import *
    from helper_item import *
    from session import *
    from helper_print import *
    from downloader import *
except ImportError:
    from .static import *
    from .uploader import *
    from .helper_file import *
    from .helper_item import *
    from .session import *
    from .helper_print import *
    from .downloader import *

try:
    from urlparse import urlparse # python 2
except:
    from urllib.parse import urlparse

import onedrivesdk
from onedrivesdk.helpers.resource_discovery import ResourceDiscoveryRequest
from os.path import splitext

### Action

##Init
def init_business(client):
    """onedrivesdk.request.one_drive_client.OneDriveClient->onedrivesdk.request.one_drive_client.OneDriveClient

    Important: Only used for Business/Office 365!

    Init of the script.

    Let user login, get the details, save the details in a conf file.

    Used at the first time login.

    Ref:
    https://github.com/OneDrive/onedrive-sdk-python#onedrive-for-business
    https://dev.onedrive.com/auth/aad_oauth.htm#register-your-app-with-azure-active-directory
    """
    # auth url:
    # https://login.microsoftonline.com/common/oauth2/authorize?scope=wl.signin+wl.offline_access+onedrive.readwrite&redirect_uri=https%3A%2F%2Fod.cnbeining.com&response_type=code&client_id=bac72a8b-77c8-4b76-8b8f-b7c65a239ce6

    http = onedrivesdk.HttpProvider()
    auth = onedrivesdk.AuthProvider(http,
                                    client_id_business,
                                    auth_server_url = auth_server_url,
                                    auth_token_url = auth_token_url)
    auth_url = auth.get_auth_url(redirect_uri)

    # now the url looks like "('https://login.microsoftonline.com/common/oauth2/authorize',)?redirect_uri=https%3A%2F%2Fod.cnbeining.com&response_type=code&client_id=bac72a8b-77c8-4b76-8b8f-b7c65a239ce6"

    try:  # Python 2
        auth_url = auth_url.encode('utf-8').replace("('", '').replace("',)", '')
    except TypeError:
        auth_url = auth_url.replace("('", '').replace("',)", '')

    # Ask for the code
    print('ATTENTION: This is for Onedrive Business and Office 365 only.')
    print('If you are using normal Onedrive, lease exit and run')
    print('')
    print('onedrivecmd init')
    print('')
    print(auth_url)
    print('')
    print('Paste this URL into your browser, approve the app\'s access.')
    print('Copy all the code in the new window, and paste it below:')

    code = input('Paste code here: ')

    auth.authenticate(code, redirect_uri, client_secret_business, resource = 'https://api.office.com/discovery/')

    # this step is slow
    service_info = ResourceDiscoveryRequest().get_service_info(auth.access_token)[0]

    auth.redeem_refresh_token(service_info.service_resource_id)

    client = onedrivesdk.OneDriveClient(service_info.service_resource_id + '_api/v2.0/', auth, http)

    # print(client)

    return client


def init_normal(client):
    """onedrivesdk.request.one_drive_client.OneDriveClient->onedrivesdk.request.one_drive_client.OneDriveClient

    Important: Used for normal Onedrive account, NOT office 365!

    Init of the script.

    Let user login, get the details, save the details in a conf file.

    Used at the first time login.
    """

    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(
        http_provider = http_provider,
        client_id = client_id_normal,
        scopes = scopes)

    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

    auth_url = client.auth_provider.get_auth_url(redirect_uri)

    # Ask for the code
    print('ATTENTION: This is for normal Onedrive only.')
    print('If you are using Onedrive Business and Office 365,')
    print('Please exit and run')
    print('')
    print('onedrivecmd init_business')
    print('')
    print(auth_url)
    print('')
    print('Paste this URL into your browser, approve the app\'s access.')
    print('Copy all the code in the new window, and paste it below:')

    code = input('Paste code here: ')

    client.auth_provider.authenticate(code, redirect_uri, client_secret_normal)

    return client


def do_init(client, args):
    """onedrivesdk.request.one_drive_client.OneDriveClient, args->onedrivesdk.request.one_drive_client.OneDriveClient

    Init of the script.

    Let user login, get the details

    Used at the first time login.
    """
    if args.mode == 'init_business':
        client = init_business(client)
    else:
        client = init_normal(client)

    return client


## Others
def do_get(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Get a remote files information,
    then get the temp download link that is only vaild for a couple of minutes,
    download it with a homebrew single-thread downloader with progress bar,
    or call aria2 to do the download.
    """
    if not args.rest[-1].startswith('od:/'):
        local_dir=args.rest[-1]
        if local_dir.endswith("/") and local_dir is not "/":
            local_dir=local_dir[:-1]
        args.rest=args.rest[:-1]
    else:
        local_dir='.'

    for f in args.rest:
        if not f.startswith("od:/"):
            continue
        download_self(client=client, 
                      remote_path=f,
                      local_dir=local_dir,
                      url=args.url,
                      hack=args.hack)
    return client


def do_share(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Get a remote file/folder's information,
    then create share link of such item,
    and print it.

    Supposedly this is a permanent link.
    """

    for f in args.rest:

        # get a file item
        item = get_remote_item(client, path = f)

        # some error handling
        if item is None:
            print_error("Remote file", "File {path} does not exist!".format(path = f))
            #logging.warning('File {path} do not exist!'.format(path = f))
            return None

        permission = client.item(id = item.id).create_link("view").post()

        print(permission.link.web_url.replace('15/guestaccess.aspx', '15/download.aspx'))

    return client


def do_direct(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Get a remote file/folder's information,
    then create share link of such item,
    convert the link to direct link,
    and print it.

    Supposedly this is a permanent link. Could use another 301 to final link.
    """

    for f in args.rest:

        # get a file item
        item = get_remote_item(client, path = f)

        # some error handling
        if item is None:
            print_error("Remote file", "File {path} does not exist!".format(path = f))
            break

        permission = client.item(id = item.id).create_link("view").post()

        if 'sharepoint.com' in permission.link.web_url:  # office 365
            # link like:
            # https://xxx-my.sharepoint.com/:b:/g/personal/xx_xxx_onmicrosoft_com/blah-blah
            parsed_uri = urlparse(permission.link.web_url)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri = parsed_uri) #https://xxx-my.sharepoint.com/
            resid = str(parsed_uri.path.split('/')[-1]) # blah-blah
            user_info = str(parsed_uri.path.split('personal/')[1].split('/')[0]) # xxx_xxxxxx_onmicrosoft_com

            # Use the original file extension for the URL
            extention = str(splitext(item.name)[1])

            direct_link = domain + 'personal/' + user_info + '/_layouts/15/download.aspx?share=' + resid
            if len(extention[1]) > 0:
                direct_link += '&ext=' + extention

            print(direct_link)
            

        if '1drv.ms' in permission.link.web_url:  # personal
            # link like: https://1drv.ms/u/s!blahblah
            req = requests.get(permission.link.web_url, allow_redirects = False)
            if req.status_code > 201:
                print_error("Request", str(req.status_code)+" "+req.json()['error']['message'])
                return None
            # link become: https://onedrive.live.com/redir?resid=xxx!111&authkey=!xxx
            print(req.headers['Location'].replace('redir?', 'download?'))

    return client


def do_list(client, args, lFolders = None):
    """OneDriveClient, [str], str -> OneDriveClient

    List the content of a remote folder,
    with possbility of doing a recurrsive listing.

    If the user is using both flag recurrsive and multiple targets,
    or listing a huge drive at its root folder,
    the programme can just...crash. But who cares? I do not own Microsoft.
    """

    is_recursive = args.recursive
    show_fullpath = args.fullpath

    # recursive call
    if isinstance(lFolders, list):
        folder_list = lFolders
    else:  # first call
        folder_list = args.rest

    # Nothing provided. Instead of giving a error, list the root folder
    if folder_list == []:
        folder_list.append('/')

    for path in folder_list:
        # get the folder entry point
        curPath=path
        if not curPath.endswith("/"):
            curPath=curPath+"/"
        folder = get_remote_item(client, path = curPath)
        
        if not folder.folder:
            print_error("Remote item", curPath+" is not a folder!")
            return client
        else:
            folder=get_remote_folder_children(client, id=folder.id)

        for i in folder:
            if show_fullpath:
                name = 'od:' + curPath + '/' + i.name
            else:
                # if name start with 'od:/', users may think it was in the root directory '/'
                name = 'od:' + i.name

            if i.folder:
                # make a little difference so the user can notice
                name += '/'

                # handle recursive
                if is_recursive:
                    do_list(client, args, [curPath + i.name + '/'])

            # format as megacmd

            # for some machines a time data does not not match error will be raised
            # for whatever reason so I just put a whatever patch here
            try:
                created_date_time = i.created_date_time.strftime(i.DATETIME_FORMAT)
            except ValueError as e:
                created_date_time = i._prop_dict["createdDateTime"]

            print('{name}\t{size}\t{created_date_time}'.format(name = name,
                                                               size = i.size,
                                                               created_date_time = created_date_time))

    return client


def do_put(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Put local item(s) to a remote FOLDER.

    If no remote dir is specfied, will upload to root dir.

    A home brew uploading option is provided to show progress bar
    and manually adjust chunk size.

    The chunk size should be times of 320KiB, or shoot could happen:
    https://dev.onedrive.com/items/upload_large_files.htm#best-practices
    """
    # set target dir
    if not args.rest[-1].startswith('od:/'):
        from_list = args.rest
        target_dir = 'od:/'

    else:
        from_list = args.rest[:-1]
        target_dir = args.rest[-1]

        # fix python cannot split path without / at end
        if not target_dir.endswith('/'):
            target_dir += '/'

    for i in from_list:
        # SDK one
        # ONLY USED WITH HACK
        if args.hack:
            upload_self_hack(client=client,
                             source_file = i,
                             dest_path = target_dir)
            #client.item(drive = "me", path = target_dir[3:-1]).upload_async(i)

        # Home brew one, with progress bar
        else:
            upload_self(client = client,
                        source_file = i,
                        dest_path = target_dir,
                        chunksize = int(args.chunk))

    return client


def do_delete(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Move an item into trash bin.

    The folder must be empty before being deleted.

    There is currently NO WAY of permanently deleting an item via API/SDK.

    Somehow the SDK does not have this function.
    """
    for i in args.rest:
        if i.startswith('od:/'):  # is somewhere remote
            f = get_remote_item(client, path = i)
            
            # make the request, we have to do it ourselves
            req = requests.delete(client.base_url + '/drive/items/{id}'.format(id = f.id),
                                  headers = {'Authorization': 'bearer {access_token}'.format(
                                      access_token = get_access_token(client)), })
            if req.status_code is not 204:
                print_error("Request", str(req.status_code)+" "+req.json()['error']['message'])
                return None

    return client


def do_mkdir(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Make a remote folder.

    This is NOT a recursive one: the father folder must exist.

    The SDK somehow refuse to work. Have to use API.
    """
    for folder_path in args.rest:
        if folder_path.startswith('od:'):
            folder_path = folder_path[3:]

        # make sure we are making the right folder
        if folder_path.endswith('/'):
            folder_path = folder_path[:-1]

        parent_path = os.path.dirname(folder_path)

        req = requests.get(client.base_url + '/drive/root:{parent_path}'.format(parent_path = parent_path),
                           headers = {'Authorization': 'bearer {access_token}'.format(
                               access_token = get_access_token(client)),
                               'Content-Type': 'application/json',
                               'Prefer': 'respond-async', })

        if req.status_code > 201:
            print_error("Request",str(req.status_code)+" "+req.json()['error']['message'])
            return None

        req = convert_utf8_dict_to_dict(req.json())
        parent_id = req['id']

        data = OrderedDict([
            ("name", path_to_name(folder_path)),
            ("folder", {})
        ])

        req = requests.post(client.base_url + '/drive/items/{parent_id}/children'.format(parent_id = parent_id),
                            headers = {'Authorization': 'bearer {access_token}'.format(
                                access_token = get_access_token(client)),
                                'Content-Type': 'application/json',
                                'Prefer': 'respond-async', },
                            json = data)

        if req.status_code > 201:
            print("\033[31mRequest error:\033[0m "+req.json()['error']['message'])
            return None

        req = convert_utf8_dict_to_dict(req.json())

        if not req['name']:
            print_error("Remote file", "Cannot create {folder_path}".format(folder_path = folder_path))
            return None

    return client


def do_move(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Move a remote item to a remote location.

    Also can be used to rename.

    Not working so well....
    """
    from_location = args.rest[0]
    to_location = args.rest[1]

    # rename
    if path_to_remote_path(from_location) == path_to_remote_path(to_location):
        renamed_item = onedrivesdk.Item()
        renamed_item.name = path_to_name(to_location)

        get_bare_item_by_path(client, from_location).update(renamed_item)
        return client

    # real move
    moved_item = onedrivesdk.Item()
    to_item = get_bare_item_by_path(client, to_location)

    # if target is folder, put the item under
    if to_item.folder:
        moved_item.parent_reference = to_item
        get_bare_item_by_path(client, from_location).update(renamed_item)


def do_remote(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Do a remote upload to the Drive.

    A link will be shown to get the current state of uploading.

    This is ONLY vaild for PERSONAL!

    args.rest: list of remote URLs.
    """
    for i in args.rest:
        # There is no guarantee that this shall be normal, JUST like
        # all the similar services
        json_data = OrderedDict([('@content.sourceUrl', i), ('file', {}), ('name', path_to_name(i))])

        root = client.item(drive = 'me', id = 'root').get()
        parent_id = root.id

        req = requests.post(client.base_url + 'drive/items/{parent_id}/children'.format(parent_id = parent_id),
                            data = json.dumps(json_data),
                            headers = {'Authorization': 'bearer {access_token}'.format(
                                access_token = get_access_token(client)),
                                'Content-Type': 'application/json',
                                'Prefer': 'respond-async', })
        if req.status_code > 201:
            print_error("Request", str(req.status_code)+" "+req.json()['error']['message'])
            return None
        print(req.headers['location'])

    return client


def do_quota(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Check the quota of the drive and print the data.

    A link will be shown to get the current state of uploading.

    Details of the states:
    https://dev.onedrive.com/facets/quotainfo_facet.htm

    WARNING:
    At least for Business account,
    "used" is not returned, UNLIKE stated in the documentation!
    """
    req = requests.get(client.base_url + 'drive/',
                       headers = {
                           'Authorization': 'bearer {access_token}'.format(access_token = get_access_token(client)),
                           'content-type': 'application/json'})
    if req.status_code > 201:
        print_error("Request", str(req.status_code)+" "+req.json()['error']['message'])
        return None
    print('''
    Total Size: {total},
    Used: {used},
    Remaining: {remaining},
    Deleted: {deleted},

    Your state is: {state}
    '''.format(total = sizeof_fmt(req.json()['quota']['total']),
               used = sizeof_fmt(req.json()['quota']['total'] - req.json()['quota']['remaining']),
               remaining = sizeof_fmt(req.json()['quota']['remaining']),
               deleted = sizeof_fmt(req.json()['quota']['deleted']),
               state = req.json()['quota']['state']
               )
          )

    return client


def do_search(client, args):
    """OneDriveClient, [str] -> OneDriveClient

    Search the drive and get list of files.

    A link will be shown to get the current state of uploading.

    Details of the states:
    https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_search
    """



    # reuse session for faster multi page query
    requests_session = requests.Session()

    search_query = ' '.join(args.rest)

    search_url = client.base_url + "drive//root/search(q='{search_query}')".format(search_query = search_query)

    access_token = get_access_token(client)

    item_list = get_search_item_list_single_page_by_url_rec(requests_session, access_token, search_url, item_list = [])

    for item in item_list:
        print('{id}\t{name}\t{size}\t{created_date_time}'.format(id = item['id'],
                                                                 name = item['name'],
                                                                 size = item['size'],
                                                                 created_date_time = item['lastModifiedDateTime']
                                                                 ))

    return client


if __name__ == '__main__':
    pass

"""
The old do_get

        # if directly download, use the build in download() method
        # this method does not have any verbose so good luck with your
        # life downloading large files.
        # It would not be so miserble since OneDrive solely support filesize
        # as huge as 10GiB, and 2GiB for Business accounts. Yay!
        logging.info('Downloading {local_name}'.format(local_name = local_name))
        client.item(drive='me', id=item.id).download('./' + local_name)
"""
