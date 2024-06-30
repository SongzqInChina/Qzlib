import importlib
import os.path

from . import system, path


def load_module(name, package=...):
    return importlib.import_module(name, package)


def reload_module(module):
    return importlib.reload(module)


def load_path(__path):
    env = system.LocalEnv()
    index = env.create_env()

    directory = os.path.dirname(__path)

    env.add(index, 'PYTHONPATH', directory)
    env.activate(index)

    module_name = os.path.basename(__path)

    module = load_module(module_name)

    env.activate(0)
    env.remove(index)

    return module




