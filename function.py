#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import importlib
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import os
import pyautogui as pya
import pyperclip
import time
import keyboard as kd

ce = importlib.import_module('special_label')

# def copyclip():
    # pyperclip.copy("")


def myglobal(value):
    """myglobal

    :param value:k是一个重要的全局变量,可以在文件之间相互调用和修改,方法是通过函数实现的,用来表达文本内容是否需要清空的状态.
    """
    global k
    k = value


class clicktext(tk.Frame):
    """clickentry"""

    """一个可以自动清空的文本框"""

    def __init__(self, master, x, y, text,w,h,usek = True):
        """传入元素进行构造"""

        tk.Frame.__init__(self, master,width = w,height = h)
        sb = tk.Scrollbar(self)
        sb.pack(side = tk.RIGHT, fill = tk.Y)
        self.usek = usek

        self.myvar = tk.StringVar()
        self.myvar.set(text)
        self.text = tk.Text(self, bg = '#f8f8ee',yscrollcommand = sb.set)
        self.text.insert(tk.INSERT,self.myvar.get())
        self.text.focus()
        self.text.pack(expand = tk.YES, fill = tk.BOTH)
        self.text.bind("<Button-1>", self.on_click)
        self.text.bind('<KeyPress>', self.on_edit)
        sb.config(command = self.text.yview)
    def on_click(self, event):
        """on_click

        :param event: 一旦点击就清空
        """
        global k
        if k == 0 and self.usek == True:
            event.widget.delete('1.0', tk.END)
            k += 1
#         if self.usek == False:
            # k = 0

    def on_edit(self, event):
        """on_edit

        :param event: 一编辑就清空
        """
        global k
        if k == 0 and self.usek == True:
            event.widget.delete('1.0',tk.END)
            k += 1
#         if self.usek == False:
            # k = 0

    def save_file_as(self, whatever = None,varr= None):
        """save_file_as

        :param whatever:另存为
        """
        self.filename = filedialog.asksaveasfilename(filetypes = [
        ('Text', '*.txt'),
            ('All files', '*'),
            ])
        
        with open(self.filename, 'w') as f:
            f.write(varr.get() + '\n' + self.text.get('1.0', 'end'))
        
        messagebox.showinfo('Good Output!', 'File Saved')

    def open_file(self, whatever = None, filename = None,var= None,varr = None):
        """open_file

        :param whatever:打开一个模版文件
        :param filename:open txt
        """
        global k
        if not filename:
            self.filename = filedialog.askopenfilename(filetypes = [
        ('Text', '*.txt'),
            ('All files', '*'),
            ])
        else:
            self.filename = filename
        if not (self.filename == ''):
            with open(self.filename, 'r') as f:
                f2 = f.read()
                self.text.delete('1.0', 'end')
                self.text.insert('1.0', f2)
            var.set(self.filename)
            varr.set('经过处理的模版:'+(var.get().split(os.path.sep))[-1])
            if self.usek == True:
                k += 1

def clean(widget):
    widget.text.delete('1.0','end')
    global k
    if widget.usek == True:
        k = 1

def callback(widget,var,varr,ttl):
    """callback"""
    """控制按钮触发"""
    print(ttl.entry.get())
    var.set(ttl.entry.get())
    title = beautify(var.get())
    # text.myvar.set(latex_template(var.get(),title))
    widget.text.delete('1.0','end')
    widget.text.insert('1.0',latex_template(var.get(),title))
    pyperclip.copy(latex_template(var.get(),title))
    varr.set('经过处理的图片题目:'+title)


def latex_template(name, title):
    """生成latex图片模版名称,为后面的其他模版做借鉴"""
    global k
    k = 1
    return '\n'.join((
        r"\begin{figure}[ht]",
        r"    \centering",
        rf"    \incfig{{{name}}}",
        rf"    \caption{{{title}}}",
        rf"    \label{{fig:{name}}}",
        r"\end{figure}"))

def beautify(name):
    return name.replace('_', ' ').replace('-', ' ').title()

def menucallback(command,widget,var,varr):
    """menucallback

    :param command: 菜单栏控制
    """
    if command == 'about':
        messagebox.showinfo('Help',message= '这是一个latex模版生成程序.\n 温刚于4.15最后一次修改, 1800011095,\n school of mathematics, Peking University.')
    if command == 'hint':
        messagebox.showinfo('Hint',message = '图片标题的处理是为了防止不合法的标题,所以不建议或者未开放关闭自动处理功能.')
    if command == 'save':
        widget.save_file_as(None,varr)
    if command == 'open':
        widget.open_file(None,None,var,varr)

