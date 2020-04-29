#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        with keyboard_controller.pressed(keyboard.Key.ctrl):
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
        with keyboard_controller.pressed(keyboard.Key.ctrl):
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
            keyboard.HotKey.parse('<ctrl>+u'),
            on_activate)
        
        l = keyboard.Listener(
                on_press=for_canonical(hotkey.press), 
                on_release=for_canonical(hotkey.release),
                #suppress=True
                )
        l.start()
    elif SYSTEM == "Windows":
        keyboard.add_hotkey('ctrl+u', on_activate,)# suppress=True)