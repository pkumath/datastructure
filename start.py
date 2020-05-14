#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 温刚
# 北京大学数学科学学院，jnwengang@pku.edu.cn
import os
from pathlib import Path
from globe import Globe as globe
import logging as log

log.basicConfig(level=log.DEBUG, format='[%(levelname)s] %(message)s - %(module)s::%(funcName)s(%(lineno)d)')
import time

# 如果程序不能正常运行（比如崩溃），会返回非零值；如果正常运行，就会返回零。

SYSTEM = globe.SYSTEM

log.info('Check requirements...')
os.system('pip install -r requirements.txt')

if SYSTEM == "Darwin":
    gvim = Path('/Applications/MacVim.app')
    # os.chdir(os.path.expanduser('~')+'/Desktop/jb')

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
