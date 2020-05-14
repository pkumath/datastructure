#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import paste
import subprocess
from multiprocessing import Process
from pathlib import Path
from shutil import copy
from appdirs import user_config_dir

import logging as log

from globe import Globe as globe
from util import StrUtil as strutil
import workspace
SYSTEM = globe.SYSTEM

if SYSTEM == "Darwin":
    from pynput import keyboard
elif SYSTEM == "Windows":
    import keyboard
    import mouse as w_mouse

user_dir = Path(user_config_dir("project", "ww"))
if not user_dir.is_dir():
    user_dir.mkdir(parents=True)

roots_file =  user_dir / 'roots'
template = user_dir / 'template.svg'
config = user_dir / 'config.py'

if not template.is_file():
    source = str(Path(__file__).parent / 'template.svg')
    destination = str(template)
    copy(source, destination)

def inkscape(path):
    log.info("Inkscape function started")
    #
    # def for_canonical(f):
    #     log.info("for_canonical")
    #     return lambda k: f(l.canonical(k))

    # hotkey = keyboard.HotKey(
    #     keyboard.HotKey.parse('<cmd>+u'),
    #     on_activate)
    if SYSTEM == "Darwin":
        processOpen = subprocess.Popen(['/Applications/Inkscape.app/Contents/MacOS/inkscape', str(path)])
        log.info("Opening file")
    elif SYSTEM == "Windows":
        processOpen = subprocess.Popen(['inkscape', str(path)])
        log.info("Opening file")
    # with keyboard.GlobalHotKeys({'<cmd>+i': paste.open_vim}) as hotkey:
    #     hotkey.join()
    # l = keyboard.Listener(
    #     on_press=for_canonical(hotkey.press),
    #     on_release=for_canonical(hotkey.release),
    #     # suppress=True
    # )
    # l.start()
    processOpen.wait()
    log.info("Inkscape terminated")
    if SYSTEM == "Darwin":
        os.system('/Applications/Inkscape.app/Contents/MacOS/inkscape '+ str(path)+ ' --export-file='+str(path.with_suffix(".pdf"))+' --export-latex')
    elif SYSTEM == "Windows":
        subprocess.Popen(['inkscape', str(path), '-o', str(path.with_suffix(".pdf")), '--export-latex'])
    log.info("Export to pdf_tex process and InkscapeProcess terminated")

def create(factor):
#     """
    # Creates a figure.

    # First argument is the title of the figure
    # Second argument is the figure directory.

    # """
    # title = title.strip()
    # file_name = title.replace(' ', '-').lower() + '.svg'
    # figures = root + os.path.sep + 'figures'+os.path.sep
    # figure_path = figures + file_name

    # # If a file with this name already exists, append a '2'.
    # if Path(figure_path).exists():
        # title = title + '-2'
        # create(title,root)
    # else:
        # figure_path = Path(figure_path).absolute()
        # inkscape(figure_path)
    """
    Creates a figure.

    First argument is the title of the figure
    Second argument is the figure directory.

    """
    workspace.sub('figures')

    log.debug("File name without extension " + factor['fileName'])
    file_fullname = factor['fileName'] + '.svg'
    log.debug("File name " + file_fullname)

    figures_dir = Path(globe.workspace['sub']['figures'])

    figure_path = figures_dir / file_fullname

    # If a file with this name already exists, quit
    #TODO: 查重工作应该放在paste中完成，也许可以将功能封装，放在util里
    if figure_path.exists():
        log.warning("{} already exists. Edit but not create.".format(str(figure_path)))

    else:
        copy(str(template), str(figure_path))
        log.info("Template copied")
    
    log.info("Starting Inkscape")
    process_inkscape = Process(target=inkscape, args=(figure_path,))
    process_inkscape.start()
    return