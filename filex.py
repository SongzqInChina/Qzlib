import datetime
import os
from typing import Any

from .json import *


def property_class(*argv, **kwargs):
    class noCall:
        def __init__(self, cls):
            self.cls = cls

        @property
        def get(self):
            return self.cls(*argv, **kwargs)

    def wrap(cls):
        return noCall(cls).get

    return wrap


@property_class()
class null:
    ...


class _rw:

    def __init__(self, filename):
        if not os.path.isfile(filename):
            open(filename, 'w').close()
        self._io = open(filename, 'r+')
        self._data = {}
        self._indent = 4
        if not self._getfile():
            self._data = {}
            self._setfile()

    @property
    def indent(self):
        return self._indent

    @indent.setter
    def indent(self, value):
        """
        设置缩进
        :param value:
        :return:
        """
        self._indent = value
        self._setfile()

    def _getfile(self):
        self._io.seek(0)
        data = self._io.read()
        if len(data) < 1:
            data = "null"
        enc = pickle_free.decode(data)
        self._data = enc
        return enc

    def _clear(self):
        self._io.close()
        self._io = open(self._io.name, 'w+')

    def clear(self):
        """
        清空数据
        :return:
        """
        self._data = {}
        return self

    def _setfile(self):
        self._clear()
        self._io.write(pickle_free.encode(self._data, self._indent))

    def __setitem__(self, key, value):
        self._data[key] = value
        return self

    def __getitem__(self, item):
        return self._data[item]

    def __delitem__(self, key):
        self._data.pop(key, None)
        return self

    def get(self, key, default: object = null):
        """
        获取数据
        :param key:
        :param default: 如果不是null类，那么出错时将返回default
        :return:
        """
        if key in self._data:
            return self[key]
        elif default == null:
            return self[key]
        else:
            return default

    def set(self, key, value):
        self[key] = value
        return self

    def __len__(self):
        return len(self._data)

    def keys(self):
        """
        dict.keys()
        :return:
        """
        return self._data.keys()

    def items(self):
        """
        dict.keys()
        :return:
        """
        return self._data.items()

    def values(self):
        """
        dict.keys()
        :return:
        """
        return self._data.values()

    def __iter__(self):
        return self._data.__iter__()

    def flush_save(self):
        """
        同save
        :return:
        """
        self._setfile()
        return self

    def flush_get(self):
        """
        同flush
        :return:
        """
        self._getfile()
        return self

    def save(self):
        """
        将数据保存至文件
        :return:
        """
        self._setfile()
        return self

    def flush(self):
        """
        从文件读取数据
        :return:
        """
        self._getfile()
        return self

    def close(self):
        self.save()
        self._io.close()
        return self

    def write(self, **dic):
        self._data = dic
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def JsonFileOpen(filename):
    rw = _rw(filename)
    rw.flush_get()
    return rw


class _LogFile:
    def __init__(self, filename, clean: bool = False):
        self._f = JsonFileOpen(filename)
        self._f.indent = 4
        self._f.flush_get()
        if clean:
            self._f.clear()
            self._f.flush_save()

    def write(self, text="None", head="info", t=None):
        if not t:
            t = datetime.datetime.now()
        self._f[t] = (head, text)
        self._f.flush_save()

    def reads(self) -> list[tuple[datetime.datetime, tuple[Any, Any]]]:
        self._f.flush_get()
        objs = []
        # 返回一个列表
        for k, v in self._f.items():
            objs.append((k, v))
        for i in range(len(objs)):
            objs[i] = eval(objs[i][0], globals(), locals()), objs[i][1]
        return objs

    def clear(self):
        self._f.clear()


def LogFileOpen(filename, clean: bool = False):
    return _LogFile(filename, clean)


class _filelist:
    def __init__(self, file):
        self._f = JsonFileOpen(file)
        self._f["lst"] = []
        self._f.indent = 4

    def __iter__(self):
        return self._f["lst"].__iter__()

    def __len__(self):
        return len(self._f["lst"])

    def all(self):
        return self._f["lst"]

    def append(self, __o):
        self._f["lst"].append(__o)

    def insert(self, index, obj):
        self._f["lst"].insert(index, obj)

    def pop(self, index):
        return self._f["lst"].pop(index)

    def remove(self, obj):
        self._f["lst"].remove(obj)


def FileListOpen(file):
    return _filelist(file)


def FileCreate(filename):
    open(filename, 'a').close()


def FileDelete(filename):
    os.remove(filename)


def FileExists(filename):
    return os.path.exists(filename)


class File:
    @staticmethod
    def create(path):
        open(path, 'a').close()

    @staticmethod
    def read(path):
        with open(path, 'r') as f:
            t = f.read()
        return t

    @staticmethod
    def write(path, content):
        f = open(path, 'w')
        f.write(content)
        f.close()

    @staticmethod
    def append(path, content):
        f = open(path, 'a')
        f.write(content)
        f.close()

    @staticmethod
    def delete(path):
        import os
        os.remove(path)

    @staticmethod
    def clear(path):
        open(path, 'w').close()

    @staticmethod
    def getLogClass(path):
        return LogFileOpen(path)

    @staticmethod
    def getInfoClass(path):
        return JsonFileOpen(path)

    @staticmethod
    def getListClass(path):
        return FileListOpen(path)


def JsonGet(file, key=None):
    io = JsonFileOpen(file)
    data = dict(io)
    io.close()
    if key is None:
        return data
    elif key in data:
        return data.get(key)
    else:
        return None


def JsonSet(file, **value):
    io = JsonFileOpen(file)
    for key in value:
        io[key] = value[key]
    io.close()


def JsonSuSet(file, **dic):
    JsonFileOpen(file).clear().write(**dic).close()


def JsonClear(file):
    JsonFileOpen(file).clear().close()


def JsonEntrypt(file, key, iv=None):
    from .entrypt import aes_encrypt
    data = JsonGet(file)
    JsonClear(file)
    dstr = encode(data)
    JsonSet(file, data=aes_encrypt(dstr, key, iv))  # 将加密后的内容写入data项


def JsonDecrypt(file, key, iv=None):
    from .entrypt import aes_decrypt
    data = JsonGet(file, 'data')  # 读取data项
    data = aes_decrypt(data, key, iv)  # 解密
    JsonClear(file)
    JsonSuSet(file, **decode(data))


def JsonDecryGet(file, key, iv=None):
    from .entrypt import aes_decrypt
    data = JsonGet(file, 'data')
    return aes_decrypt(data, key, iv)


def encode(obj):
    return pickle_simple.encode(obj)


def decode(obj):
    return pickle_simple.decode(obj)
