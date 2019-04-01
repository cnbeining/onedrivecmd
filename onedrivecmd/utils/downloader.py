#!/usr/bin/env python
# coding:utf-8
# Author: Dict Xiong  --<me@beardic.cn>
# Purpose: File downloader
# Create: 04/01/2019

from progress.bar import Bar
import requests

try:
    from static import *
    from helper_file import *
    from helper_print import *
    from helper_item import *
    from session import *
except ImportError:
    from .static import *
    from .helper_file import *
    from .helper_print import *
    from .helper_item import *
    from .session import *

def download_self(client, remote_path="", local_dir="", chunksize = 10247680, url=False):
    """ OneDriveClient, str, str, int, Bool -> Bool

    Download a file with in our own way
    with progress bar.
    This should be better than the built-in one
    since that one does not comes with any bar, not even a callback point.
    From http://stackoverflow.com/a/20943461/2946714
    This is slower than I thought.

    """
    if not local_dir.endswith("/"):
        local_dir+="/"

    item=get_remote_item(client, path=remote_path)
    if item is None:
        print_error("Remote file", "File {path} does not exist!".format(path=f))
        return False
    # fetch the file [url, size]
    item_info=get_item_temp_download_info(item)
    # if only show thr url '-url'
    if url:
        print(remote_path+": "+item_info[0])
        return True
    
    local_path=local_dir+path_to_name(remote_path)

    r=requests.get(item_info[0], stream=True)
    if r.status_code > 201:
        print_error("Request",str(req.status_code)+" "+r.json()["error"]["message"])
        return False
    total_length=int(item_info[1])
    
    # Stamps
    print(" ")
    print_time()
    print_job_binary(remote_path,local_path)

    # bar init
    bar=Bar('Downloading', max = total_length / chunksize, suffix = '%(percent).1f%% - %(eta)ds')
    # Save file as chunk, upload Bar as chunk written
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunksize):
            if chunk:
                f.write(chunk)
                f.flush()
                bar.next()
        bar.finish()
    return True



