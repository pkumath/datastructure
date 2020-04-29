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
import blueprint
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
    blueprint.default()
    workspace.cwd()
        
    threads = []

    thread_autopaste = threading.Thread(target=thread2,args=(), name="AutopasteThread")

    threads.append(thread_autopaste)
    thread_autopaste.setDaemon(True)
    thread_autopaste.start()

    gui.init()
    
    log.info("Program terminated")
