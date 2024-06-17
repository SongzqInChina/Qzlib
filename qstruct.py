from typing import Any

from . import _ostruct as ostruct
from . import hash as shash
from . import typefunc, time
from .json import pickle_simple


def simple_pack(data: bytes):
    data_bytes = data
    data_len = len(data_bytes)
    data_len_bytes = ostruct.pack(data_len)
    return data_len_bytes + data_bytes


def simple_unpack(data: bytes) -> bytes:
    data_offset = typefunc.index_offset.Offset(data)
    data_lenght = ostruct.unpack(int, data_offset > 8)
    return data_offset.offset(data_lenght)


def simple_unpacks(data: bytes):
    data_offset = typefunc.index_offset.Offset(data)
    data_lenght = ostruct.unpack(int, data_offset > 8)
    one_data = data_offset.offset(data_lenght)
    if data_offset.isend():
        return [one_data]
    else:
        return [one_data, *simple_unpacks(bytes([*data_offset]))]


def simple_unpack_one(data: bytes):
    data_offset = typefunc.index_offset.Offset(data)
    data_lenght = ostruct.unpack(int, data_offset > 8)
    return (data_offset.offset(data_lenght)), bytes(list(data_offset))


def simple_jsonpickle_pack(data: Any):
    jsonpickle_data = pickle_simple.encode(data)
    return simple_pack(jsonpickle_data.encode())


def simple_jsonpickle_unpack(data: bytes):
    orial_data = simple_unpack(data)
    return pickle_simple.decode(orial_data.decode())


def simple_jsonpickle_unpacks(data: bytes):
    orial_data_list = simple_unpacks(data)
    return [pickle_simple.decode(x.decode()) for x in orial_data_list]


def simple_jsonpickle_unpack_one(data: bytes):
    orial_one_data, data_ = simple_unpack_one(data)
    return pickle_simple.decode(orial_one_data.decode()), data_


def pack(data_format: list[str], data_format_lenghts: list[int | tuple], data):
    """
    pack a str object

    :param data_format: formating list.
    :param data_format_lenghts: formating list.
    :param data:
    :return:
    """
    # ["lenght"]
    data_format_packing_str = simple_pack(  # 打包格式化字符串，用于在解包时使用
        pickle_simple.encode(data_format).encode()
    )
    data_format_str_lenght_bytes = simple_pack(  # 打包格式化字符串长度，用于在解包时使用
        pickle_simple.encode(data_format_lenghts).encode()
    )

    data_lenght = len(data)  # 获取数据长度

    if len(data_format) != len(data_format_lenghts):  # 判断格式化字符串长度是否一致
        raise Exception("data_format and data_format_lenghts must have same length")

    result = b''

    for x, y in zip(data_format, data_format_lenghts):
        if x == "lenght":
            result += ostruct.pack_anylenght(data_lenght, y)
            continue
        if x == "data":
            result += ostruct.pack_anylenght(data, y)
            continue
        if x == "timestamp":
            result += ostruct.pack_anylenght(int(time.time.time()), y)
            continue
        if x == "hash":
            hash_name = y[0]
            hash_lenght = y[1]
            hash_value = shash.gethashByName(data, hash_name, hash_lenght)
            result += simple_jsonpickle_pack((hash_name, hash_value))
            continue
    #      # simple_pack(data_format_str_lenght_bytes)              # simple_pack(result)
    return data_format_str_lenght_bytes + data_format_packing_str + simple_pack(result)
    #                                    # simple_pack(data_format_packing_str)

def unpack(__data):
    datas = simple_unpacks(__data)
    data_format_str_list = pickle_simple.decode(datas[0])  # 解包格式化字符串
    data_format_lenghts_list = pickle_simple.decode(datas[1])  # 解包格式化字符串长度
    orial_data = typefunc.index_offset.Offset(datas[2])  # 获取数据

    # 根据format解包数据
    data_data = []
    for x, y in zip(data_format_str_list, data_format_lenghts_list):  # 遍历格式化字符串
        if x == "lenght":
            data_data.append(ostruct.unpack_anylenght(int, orial_data.offset(y), y))
            continue
        if x == "data":
            data_data.append(ostruct.unpack_anylenght(bytes, orial_data.offset(y), y))
            continue
        if x == "timestamp":
            data_data.append(ostruct.unpack_anylenght(int, orial_data.offset(y), y))
            continue
        if x == "hash":
            hash_name, hash_lenght, hash_value = pickle_simple.decode(
                ostruct.unpack_anylenght(bytes, orial_data.offset(y), y)
            )
            data_data.append((hash_name, hash_lenght, hash_value))

    return data_format_str_list, data_format_lenghts_list, data_data
