#!/usr/bin/env python
# coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: Static varibles for onedrivecmd
# Created: 09/24/2016


global VER, redirect_uri, client_secret, client_id, api_base_url, scopes, discovery_uri, auth_server_url, auth_token_url

VER = 'OnedriveCMD V0.1.8'

# If you are not sure whether this is safe,
# you can register your own APP and use your own URL.
# Don't just change it: you will have error.
redirect_uri = 'https://od.cnbeining.com'

## Normal
client_secret_normal = 'RQdGA24FctsiBGuP8v3juea'
client_id_normal = 'aeba6391-92fd-437d-a9d9-33a258b96c4e'
api_base_url = 'https://api.onedrive.com/v1.0/'
scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

## Business
discovery_uri = 'https://api.office.com/discovery/'
auth_server_url = 'https://login.microsoftonline.com/common/oauth2/authorize',
auth_token_url = 'https://login.microsoftonline.com/common/oauth2/token'

# If you are working with Office 365 you may want to create your own app
# and change the following:
# You can still use https://od.cnbeining.com as redirect URL.
client_id_business = '6fdb55b4-c905-4612-bd23-306c3918217c'
client_secret_business = 'HThkLCvKhqoxTDV9Y9uS+EvdQ72fbWr/Qrn2PFBZ/Ow='

if __name__ == '__main__':
    pass
