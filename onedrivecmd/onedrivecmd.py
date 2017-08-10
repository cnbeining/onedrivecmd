#!/usr/bin/env python
# coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: A command line client for OneDrive
# Created: 09/23/2016

try:
    from onedrivecmd.utils.actions import *
    from onedrivecmd.utils.arguments import parse_args
    from onedrivecmd.utils.session import *
    from onedrivecmd.utils.static import *
    from onedrivecmd.utils.uploader import *
    from onedrivecmd.utils.helper_item import *
    from onedrivecmd.utils.helper_file import *
except ImportError:
    from .utils.actions import *
    from .utils.arguments import parse_args
    from .utils.session import *
    from .utils.static import *
    from .utils.uploader import *
    from .utils.helper_item import *
    from .utils.helper_file import *


def main():
    """None->None

    Main entrance of the script.

    Init the script,
    Parse arguments,
    Call the right action.
    """
    ## parse arguments
    args = parse_args()

    # mock client
    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider

    client = onedrivesdk.OneDriveClient

    ## Call action
    # Init
    if args.mode == 'init' or args.mode == 'init_business':
        client = do_init(client, args)

        # We assume that the init is successful
        print('Logged in, saving information...')

        save_session(client, path = args.conf)
        return

    ## Load session
    # If the mode is not init, there has to be a working session
    # located at the conf path.
    client = load_session(client, path = args.conf)

    # get
    if args.mode == 'get':
        do_get(client, args)

    elif args.mode == 'list':
        do_list(client, args)

    elif args.mode == 'put':
        do_put(client, args)

    elif args.mode == 'share':
        do_share(client, args)

    elif args.mode == 'direct':
        do_direct(client, args)

    elif args.mode == 'delete':
        do_delete(client, args)

    elif args.mode == 'mkdir':
        do_mkdir(client, args)

    elif args.mode == 'move':
        do_move(client, args)

    elif args.mode == 'remote':
        do_remote(client, args)

    elif args.mode == 'quota':
        do_quota(client, args)


if __name__ == '__main__':
    main()
