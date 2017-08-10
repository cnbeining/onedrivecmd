#!/usr/bin/env python
#coding:utf-8
# Author: Beining  --<i@cnbeining.com>
# Purpose: Helpers for Item operations for onedrivecmd
# Created: 09/24/2016

import onedrivesdk

from onedrivecmd.utils import convert_utf8_dict_to_dict

try:
    from helper_file import *
except ImportError:
    from .helper_file import *


### Helper functions

## item related
def get_remote_item(client, path = '', id = ''):
    """str->A item
    
    Return a file/folder item.
    If item not exist at remote, return None.
    
    Only works with path OR id.
    """
    try:
        if path != '':  #check path
            path = od_path_to_api_path(path)
            f = client.item(drive='me', path = path).get()
        elif id != '':  #check id
            f = client.item(drive='me', id= id).get()

    except onedrivesdk.error.OneDriveError:
        # onedrivesdk.error.OneDriveError: itemNotFound - Item does not exist
        return None

    if f.folder:
        f = client.item(drive = 'me', id = f.id).children.get()

    return f


def od_path_to_api_path(path):
    """str->str
    
    In case of mixing remote stuff and local stuff,
    I am requesting a od:/path/to/file/or/folder/1.txt like remote path.
    """
    return (path[3:] if path.startswith('od:') else path)

 
def get_item_temp_download_info(item):
    """onedrivesdk.model.item.Item->(str, int, str)
    
    Get the direct download link of a file item so
    we can use tools like aria2 or make our own download.
    
    This link is only vaild for a few minutes.
    
    Return:
    
    (URL, file_size)
    
    We cannot return a hash since only personal has SHA1,
    sometimes only quickXorHash. 
    
    """
    file_info = convert_utf8_dict_to_dict(item.to_dict())
    return (file_info['@content.downloadUrl'],
            file_info['size'], )
            #file_info['file']['hashes']['sha1Hash'].encode('utf-8'))


def get_bare_item_by_path(client, path = ''):
    """str->item
    
    Just return a Item object.
    
    If not exist, return None.
    """
    return client.item(drive='me',
                       path= path_to_remote_path(path) + '/' + path_to_name(path))


if __name__=='__main__':
    pass
