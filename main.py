#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


# def myglobal(value):
    # """myglobal

    # :param value:k是一个重要的全局变量,可以在文件之间相互调用和修改,方法是通过函数实现的,用来表达文本内容是否需要清空的状态.
    # """
    # global k
    # k = value

ce = importlib.import_module('special_label')

if __name__ == '__main__':
    # 路径处理
    # TODO 引入工作区机制
    figpath = os.path.split(os.path.realpath(__file__))[0]
    print(figpath)
    save_dir = "figures"+os.path.sep
    if os.path.exists(save_dir) is False:
        os.makedirs(save_dir)
    
    # GUI
    root = tk.Tk()
    root.title('LaTeX模版生成程序')
    root.geometry('600x800')
    ce.myglobal(0)
    k = 0
    myglobal(0) #function.myglobal
    var = tk.StringVar() #fig title var
    var_dependency = tk.StringVar() #dependency var
    varr = tk.StringVar() #fig title beautified var
    varr_dependency = tk.StringVar() #dependency beautified var
    varr.set('经过处理的图片题目:'+var.get())
    hint = ' 提示:这是一个自制的简易LaTeX模版生成程序,我们将持续加入其他模版作为扩展,这是在macOS下制作的,我本人不是很清楚Menu组件和Windows显示的是否一致.\n众所周知的是,原来课本上的menu写法只在Windows上生效,因为Mac里的menu是显示在屏幕最上方而不是窗口里面的.\n如果您没有成功显示,换一个电脑,或者忽略格式错误.\n'+\
'**********************************************************************************\n下方浅黄色区域时就是您的工作区域.\n请输入...'
    
    ## GUI::Buttons
    # TODO 用pack代替place
    ttl = ce.clickentry(root,0,0,'键入图片标题...') #hinted entry: fig title 
    ttl.place(relx = 0.5,rely = 0.05, anchor = tk.CENTER)

    ttlbut = tk.Button(root, text = '生成LaTeX图片模版并复制',command = lambda : callback(text,var,varr,ttl)) #button: generate snippet from title
    ttlbut.place(relx = 0.7, rely = 0.04)

    ttllab = tk.Label(root, textvariable = varr) #label: fig title beautified
    ttllab.place(relx = 0.5, rely = 0.1,anchor = tk.CENTER)

    text = clicktext(root,0,0,hint,80,40) #click text: snippet
    text.place(relheight = 0.4, relwidth = 1, rely = 0.15)

    dependencyclaim = '这里是上面模版所需的LaTeX依赖展示区.是需要被放入导言区的内容.'
    show_dependency = clicktext(root,0,0,dependencyclaim,80,40, usek = False) #click text: dependency
    show_dependency.place(relheight = 0.4, relwidth = 1, rely = 0.55)

    ttlbut2 = tk.Button(root, text = '清空内容',command = lambda : clean(text))#button: clear snippet
    ttlbut2.place(relx = 0.2,rely = 0.04)

    ttlbut3 = tk.Button(root, text = '清空依赖区',command = lambda : clean(show_dependency))#button: clear dependency
    ttlbut3.place(relx = 0.05,rely = 0.04)

    ttlbut4 = tk.Button(root, text = 'create!',command = lambda : create(beautify(var.get()),figpath))#button: create fig
    ttlbut4.place(relx = 0.05,rely = 0.08)

    ## GUI::Menu
    menubar = tk.Menu(root)

    filemenu = tk.Menu(menubar, tearoff = False)
    filemenu.add_command(label = '打开',command = lambda : menucallback('open',text,var,varr))
    filemenu.add_command(label = '导入依赖区',command = lambda : menucallback('open',show_dependency,var_dependency,varr_dependency))
    filemenu.add_command(label = '退出',command = root.quit)
    filemenu.add_separator()
    filemenu.add_command(label ='保存',command = lambda : menucallback('save',text,var,varr))#menu: save snippet
    filemenu.add_command(label ='保存依赖区',command = lambda : menucallback('save',show_dependency,var_dependency,varr_dependency))


    helpmenu = tk.Menu(menubar, tearoff = False)
    helpmenu.add_command(label = '关于...',command = lambda : menucallback('about',text,var,varr))
    helpmenu.add_command(label = '使用说明',command = lambda : menucallback('hint',text,var,varr))

    menubar.add_cascade(label = '文件',menu = filemenu)
    menubar.add_cascade(label = '帮助', menu = helpmenu)

    root.config(menu=menubar)
#    menu = tk.Menu(root,tearoff = False)

    tk.mainloop()
