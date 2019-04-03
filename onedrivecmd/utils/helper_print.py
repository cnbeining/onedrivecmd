#!/usr/bin/env python 
# coding: utf-8
# Author: Dict Xiong --<me@beardic.cn>
# Purpose: print logs which may be useful to users and us maintainers too :)
# Created: 03/29/2019

import time

def print_error(error_type="",note=""):
    """ str->None

    Print structured error note.
    Chars between '\033[31m' and '\033[0m' 
    will be printed in red.
    """

    if error_type is "":
        print("\033[31m"+note+"\033[0m")
    elif note is "":
        print("\033[31m"+error_type+" error.\033[0m")
    else:
        print("\033[31m"+error_type+" error:\033[0m "+note)

def print_time():
    """

    Print time now like:
    [08:00:00]
    """
    print("["+time.strftime("%H:%M:%S",time.localtime())+"]")

def print_job_binary(source,dest):
    """str,str->None
    
    Print a job that will deal with two files
    i.e. 'put' and 'get'.
    Chars between '\033[36m' and '\033[0m'
    will be printed in blue.
    """
    print("\033[36m"+source+"\033[0m ==> \033[36m"+dest+"\033[0m")
