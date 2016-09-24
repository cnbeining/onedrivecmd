#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: Argument parser for onedrivecmd
# Created: 09/24/2016

import argparse

from static import *

### Arguments
def parse_args():
    """None->???
    
    Argument parser of the script.
    
    Supported arguments:
    
    --version: Print version
    
    Actions, these are mutually exclusive:
    
    list: List the remote dir's content
    
    get: Fetch a remote file and put the file in a local location
    
    put: Upload a local file to the remote location
    
    delete: Delete a remote file/folder
    
    mkdir: Make a folder at remote location
    
    move: Move a remote file to a remote location
    
    sync: TODO
    
    """

    ## Parser Init
    parser = argparse.ArgumentParser()


    ## Basic functions
    parser.add_argument('--version', action = 'version', version = VER)

    # Set the config file location
    parser.add_argument('-chunk',
                        default = 10485760,
                        type = int, 
                        help = 'Set the chunk size when uploading, use with -hack, must be times of 327680')

    # Set the config file location
    parser.add_argument('-conf',
                        default = '~/onedrive.pickle',
                        help = 'Set the location of config file')

    # Whether Force hard delete or overwrite, default if False
    parser.add_argument('-force',
                        action = 'store_true',
                        default = False,
                        help = 'Force delete or overwrite when performing')

    # Whether Recursive listing folder, default if False
    parser.add_argument('-recursive',
                        action = 'store_true',
                        default = False,
                        help = 'Recursively listing folder')

    # Use downloader to download, or use multi-thread upload(highly exp)
    parser.add_argument('-hack',
                        action = 'store_true',
                        default = False,
                        help = '')

    # Only output the download links
    parser.add_argument('-url',
                        action = 'store_true',
                        default = False,
                        help = 'Only display the download link(s)')

    # Set the logging level
    parser.add_argument('-verbose',
                        action = 'store',
                        choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                        default = 'WARNING',
                        help = 'Set the logging level')


    ## Script actions
    # Set mutually exclusive actions
    parser.add_argument('mode',
                        choices = ['init', 'get', 'list', 'put', 'delete', 'mkdir', 'move', 'remote'],
                        help = """Action to be done.
                        init: Use OAuth to setup the programme
                        get: get a remote item to local
                        list: list a remote folder
                        put: put a local item to remote
                        delete: delete a remote item
                        mkdir: make a folder at remote
                        move: move a remote item to a remote location
                        remote: download a remote link to drive""")

    # Take the rest of arguments for further parsing
    parser.add_argument('rest',
                        nargs = '*',
                        help = 'Nah, placeholder for arguments')

    # Return the parsed content
    return parser.parse_args()


if __name__=='__main__':
    pass