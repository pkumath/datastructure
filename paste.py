#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyperclip as pyperclip
import time
import subprocess
import tempfile
import shutil

import os

import logging as log
from globe import Globe as globe
import inkscape_control
from util import StrUtil as strutil

SYSTEM = globe.SYSTEM

if SYSTEM == "Darwin":
    from pynput import keyboard
    from pynput.mouse import Button, Controller
elif SYSTEM == "Windows":
    import keyboard
    import mouse as w_mouse


def open_editor(filename):
    if SYSTEM == "Darwin":
        subprocess.run([
            '/Applications/MacVim.app/Contents/MacOS/Vim',
            '-fg',
            f"{filename}",
            '+45'
        ])
    elif SYSTEM == "Windows":
        subprocess.run([
            'gvim',
            f"{filename}",
            '+45'
        ])


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

    if SYSTEM == "Darwin":
        mouse = Controller()
        time.sleep(0.1)
        mouse.press(Button.left)
        mouse.release(Button.left)
        keyboard_controller = keyboard.Controller()
        time.sleep(0.1)
        keyboard_controller.press(keyboard.Key.esc)
        keyboard_controller.release(keyboard.Key.esc)
        time.sleep(0.1)
        keyboard_controller.press('t')
        keyboard_controller.release('t')

        mouse.press(Button.left)
        mouse.release(Button.left)

        with keyboard_controller.pressed(keyboard.Key.cmd):
            keyboard_controller.press('v')
            keyboard_controller.release('v')
    elif SYSTEM == "Windows":
        w_mouse.click("left")
        time.sleep(0.5)
        keyboard.send("F8")
        w_mouse.click("left")
        keyboard.send("ctrl+v")
    
    os.remove(f.name)


def open_tiny_latex():
    f = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.tex')

    content = r'''\documentclass[AutoFakeBold,twoside]{article}
\usepackage{xeCJK}
%\setCJKmainfont{AR PL UMing CN} % the font will work on every ubuntu but it's ugly
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{amsthm}
\usepackage{bm}
\usepackage[colorlinks,
            linkcolor=red,
            anchorcolor=blue,
            citecolor=green
            ]{hyperref}
%\usepackage{pgf,tikz}
\usepackage{colortbl}
\usepackage{framed}
\usepackage{enumerate}
\usepackage{showkeys} % easy to line label and content
%\usetikzlibrary{arrows,shapes,chains}
\newtheorem{Thm}{定理}[subsection]
\newtheorem{Axi}{公理}[subsection]
\newtheorem{Lem}{引理}[subsection]
\newtheorem{Prop}{命题}[subsection]
\newtheorem{Cor}{推论}[subsection]
\newtheorem{Def}{定义}[subsection]
\newtheorem{Exa}{例子}[subsection]
\newtheorem*{pro}{证明}
\newtheorem*{sol}{解}
\newtheorem*{Rmk}{注意}
\newtheorem*{Not}{标记}
\newtheorem{Pro}{问题}[subsection]

\usepackage{import}
\usepackage{float}
\usepackage{pdfpages}
%\usepackage{transparent}
\usepackage{xcolor}

\newcommand{\incfig}[1]{%
    \def\svgwidth{\columnwidth}
    \import{./figures/}{#1.pdf_tex}
}
%\pdfsuppresswarningpagegroup=1
\begin{document}
    
\end{document}'''
    f.write(content)
    f.close()
    log.info(f'{f.name}' + ' should be open!')
    open_editor(f.name)

    latex = ""
    with open(f.name, 'r') as g:
        latex = g.read().strip()
    print(latex)
    pyperclip.copy(latex)
    #
    # if SYSTEM == "Darwin":
    #     mouse = Controller()
    #     time.sleep(0.1)
    #     mouse.press(Button.left)
    #     mouse.release(Button.left)
    #     keyboard_controller = keyboard.Controller()
    #     time.sleep(0.1)
    #     keyboard_controller.press(keyboard.Key.esc)
    #     keyboard_controller.release(keyboard.Key.esc)
    #     time.sleep(0.1)
    #     keyboard_controller.press('t')
    #     keyboard_controller.release('t')
    #
    #     mouse.press(Button.left)
    #     mouse.release(Button.left)
    #
    #     with keyboard_controller.pressed(keyboard.Key.cmd):
    #         keyboard_controller.press('v')
    #         keyboard_controller.release('v')
    # elif SYSTEM == "Windows":
    #     w_mouse.click("left")
    #     time.sleep(0.5)
    #     keyboard.send("F8")
    #     w_mouse.click("left")
    #     keyboard.send("ctrl+v")

    os.remove(f.name)
    shutil.rmtree(os.path.dirname(f.name) + os.path.sep + 'figures')

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
    if variable == '':
        variable = 'untitled'
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
        #Mac无法两个快捷键同时运行
        with keyboard.GlobalHotKeys({'<cmd>+u': on_activate,
                                     '<cmd>+0': open_vim,
                                     '<cmd>+j': open_tiny_latex}) as hotkey:
            hotkey.join()
        l = keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release),
            # suppress=True
        )
        l.start()
    elif SYSTEM == "Windows":
        keyboard.add_hotkey('ctrl+u', on_activate, )  # suppress=True)
        keyboard.add_hotkey('ctrl+alt+i', open_vim)
        keyboard.add_hotkey('ctrl+j', open_tiny_latex)
