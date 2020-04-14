#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from os import system as st
#encoding: UTF-8

import sys,os
from hashlib import sha256

def which(cmd):
    ret_code = st('which {0} > /dev/null'.format(cmd))
    if ret_code == 0: return True
    else: return False

def ocr(image):

    #if len(sys.argv) < 2: sys.exit(1)

    #filename = sys.argv[1]
    #extension = filename.split('.')[-1]
    #extension = extension.lower()

    #ext_list = ['png','bmp','jpg','jpeg','jpe']
    #if not extension in ext_list: return ''
    filename = "/dev/shm/" + sha256(image).hexdigest()
    with open(filename,"wb") as fp: fp.write(image)

    ret = os.popen2('tesseract {filename} - 2>/dev/null'.format(filename=filename))[1].read()
    os.remove(filename)
    return ret

    #sys.exit(0)
