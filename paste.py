#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pynput import keyboard
import pyperclip as pp
import time
import function as ftn
from inkscape_control import *

def on_activate():
    global name
    global title
    print('Global hotkey activated!')
    ky = keyboard.Controller()
#     print(pp.paste())

    with ky.pressed(keyboard.Key.cmd):
#         with ky.pressed(keyboard.Key.shift):
        ky.press('c')
#         print(pp.paste())
        ky.release('c')
#         print(pp.paste())
    time.sleep(0.5)
    clip = pp.paste()
    print(clip)
    name = clip
    title = ftn.beautify(name)
    manage_string = ftn.latex_template(name,title)
    pp.copy(manage_string)
    ky.press(keyboard.Key.cmd)
    ky.press('v')
    ky.release('v')
    ky.release(keyboard.Key.cmd)
    figpath = os.path.split(os.path.realpath(__file__))[0]
    print('paste.py',figpath)
    time.sleep(0.5)
    pp.copy('')
    create(title,figpath)


def for_canonical(f):
#     print(pp.paste())
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<cmd>+u'),
    on_activate)

def trigger():
    global name
    global title
    global l
    l = keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release))
    l.start()

def get_name_title():
    return name,title
