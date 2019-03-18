#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: Session helper for onedrivecmd
# Created: 09/24/2016

import onedrivesdk
import logging
import json
from time import time

try:
    from static import *
    from helper_file import *
except ImportError:
    from .static import *
    from .helper_file import *

### Session

def get_access_token(client):
    """OneDriveClient->str
    
    Get the access token that shall be used with all the request that
    would require authorization.
    
    This is just a helper function to assist with self-defined
    downloading and uploading.
    """
    return str(client.auth_provider.access_token)


def refresh_token(client):
    """OneDriveClient->OneDriveClient
    
    Refresh token of the client.
    
    The default expire time of one token is 3600 secs.
    """
    client.auth_provider.refresh_token()
    return

def token_time_to_live(client):
    """OneDriveClient->int
    
    Get the expiration time of token in sec. 
    
    We have to make sure the token is available. 
    """
    return int(client.auth_provider._session._expires_at - time())

## Make our own even worse Session


def save_session(client, path = ''):
    """Client, str->None
    
    Save the current status to a JSON file
    
    so can be loaded later on to resume the
    current status.
    
    Compared to pickle,
    save whether the client is Business or personal account,
    and if Business, save its API endpoint
    so we can save 1 API call to retrive the endpoint.
    
    The session JSON file is as important as the user's password.
    """
    if client.base_url == 'https://api.onedrive.com/v1.0/':
        # Normal
        status_dict = {
            'is_business': False,
            'client_id': client.auth_provider._client_id,
            'client.base_url': client.base_url,  #'https://api.onedrive.com/v1.0/'
            'client.auth_provider.auth_token_url': client.auth_provider.auth_token_url,  #'https://login.live.com/oauth20_token.srf'
            'client.auth_provider.auth_server_url': client.auth_provider.auth_server_url,  #'https://login.live.com/oauth20_authorize.srf'
            'client.auth_provider.scopes': client.auth_provider.scopes,
        }
        status_dict['client.auth_provider._session'] = dict_merge(client.auth_provider._session.__dict__,
                                                                  {'_expires_at': int(client.auth_provider._session._expires_at),
                                                                   'scope_string': ' '.join([str(i) for i in client.auth_provider._session.scope]),
                                                                   })

    else:
        # Business/office 365
        status_dict = {
            'is_business': True,
            'client_id': client.auth_provider._client_id,
            'client.base_url': client.base_url,  #'https://{.....}.sharepoint.com/_api/v2.0/'
            'client.auth_provider.auth_token_url': client.auth_provider.auth_token_url,  #'https://login.microsoftonline.com/common/oauth2/token'
            'client.auth_provider.auth_server_url': client.auth_provider.auth_server_url[0],  #'https://login.microsoftonline.com/common/oauth2/authorize'
            'client.auth_provider.scopes': client.auth_provider.scopes,  # empty for business
        }

        status_dict['client.auth_provider._session'] = dict_merge(client.auth_provider._session.__dict__,
                                                                  {'_expires_at': int(client.auth_provider._session._expires_at),
                                                                   'scope_string': ' '.join([str(i) for i in client.auth_provider._session.scope]),
                                                                   })

    status = json.dumps(status_dict)

    with open(path, "w+") as session_file:
        session_file.write(status)

    return


def load_session(client, path = ''):
    """str->Client
    
    Load a new client from the saved status file.
    """
    ## helper: making a Session from dict we get from session file
    # main entrance of function to come after this function
    def make_session_from_dict(status_dict):
        return onedrivesdk.auth_provider.Session(status_dict['client.auth_provider._session']['token_type'], 
                                                         status_dict['client.auth_provider._session']['_expires_at'] - time(), 
                                                         status_dict['client.auth_provider._session']['scope_string'], 
                                                         status_dict['client.auth_provider._session']['access_token'], 
                                                         status_dict['client.auth_provider._session']['client_id'], 
                                                         status_dict['client.auth_provider._session']['auth_server_url'],
                                                         status_dict['client.auth_provider._session']['redirect_uri'], 
                                                         refresh_token=status_dict['client.auth_provider._session']['refresh_token'], 
                                                         client_secret=status_dict['client.auth_provider._session']['client_secret'])

    ## start of function
    ## Read Session file
    try:
        with open(path, 'r') as session_file:
            status_dict = json.loads(session_file.read())
    except IOError as e:
        # file not exist or some other problems...
        logging.fatal(e.strerror)
        logging.fatal('Cannot read the session file!')
        exit()  #have to die now, or what else can we do?

    ## deterime type of account, run different logics
    # Business
    if status_dict['is_business']:
        # mock http and auth
        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(http_provider,
                                        client_id_business,
                                        auth_server_url=status_dict['client.auth_provider.auth_server_url'],
                                        auth_token_url=status_dict['client.auth_provider.auth_token_url'])

    else:
        # personal
        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(
            http_provider=http_provider,
            client_id=status_dict['client_id'],
            scopes=scopes)

    ## inject a Session in
    auth_provider._session = make_session_from_dict(status_dict)
    
    auth_provider.refresh_token()

    ## put API endpoint in
    return onedrivesdk.OneDriveClient(status_dict['client.base_url'], auth_provider, http_provider)


if __name__=='__main__':
    pass


'''

The old way that save the whole session in a pickle file.

Replaced by saving more information in JSON
in order to know whether is Business account and its API endpoint.

# def save_session(client, path = ''):
    # """OneDriveClient, str->None
    
    # Save the session info in a pickle file.
    
    # Not safe, but whatever.
    # """
    # client.auth_provider.save_session(path = path)
    # return


# def load_session(client, path = ''):
    # """str->OneDriveClient
    
    # Determine whether the session is a normal or Business one,
    # load a session from the storaged pickle,
    # then refresh so the session is available to use immediately.
    # """
    # if not os.path.isfile(path):
        # logging.error('Session dump path does not exist')
        # raise Exception
    
    # # look inside the pickle to determine whether is normal or Business
    # session_standalone =onedrivesdk.auth_provider.Session.load_session(path = path)
    
    # if session_standalone.auth_server_url == 'https://login.microsoftonline.com/common/oauth2/token':
        # # Business
            # http = onedrivesdk.HttpProvider()
            # auth = onedrivesdk.AuthProvider(http,
                                            # client_id_business ,
                                            # auth_server_url=auth_server_url,
                                            # auth_token_url=auth_token_url)

    # client.auth_provider.load_session(path = path)
    
    # # refresh token so session good to use immediately
    # client.auth_provider.refresh_token()

    # return client
'''