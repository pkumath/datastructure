#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 温刚
# 北京大学数学科学学院，jnwengang@pku.edu.cn
import os
from pathlib import Path
import platform
import logging as log
import requests
import tkinter as tk
import tkinter.messagebox as messagebox
from appdirs import *
from multiprocessing import Process
import time

SYSTEM = platform.system()
log.basicConfig(level=log.DEBUG, format='[%(levelname)s] %(message)s - %(module)s::%(funcName)s(%(lineno)d)')

user_dir = Path(user_config_dir("project", "ww"))
#用于存放数据文件
if not user_dir.is_dir():
    user_dir.mkdir(parents=True)

data_dir = Path(user_data_dir('project','ww'))
#用于存放数据
if not data_dir.is_dir():
    user_dir.mkdir(parents=True)


def other_tk(path):
    #创建新的主线程弹窗
    os.system('python3 ' +str(path))

def readme2(setup_path):
    #安装成功之后弹出使用手册
    software_path = setup_path / 'project'
    manual_path = software_path / 'manual.pdf'
    flag_path = data_dir / 'flag.txt'

    if software_path.exists():
        print('系统检测到您完成了安装。')
        if flag_path.exists():
            print('系统检测到您已经读过使用手册。若要再次阅读，请手动打开软件目录下的manual.pdf.')
            pass
        else:
            os.system('open '+f'{manual_path}')
            f = open(flag_path,'w')
            f.write('True')
            f.close()
    else:
        log.warning('系统检测到软件没有被安装到/Applications.请阅读说明文件并检查！')

def readme1(setup_path):
    #安装提示和指南
    pdf_url = 'http://39.107.57.131/wp-content/uploads/2020/05/安装指南.pdf'
    software_path = setup_path /'project'
    manual_path = software_path  /'manual.pdf'
    flag_path = data_dir/ 'flag.txt'

    readme = data_dir/ '安装指南.pdf'

    if readme.exists():
        pass
        log.info('Readme downloaded.')
    else:
        r = requests.get(pdf_url)
        with open(str(readme), 'wb') as f:
            f.write(r.content)

        log.warning('Readme downloading...')
        messagebox.showinfo('基本组件安装成功！','请仔细阅读安装指南并重启软件')
        os.system('open '+ str(readme).replace(' ','\ '))
        raise KeyError

    if software_path.exists():
        pass
    else:
        log.warning('系统检测到软件没有被安装到/Applications.请阅读说明文件并检查！')
        os.system('open ' + str(readme).replace(' ', '\ '))

def readme0(setup_path):
    #运行弹窗
    software_path = setup_path / 'project'
    manual_path = software_path / 'manual.pdf'
    flag_path = data_dir / 'flag.txt'

    readme = data_dir / '安装指南.pdf'

    if readme.exists():
        pass
        log.info('Readme downloaded.')
    else:
        messagebox.showinfo('来自latex模版管理器','检测到您是第一次使用，正在初始化！正在安装和检测运行环境，请耐心等待，大概需要几分钟，中途可能卡顿，需要联网.点击ok按钮进行安装.如果一直没有成功，尝试从命令行启动看错误提示。')



# 如果程序不能正常运行（比如崩溃），会返回非零值；如果正常运行，就会返回零。

log.warning('安装需要连接网络！')
setup_path = Path('/Applications')

if SYSTEM == "Darwin":
    root = tk.Tk()
    root.withdraw()

    readme0(setup_path)
    gvim = Path('/Applications/MacVim.app')

    readme1(setup_path)
    readme2(setup_path)
    try:
        os.chdir('/Applications/project')
    except:
        messagebox.showinfo('错误报告','检测到您没有安装成功！请阅读安装指南！')
        raise KeyError

    log.info('Check requirements...')
    os.system('pip install -r requirements.txt')

    if gvim.exists():
        pass
        log.info('MacVim exists in Applications.')
    else:
        os.system('cp -r AttachApp/MacVim.app /Applications')
        log.warning('Created MacVim!')

    a = 4
    while a != 0:
        a = os.system("python3 main.py")
        print(a)
