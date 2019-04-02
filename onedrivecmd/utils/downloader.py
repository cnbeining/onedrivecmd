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

def download_self(client, remote_path="", local_dir="", chunksize = 10247680, url=False, hack=False):
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

    if remote_path.endswith("/") and remote_path is not "/":
        remote_path=remote_path[:-1]

    item=get_remote_item(client, path=remote_path)
    if item is None:
        print_error("Remote file", "File {path} does not exist!".format(path=remote_path))
        return False
    
    if os.path.isfile(local_dir):
        print_error("File","The dest dir {dir} is a file!".format(dir=local_dir))
        return None
    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)

    if not item.folder:
        if token_time_to_live(client) < 50*60:
            refresh_token(client)
        # fetch the file [url, size]
        item_info=get_item_temp_download_info(item)
        # if only show thr url '-url'
        if url:
            print(remote_path+": "+item_info[0])
            return True
        
        local_path=local_dir+path_to_name(remote_path)
    
        #Stamps
        print(" ")
        print_time()
        print_job_binary(remote_path,local_path)
        

        if not hack:        
            r=requests.get(item_info[0], stream=True)
            if r.status_code > 201:
                print_error("Request",str(req.status_code)+" "+r.json()["error"]["message"])
                return False
            total_length=int(item_info[1])
             
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
        else:
            cmd = 'aria2c -c -o "{local_name}" -s16 -x16 -k1M "{remote_link}"'.format(local_name=local_path, remote_link=item_info[0])
            execute_cmd(cmd)
    else:
        new_local_dir=local_dir+path_to_name(remote_path)
        item=get_remote_folder_children(client,id=item.id)
        for i in item:
            download_self(client, remote_path+"/"+i.name, new_local_dir, chunksize, url, hack)
    return True

