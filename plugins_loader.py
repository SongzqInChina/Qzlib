"""
一个简单的程序插件加载器

注：本模块并非`SzQlib`的插件加载器
"""

import multiprocessing
import importlib
import os
import sys
from . import path, system, out, other


class PluginClientByProcess:
    def __init__(self):
        """
        作为插件的程序必须继承或实例化这个类
        """
        self.pipe = None

    def setpipe(self, pipe):
        """
        设置管道
        :param pipe: 管道，来自模块`multiprocessing`
        """
        self.pipe = pipe
