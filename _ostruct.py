import struct


def pack(data):
    """
    **Format Mro**

    - x           pad byte
    - c           char
    - b           int8
    - B           uint8
    - h           int16
    - H           uint16
    - i           int32
    - I           uint32
    - l           int64
    - L           uint64
    - f           float
    - d           double
    - s           char[]
    - q           long long
    - Q           unsigned long long
    - e           half float
    - f           float
    - d           double
    - n           long long
    - N           unsigned long long
    - p           bytes
    - P           int(Point)
    - ?           bool
    """
    data_type = type(data)
    if data_type == int:
        if data > 0:
            return struct.pack("<q", data)
        return struct.pack("<q", data)
    elif data_type == float:
        return struct.pack("<d", data)
    elif data_type == str:
        raise TypeError from TypeError("argument for 's' must be a bytes object")
    elif data_type == bytes:
        return data
    elif data_type == bool:
        return struct.pack("<?", data)
    else:
        raise TypeError("unsupported data type: {}".format(data_type))


def unpack(data_type, data):
    if data_type == int:
        return struct.unpack("<q", data)[0]
    elif data_type == float:
        return struct.unpack("<d", data)[0]
    elif data_type == str:
        return struct.unpack("<s", data)[0]
    elif data_type == bytes:
        return struct.unpack("<p", data)[0]
    elif data_type == bool:
        return struct.unpack("<?", data)[0]
    else:
        raise TypeError("Unsupported data type: {}".format(data_type))
