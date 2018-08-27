#!/usr/bin/env python
# coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: Argument parser for onedrivecmd
# Created: 09/24/2016

import argparse
import os

try:
    from static import *
except ImportError:
    from .static import *


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

    remote: remote download a link to drive
    """

    ## Parser Init
    parser = argparse.ArgumentParser()

    ## Basic functions
    parser.add_argument('--version', action = 'version', version = VER)

    # Set the config file location
    parser.add_argument('-chunk',
                        default = 62914560,
                        type = int,
                        help = 'Set the chunk size when uploading, use with -hack, must be times of 327680. Max is 62914560.')

    # Set the config file location
    parser.add_argument('-conf',
                        default = os.path.expanduser('~/.onedrive.json'),
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

    # TODO: asc when listing folder and searching. But by which field?
    parser.add_argument('-asc',
                        action = 'store_true',
                        default = False,
                        help = 'Recursively listing folder')

    # TODO: desc when listing folder and searching
    parser.add_argument('-desc',
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
                        help = 'Only display the download link(s), temp one')

    # Set the logging level
    parser.add_argument('-verbose',
                        action = 'store',
                        choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default = 'WARNING',
                        help = 'Set the logging level')
    
    # Show full path instead of short one while listing
    parser.add_argument('-fullpath',
                        action = 'store_true',
                        default = False,
                        help = 'Show full path instead of short one while listing')

    ## Script actions
    # Set mutually exclusive actions
    parser.add_argument('mode',
                        choices = ['init_business', 'init', 'get', 'list', 'put', 'delete', 'mkdir', 'move', 'remote',
                                   'quota', 'share', 'direct', 'search'],
                        help = """Action to be done.\n
                        init: Use OAuth to setup the programme\n
                        init_business: Use OAuth to setup the programme with Office 365\n
                        get: get a remote item to local\n
                        list: list a remote folder\n
                        put: put a local item to remote\n
                        delete: delete a remote item\n
                        mkdir: make a folder at remote\n
                        move: move a remote item to a remote location\n
                        remote: download a remote link to drive\n
                        search: search from your drive
                        share: get the download link of the file/folder\n
                        direct: get the direct download link of the file\n
                        quota: Get the quota of the drive""")

    # Return the parsed content
    args, rest = parser.parse_known_args()
    args.rest = rest
    return args


if __name__ == '__main__':
    pass
