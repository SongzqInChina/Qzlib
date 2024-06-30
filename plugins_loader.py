"""
一个简单的程序插件加载器

注：本模块并非`SzQlib`的插件加载器
"""

import multiprocessing
import importlib
import os
import sys
from . import path, system, out, other

class ImportMode(object):
    pass

class PluginServerImportMode(ImportMode):
    """
    PluginServer with Import Mode
    """
    def __init__(self, program_name):
        self.program_name = program_name
        self.plugins = {}

    def add_plugin(self, plugin_path):
        pass