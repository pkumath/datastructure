#!/usr/bin/env python
# -*- coding: utf-8 -*-

<<<<<<< HEAD
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
=======
import pyperclip as pyperclip
import time

import os

import logging as log

from globe import Globe as globe
import inkscape_control
from util import StrUtil as strutil
SYSTEM = globe.SYSTEM


if SYSTEM == "Darwin":
    from pynput import keyboard
elif SYSTEM == "Windows":
    import keyboard

def on_activate():
    log.info('Global hotkey activated')
    
    if SYSTEM == "Darwin":
        keyboard_controller = keyboard.Controller()
        with keyboard_controller.pressed(keyboard.Key.cmd):
            keyboard_controller.press('c')
            keyboard_controller.release('c')
    elif SYSTEM == "Windows":
        keyboard.send('ctrl+c')
    else: return   

    time.sleep(0.5)

    variable = pyperclip.paste()
    fragment = globe.blueprint.get_fragment(**{'name': variable})
    pyperclip.copy(fragment)

    time.sleep(0.5)

    if SYSTEM == "Darwin":
        with keyboard_controller.pressed(keyboard.Key.cmd):
            keyboard_controller.press('v')
            keyboard_controller.release('v')
    elif SYSTEM == "Windows":
        keyboard.send('ctrl+v')

    time.sleep(0.5)

    if SYSTEM == "Darwin": pyperclip.copy('')

    globe.blueprint.do_macro(name=variable)
    log.info('Global hotkey function terminated')

def trigger():
    if SYSTEM == "Darwin":
        def for_canonical(f):
            log.info("for_canonical")
            return lambda k: f(l.canonical(k))

        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse('<cmd>+u'),
            on_activate)
        
        l = keyboard.Listener(
                on_press=for_canonical(hotkey.press), 
                on_release=for_canonical(hotkey.release),
                #suppress=True
                )
        l.start()
    elif SYSTEM == "Windows":
        keyboard.add_hotkey('ctrl+u', on_activate,)# suppress=True)
>>>>>>> 9c77d4c833ef4264965f179b03ab797ef73461fd
