#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 温刚
# 北京大学数学科学学院，jnwengang@pku.edu.cn
import os


def get_svgnames(path):
    path = rf"{path}"+os.path.sep+'figures'
    all_file = os.listdir(path)
    svg_file = []
    for i in all_file:
        if list(i.split('.'))[-1] == 'svg':
            svg_file.append(i)
    return svg_file
