#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk


def myglobal(value):
    global k
    k = value


class clickentry(tk.Frame):
    """clickentry"""

    """an entry which will clear up when focused on"""

    def __init__(self, master, x, y, text):
        """TODO: to be defined1. """

        tk.Frame.__init__(self, master)
        self.myvar = tk.StringVar()
        self.myvar.set(text)
        self.entry = tk.Entry(self, textvariable = self.myvar)
        self.entry.focus()
        self.entry.grid(row = x, column = y)
        self.entry.bind("<Button-1>", self.on_click)
        self.entry.bind('<KeyPress>', self.on_edit)

    def on_click(self, event):
        """on_click

        :param event:
        """
        global k
        if k == 0:
            event.widget.delete(0, tk.END)
        k += 1

    def on_edit(self, event):
        global k
        if k == 0:
            event.widget.delete(0,tk.END)
        k += 1

def callback(operater):
    """callback

    :param operater:str for control
    """
    global k
    if operater != '=' and operater != 'CA':
        if k == 0:
            expression.entry.delete(0,tk.END)
            k = 1
        temp = expression.myvar.get() + operater
        expression.entry.delete(0,tk.END)
#     expression.myvar.set(temp)
        expression.entry.insert(0,temp)
#     print(expression.myvar.get())
    elif operater == '=':
        if k == 0:
            expression.entry.delete(0,tk.END)
            k = 1
        temp = calcu(expression.myvar.get())
        expression.entry.delete(0,tk.END)
        expression.entry.insert(0,temp)
    else:
        expression.entry.delete(0,tk.END)
    


if __name__ == '__main__':
    k = 0