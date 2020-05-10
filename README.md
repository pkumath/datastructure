# LaTeX代码模版管理器

数据结构与算法.[wg,wyx]

## 变动

- 调整了各个函数、模块的[编排](#文件结构)
- 引入了一些新的[术语](#术语)
- 调整了[依赖](#依赖)
- `遗留问题1` 设置工作路径及 /figures 路径，包括初步的图形界面实现
- `遗留问题2` 自动复制功能 Autopaste 的跨平台实现
- `遗留问题3` 打开、保存文件时自动保存至工作路径
- 关闭 Inkscape 窗口后，自动导出 pdf 和 pdf_tex
- 原有功能初步模块化，称为“蓝图”

## 编排

- main.py 主文件
- globe.py 定义了全局变量类
- workspace.py 定义了与工作区(工作路径)有关的函数
- blueprint.py 定义了蓝图类和默认蓝图
- util.py 实用函数，目前有 StrUtil 字符串函数
- widget.py 自定义 GUI 组件
- paste.py 自动复制功能 Autopaste
- inkscape_control.py 自带的 inkscape 宏

## 术语

增加了一些（奇怪的）构想，比如工作区、蓝图……几个核心概念如下：

- 工作区 workspace：工作路径和自动生成文件的子文件夹（现在是 /figures ）
- 蓝图 blueprint：围绕着一个 tex 代码模板的一系列功能集合
  - 变量 variable：原 ttl 中的内容，即一组**原始数据**，需要在蓝图中指定变量的名称（现在只有一个：name）
  - 要素 factor：原来的 name、title，即生成代码片段中使用到的量（如图片标题、引用标签、文件名等）
  - 模板 snippet：插入 tex 正文的模板（原 latex_template）
  - 片段 fragment：一个可以直接插入 tex 源码的片段，根据变量的值和模板生成（目前也显示在模板文本框 field_snippet 内）
  - 宏 macro：一段实用程序，在生成片段后执行（inkscape.create）

## 依赖

第三方库没有改变，增加了平台判断，免于在 Mac 上安装根本跑不了的 keyboard 包。

## 全局变量

原有的全局变量有些奇怪，VSCode 一直报错，报了几十个，把真正的错误埋了，​因此去掉了，k 变成了组件自带的 hinting 属性，又使用了一个 globe 文件管理全局变量。

globe 文件里有 Globe 类，封装在类里能保证全局可用。但是 globe 文件中不能引入蓝图类 Blueprint（循环导入），因此 Globe.blueprint 初始化成了 None，容易出错。

此外，Globe 中还包括 ui、workspace 和系统类型常量。

## GUI

GUI 相关整体移到了 gui 文件，并且整理了一下，变量名改动较大，详见 CHANGELOG 文件。

field 指的是带有提示的类（HintEntry、HintText，在 widget 中，即原有的 clickentry 和 clicktext）。现在提示会显示为灰色。HintEntry 增加了获取其内容的方法 HintEntry.content()。

Tk 的组件结构有点恶心，每个组件没有名字，直接用类型和编号命名，因此全局变量使用了自定义的一个字典 Globe.ui，在 gui 的第 90 行。可以通过 ui 中的引用较为方便地在其他地方修改组件，cget 方法可以取得值，configure 方法可以设定值。

## 工作区

在文件菜单里可以设置工作路径。

Globe.workspace 中 'root' 可以取得工作路径，当然用 os 模块更方便，而 'sub' 中则是使用的子文件夹（现在只有 figures）。储存的都是字符串而非 Path 对象。

## 蓝图

原有的功能被转化为“内置的操作”，用$标明，预留了导入外部代码的可能。蓝图类中的三个生成用的方法都需要一个解包的字典做参数，现在略微有些混乱，但将来可以扩展，实现多变量的代码片段生成。

生成要素 factor 相关的方法（原来 beautify 的扩展，都在 util.StrUtil 中）：

- caption，图片标题
- fileName，文件名
- label，引用（\ref）用标签（\label）

执行宏的方法：

- inkscape

## 遗留问题和想法

- 更好地利用文件
  - 可以实现保存上次的工作路径，也许可以借助工作区的导入导出。VSCode 的工作区很强大，也许可以给我们提供一些参考。
  - 可以实现导入、导出蓝图。把一个蓝图转换成 JSON 应该比较好实现。
- GUI
  - 目前蓝图和 GUI 的配合还没有完全实现，也许可以实现将文本框中的内容保存成蓝图
  - 多变量（variable）。目前有一个变量输入框（HintEntry），只能输入一个变量，但代码片段中可能用到多个变量，因此或许可以考虑增加下拉选择框一类的组件，实现多变量。
  - 布局。目前使用 place，调参很麻烦，而且显示效果也不太稳定，也许可以换用 pack？用 Frame 嵌套配合 pack 应该可以复原现在的布局。
- 自动复制
  - 现在自动复制自动开启，也许可以加个开关
  - keyboard 的 suppress 会引起中文输入法的问题。不知道在 Mac 上用 pynput 有没有可能实现 suppress。
  - 也许可以借助工作区/蓝图实现自定义快捷键，两个包都能将字符串转化成快捷键组合。
- 外部代码：也许可以允许蓝图执行外部导入的代码？
- 文件已存在：如果文件已存在，当前 inkscape_control.create() 会直接退出。也许可以增加一个重命名的方法。

## wg路线:(2020-05-02)

- 鉴于已经初步成型,分化的可能性越来越大,为避免不同分支出现冲突先记录下自己的优先打算.
- 这两周我的重点在inkscape线程的处理.
- 希望能实现在操作Inkscape时,按快捷键可以触发外部窗口输入代码片段,并且在退出时自动粘贴到鼠标所在位置,使Inkscape极佳的与latex互动而不需要再切换到外部文本编辑.至于这一条的必要性,我想inkscape的文本插入烂到家的表现已经说明了一切.
  - 希望能实现图片的复制粘贴自动化操作,提高作图效率.
- 优先级较低的操作:
  - 希望在gui中集成目录下svg的显示,并创建edit按钮,免去查重和来回切换目录的麻烦.这将间接解决[遗留问题和想法](#遗留问题和想法)的最后一条.
  - 希望实现“蓝图”中图片标题和依赖区的同步出现,这将在极小的一部分实现与gui的配合.详细的说,是导入(图片)片段或者依赖区之后,另外一者能同步刷新.
  - 另外, 我也将试图解决上面问题中的其他方面,但是优先级更低.


