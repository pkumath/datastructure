from platform import system

class Globe():
    '''Globe

    模块之间共用的全局变量。
    - ui: 包含GUI各元素引用的字典
    - workspace: 工作区文件夹
    - template: 模板设置
    - SYSTEM: 操作系统名称，Darwin/Windows
    '''
    
    ui = {}
    '''
    Globe.ui[widget][name]

    修改界面元素：
    some.cget("somecfg")
    some.configure(somecfg=somevalue)
    '''
  
    workspace = {}
    workspace['sub'] = {}

    template = {}

    SYSTEM = system()
