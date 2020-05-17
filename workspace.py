#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from appdirs import user_config_dir
import json
import os
import logging as log

from globe import Globe as globe
workspace = globe.workspace

user_dir = Path(user_config_dir("project", "ww"))
if not user_dir.is_dir():
    user_dir.mkdir(parents=True)

def cwd(path = None):
    '''设置工作路径
    '''
    if path == None: dir_root = Path(load_history())
    else: 
        dir_root = Path(path)
        set_history(path)
    os.chdir(dir_root)

    log.debug("CWD: %s" % os.getcwd())
    workspace['root'] = str(dir_root)

    # if os.path.isdir(os.getcwd()+os.path.sep+ 'figures'):
    #     pass
    # else:
    #     os.mkdir('figures')
    sub('figures')

    """ if 'root' in globe.ui:
        globe.ui['root'].title(' '.join((globe.ui['root'].title(), '@', str(dir_root.base)))) """
    
def sub(name):
    '''在工作路径中增加一个子文件夹
    '''
    dir_sub = Path(workspace['root']) / name

    if not dir_sub.is_dir():
        dir_sub.mkdir(parents=True)

    log.debug("Subfolder: %s" % str(dir_sub))
    workspace['sub'][name] = str(dir_sub)

def load_history():

    history_path = Path(user_config_dir("project", "ww")) / ".history"
    if not history_path.is_file():
        return default_history()
    
    try:
        with open(str(history_path), "r", encoding="utf-8") as history_json:
            history = json.load(history_json)
        
        path = Path(history)
        if not path.is_dir():
            return default_history()
        else:
            return str(path)
    except BaseException as err:
        log.error("Using default cwd because of: " + str(err))
        return default_history()

def default_history():
    cwd = str(Path(os.getcwd()).absolute())
    set_history(cwd)
    return cwd

def set_history(path):
    history_path = Path(user_config_dir("project", "ww")) / ".history"
    try:
        assert Path(path).is_dir()
        with open(str(history_path), "w", encoding="utf-8") as history_json:
            json.dump(path, history_json)
    except BaseException as err:
        log.error("Using default cwd because of: " + str(err))
        default_history()