import hashlib
import re
import socket
import struct
from typing import Iterable, Any, Literal

import ping3

from . import encrypt, typefunc
from . import thread as threading
from .json import *


def _ipa():
    """
    返回一个A类IP地址的迭代器
    :return:
    """
    i1 = 10
    for i2 in range(256):
        for i3 in range(256):
            for i4 in range(256):
                yield f"{i1}.{i2}.{i3}.{i4}"


def _ipb():
    """
    返回一个B类IP地址的迭代器
    :return:
    """
    i1 = 172
    for i2 in range(16, 32):
        for i3 in range(256):
            for i4 in range(256):
                yield f"{i1}.{i2}.{i3}.{i4}"


def _ipc():
    """
    返回一个C类IP地址的迭代器
    :return:
    """
    i1 = 192
    i2 = 168
    for i3 in range(256):
        for i4 in range(256):
            yield f"{i1}.{i2}.{i3}.{i4}"


def _ipd():
    """
    返回一个D类IP地址的迭代器
    :return:
    """
    for i1 in range(110, 132):
        for i2 in range(256):
            for i3 in range(256):
                for i4 in range(256):
                    yield f"{i1}.{i2}.{i3}.{i4}"


def _ipe():
    """
    返回一个E类IP地址的迭代器
    :return:
    """
    i1 = 127
    for i2 in range(256):
        for i3 in range(256):
            for i4 in range(256):
                yield f"{i1}.{i2}.{i3}.{i4}"


def _ipf():
    """
    返回一个F类IP地址的迭代器
    :return:
    """
    i1 = 169
    i2 = 254
    for i3 in range(256):
        for i4 in range(256):
            yield f"{i1}.{i2}.{i3}.{i4}"


def _getIP(IPClass: str):
    IPClass = IPClass.upper()[0]
    if IPClass == "A":
        return _ipa()
    elif IPClass == "B":
        return _ipb()
    elif IPClass == "C":
        return _ipc()
    elif IPClass == "D":
        return _ipd()
    elif IPClass == "E":
        return _ipe()
    elif IPClass == "F":
        return _ipf()
    else:
        return None


def getIP(IPClass: str):
    """
    IP范围：\n
    - A: 10.0.0.0-10.255.255.255\n
    - B: 172.16.0.0-172.31.255.255\n
    - C: 192.168.0.0-192.168.255.255\n
    - D: 110.0.0.0-127.255.255.255\n
    - E: 127.0.0.0-127.255.255.255\n
    - F: 169.254.0.0-169.254.255.255\n
    :param IPClass: A, B, C, D, E, F
    :return:
    """
    for i in _getIP(IPClass):
        yield i


def ping(name, timeout=1):
    """
    检查网络连通性
    :param name:
    :param timeout:
    :return:
    """
    return ping3.ping(name, timeout=timeout)


def can_ping(name, timeout=1):
    """
    是否能ping通
    :param name:
    :param timeout:
    :return:
    """
    return bool(ping(name, timeout))


def getIPseq(ip1a, ip1b, ip2a, ip2b, ip3a, ip3b, ip4a, ip4b):
    for ip1 in range(ip1a, ip1b):
        for ip2 in range(ip2a, ip2b):
            for ip3 in range(ip3a, ip3b):
                for ip4 in range(ip4a, ip4b):
                    yield f"{ip1}.{ip2}.{ip3}.{ip4}"


def _getIPv6seq(ip_ranges):
    def parse_hex_range(hex_range: str):
        match = re.match(r'^0x([0-9a-fA-F]+)-0x([0-9a-fA-F]+)$', hex_range)
        if match:
            return int(match.group(1), 16), int(match.group(2), 16)
        else:
            raise ValueError(f"Invalid hexadecimal range: {hex_range}")

    parsed_ranges = [parse_hex_range(hr) for hr in ip_ranges]

    for ip1 in range(parsed_ranges[0][0], parsed_ranges[0][1]):
        for ip2 in range(parsed_ranges[1][0], parsed_ranges[1][1]):
            for ip3 in range(parsed_ranges[2][0], parsed_ranges[2][1]):
                for ip4 in range(parsed_ranges[3][0], parsed_ranges[3][1]):
                    for ip5 in range(parsed_ranges[4][0], parsed_ranges[4][1]):
                        for ip6 in range(parsed_ranges[5][0], parsed_ranges[5][1]):
                            for ip7 in range(parsed_ranges[6][0], parsed_ranges[6][1]):
                                for ip8 in range(parsed_ranges[7][0], parsed_ranges[7][1]):
                                    hex_ip1 = format(ip1, '04x')
                                    hex_ip2 = format(ip2, '04x')
                                    hex_ip3 = format(ip3, '04x')
                                    hex_ip4 = format(ip4, '04x')
                                    hex_ip5 = format(ip5, '04x')
                                    hex_ip6 = format(ip6, '04x')
                                    hex_ip7 = format(ip7, '04x')
                                    hex_ip8 = format(ip8, '04x')

                                    yield \
                                        f"{hex_ip1}:{hex_ip2}:{hex_ip3}:{hex_ip4}:{hex_ip5}:{hex_ip6}:{hex_ip7}:{hex_ip8}"


def getIPv6seq(
        ip1='0x0-0xffff',
        ip2='0x0-0xffff',
        ip3='0x0-0xffff',
        ip4='0x0-0xffff',
        ip5='0x0-0xffff',
        ip6='0x0-0xffff',
        ip7='0x0-0xffff',
        ip8='0x0-0xffff'
):
    return _getIPv6seq([ip1, ip2, ip3, ip4, ip5, ip6, ip7, ip8])


def getIPv6seqi(
        ip1='0-65536',
        ip2='0-65536',
        ip3='0-65536',
        ip4='0-65536',
        ip5='0-65536',
        ip6='0-65536',
        ip7='0-65536',
        ip8='0-65536'
):
    # Convert integer ranges to hexadecimal format for compatibility with _getIPv6seq function
    hex_ip_ranges = [f"0x{ip1[0]:04x}-0x{ip1[1]:04x}",
                     f"0x{ip2[0]:04x}-0x{ip2[1]:04x}",
                     f"0x{ip3[0]:04x}-0x{ip3[1]:04x}",
                     f"0x{ip4[0]:04x}-0x{ip4[1]:04x}",
                     f"0x{ip5[0]:04x}-0x{ip5[1]:04x}",
                     f"0x{ip6[0]:04x}-0x{ip6[1]:04x}",
                     f"0x{ip7[0]:04x}-0x{ip7[1]:04x}",
                     f"0x{ip8[0]:04x}-0x{ip8[1]:04x}"]

    # Validate the input ranges
    for range_str in hex_ip_ranges:
        start, end = range_str.split('-')
        if int(start, 16) < 0 or int(end, 16) > 0xffff:
            raise ValueError(f"Invalid IPv6 sequence integer range: {range_str}")

    return _getIPv6seq(hex_ip_ranges)


def IP4to6(ip4):
    ipv4_bytes = ip4.split('.')

    # 将每个字节转换为十六进制并补足到四位（例如 '0' + '123' -> '0123'）
    ipv4_hex = [hex(int(byte))[2:].zfill(2) for byte in ipv4_bytes]

    # IPv4地址内嵌到IPv6地址的格式为 ::ffff:0a0b:0c0d，其中0a0b:0c0d是IPv4地址的十六进制形式
    ipv6_prefix = "ffff:"
    ipv6_mapped = ipv6_prefix + ":".join(ipv4_hex)

    # 前面添加 "::" 表示高位部分全为0
    full_ipv6_address = "::" + ipv6_mapped

    return full_ipv6_address


def toip(url):
    try:
        ip = socket.gethostbyname(url)
    except socket.gaierror:
        ip = None
    return ip


def toname(ip):
    # 尝试将IP地址解析为域名
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        # 如果出现无法反向解析IP地址的情况，返回错误信息
        return None


def pack(data):
    # --------------------
    #   8   |   32  |   16  |   64     | *
    # 长度报文| sha256 | md5  |  sha512 |数据
    data_size = struct.pack("<Q", len(data))  # 使用小端序8个字节无符号整数表示数据长度
    sha256 = hashlib.sha256(data).digest()  # 直接获取二进制哈希值，无需hexdigest()
    md5 = hashlib.md5(data).digest()
    sha512 = hashlib.sha512(data).digest()
    data_bytes = data_size + sha256 + md5 + sha512 + data
    return data_bytes


def unpack(data):
    data_size = struct.unpack("<Q", data[:8])[0]  # 解码数据长度
    offset = typefunc.index_offset.offset(data)
    offset.start = 8
    sha256 = offset.offset(32)
    md5 = offset.offset(16)
    sha512 = offset.offset(64)
    o_data = offset.offset(data_size)
    return o_data, sha256, md5, sha512, data_size


def unpacks(__data: bytes):
    data = typefunc.index_offset.offset(__data)

    hash_size = 32 + 16 + 64
    head_size = 8

    result = []

    while not data.isend():
        data_size = struct.unpack("<Q", data.n_offset(head_size))[0]
        data_bytes = data.offset(head_size + hash_size + data_size)
        unpacking_data = unpack(data_bytes)
        result.append({
            "data": unpacking_data[0],
            "sha256": unpacking_data[1],
            "md5": unpacking_data[2],
            "sha512": unpacking_data[3],
            "lenght": data_size
        })
    return result  # type: list[dict[Literal["data", "sha256", "md5", "sha512", "lenght"]]]


def unpackskey(__data, *keys):
    unpacking_data = unpacks(__data)
    for item in range(len(unpacking_data)):
        item_dict = ()
        for key in keys:
            item_dict += (unpacking_data[item][key],)
        yield item_dict


def _packs(data_list: Iterable[bytes]):
    for data in data_list:
        yield pack(data)


def packs(data_list: Iterable[bytes]):
    return b''.join(_packs(data_list))


class SimpleSocket:
    def __init__(self):
        self.thread = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lasterror = None
        self._buffer = []
        self.lock = threading.Lock()

    def set(self, sock, start_server=True):
        self.sock.close()
        self.sock = sock  # type: socket.socket
        if start_server:
            self.start_server()

    def getlasterror(self):
        e = self.lasterror
        self.lasterror = None
        return e

    def settimeout(self, timeout):
        self.sock.settimeout(timeout)

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            self.getlasterror()
            self.start_server()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def bindport(self, port):  # 绑定端口
        try:
            self.sock.bind(('', port))
            self.getlasterror()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def bind(self, host, port):  # 绑定端口
        try:
            self.sock.bind((host, port))
            self.getlasterror()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def listen(self, backlog=1):
        try:
            self.sock.listen(backlog)
            self.getlasterror()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def accept(self):
        conn, addr = self.sock.accept()
        conn_simple = self.__class__()
        conn_simple.set(conn)
        return conn_simple, addr

    def write(self, data):
        data_bytes = pickle_simple.encode(data).encode()
        packing_data_bytes = pack(data_bytes)

        try:
            self.sock.sendall(packing_data_bytes)
            self.getlasterror()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def _read_loop(self):
        while True:
            try:
                data = self._read()
                if data is not None:
                    for item in data:
                        self.lock.acquire()
                        self._buffer.append(item['data'])
                        self.lock.release()
            except Exception as e:
                self._thread_lasterror = e
                print(e)

    def _read(self):
        every_data = b""
        try:
            while True:
                every_data += self.sock.recv(65535)
                if len(every_data) < 65535:
                    break

        except socket.herror as e:
            self.lasterror = e
            return None

        if every_data == b'':
            return None

        unpacking_datas = unpacks(every_data)
        return unpacking_datas

    def read(self):
        self.lock.acquire()
        data = self._buffer.pop(0) if typefunc.list.hasindex(self._buffer, 0) else None  # type: bytes | None
        self.lock.release()
        if data is not None:
            data_str = data.decode()
            original_data = pickle_simple.decode(data_str)
            return original_data
        return data

    def start_server(self):
        if self.thread is not None:
            raise "Server is running already" from 0
        self.thread = threading.get_new_thread(self._read_loop)
        self.thread.setDaemon(True)
        self.thread.start()
