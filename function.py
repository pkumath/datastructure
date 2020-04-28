#!/usr/bin/env python
# -*- coding: utf-8 -*-
def latex_template(name, title):
    """生成latex图片模版名称,为后面的其他模版做借鉴"""
    #TODO: Remove!
    
    return '\n'.join((
        r"\begin{figure}[ht]",
        r"    \centering",
        rf"    \incfig{{{name}}}",
        rf"    \caption{{{title}}}",
        rf"    \label{{fig:{name}}}",
        r"\end{figure}"))