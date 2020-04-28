#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import threading
from pathlib import Path
from shutil import copy
from appdirs import user_config_dir

import logging as log

from globe import Globe as globe
from util import StrUtil as strutil

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
    log.info("InkscapeThread started")

    processOpen = subprocess.Popen(['inkscape', str(path)])
    log.info("Opening file")

    processOpen.wait()
    log.info("Inkscape process terminated")

    subprocess.Popen(['inkscape', str(path), '-A', str(path.with_suffix(".pdf")), '--export-latex'])
    log.info("Export to pdf_tex process and InkscapeThread terminated")

def create(title, root):
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

    log.debug("Title " + title)
    title = strutil.fileName(title)
    file_name = title + '.svg'
    log.debug("File name " + file_name)

    figures = Path(root).absolute()/'figures' # TODO: 自定义文件夹
    if not figures.exists():
        figures.mkdir()

    figure_path = figures / file_name

    # If a file with this name already exists, quit
    #TODO: 查重工作应该放在paste中完成，也许可以将功能封装，放在util里
    if figure_path.exists():
        log.warning("{} already exists. Quit.".format(str(figure_path)))
        return 
    else:
        copy(str(template), str(figure_path))
    
    log.info("Template copied")
    inkscape_thread = threading.Thread(target=inkscape, args=(figure_path,), name="InkscapeThread")
    inkscape_thread.setDaemon(True)
    inkscape_thread.start()
    log.info("Starting InkscapeThread")
    return