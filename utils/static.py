#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: Static varibles for onedrivecmd
# Created: 09/24/2016


global VER, redirect_uri, client_secret, client_id, api_base_url, scopes

VER = 'OnedriveCMD V0.0.1'

redirect_uri = 'https://od.cnbeining.com'
client_secret = 'RQdGA24FctsiBGuP8v3juea'
client_id='aeba6391-92fd-437d-a9d9-33a258b96c4e'
api_base_url='https://api.onedrive.com/v1.0/'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']


if __name__=='__main__':
    pass
