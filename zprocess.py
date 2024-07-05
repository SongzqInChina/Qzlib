import time
from os import system as cmd
from typing import Any

import psutil


class CProcess(psutil.Process):
    def runtime(self):
        return time.time() - self.create_time()

    def as_dict(self, attrs: list[str] |
                             tuple[str, ...] |
                             set[str] |
                             frozenset[str] | None = (),
                ad_value: Any | None = ...):
        o = psutil.Process.as_dict(self, attrs, ad_value)
        o["runtime"] = self.runtime()
        return o


class ProcessInfo:
    def __init__(self, ps: CProcess):
        self._dict = ps.as_dict()

    def name(self):
        return self._dict["name"]

    @property
    def pid(self):
        return self._dict["pid"]

    def pwd(self):
        return self._dict["pwd"]

    def exe(self):
        return self._dict["exe"]

    def create_time(self):
        return self._dict["create_time"]

    def runtime(self):
        return self._dict["runtime"]

    def status(self):
        return self._dict["status"]

    def environ(self):
        return self._dict["environ"]

    def cmdline(self):
        return self._dict["cmdline"]

    def username(self):
        return self._dict["username"]

    def open_files(self):
        return self._dict["open_files"]

    def threads(self):
        return self._dict["threads"]

    @property
    def ppid(self):
        return self._dict["ppid"]

    def num_threads(self):
        return self._dict["num_threads"]

    def __str__(self):
        return f"name:{self.name()}\n" \
               f"pid:{self.pid}\n" \
               f"pwd:{self.pwd()}\n" \
               f"exe:{self.exe()}\n" \
               f"create_time:{self.create_time()}\n" \
               f"runtime:{self.runtime()}\n" \
               f"status:{self.status()}\n"

    def __repr__(self):
        return f"name:{self.name()}\n" \
               f"pid:{self.pid}\n" \
               f"pwd:{self.pwd()}\n" \
               f"exe:{self.exe()}\n" \
               f"create_time:{self.create_time()}\n" \
               f"runtime:{self.runtime()}\n" \
               f"status:{self.status()}\n"


def sys_process() -> tuple[CProcess, ...]:
    """
    return Process()
    """
    p = Any
    objects = ()
    for p in psutil.process_iter():
        try:
            objects += (CProcess(p.pid),)
        except psutil.NoSuchProcess:
            continue

    return objects


def find_processes(name):
    p = sys_process()
    objs = []
    for i in p:
        if i.name() == name:
            objs.append(i)
    return objs


def NAME_killPrcess(ProcessName):
    cmd(f"taskkill /f /im {ProcessName}")


def PID_killPrcess(pid: int):
    cmd(f"taskkill /f /pid {pid}")


def to_info(ps: tuple[CProcess, ...]):
    objs = []
    for i in ps:
        o = ProcessInfo(i)
        objs.append(o)
    return objs
