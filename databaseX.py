import hashlib

from .filex import JsonFileOpen, JsonGet, JsonSet
from .json import *
from .libcon import *
from .path import *


class _Database_Index:
    def __init__(self, mro_path):
        self._path = mro_path
        self._index = JsonFileOpen(path_to(mro_path, "index.json"))

    def processing(self, data: dict):
        # data 是一个字典
        keys = list(data.keys())
        keys.sort()
        items = [(k, data[k]) for k in keys]
        items = map(lambda tp: getkhash(str(tp)), items)  # 获取 k 的 hash
        res_str = '-'.join(items)  # 拼接成字符串
        return res_str

    def add(self, data: dict, file: str):
        res_str = self.processing(data)

        self._index[res_str] = file  # 添加到索引中

    def remove(self, data: dict):
        res_str = self.processing(data)

        del self._index[res_str]  # 删除

    def get(self, mro, data: dict):
        res_str = self.processing(data)

        return self._index.get(res_str, None)  # 正常应该是一个文件名

    def inner(self, index):
        return





def getkstr(obj):
    return json_simple.encode(obj)  # type: str


def getkhash(kstr: str):
    return hashlib.sha256(kstr.encode()).hexdigest()  # type: str


def getkshash(obj):
    return getkhash(getkstr(obj))  # type: str


class Database:
    @property
    def dir(self):
        return self._dir

    @property
    def config(self):
        return self._config

    @property
    def data(self):
        return self._data

    def __init__(self, _dir):
        self._dir = _dir
        if not isdir(self._dir):
            mkdirs(path_to(self._dir, "data"))
        if not isdir(path_to(self._dir, "data")):
            mkdir(path_to(self._dir, "data"))

        self._config = path_to(self._dir, "config.json")
        self._data = path_to(self._dir, "data")
        self._io = JsonFileOpen(self.config)

    def setname(self, name):
        self._io['name'] = name

    def getname(self):
        return self._io['name']  # type: str

    def setversion(self, version):
        self._io['version'] = version

    def getversion(self):
        return self._io['version']

    def setauthor(self, author):
        self._io['author'] = author

    def getauthor(self):
        return self._io['author']

    def setpasswd(self, old_passwd, new_passwd):
        if hashlib.sha256(old_passwd.encode()) == self._io['passwd']:
            self._io['passwd'] = hashlib.sha256(new_passwd.encode())
            return True
        else:
            return False

    def getpasswd(self):
        return self._io['passwd']

    # 接下来是关于数据库操作的函数，需要对实际的文件进行操作
    def clear(self):
        rmdirsX(self.data)
        mkdir(self.data)

    def mkmro(self, mro):
        if isdir(path_to(self.data, mro)):
            return False
        mkdir(path_to(self.data, mro))
        # 进行初始化
        JsonSet(path_to(self.data, mro, "config.json"), version=1, name=mro)
        # -------------
        return True

    def delmro(self, mro):
        if not isdir(path_to(self.data, mro)):
            return False
        rmdirs(path_to(self.data, mro))
        return True

    def getfuncOf(self, Type=DBX_FUNC_TYPE_MRO, key=None):
        if key is None:
            raise ValueError("The 'key' parameter must be provided and cannot be None.")
        if Type == DBX_FUNC_TYPE_MRO:
            return MroFunc(self, key)
        elif Type == DBX_FUNC_TYPE_GET:  # TODO: we don't finish this func now
            raise "We don't finish this func now"
        else:
            raise ValueError("The 'Type' parameter must be DBX_FUNC_TYPE_MRO or DBX_FUNC_TYPE_FUNC.")


class MroFunc:
    def __init__(self, dbclass: Database, mro):
        self._dir = path_to(dbclass.data, mro)
        self._config = path_to(dbclass.data, mro, "config.json")
        self._template = JsonFileOpen(self._config).get('template', mktemplate())

        self._index = _Database_Index(dbclass.data)

    def settemplate(self, template, update=True):
        self._template = template
        JsonFileOpen(self._config).set('template', template).save()
        if update:
            self.update()
        return self

    def update(self):
        mro_dir = self._dir
        template = self._template

        for file_path in scandir_ls(mro_dir):
            data = JsonGet(file_path, 'data')
            if data is None:
                continue
            if not cx.Library.typefunc.template.sub(template, data):
                with JsonFileOpen(file_path) as json_file:
                    json_file.clear()
                    sorted_data = cx.Library.typefunc.template.sort(data, template)
                    json_file.set('data', sorted_data)

        return self

    def add(self, **key):
        khash = path_to(self._dir, getkshash(key))
        mkfile(khash)
        JsonSet(khash, data=key)
        self._index.add(key, khash)
        return self

    def remove(self, **key):
        if self._index.inner(key):
            self._index.remove(key)
        rmfile(path_to(self._dir, getkshash(key)))

    def absquery(self, **key):
        kstr = getkstr(key)
        khash = getkhash(kstr)
        if khash not in scandir_ls(self._dir):
            raise ValueError("The key is not exist.")
        # 返回文件内容
        return JsonGet(khash, 'data')

    def absexist(self, **key):
        khash = getkshash(key)
        return exists(path_to(self._dir, khash))


def mktemplate(**dic):
    return cx.Library.typefunc.template.Template(**dic)
