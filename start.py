#!/usr/bin/env python
# -*- coding: utf-8 -*-
#温刚
#北京大学数学科学学院，jnwengang@pku.edu.cn
import os
import time

a = 4
while a != 0:
   try:
      a = os.system("python3 main.py")
      print(a)
   except Exception as e:
      print("Exception occured:")