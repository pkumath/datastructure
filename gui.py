import tkinter as tk
from tkinter import filedialog as tkfiledialog
from tkinter import messagebox as tkmessagebox
from pathlib import Path
import sys
import pyperclip
from multiprocessing import Process
import threading
import webbrowser
import os
from appdirs import *
import logging as log

import inkscape_control

from globe import Globe as globe
import widget
import  edit_scroll_process as svg_file
import workspace
from blueprint import show_blueprint, export_blueprint, import_blueprint
from util import StrUtil as strutil

user_dir = Path(user_config_dir("project", "ww"))
#用于存放数据文件
if not user_dir.is_dir():
    user_dir.mkdir(parents=True)

data_dir = Path(user_data_dir('project','ww'))
#用于存放数据
if not data_dir.is_dir():
    user_dir.mkdir(parents=True)

flag_path = data_dir / 'flag.txt'

def init():
    # Root
    if flag_path.exists():
        pass
    else:
        f = open(flag_path, 'w')
        f.write('Browser')
        f.close()

    root = tk.Tk()
    root.title('LaTeX模版生成程序')
    root.geometry('700x800')

    # Var
    var_snippet = tk.StringVar()
    var_dependency = tk.StringVar()

    varr_snippet = tk.StringVar()
    varr_dependency = tk.StringVar()
    varr_workpath = tk.StringVar()

    varr_snippet.set('经过处理的图片文件名:'+var_snippet.get())

    # Hint
    hint_variable = '图片名称'
    hint_snippet = ' 提示:这是一个自制的简易LaTeX模版生成程序,我们将持续加入其他模版作为扩展,这是在macOS下制作的,我本人不是很清楚Menu组件和Windows显示的是否一致.\n众所周知的是,原来课本上的menu写法只在Windows上生效,因为Mac里的menu是显示在屏幕最上方而不是窗口里面的.\n如果您没有成功显示,换一个电脑,或者忽略格式错误.\n'+\
'**********************************************************************************\n下方浅黄色区域时就是您的工作区域.\n请输入...\n欲获取详细信息，请查看菜单栏的"使用说明"'
    hint_dependency = '这里是上面模版所需的LaTeX依赖展示区.是需要被放入导言区的内容.'

    # Field
    field_variable = widget.HintEntry(root,0,0,hint_variable) 
    field_variable.place(relx = 0.5,rely = 0.05, anchor = tk.CENTER)

    field_list = widget.make_list(root,svg_file.get_svgnames(os.getcwd()),os.getcwd())
    field_list.place(relheight = 0.8,relwidth = 0.27,relx = 0.7,rely = 0.15)

    field_snippet = widget.HintText(root,0,0,hint_snippet,80,40) 
    field_snippet.place(relheight = 0.4, relwidth = 0.7, rely = 0.15)

    field_dependency = widget.HintText(root,0,0,hint_dependency,80,40)# useHint = False)
    field_dependency.place(relheight = 0.4, relwidth = 0.7, rely = 0.55)

    # Label

    label_variable = tk.Label(root, textvariable = varr_snippet) 
    label_variable.place(relx = 0.5, rely = 0.1,anchor = tk.CENTER)

    warning = '请注意，工作路径须与tex文件保持一致。\n如果要修改工作路径，请在菜单栏当中选取"切换工作路径"。'
    varr_workpath.set('当前工作路径：'+os.getcwd()+'.'+warning)
    label_workpath = widget.auto_label(root,varr_workpath)
    label_workpath.place(relx=0.5, rely=0.98, anchor=tk.CENTER)

    # Button

    btn_generate = tk.Button(root, text = '生成片段并复制',command = lambda : callback(field_snippet, var_snippet,varr_snippet,field_variable))
    btn_generate.place(relx = 0.7, rely = 0.04)

    btn_edit = tk.Button(root, text='编辑已有图片！',
                             command=lambda : globe.blueprint.do_macro(name=field_list.content()))
    btn_edit.place(relx=0.7, rely=0.08)

    btn_clrsnip = tk.Button(root, text = '清空片段',command = lambda : field_snippet.clear())
    btn_clrsnip.place(relx = 0.2,rely = 0.04)

    btn_clrdep = tk.Button(root, text = '清空依赖区',command = lambda : field_dependency.clear())#button: clear dependency
    btn_clrdep.place(relx = 0.05,rely = 0.04)

    btn_inkscape = tk.Button(root, text = '执行宏',command = lambda : globe.blueprint.do_macro(name=field_variable.content()) if not field_variable.hinting else None)#inkscape_control.create(strutil.label(var_snippet.get())))
    btn_inkscape.place(relx = 0.05,rely = 0.08)

    # Menu
    menubar = tk.Menu(root)

    menu_file = tk.Menu(menubar, tearoff = False)
    menu_file.add_command(label = '切换工作路径',command = lambda : menu_callback('cwd',field_snippet,var_snippet,varr_snippet,field_list))
    menu_file.add_separator()
    menu_file.add_command(label = '导入片段',command = lambda : menu_callback('open',field_snippet,var_snippet,varr_snippet,field_list))
    menu_file.add_command(label = '导入依赖区',command = lambda : menu_callback('open',field_dependency,var_dependency,varr_dependency,field_list))
    menu_file.add_command(label = '退出',command = root.quit)
    menu_file.add_separator()
    menu_file.add_command(label ='保存片段',command = lambda : menu_callback('save',field_snippet,var_snippet,varr_snippet,field_list))
    menu_file.add_command(label ='保存依赖区',command = lambda : menu_callback('save',field_dependency,var_dependency,varr_dependency,field_list))
    menu_file.add_separator()
    menu_file.add_command(label = '导入蓝图',command = lambda : import_filedialog())
    menu_file.add_command(label ='导出蓝图',command = lambda : export_filedialog())


    menu_help = tk.Menu(menubar, tearoff = False)
    menu_help.add_command(label = '关于...',command = lambda : menu_callback('about',field_snippet,var_snippet,varr_snippet,field_list))
    menu_help.add_command(label = '使用说明',command = lambda : menu_callback('hint',field_snippet,var_snippet,varr_snippet,field_list))
    menu_help.add_command(label='获取教学视频',
                          command=lambda: menu_callback('video', field_snippet, var_snippet, varr_snippet, field_list))

    menubar.add_cascade(label = '文件',menu = menu_file)
    menubar.add_cascade(label = '帮助', menu = menu_help)

    root.config(menu=menubar)
    
    globe.ui = {
        "root": root,
        "var": {
            "snippet": var_snippet,
            "dependency": var_dependency,
        },
        "varr": {
            "snippet": varr_snippet,
            "dependency": varr_dependency,
        },
        "field": {
            "variable": field_variable,
            "snippet": field_snippet,
            "dependency": field_dependency,
            "list": field_list,
        },
        "label": {
            "variable": label_variable,
        },
        "button": {
            "generate": btn_generate,
            "clrsnip": btn_clrsnip,
            "clrdep": btn_clrdep,
            "inkscape": btn_inkscape,
            "edit": btn_edit,
        },
        "menubar": menubar,
        "menu": {
            "file": menu_file,
            "help": menu_help,
        }
    }
    field_list.auto_check()
    label_workpath.auto_check(varr_workpath,warning)
    # check_inkscape()
    log.info("GUI initiated")

    show_blueprint() #显示默认蓝图

    root.mainloop()

    log.info("GUI destroyed")


def callback(widget,var,varr,field_variable):
    """callback"""
    """控制按钮触发"""
    if field_variable.hinting:
        log.warning("Still hinting")
        return
    log.info(field_variable.content())
    var.set(field_variable.content())

    variable = var.get()
    fileName = globe.blueprint.get_factor(**{'name': variable})['fileName']
    fragment = globe.blueprint.get_fragment(**{'name': variable})

    # text.myvar.set(latex_template(var.get(),title))
    widget.text.delete('1.0','end')
    widget.text.insert('1.0', fragment)
    pyperclip.copy(fragment)
    varr.set('经过处理的图片题目:'+fileName)
    
    if widget.hinting == True:
        widget.unhint()

def menu_callback(command,widget,var,varr,listbox):
    """menu_callback

    :param command: 菜单栏控制
    """
    if command == 'about':
        tkmessagebox.showinfo('Help',message= '这是一个latex模版生成程序.\n 温刚于5.10最后一次修改, 1800011095,\n school of mathematics, Peking University.\n 王奕轩, 1900014136, department of chinese, Peking University.')
        # listbox.update()
    elif command == 'hint':
        tkmessagebox.showinfo('Hint',message = '图片标题的处理是为了防止不合法的标题,所以不建议或者未开放关闭自动处理功能.')
        with open(str(flag_path), 'r') as f:
            manual_state = f.read()
            if 'Browser' in manual_state:
                sys.path.append("libs")
                url = 'http://39.107.57.131/?p=605'
                webbrowser.open(url)
                listbox.update()
            elif 'True' in manual_state:
                print('here!')
                os.system('open ' + str(data_dir/'manual.pdf').replace(' ', '\ '))
    elif command == 'save':
        widget.save_file_as(None,varr)
        # listbox.update()
    elif command == 'open':
        widget.open_file(None,None,var,varr)
        # listbox.update()
    elif command == 'cwd':
        cwd_select()
        # listbox.update()
    elif command == 'video':
        sys.path.append("libs")
        url = 'http://39.107.57.131/?p=593'
        webbrowser.open(url)

def cwd_select():
        """cwd_select

        选择工作路径
        """
        cwdpath = tk.filedialog.askdirectory(initialdir=os.getcwd())
        
        if not (cwdpath == ''):
            workspace.cwd(cwdpath)
            tkmessagebox.showinfo('工作路径', '当前工作路径已切换至 {}'.format(os.getcwd()))
        else: log.warning("Selection cancelled.")

def export_filedialog(kind='json'):
        filename = tk.filedialog.asksaveasfilename(initialdir=os.getcwd(), filetypes=[
            (kind.upper(), '*.%s'%kind),
        ], )

        if not (filename == ''):
            if filename[-len(kind)-1:] != ".%s"%kind: filename += ".%s"%kind
            export_blueprint(filename)
        else:
            log.info("Save cancelled.")

def import_filedialog():
        filename = tk.filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[
            ('JSON', '*.json'),
        ])

        if not (filename == ''):
            return_code = import_blueprint(filename)
            if return_code ==-1:
                tkmessagebox.showerror('导入失败', '{} 不是合法的蓝图文件。'.format(filename))
