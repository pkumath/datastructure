#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import tkinter as tk
#import importlib
#import tkinter.messagebox as messagebox
#import tkinter.filedialog as filedialog
import os
#import pyautogui as pya
#import pyperclip
#import time
import sys
#import keyboard as kd
#import inkscape_control import *
#from function import *
import threading
import paste as autopaste

import logging as log
log.basicConfig(level=log.DEBUG, format='[%(levelname)s] %(message)s - %(module)s::%(funcName)s(%(lineno)d)')

import gui
import workspace
from globe import Globe as globe

# def myglobal(value):
    # """myglobal

    # :param value:k是一个重要的全局变量,可以在文件之间相互调用和修改,方法是通过函数实现的,用来表达文本内容是否需要清空的状态.
    # """
    # global k
    # k = value

#ce = importlib.import_module('special_label')


def thread2():
    autopaste.trigger()

if __name__ == '__main__':
    # 路径处理
    """ # TODO 引入工作区机制
    figpath = os.path.split(os.path.realpath(__file__))[0]
    print('main.py',figpath)
    save_dir = "figures"+os.path.sep
    if os.path.exists(save_dir) is False:
        os.makedirs(save_dir)

    gui.figpath = figpath"""
    
    workspace.cwd()
    workspace.sub('figures')#!TEMP
    
    # GUI
    #! MOVETO: gui
    
#    menu = tk.Menu(root,tearoff = False)
    threads = []

    t2 = threading.Thread(target=thread2,args=(), name="AutopasteThread")

    threads.append(t2)
    """ for t in threads:
        t.setDaemon(True)
        t.start() """
    t2.setDaemon(True)
    t2.start()

    gui.init()
    
    log.info("Program terminated")
