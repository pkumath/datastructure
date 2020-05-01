#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading


import logging as log
log.basicConfig(level=log.DEBUG, format='[%(levelname)s] %(message)s - %(module)s::%(funcName)s(%(lineno)d)')

from globe import Globe as globe
import gui
import workspace
import blueprint
import paste as autopaste


if __name__ == '__main__':
    blueprint.default() # 加载默认蓝图，最好在最前面执行
    workspace.cwd() # 加载默认工作路径，即 py 所在路径 #TODO 保存上次的工作路径？
        
    threads = []

    thread_autopaste = threading.Thread(target=autopaste.trigger, args=(), name="AutopasteThread")

    threads.append(thread_autopaste)
    thread_autopaste.setDaemon(True)
    thread_autopaste.start() # 启动自动复制线程

    gui.init() # 启动 GUI
    # 据称 Tk ‘线程不安全’，只能在主线程中执行
    
    log.info("Program terminated")
