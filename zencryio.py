import logging

from SzQlib.zencrypt import decode, encode
from SzQlib.zfilex import JsonFileOpen, null
from SzQlib.zjson import pickle_simple

zencryio_logger = logging.getLogger("SzQlib.zencryio")


class _entryptJsonFile:
    """
    entrypt the value , not key and value
    """

    def __init__(self, filename, key, iv):
        zencryio_logger.debug("Create a encryptJsonFile object")
        self.iostream = JsonFileOpen(filename)
        self.key, self.iv = key, iv

    def __getitem__(self, item):
        cry_text = self.iostream[item]
        plain_text = decode(cry_text, self.key, self.iv)
        return pickle_simple.decode(plain_text)

    def __setitem__(self, key, value):
        value = pickle_simple.encode(value)
        cry_text = encode(value, self.key, self.iv)
        self.iostream[key] = cry_text

    def __delitem__(self, key):
        del self.iostream[key]

    def get(self, key, default=null):
        return self.iostream.get(key, default)

    def clear(self):
        self.iostream.clear()

    def set(self, key, value):
        self[key] = value

    def keys(self):
        return self.iostream.keys()

    def values(self):
        return self.iostream.values()

    def items(self):
        return self.iostream.items()

    def __iter__(self):
        return self.iostream.__iter__()

    def save(self):
        self.iostream.save()

    def flush(self):
        self.iostream.flush()

    def close(self):
        self.iostream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def EncryptJsonOpen(filename, key, iv):
    return _entryptJsonFile(filename, key, iv)


zencryio_logger.debug("Module zencryio loading ...")
