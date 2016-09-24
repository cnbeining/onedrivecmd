#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: Session helper for onedrivecmd
# Created: 09/24/2016

import argparse

from static import *
import onedrivesdk
import logging
import os


### Session

def get_access_token(client):
    """OneDriveClient->str
    
    Get the access token that shall be used with all the request that
    would require authorization.
    
    This is just a helper function to assist with self-defined
    downloading and uploading.
    """
    return client.auth_provider.access_token.encode('utf-8')


def refresh_token(client):
    """OneDriveClient->OneDriveClient
    
    Refresh token of the client.
    
    The default expire time of one token is 3600 secs.
    """
    client.auth_provider.refresh_token()
    return


def save_session(client, path = ''):
    """OneDriveClient, str->None
    
    Save the session info in a pickle file.
    
    Not safe, but whatever.
    """
    client.auth_provider.save_session(path = path)
    return


def load_session(client, path = ''):
    """str->OneDriveClient
    
    Load a session from the storaged pickle,
    then refresh so the session is available to use immediately.
    """
    if not os.path.isfile(path):
        logging.error('Session dump path does not exist')
        raise Exception

    client.auth_provider.load_session(path = path)
    
    # refresh token so session good to use immediately
    client.auth_provider.refresh_token()

    return client


if __name__=='__main__':
    pass
