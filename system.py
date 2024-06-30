import copy
import inspect
import os

import psutil
from win32com import client

from .processx import Process, CProcess


def wmi():
    return client.GetObject("winmgmts:")


def wmi_process():
    return wmi().InstancesOf("win32_process")


def wmi_service():
    return wmi().InstancesOf("win32_service")


def wmi_disk():
    return wmi().InstancesOf("win32_logicaldisk")


def wmi_network():
    return wmi().InstancesOf("win32_networkadapterconfiguration")


def wmi_bios():
    return wmi().InstancesOf("win32_bios")


def wmi_cpu():
    return wmi().InstancesOf("win32_processor")


def wmi_os():
    return wmi().InstancesOf("win32_operatingsystem")


def wmi_user():
    return wmi().InstancesOf("win32_useraccount")


def wmi_group():
    return wmi().InstancesOf("win32_group")


def wmi_group_user():
    return wmi().InstancesOf("win32_groupuser")


def wmi_share():
    return wmi().InstancesOf("win32_share")


def shutdown(mode: str, _time: int = 1):
    if _time < 1:
        _time = 1
    return os.system(f'shutdown -{mode} -t {_time}')


class EnvVar:
    @staticmethod
    def to_list(__value, __value_sep: str = ';'):
        return [i for i in __value.split(__value_sep) if not i.isspace() if i]

    def __init__(self, __key, __v, __value_sep: str = ';'):
        self.__value_sep = __value_sep
        self.key = __key
        self.value = __v
        # 解析value为列表
        self.value_list = self.to_list(self.value, self.__value_sep)

    def set(self, __i, __v: str):
        """
        set a new value to `env var`

        :param __i: index of env var
        :param __v: new value
        :raise ValueError: if ';' in your value
        """
        if self.__value_sep in __v:
            raise ValueError(f"value must not contain '{self.__value_sep}'")
        if __i >= len(self.value_list):
            return self.value_list.append(__v)
        self.value_list[__i] = __v

    def pop(self, __i):
        if __i >= len(self.value_list):
            raise IndexError(f'index out of range: {__i}')
        return self.value_list.pop(__i)

    def remove(self, _item):
        if _item not in self.value_list:
            raise ValueError(f'{_item} not in env var')
        self.value_list.remove(_item)

    def insert(self, __i, __v: str):
        self.value_list.insert(__i, __v)

    def append(self, __v: str):
        self.value_list.append(__v)

    def get(self, __i):
        if __i >= len(self.value_list):
            raise IndexError(f'index out of range: {__i}')
        return self.value_list[__i]

    def clear(self):
        self.value_list = []

    def load(self, string: str | None = None):
        if string is None:
            self.value_list = self.to_list(self.value, self.__value_sep)
        else:
            self.value_list = self.to_list(string, self.__value_sep)

    def __str__(self):
        return self.__value_sep.join(self.value_list)

    __repr__ = __str__


class LocalEnv:
    def __init__(self, envs: list | None = None):
        if envs is None:
            self._envs = [os.environ.copy()]  # index 0 is os.environ
        else:
            self._envs = [os.environ.copy(), *copy.deepcopy(envs)]  # copy envs

    def set(self, __i: int, __k: str, __v: str) -> None:
        self._envs[__i][__k] = __v

    def get(self, __i: int, __k: str) -> str:
        return self._envs[__i][__k]

    def add(self, __i: int, __key: str, _item: str):
        """
        add a item into a env
        """
        if __key not in self._envs[__i]:
            self._envs[__i][__key] = ""
        # get EnvVar object
        env_var = EnvVar(__key, self._envs[__i][__key])
        env_var.append(_item)
        self._envs[__i][__key] = str(env_var)

    def activate(self, __i: int):
        if __i >= len(self._envs):
            raise IndexError(f'index out of range: {__i}')
        env = self._envs[__i]
        os.environ.clear()
        os.environ.update(env)


class Runtime:
    _instance = None

    @classmethod
    def __getruntime(cls, *args, **kwargs):
        return cls.__new__(cls, *args, **kwargs)

    def __new__(cls, *args, **kwargs):
        stact = inspect.stack()[1].function
        if stact != "__getruntime":
            raise RuntimeError("Runtime class can only be instantiated by the __getruntime method")
        if cls._instance is None:
            cls._instance = super(Runtime, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self._c = Process.myClass()

    @property
    def pid(self):
        return self._c.pid

    def cpu_count(self):
        return os.cpu_count()

    def num_threads(self):
        return self._c.num_threads()

    def cpu_percent(self):
        return self._c.cpu_percent()

    def memory_percent(self):
        return self._c.memory_percent()

    def memory_info(self):
        return self._c.memory_info()

    def memory_full_info(self):
        return self._c.memory_full_info()

    def kill(self):
        self._c.kill()

    def exit(self, code):
        exit(code)

    def environ(self):
        return self._c.environ()

    def cmdline(self):
        return self._c.cmdline()

    def exec(self, command):
        return psutil.Popen(command)

    def execute(self, command):
        return CProcess(psutil.Popen(command).pid)

    @classmethod
    def getRuntime(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
