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


class Environment:
    def __init__(self):
        self._env = os.environ

    def set(self, key: str, value: str):
        self._env[key] = value

    def get(self, key: str):
        return self._env.get(key)

    def delete(self, key: str):
        if key not in self._env:
            return
        del self._env[key]

    def add(self, key: str, value: str):
        if key not in self._env:
            self._env[key] = value
            return
        self._env[key] += value

    def sub(self, key: str, value: str):
        if key not in self._env:
            return
        values = self._env[key].split(';')
        self._env[key] = ';'.join(filter(lambda v: v != value, values))

    def clear(self):
        self._env.clear()

    def get_values(self, key):
        return self._env[key].split(';')

    def __iter__(self):
        for key in self._env:
            values = self.get_values(key)
            yield key, values

    def add_item(self, key, value):
        if key not in self._env:
            self.set(key, value)
            return
        values = self.get_values(key)
        if value in values:
            return
        values.append(value)
        self.set(key, ';'.join(values))


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
