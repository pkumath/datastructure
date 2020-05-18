# LaTex代码模版管理器1.0.[数据结构与算法,wg,wyx]

在线安装指南请见:http://39.107.57.131/?p=568

在线安装和初级教学视频见:http://39.107.57.131/?p=593.如果加载过慢请从网盘下载

链接: https://pan.baidu.com/s/1nunaRNsVQZz5Kk1zUYdUkA  密码: hkmd

在线使用手册manual.pdf(如果您安装Mac版会在下载的文件中附加):http://39.107.57.131/?p=605

## 依赖

Python3.6以上.我已经在代码中尽量使用了跨平台的描述.如果还有问题,换一个Mac电脑或者交流修改.
另外需要系统预安装了inkscape,并且勾选添加到环境变量(或者只要你能从命令行启动就可以.)
使用的python库如下:(有一些在调试的过程可能已经没有用了,但是先放在这)

* tkinter,tkinter.messagebox,tkinter.filedialog(后两个是第一个子模块)
* importlib
* os
* pyautogui
* pyperclip
* time
* keyboard
* subprocess
* pathlib
* shutil
* appdirs
* sys

## 安装

见安装指南.


## 文件结构及说明

文件结构应该是这样的(Mac上父目录应为Applications):
```
project/

    __pycache__
    template
    dependency
    figures
    requirements.txt
    function.py
    inkscape_control.py
    main.py
    special_label.py
    template.svg
    ...
```
* dependency文件夹用来放置和存储需要放在LaTex导言区(preamble)的模版,示例:

```
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
%在中文的ctex被xelatex编译的环境下注释掉的项会出错;但是如果你使用pdflatex可以加上.
%程序会自动给你创建(如果没有的话)图片存放目录figures.
```
* template文件夹用来放置和存储出现在LaTex主体中的模版,示例:
```
\begin{figure}[ht]
    \centering
    \incfig{键入图片标题...}
    \caption{键入图片标题...}
    \label{fig:键入图片标题...}
\end{figure}
```
* figures用来存储点击create之后生成的图片.
* inkscape_control.py主要是控制inkscape的函数文档.
* main.py是主程序.
* template.svg是默认svg模版.


## 详细的代码说明:

见doc.


## 使用说明

见教学视频.

