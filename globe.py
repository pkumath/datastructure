#!/usr/bin/env python
# -*- coding: utf-8 -*-

from platform import system

class Globe():
    '''Globe

    模块之间共用的全局变量。
    - ui: 包含GUI各元素引用的字典
    - workspace: 工作区文件夹
    - blueprint: 蓝图设置
    - SYSTEM: 操作系统名称，Darwin/Windows
    '''
    
    ui = {}
    '''
    Globe.ui[widget][name]

    修改界面元素：
    some.cget("somecfg")
    some.configure(somecfg=somevalue)
    '''
  
    workspace = {}
    workspace['sub'] = {} # 工作区：子文件夹

    blueprint = None # 蓝图

    SYSTEM = system() # 操作系统
