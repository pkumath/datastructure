# LaTex代码模版管理器1.0(仅支持图片).[数据结构与算法,wg,wyx]

这是一个初步的版本,仅有支持图片的代码段管理功能.
手边没有Windows机器参考,我修改了初始的思路,原因见最后:**‌遗留的问题和建议**

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

我已经使用pip生成了部分包的requirements;若不完整,只需要按照错误提示逐个下载,希望在这个过程中可以尝试手动添加一下requirements;如果都安装以后就很难再手动添加了.

使用只需在项目根目录下:
```
pip install -r requirements.txt
```


## 文件结构及说明

文件结构应该是这样的:
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
* function.py是主要的函数文档.
* inkscape_control.py主要是控制inkscape的函数文档.
* main.py是主程序.
* special_label.py是特殊label类,点击或者编辑都会自动清空提示文本.(function.py中含有特殊text类,定义如上)
* template.svg是默认svg模版.


## 详细的代码说明:

### special_label.py

摘自个人的计算器作业(所以出现奇怪的expression不要奇怪).
主要是利用定义的label类,可以显示提示文字,而无论是鼠标点击还是键盘聚焦都会自动删除提示文字.

### function.py

这是主要的函数文档.

* myglobal.这是为了几个文档共享一个全局变量k创造的函数;k的作用是控制鼠标点击或者键盘聚焦都会自动删除提示文字,而且只会在非依赖区(导言区)运行一次,防止删除有用内容.
* clicktext.是类似于上面的label的类,方法见源码.
* clean.清空内容
* callback.按钮触发的主要控制函数.
* latex_template.模版生成器,其他(不光图片)可以参考.
* beautify.防止用户输入的标题不合法,进行自动处理.
* menucallback.菜单栏控制.
### main.py
这是主程序.

* figpath是找到当前py的运行目录.
* save_dir部分放置figures目录不存在
* var是entry上的文字,varr是标题显示的文字.
* text是模版生成区,最好有良好的可修改性;show_dependency是导言区展示区,修改性不能太好.

### inkscape_control.py

当点击"create"按钮后,在project的figures中创建以用户输入的标题为文件名的svg.

## 使用说明

首先保证你确实能够从命令行启动inkscape.测试一下,在命令行输入:
```
inkscape 
```
如果可以的话直接
```
python3 main.py
```
就可以运行程序了.见图.

![Alt text](/screenshots/manual.png)

需要注意的是,还没有加入inkscape的自动保存机制,所以在编辑完svg后要手动保存成pdf+tex格式,否则latex不会识别你的图片. 
![Alt text](/screenshots/save_manual.jpg)

## 遗留的问题和建议

导言区

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
```

中的路径是./figures;然而tex文档几乎不可能和py放在同一目录下,所以是否有什么办法动态修改这个figures目录?或者实在不行就把figures文件夹的路径展示出来?

Python用快捷键操作剪贴板并把字符串原地替换这个功能跨平台是在难度太大,Mac上是要辅以swift和O-C才能使用的,而这几乎不可能(完全不可能)拓展到Windows机器上,所以我采用了这种外部窗口控制做法,而不是快捷键的做法.

另外这种做法也有它的优点:它可以有多种扩展,不光可以控制图片的模版生成;实际上,我们完全可以把它做成ltex的代码仓库!

还有一个缺点就是open_file和save_file没有设置默认路径,如果设置默认路径的话会舒服很多,这些细节我先留下来“接力”解决吧.
