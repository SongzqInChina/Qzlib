import hashlib
import struct

from . import hash as shash
from . import typefunc
from typing import Generator
from .typefunc.index_offset import offset

cdef bytes pack(bytes data, hashes=None):
    # --------------------
    # init_head |  8       | hash报文  | *
    # 初始化头    |长度报文 | hash报文 | 数据
    # init_head = struct.pack("<Q", len(data_bytes+8))  # 加上自己的长度
    if hashes is None:
        hashes = ["md5", "sha256", "sha512"]
    cdef bytes data_size = struct.pack("<Q", len(data))  # 使用小端序8个字节无符号整数表示数据长度
    cdef bytes hash_head = b""
    for hash_name in hashes:
        # hash_size hash_name_size data_hash hash_name
        if hash_name in hashlib.__dict__:
            cdef bytes data_hash = shash.gethashByName(data, hash_name)
            cdef bytes hash_name_bytes = hash_name.encode("utf-8")
            cdef bytes hash_name_size = struct.pack("<Q", len(hash_name_bytes))
            cdef bytes hash_size = struct.pack("<Q", len(data_hash))
            hash_head += hash_size + hash_name_size + data_hash + hash_name_bytes

    cdef bytes data_bytes = data_size + hash_head + data
    cdef bytes init_head = struct.pack("<Q", len(data_bytes) + 8)
    return init_head + data_bytes


cdef tuple[bytes, dict] __unpack(bytes __data):
    cdef offset data = offset(__data)
    cdef int init_head = struct.unpack("<Q", data > 8)[0]

    cdef offset now_data = data.offseter(init_head - 8)

    cdef int data_size = struct.unpack("<Q", now_data > 8)[0]
    data_bytes = now_data[-data_size:]
    cdef offset data_hashes = offset(now_data[: -data_size])
    data_hashes += 8
    cdef dict hashes = {}
    # 分离hash
    while True:
        cdef bytes hash_size = struct.unpack("<Q", data_hashes > 8)[0]
        cdef bytes hash_name_size = struct.unpack("<Q", data_hashes > 8)[0]
        cdef bytes data_hash = data_hashes > hash_size
        cdef bytes hash_name = data_hashes > hash_name_size
        hashes[hash_name.decode()] = data_hash
        if data_hashes.isend():
            break
    return data_bytes, hashes


cdef list __unpacks(offset __data):
    data = __data
    init_head = struct.unpack("<Q", data >= 8)[0]
    now_data = data.offseter(init_head)
    if not data.isend():
        return [now_data, *__unpacks(data)]
    return [now_data]


cdef Generator unpacks(__data):
    cdef offset data = offset(__data)
    cdef map map_data = map(lambda x: __unpack(x.to(bytes)), __unpacks(data))
    for i in map_data:
        yield i


cdef list lunpacks(__data):
    return list(unpacks(__data))
