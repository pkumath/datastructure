#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyperclip as pp
import time
import function as ftn
import inkscape_control as ink
import os
from platform import system

if system() == "Darwin":
    from pynput import keyboard

elif system() == "Windows":
    import keyboard

def on_activate():
    global name
    global title
    print('Global hotkey activated!')

    
    if system() == "Darwin":
        ky = keyboard.Controller()
        with ky.pressed(keyboard.Key.ctrl):
            ky.press('c')
            ky.release('c')
    elif system() == "Windows":
        keyboard.send('ctrl+c')
    else: return   

    time.sleep(0.5)

    clip = pp.paste()
    name = clip

    name = ftn.valid(name)
    title = ftn.valid(name)
    if title == "": return
    title = ftn.beautify(title)

    
    manage_string = ftn.latex_template(name, title)
    pp.copy(manage_string)

    time.sleep(0.5)

    if system() == "Darwin":
        with ky.pressed(keyboard.Key.ctrl):
            ky.press('v')
            ky.release('v')
    elif system() == "Windows":
        keyboard.send('ctrl+v')

    figpath = os.path.split(os.path.realpath(__file__))[0]
    time.sleep(0.5)

    if system() == "Darwin": pp.copy('')

    ink.create(title,figpath)

if system() == "Darwin":
    def for_canonical(f):
        print("for_canonical")
        return lambda k: f(l.canonical(k))

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+u'),
        on_activate)

def trigger():
    global name
    global title

    if system() == "Darwin":
        global l
        l = keyboard.Listener(
                on_press=for_canonical(hotkey.press), 
                on_release=for_canonical(hotkey.release),
                #suppress=True
                )
        l.start()
    elif system() == "Windows":
        keyboard.add_hotkey('ctrl+u', on_activate,)# suppress=True)