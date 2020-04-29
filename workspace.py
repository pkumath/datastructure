#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import os
import logging as log
log.basicConfig(level=log.DEBUG, format='[%(levelname)s] %(message)s - %(module)s::%(funcName)s(%(lineno)d)')#!TEMP


from globe import Globe as globe
workspace = globe.workspace

def cwd(path = None):
    if path == None: dir_root = Path(__file__).parent
    else: 
        dir_root = Path(path)
    os.chdir(dir_root)

    log.debug("CWD: %s" % os.getcwd())
    workspace['root'] = str(dir_root)
    
def sub(name):
    dir_sub = Path(workspace['root']) / name

    if not dir_sub.is_dir():
        dir_sub.mkdir(parents=True)

    log.debug("Subfolder: %s" % str(dir_sub))
    workspace['sub'][name] = str(dir_sub)

'''
def path(name):
    if name != "root":
        return Path(workspace['sub'].get(name))
    else:
        return Path(workspace['root'])'''
