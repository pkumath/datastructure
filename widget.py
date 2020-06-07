#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import logging as log
from tkinter import filedialog as tkfiledialog
from tkinter import messagebox as tkmessagebox
import os
import logging as log
import edit_scroll_process as svg_file

from globe import Globe as globe


class HintEntry(tk.Frame):
    """HintEntry
    
    an entry which will clear up when focused on
    (原special_label.clickentry)"""

    def __init__(self, master, x, y, text, useHint=True):
        """TODO: to be defined1. """

        tk.Frame.__init__(self, master)
        self.myvar = tk.StringVar()
        self.myvar.set(text)
        self.entry = tk.Entry(self, textvariable=self.myvar)
        self.entry.focus()
        self.entry.grid(row=x, column=y)
        self.entry.bind("<Button-1>", self.on_click)
        self.entry.bind('<KeyPress>', self.on_edit)

        self.useHint = useHint
        self.hinting = True if useHint else False
        if useHint: self.entry.configure(foreground="grey")

    def content(self):
        return self.entry.get()

    def on_click(self, event):
        """on_click

        :param event:
        """
        if self.hinting == True and self.useHint == True:
            # event.widget.delete(0, tk.END)
            self.entry.delete(0, tk.END)
            self.unhint()

    def on_edit(self, event):
        if self.hinting == True and self.useHint == True:
            event.widget.delete(0, tk.END)
            self.unhint()

    def unhint(self):
        self.hinting = False
        self.entry.configure(foreground="black")

    def clear(self):
        self.entry.delete('1.0', 'end')
        if self.useHint == True:
            self.unhint()


class HintText(tk.Frame):
    """HintText
    
    一个可以自动清空的文本框
    (原function.clicktext)"""

    def __init__(self, master, x, y, text, w, h, useHint=True):
        """传入元素进行构造"""

        tk.Frame.__init__(self, master, width=w, height=h)
        sb = tk.Scrollbar(self)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.myvar = tk.StringVar()
        self.myvar.set(text)
        self.text = tk.Text(self, bg='#f8f8ee', yscrollcommand=sb.set)
        self.text.insert(tk.INSERT, self.myvar.get())
        self.text.focus()
        self.text.pack(expand=tk.YES, fill=tk.BOTH)
        self.text.bind("<Button-1>", self.on_click)
        self.text.bind('<KeyPress>', self.on_edit)
        sb.config(command=self.text.yview)

        self.useHint = useHint
        self.hinting = True if useHint else False
        if useHint:
            self.text.tag_add("hint", "1.0", "end")
            self.text.tag_config("hint", foreground="grey")

    @property
    def content(self):
        return self.text.get('1.0', 'end')

    @content.setter
    def content(self, value):
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', value)

    def on_click(self, event):
        """on_click

        :param event: 一旦点击就清空
        """
        if self.hinting == True and self.useHint == True:
            event.widget.delete('1.0', tk.END)
            self.unhint()  # k += 1
        # if self.useHint == False:
        # k = 0

    def on_edit(self, event):
        """on_edit

        :param event: 一编辑就清空
        """
        if self.hinting == True and self.useHint == True:
            event.widget.delete('1.0', tk.END)
            self.unhint()
        # if self.useHint == False:
        # k = 0

    def clear(self):
        self.text.delete('1.0', 'end')
        if self.useHint == True:
            self.unhint()

    def unhint(self):
        self.hinting = False
        self.text.tag_add("normal", "1.0", "end")
        self.text.tag_config("hint", foreground="black")

    def save_file_as(self, whatever=None, varr=None):
        """save_file_as

        :param whatever:另存为
        """
        self.filename = tk.filedialog.asksaveasfilename(initialdir=os.getcwd(), filetypes=[
            ('Text', '*.txt'),
        ], )

        if not (self.filename == ''):
            if self.filename[-4:] != ".txt": self.filename += ".txt"
            with open(self.filename, 'w') as f:
                f.write(varr.get() + '\n' + self.text.get('1.0', 'end'))
            tkmessagebox.showinfo('Good Output!', 'File Saved')
        else:
            log.info("Save cancelled.")

    def open_file(self, whatever=None, filename=None, var=None, varr=None):
        """open_file

        :param whatever:打开一个模版文件
        :param filename:open txt
        """
        if not filename:
            self.filename = tk.filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[
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
            varr.set('经过处理的模版:' + (var.get().split('/'))[-1])
            if self.useHint == True and self.hinting == True:
                self.unhint()

class make_list(tk.Frame):
    def __init__(self, master,list1,path):
        self.list = list1
        self.path = path + os.path.sep + 'figures'
        tk.Frame.__init__(self, master)

        # 添加一个滚动条Scrollbar,靠右，填充。
        sb = tk.Scrollbar(self)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.filename = tk.StringVar()
        # listbox 生成列表选框,selectmode设置选择模式，SINGLE单选，EXTENDED多选
        self.lb = tk.Listbox(self, selectmode=tk.SINGLE, yscrollcommand=sb.set, listvariable = self.filename)
        self.lb.place(relheight = 0.9,relwidth = 0.9)

        sb.config(command=self.lb.yview)

        # insert 添加选项
        for key in self.list:
            self.lb.insert(tk.END, key)

        # 打印所有选项
        log.info(self.lb.get(0, tk.END))
        #删除选中的选项
        b1 = tk.Button(self, text="删除此文件", command=lambda : self.delete(self.list[self.lb.curselection()[0]]))
        b1.place(rely = 0.9,relx = 0.25)
        b2 = tk.Button(self, text="强制更新文件列表", command=lambda: self.update())
        b2.place(rely=0.95, relx=0.25)

    def delete(self,filename):

        log.info('Select cordinates:' + str(self.lb.curselection()))
        log.warning(f'{filename}' + ' to be destroyed!')
        # for i in filename:
        #     print(i)
        self.lb.delete(tk.ACTIVE)
        die_file = [self.path + os.path.sep + filename,self.path + os.path.sep + list(filename.split('.'))[0]+'.pdf',self.path + os.path.sep + list(filename.split('.'))[0]+'.pdf_tex']
        for i in die_file:
            log.warning('The file '+f'{i}' +' will be destroyed totally. And its existence state before is '+str(os.path.exists(i)))
            if os.path.exists(i):
                os.remove(i)
        self.list.remove(filename)

    def update(self):
        now_files = svg_file.get_svgnames(os.getcwd())
        self.list = now_files
        self.path = os.getcwd() +os.path.sep + 'figures'
        self.filename.set(tuple(now_files))

    def content(self):
        print(self.list[self.lb.curselection()[0]])
        print(self.list[self.lb.curselection()[0]][:-4])
        return self.list[self.lb.curselection()[0]][:-4]

    def auto_check(self):
        self.update()
        self.after(100, self.auto_check)

class auto_label(tk.Label):
    def __init__(self,root,varr):
        tk.Label.__init__(self,root, textvariable=varr)

    def auto_check(self,varr,warning):
        varr.set('当前工作路径：' + os.getcwd() + '.' + warning)
        self.after(100, lambda : self.auto_check(varr,warning))






