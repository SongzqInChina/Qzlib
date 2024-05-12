import os
import random
import time

import psutil

from .process import CProcess as _CProcess
from .process import PID_killPrcess, NAME_killPrcess, ProcessInfo


class Xfunc:
    ...


class CProcess(Xfunc, _CProcess):
    def pause(self):
        self.suspend()

    def recover(self):
        self.resume()

    def exitcode(self) -> int | None:
        return self.wait()


class Process(Xfunc):
    @staticmethod
    def KillById(pid):
        PID_killPrcess(pid)

    @staticmethod
    def killByName(name):
        NAME_killPrcess(name)

    @staticmethod
    def isactiveById(pid):
        return pid in psutil.pids()

    @staticmethod
    def isactiveByName(name):
        for pid in psutil.pids():
            if name == psutil.Process(pid).name():
                return True
        return False

    @staticmethod
    def get(pid):
        if Process.isactiveById(pid):
            return psutil.Process(pid)
        else:
            return None

    @staticmethod
    def getByName(name):
        for pid in psutil.pids():
            if name == psutil.Process(pid).name():
                return psutil.Process(pid)
        return None

    @staticmethod
    def getInfo(pid):
        return ProcessInfo(CProcess(pid))

    @staticmethod
    def getRuntimes(pid):
        return ProcessInfo(CProcess(pid)).runtime()

    @staticmethod
    def getCreatetime(pid):
        return ProcessInfo(CProcess(pid)).create_time()

    @staticmethod
    def getUsername(pid):
        return ProcessInfo(CProcess(pid)).username()

    @staticmethod
    def getProcessName(pid):
        return ProcessInfo(CProcess(pid)).name()

    @staticmethod
    def myPid():
        return os.getpid()

    @staticmethod
    def myClass():
        return CProcess(Process.myPid())


class Runtime(Xfunc):
    _Key = None

    @classmethod
    def _flash_key(cls):
        cls._Key = ()
        for i in range(9):
            cls._Key += (random.randint(0, 100),)

    def __init__(self, a, b, c, d, e, f, g, h, i, /):
        if (a, b, c, d, e, f, g, h, i) \
                != \
                self._Key:
            raise TypeError("Can't instantiate abstract class Callable with abstract method __call__")

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
        cls._flash_key()
        return Runtime(*cls._Key)


class Timer(Xfunc):
    def __init__(self):
        self._time = 0
        self._res = 0

    def start(self):
        self._time = time.time()

    def stop(self):
        self._res = time.time() - self._time
        return self._res

    def reset(self):
        self._time = 0
        self._res = 0

    @property
    def res(self):
        return self._res
