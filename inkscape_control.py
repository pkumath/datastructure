#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
from pathlib import Path
from shutil import copy
from appdirs import user_config_dir

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
    subprocess.Popen(['inkscape', str(path)])

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
    title = title.strip()
    file_name = title.replace(' ', '-').lower() + '.svg'
    figures = Path(root).absolute()/'figures'
    if not figures.exists():
        figures.mkdir()

    figure_path = figures / file_name

    # If a file with this name already exists, append a '2'.
    if figure_path.exists():
        print(title + ' 2')
        return
    copy(str(template), str(figure_path))
    inkscape(figure_path)

