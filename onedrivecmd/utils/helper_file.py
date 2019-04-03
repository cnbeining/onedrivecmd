#!/usr/bin/env python
# coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: File, path and OS related helpers for onedrivecmd
# Created: 09/24/2016

import sys
import os

# compact Python 2.*
if sys.version_info < (3, 0):
    input = raw_input
    from urllib import unquote
else:
    from urllib.parse import unquote


## os related
def execute_cmd(cmd):
    """str->int

    Execute a command,
    send the command output to the screen,
    give a simple warning if the command failed,
    return the exit code of the command.
    """
    try:
        os.system(cmd.decode("utf-8").encode(sys.stdout.encoding))
    # python 3
    except AttributeError:
        os.system(cmd)


## file related
def file_read_seek_len(filename, from_byte, step_byte):
    """str, int, int->byte

    Read a file from particular byte to somewhere.

    Used for multi thread uploading.
    """
    with open(filename, 'rb') as f:
        f.seek(from_byte)
        return f.read(step_byte)


## path related
def path_to_name(path):
    """str->str

    Strip a file path to filename,
    which is quoted so Linux would not complain.

    Works with both od:/ and real path.
    """
    return os.path.basename(path)


def path_to_remote_path(path):
    """str->str

    Return a remote path or local path, with filename striped.

    Works with both od:/ and real path.
    """
    if path.startswith('od:'):
        path = path[3:]

    return os.path.split(path)[0]


def get_remote_path_by_item(item):
    """str->str

    Get the remote path in string for any item,
    including the root folder.

    /drive/root: cannot exist or the SDK shall throw error.
    """
    try:
        info_dict = item.to_dict()

    except AttributeError:
        # only root node does not have this attribute
        return '/'

    try:
        return unquote(item.to_dict()['parentReference']['path'] + '/' + item.to_dict()['name']).encode(
            'utf-8').replace('/drive/root:', '')
    except:
        return unquote(item.to_dict()['parentReference']['path'] + '/' + item.to_dict()['name']).replace('/drive/root:',
                                                                                                         '')


def dict_merge(a, b):
    c = a.copy()
    c.update(b)
    return c


def sizeof_fmt(num, suffix = 'B'):
    '''int, str->str

    Format file size as human readable.

    From:
    https://web.archive.org/web/20111010015624/http://blogmag.net/blog/read/38/Print_human_readable_file_size
    '''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


if __name__ == '__main__':
    pass
