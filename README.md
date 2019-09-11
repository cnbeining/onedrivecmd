onedrivecmd
=======

<a href="https://996.icu"><img src="https://img.shields.io/badge/link-996.icu-red.svg"></a>

A command line client for Onedrive(including Office 365 and Business).

Based on [onedrive-sdk-python](https://github.com/OneDrive/onedrive-sdk-python) , with lots of modifications.

This is very much a copycat of [megacmd](https://github.com/t3rm1n4l/megacmd) , but in different language.

### Why onedrivecmd?
Onedrive is a cloud-storage service provided by Microsoft. Education users can get 1TB of storage for free, which can be redeemed at https://products.office.com/en-us/student?tab=students .

Since the recent update of Onedrive's API, there aren't a lot of *nix softwares that would provide support to Onedrive, most of them are syncing softwares: But I prefer have more control of what I am doing. So here it is, a tiny client that can do the jobs for you.

### Features
  - Ability to access files and folders using a path URI
  - Configuration file (~/.onedrive.json)
  - Folder/file get operations, and retry when failed (experimental)
  - Folder/file put operations, and retry when failed (experimental)
  - List operation (shows file size and timestamp)
  - Download and upload with native progress bar (with option of downloading with aria2!)
  - Remote download links to your drive(NEW! Not even available via Web console) (Only available at personal due to API limit)
  - Supports Office 365!
  - Python 2 and 3 compatible. Tested with lots of cases but please report if it is not working somehow.
  - Get share link and direct download link!

## Install

As easy as: ```pip install onedrivecmd```!

Also you can clone this project, then execute ```python3 setup.py install``` or ```python setup.py install```

### Usage
    Usage onedrivecmd:
        onedrivecmd -h 
        onedrivecmd [OPTIONS] init
        onedrivecmd [OPTIONS] init_business
        onedrivecmd [OPTIONS] list od:/foo/bar/
        onedrivecmd [OPTIONS] share od:/foo/doc.txt
        onedrivecmd [OPTIONS] direct od:/foo/image.jpg
        onedrivecmd [OPTIONS] get od:/foo/file.txt /tmp/
        onedrivecmd [OPTIONS] get od:/boo/dir/ ./localdir/
        onedrivecmd [OPTIONS] put /tmp/hello.txt od:/bar/
        onedrivecmd [OPTIONS] put /tmp/dir/ od:/bar/
        onedrivecmd [OPTIONS] delete od:/foo/bar
        onedrivecmd [OPTIONS] mkdir od:/foo/bar/
        onedrivecmd [OPTIONS] search foobar
        onedrivecmd [OPTIONS] remote http://thecatapi.com/api/images/get?format=src&type=gif
        onedrivecmd [OPTIONS] quota


      -conf="~/onedrive.json": Config file path, this file is as important as your password!
      -h: Help
      -hack: Use aria2 to download file, or the SDK's built-in uploader (without progress bar!)
      -recursive=false: Recursive listing
      -chunk=62914560: Chunk size when uploading 
      -url=False: Only display the URL when downloading, temp one



### How to run onedrivecmd?

#### Install dependencies

*Only when you are installing from source code*

There are 3 packages you should install:

```
onedrivesdk < 2
progress
requests
```

Do a ```pip install -r requirements.txt``` at the folder.

#### Login

Do a ```onedrivecmd init``` , or ```onedrivecmd init_business``` if you are using Business or Office 365.

You shall be given a URL like

```
https://login.live.com/oauth20_authorize.srf?scope=wl.signin+wl.offline_access+onedrive.readwrite&redirect_uri=https%3A%2F%2Fod.cnbeining.com&response_type=code&client_id=aeba6391-92fd-437d-a9d9-33a258b96c4e
```

Authorize your login. 

Yes you shall be redirected to ```https://od.cnbeining.com/```, which apparently is owned by me. This page is hosted at [branch gh-pages](https://github.com/cnbeining/onedrivecmd/blob/gh-pages/index.html), with a Cloudflare at the front. I am doing this so you can just do a quick select-all and paste. If you have doubt, change the information in ```static.py```.

The login information is storaged at ```~/.onedrive.json```, or any location you demanded. This file should be treated as secret as your password.

After this very first time init, the ```access_token``` shall be refreshed every time you run the programme.


### Pitfalls
To list directory contents, use:

    $ onedrivecmd list od:/foo/bar/

Names ending with '/' is a directory. The size of directory is the size of the sum of its content.

To recursively list a directory use, -recursive option.

    $ onedrivecmd -recursive list od:/foo/bar/

The delete can only move the item to the trash bin, as there is no way of just delete the item. Make sure you clean your trash.

    $ onedrivecmd delete od:/foo/bar/file


### Examples

    $ onedrivecmd  init
    
    https://login.live.com/oauth20_authorize.srf?scope=wl.signin+wl.offline_access+onedrive.readwrite&redirect_uri=https%3A%2F%2Fod.cnbeining.com&response_type=code&client_id=aeba6391-92fd-437d-a9d9-33a258b96c4e
    
    Paste this URL into your browser, approve the app's access.
    Copy all the code in the new window, and paste it below:
    Paste code here: Ma0d6f772-****-e5ea-8d5a-******    
    
    $ onedrivecmd  init_business
    ATTENTION: This is for Onedrive Business and Office 365 only.
    If you are using normal Onedrive, lease exit and run
    
    onedrivecmd init
    
    https://login.microsoftonline.com/common/oauth2/authorize?redirect_uri=https%3A%2F%2Fod.cnbeining.com&response_type=code&client_id=6fdb55b4-c905-4612-bd23-306c3918217c
    
    Paste this URL into your browser, approve the app's access.
    Copy all the code in the new window, and paste it below:
    Paste code here: (Very long!)

    $ onedrivecmd list od:/
    od:/133/	0	2016-09-24T04:17:58.957000Z
    od:/134/	0	2016-09-24T05:11:17.190000Z
    od:/New Folder/	351	2016-09-22T03:02:25.423000Z
    od:/1.png	342677	2016-09-24T04:28:51.617000Z
    od:/OneDrive 入门.pdf	1159342	2016-08-23T03:03:55.043000Z

    $ onedrivecmd put /tmp/demo/ od:/test/
    
    [2019-03-19 11:57:07]
    /tmp/demo/index.html ==> od:/test/demo/index.html
    Uploading |################################| 100.0% - 0s

    [2019-03-19 11:57:26]
    /tmp/demo/Pic/1.png ==> od:/test/demo/Pic/1.png
    Uploading |################################| 100.0% - 0s

    [2019-03-19 11:57:44]
    /tmp/demo/Pic/2.png ==> od:/test/demo/Pic/2.png
    Uploading |################################| 100.0% - 0s

    [2019-03-19 11:58:03]
    /tmp/demo/Pic/test/365.ps1 ==> od:/test/demo/Pic/test/365.ps1
    Uploading |################################| 100.0% - 0s

    [2019-03-19 11:58:22]
    /tmp/demo/Pic/3.jpg ==> od:/test/demo/Pic/3.jpg
    Uploading |################################| 100.0% - 0s

    $ onedrivecmd get od:/1.pdf
    Downloading |######                          | 21.4% - 74s

    # personal
    $ onedrivecmd share od:/1.png
    https://1drv.ms/u/s!AnpifX1Elagmb_7sFIiyr2ipY1k
    
    $ onedrivecmd direct od:/1.png
    https://onedrive.live.com/download?resid=26A895447D7D627A!111&authkey=!AP7sFIiyr2ipY1k
    
    # Office 365
    $ onedrivecmd share od:/onedrive.json
    https://ad-my.sharepoint.com/personal/email/_layouts/15/guestaccess.aspx?docid=xxx&authkey=xxx

    $ onedrivecmd direct od:/onedrive.json
    https://ad-my.sharepoint.com/personal/email/_layouts/15/download.aspx?docid=md5&authkey=xxx

    $ onedrivecmd -hack get od:/1.png
    [#e257f9 16KiB/334KiB(4%) CN:1 DL:230KiB ETA:1s]                                                                                                                            
    09/24 02:10:56 [NOTICE] Download complete: **onedrivecmd/1.png
    
    Download Results:
    gid   |stat|avg speed  |path/URI
    ======+====+===========+=======================================================
    e257f9|OK  |   343KiB/s|**onedrivecmd/1.png
    
    Status Legend:
    (OK):download completed.
    
    $ onedrivecmd search file.txt
    01DERSD4MVUNK66BVQRFFZZEDK7FILJSYS	file.txt	1073741824	2017-08-30T05:55:24Z
    01DERSD4JFGCT7P2VFFVEI3KXDPASSCX2H	files.txt	89	2017-08-30T05:46:38Z

    $ onedrivecmd mkdir od:/145

    $ onedrivecmd remote "http://wscont2.apps.microsoft.com/winstore/1x/.../Screenshot.225037.100000.jpg"
    https://api.onedrive.com/v1.0/monitor/...

    $ onedrivecmd quota
    
    Total Size: 1.0TiB,
    Used: 1.6MiB,
    Remaining: 1024.0GiB,
    Deleted: 0.0B,
    
    Your state is: normal

### TODO

* Recursive 'mkdir'.
* Perfect retry-when-failed function.
* Move
* Code refactoring
* I will not write sync since we have [rclone](https://github.com/ncw/rclone) which already supports Onedrive. Feel free to send me pull requests though.
* I cannot think of anything. Open issues if you have amazing ideas.

### How to Contribute ?

Any PR or issue would be appreciated. 

### License

AGPL

### Author

Beining, https://www.cnbeining.com/ , ```i [at] cnbeining.com``` .

Driven by coffee, coffee and coffee.


Collaborator/Dict Xiong, https://beardic.cn/, ```me [at] beardic.cn```.

Furkan ÖZOĞUL (https://gitlab.com/ozogulf ) solved the SDK issue.  


### 中文说明

[点这里](https://github.com/cnbeining/onedrivecmd/wiki/%E4%B8%AD%E6%96%87%E8%AF%B4%E6%98%8E)
