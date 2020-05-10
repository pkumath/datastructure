#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyperclip as pyperclip
import time
import subprocess
import tempfile

import os

import logging as log
from pynput.mouse import Button, Controller
from globe import Globe as globe
import inkscape_control
from util import StrUtil as strutil

SYSTEM = globe.SYSTEM

if SYSTEM == "Darwin":
    from pynput import keyboard
elif SYSTEM == "Windows":
    import keyboard


def open_editor(filename):
    if SYSTEM == "Darwin":
        subprocess.run([
            'xterm',
            '-geometry', '60x5',
            '-name', 'popup-bottom-center',
            '-e', "vim",
            f"{filename}",
        ])
    elif SYSTEM == "Windows":
        pass


def open_vim():
    f = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.tex')

    f.write('$$')
    f.close()
    log.info(f'{f.name}'+' should be open!')
    open_editor(f.name)

    latex = ""
    with open(f.name, 'r') as g:
        latex = g.read().strip()
    print(latex)
    pyperclip.copy(latex)

    mouse = Controller()
    keyboard_controller = keyboard.Controller()
    keyboard_controller.press('t')
    keyboard_controller.release('t')

    mouse.press(Button.left)
    mouse.release(Button.left)

    with keyboard_controller.pressed(keyboard.Key.ctrl):
        keyboard_controller.press('v')
        keyboard_controller.release('v')
    os.remove(f.name)


def on_activate():
    log.info('Global hotkey activated')

    if SYSTEM == "Darwin":
        keyboard_controller = keyboard.Controller()
        with keyboard_controller.pressed(keyboard.Key.cmd):
            keyboard_controller.press('c')
            keyboard_controller.release('c')
    elif SYSTEM == "Windows":
        keyboard.send('ctrl+c')
    else:
        return

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

        # hotkey = keyboard.HotKey(
        #     keyboard.HotKey.parse('<cmd>+u'),
        #     on_activate)

        with keyboard.GlobalHotKeys({'<cmd>+u': on_activate,
                                     '<cmd>+i': open_vim}) as hotkey:
            hotkey.join()
        l = keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release),
            # suppress=True
        )
        l.start()
    elif SYSTEM == "Windows":
        keyboard.add_hotkey('ctrl+u', on_activate, )  # suppress=True)
