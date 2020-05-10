#!/usr/bin/env python
# -*- coding: utf-8 -*-

<<<<<<< HEAD
import tkinter as tk
import importlib
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import os
import pyautogui as pya
import pyperclip
import time
import sys
import keyboard as kd
from inkscape_control import *
from function import *
import threading
import paste as autopaste
=======
import threading
>>>>>>> 9c77d4c833ef4264965f179b03ab797ef73461fd


import logging as log
log.basicConfig(level=log.DEBUG, format='[%(levelname)s] %(message)s - %(module)s::%(funcName)s(%(lineno)d)')

from globe import Globe as globe
import gui
import workspace
import blueprint
import paste as autopaste


# def thread1():
    # root.mainloop()

def thread2():
    autopaste.trigger()

if __name__ == '__main__':
<<<<<<< HEAD
    figpath = os.path.split(os.path.realpath(__file__))[0]
    print('main.py',figpath)
    save_dir = "figures"+os.path.sep
    if os.path.exists(save_dir) is False:
        os.makedirs(save_dir)
    root = tk.Tk()
    root.title('latex模版生成程序')
    root.geometry('600x800')
    ce.myglobal(0)
    k = 0
    myglobal(0)
    var = tk.StringVar()
    var_dependency = tk.StringVar()
    varr = tk.StringVar()
    varr_dependency = tk.StringVar()
    varr.set('经过处理的图片题目:'+var.get())
    hint = ' 提示:这是一个自制的简易latex模版生成程序,我们将持续加入其他模版作为扩展,这是在macOS下制作的,我本人不是很清楚Menu组件和windows显示的是否一致.\n众所周知的是,原来课本上的menu写法只在windows上生效,因为Mac里的menu是显示在屏幕最上方而不是窗口里面的.\n如果您没有成功显示,换一个电脑,或者忽略格式错误.\n'+\
'**********************************************************************************\n下方浅黄色区域时就是您的工作区域.\n请输入...'
    
    ttl = ce.clickentry(root,0,0,'键入图片标题...')
    ttl.place(relx = 0.5,rely = 0.05, anchor = tk.CENTER)

    ttlbut = tk.Button(root, text = '生成latex图片模版并复制',command = lambda : callback(text,var,varr,ttl))
    ttlbut.place(relx = 0.7, rely = 0.04)

    ttllab = tk.Label(root, textvariable = varr)
    ttllab.place(relx = 0.5, rely = 0.1,anchor = tk.CENTER)

    text = clicktext(root,0,0,hint,80,40)
    dependencyclaim = '这里是上面模版所需的latex依赖展示区.是需要被放入导言区的内容.'
    text.place(relheight = 0.4, relwidth = 1, rely = 0.15)

    show_dependency = clicktext(root,0,0,dependencyclaim,80,40, usek = False)
    show_dependency.place(relheight = 0.4, relwidth = 1, rely = 0.55)

    ttlbut2 = tk.Button(root, text = '清空内容',command = lambda : clean(text))
    ttlbut2.place(relx = 0.2,rely = 0.04)

    ttlbut3 = tk.Button(root, text = '清空依赖区',command = lambda : clean(show_dependency))
    ttlbut3.place(relx = 0.05,rely = 0.04)
=======
    blueprint.default() # 加载默认蓝图，最好在最前面执行
    workspace.cwd() # 加载默认工作路径，即 py 所在路径 #TODO 保存上次的工作路径？
        
    threads = []
>>>>>>> 9c77d4c833ef4264965f179b03ab797ef73461fd

    thread_autopaste = threading.Thread(target=autopaste.trigger, args=(), name="AutopasteThread")

    threads.append(thread_autopaste)
    thread_autopaste.setDaemon(True)
    thread_autopaste.start() # 启动自动复制线程

<<<<<<< HEAD
    menubar = tk.Menu(root)

    filemenu = tk.Menu(menubar, tearoff = False)
    filemenu.add_command(label = '打开',command = lambda : menucallback('open',text,var,varr))
    filemenu.add_command(label = '导入依赖区',command = lambda : menucallback('open',show_dependency,var_dependency,varr_dependency))
    filemenu.add_command(label = '退出',command = root.quit)
    filemenu.add_separator()
    filemenu.add_command(label ='保存',command = lambda : menucallback('save',text,var,varr))
    filemenu.add_command(label ='保存依赖区',command = lambda : menucallback('save',show_dependency,var_dependency,varr_dependency))


    helpmenu = tk.Menu(menubar, tearoff = False)
    helpmenu.add_command(label = '关于...',command = lambda : menucallback('about',text,var,varr))
    helpmenu.add_command(label = '使用说明',command = lambda : menucallback('hint',text,var,varr))

    menubar.add_cascade(label = '文件',menu = filemenu)
    menubar.add_cascade(label = '帮助', menu = helpmenu)

    root.config(menu=menubar)
#    menu = tk.Menu(root,tearoff = False)
    threads = []

    t2 = threading.Thread(target=thread2,args=())
    threads.append(t2)
    for t in threads:
        t.start()
    
    tk.mainloop()


=======
    gui.init() # 启动 GUI
    # 据称 Tk ‘线程不安全’，只能在主线程中执行
    
    log.info("Program terminated")
>>>>>>> 9c77d4c833ef4264965f179b03ab797ef73461fd
