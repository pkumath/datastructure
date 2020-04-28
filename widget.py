#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import os

class HintEntry(tk.Frame):
    """HintEntry
    
    an entry which will clear up when focused on
    (原special_label.clickentry)"""

    def __init__(self, master, x, y, text, useHint = True):
        """TODO: to be defined1. """

        tk.Frame.__init__(self, master)
        self.myvar = tk.StringVar()
        self.myvar.set(text)
        self.entry = tk.Entry(self, textvariable = self.myvar)
        self.entry.focus()
        self.entry.grid(row = x, column = y)
        self.entry.bind("<Button-1>", self.on_click)
        self.entry.bind('<KeyPress>', self.on_edit)
        
        self.useHint = useHint
        self.hinting = True if useHint else False

    def on_click(self, event):
        """on_click

        :param event:
        """
        if self.hinting == True and self.useHint == True:
            #event.widget.delete(0, tk.END)
            self.entry.delete(0, tk.END)
            self.hinting = False

    def on_edit(self, event):
        if self.hinting == True and self.useHint == True:
            event.widget.delete(0,tk.END)
            self.hinting = False

    def clear(self):
        self.entry.delete('1.0','end')
        if self.useHint == True:
            self.hinting = False

class HintText(tk.Frame):
    """HintText
    
    一个可以自动清空的文本框
    (原function.clicktext)"""

    def __init__(self, master, x, y, text,w,h, useHint = True):
        """传入元素进行构造"""

        tk.Frame.__init__(self, master,width = w,height = h)
        sb = tk.Scrollbar(self)
        sb.pack(side = tk.RIGHT, fill = tk.Y) 

        self.myvar = tk.StringVar()
        self.myvar.set(text)
        self.text = tk.Text(self, bg = '#f8f8ee',yscrollcommand = sb.set)
        self.text.insert(tk.INSERT,self.myvar.get())
        self.text.focus()
        self.text.pack(expand = tk.YES, fill = tk.BOTH)
        self.text.bind("<Button-1>", self.on_click)
        self.text.bind('<KeyPress>', self.on_edit)
        sb.config(command = self.text.yview)

        self.useHint = useHint
        self.hinting = True if useHint else False

        
    def on_click(self, event):
        """on_click

        :param event: 一旦点击就清空
        """
        if self.hinting == True and self.useHint == True:
            event.widget.delete('1.0', tk.END)
            self.hinting = False#k += 1
        #if self.useHint == False:
            # k = 0

    def on_edit(self, event):
        """on_edit

        :param event: 一编辑就清空
        """
        if self.hinting == True and self.useHint == True:
            event.widget.delete('1.0',tk.END)
            self.hinting = False
        # if self.useHint == False:
            # k = 0

    def clear(self):
        self.text.delete('1.0','end')
        if self.useHint == True:
            self.hinting = False

    def save_file_as(self, whatever = None,varr= None):
        """save_file_as

        :param whatever:另存为
        """
        self.filename = tk.filedialog.asksaveasfilename(filetypes = [
        ('Text', '*.txt'),
            ])
        
        if not (self.filename == ''):
            if self.filename[-4:] != ".txt": self.filename += ".txt"
            with open(self.filename, 'w') as f:
                f.write(varr.get() + '\n' + self.text.get('1.0', 'end'))
            tk.messagebox.showinfo('Good Output!', 'File Saved')
        else: print("save cancelled.")

    def open_file(self, whatever = None, filename = None,var= None,varr = None):
        """open_file

        :param whatever:打开一个模版文件
        :param filename:open txt
        """
        if not filename:
            self.filename = tk.filedialog.askopenfilename(filetypes = [
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
            if self.useHint == True and self.hinting == True:
                self.hinting = False