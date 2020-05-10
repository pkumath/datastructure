# 蓝图

## variable、factor

一个代码模板好比是一个填空题，大部分的代码都是预设好的，但是里面有几处是可变的，可以由用户自己填写内容。比如生成一个svg图片的代码片段，\end{figure}就属于预设好的内容，无需改动，而\label{fig:**your-fig-label**}中的**your-fig-label**就是可变的，可自定义的，在使用的过程中可以自己指定。我们的片段中还有几处这样的空位，比如\incfig{**your-fig-file**}，\caption{**your-caption**}，都是可以自己指定的。

但这也带来了一个问题，这三处内容（**your-fig-label**，**your-fig-file**，**your-caption**）具有相关性，他们三个的值可能是同一个量的不同变化形式。比如我指定这个图片叫做`test? fig`，图片的标签应该写成`test?-fig`，而文件名中不许出现问号所以要变成`test-fig`，而标题首字母要大写，应该写成`Test? fig`。这三个量都是同一个量的变体。我们把每一个这样的变体叫做factor，把原来的那个量称作variable，从一个variable到一个factor需要一种转换操作。

我们目前的模板里只有一个variable，就是`name`，我们图片的名字。但假如说我们在不同的地方想要设置不同的浮动体位置，那么\begin{figure}[**ht**]里的**ht**也应该变成一个variable，因此预留了多个variable的可能。当然这需要GUI做出一些调整，需要增加一个下拉列表来选择entry里正在输入的是哪个量。

蓝图对象的variable属性是一个元组（因为集合不能转换成json，所以只好用元组），用来表明在这个对象的代码模板snippet里需要用到哪几个variable，元组中每个元素的值就是这个variable的名字。目前只有一个，所以默认的蓝图这个属性的值就是`('name',)`

蓝图对象的factor属性是一个字典，用来表明在这个对象的代码模板snippet中用到的这些空位。字典的键表示这个factor的名称，而字典的值是一个元组，第零位表示转换成这个factor，需要什么转换操作，而第一位则是说明这个factor是由哪个variable转换而来的。因此

```python
{
	'caption': ('$caption', 'name'),
    'fileName': ('$fileName', 'name'),
    'label': ('$label', 'name')
}
```

中第一个键值对表示`caption`这个factor是：由`name`这个variable，经过一个叫做`caption`的操作转化而来的。`$`的意思会在稍后解释。如果从variable到factor不需要任何格式转换，第零位设为空字符串即可。

## snippet、fragment

snippet就是一个代码的模板，像这样：

```latex
\begin{figure}[ht]
    \centering
    \incfig{-fileName-}
    \caption{-caption-}
    \label{fig:-label-}
\end{figure}
```

这里用`-`包裹的部分很显然就是上面提到的factor。因此，蓝图对象的snippet属性除了符合latex语法，也应该包含python中字符串替换所使用的语法。为了清楚（latex语法里面的大括号是{，而python里面的是{{，{key}表示用键key对应的字典值替换，一堆大括号很乱），这里用的是latex语法。很显然，在真正的tex文件里，我们需要把这些factor变成我们自定义的值。这个填空（或者说替换）的过程得到的结果，也就是我们直接插入tex文件的（出现在上方的text控件（field_snippet）里，或者在自动复制autopaste中自动复制到光标位置的内容），我们称作fragment，也就是如下样式的内容：

```latex
\begin{figure}[ht]
    \centering
    \incfig{my-fig}
    \caption{My? fig}
    \label{fig:my?-fig}
\end{figure}
```

因为fragment是根据variable、factor、snippet直接生成的，所以没有对应属性。

## dependency

dependency也被包在了蓝图对象的属性里。因为dependency是依附于snippet存在的。目前还没有实现关于dependency的任何操作，之后可以加一个把dependency插到下方text控件（field_dependency）里的按钮。

## macro

当我们生成了一段fragment以后，我们可能还想做点别的，比如根据我之前的输入，创建一个svg图片并再inkscape里打开……这一系列操作叫做“宏”，macro。macro属性的值就是你要执行的操作名称，在默认蓝图里就是`$inkscape`。如果不需要执行任何macro，设成空字符串即可。

## 默认蓝图

为了模块化的需要，原来所有“生成一段**_插图用的_** latex 代码并 在 **_inkscape软件_** 中打开”中粗斜体部分都被抽离到了一个蓝图对象中，我们称为默认蓝图，这个对象在程序开始时，调用blueprint文件中的default()函数生成，并直接在全局变量Globe.blueprint里引用。这个对象的初始化过程如下：

```python
default_dependency = r'''\usepackage{import}
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
'''

default_snippet = r'''\begin{{figure}}[ht]
    \centering
    \incfig{{{fileName}}}
    \caption{{{caption}}}
    \label{{fig:{label}}}
\end{{figure}}
'''

default_blueprint = Blueprint({
    'variable': ('name',),
    'dependency': default_dependency,
    'factor': {
        'caption': ('$caption', 'name'),
        'fileName': ('$fileName', 'name'),
        'label': ('$label', 'name')
    },
    'snippet': default_snippet,
    'macro': '$inkscape'
})
```

## 蓝图类的方法

蓝图类有三个方法：get_factor，get_fragment，do_macro。

这三个方法的参数完全一致，是一个解包的字典，每一个键就是variable的名称，对应的值就是variable的值。非常显然，在目前的代码里还没能实现多variable，因此所有调用的地方都直接使用了\*\*{'name': 'some-value'}这样的奇怪格式，实现多variable以后，可以很方便地改成\*\*a-dict-of-variables这样的参数。

第一个方法返回所有的factor，是一个字典，键是factor名，值是对应factor的值。第二个方法返回fragment字符串。第三个方法没有返回值，在里面调用macro。

## 字符串转函数

我们通过FacMethod和Macro两个类来实现把字符串转换成内置函数的过程。前者中插入了一个把空字符串自动改成'untitle'的功能，在blueprint.py第69行。前者可能调用的内置函数全部都是util.StrUtil的方法，而后者可能调用的内置函数则只有inkscape_control.create()。

## `$`和外部加载

当初定位是做一个代码管理库，只能调用内置的函数，可扩展性不好。在所有的内置函数前都加一个`$`，显式声明这是内置的。从第三方文件里读取函数，即外部加载功能，暂未实现。不过，应当可以用importlib实现。

## 蓝图文件化

蓝图的全部内容可以方便地转换成一个json，但现在暂未实现。直接导入导出json，比现在的导入导出txt快捷得多。当然，json的可读性不太好没有多行字符串，而yaml需要第三方库，多行字符串的第一行还需要敲空格，也不太方便（当然高级文本编辑器能解决这个空格问题）。