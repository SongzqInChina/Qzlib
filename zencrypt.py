import logging
import os

import pyaes

zencrypt_logger = logging.getLogger("SzQlib.zencrypt")


def aes_encrypt(plaintext: bytes, key, iv=None):
    if iv is None:
        iv = os.urandom(16)

    plaintext_bytes = plaintext
    padded_plaintext = plaintext_bytes
    aes = pyaes.AESModeOfOperationCBC(key, iv)
    ciphertext = aes.encrypt(padded_plaintext)
    return ciphertext, iv


def aes_decrypt(ciphertext, key, iv):
    aes = pyaes.AESModeOfOperationCBC(key, iv)
    decrypted_data = aes.decrypt(ciphertext)
    return decrypted_data


def _pkcs7_pad(data: bytes, block_size: int) -> bytes:
    if len(data) >= block_size:
        return data
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length]) * padding_length
    return data + padding


def _pkcs7_unpad(padded_data: bytes, block_size: int = 16) -> bytes:
    if not (len(padded_data) % block_size == 0 and 1 <= padded_data[-1] <= block_size):
        return padded_data  # 不需要解填充，直接返回原字节串

    last_byte = padded_data[-1]
    if last_byte > block_size:
        zencrypt_logger.error("Invalid padding byte value", last_byte)
        raise ValueError("Invalid padding byte value", last_byte)

    padding_length = last_byte
    if padded_data[-padding_length:] != bytes([last_byte]) * padding_length:
        zencrypt_logger.error("Invalid padding pattern")
        raise ValueError("Invalid padding pattern")

    return padded_data[:-padding_length]


def aes_encrypt_ls(plain_text_list, key, vi=None, NoIV=False):
    for i in plain_text_list:
        if NoIV:
            yield aes_encrypt(i, key, vi)[0]
        else:
            yield aes_encrypt(i, key, vi)


def aes_detrypt_ls(cipher_text_list, key, vi):
    for i in cipher_text_list:
        yield aes_decrypt(i, key, vi)


def split(text, size=16):
    if len(text) % size == 0:
        return [text[i:i + size] for i in range(0, len(text), size)]
    res_lenght = ((len(text) // size) + 1) * size
    add_lenght = res_lenght - len(text)
    text = pad(text, res_lenght)
    ls = split(text, size)
    ls[-1] = ls[-1][:add_lenght]
    # print(ls)
    return ls


def pad(text: bytes, size=16):
    return _pkcs7_pad(text, size)


def unpad(text: bytes, size=16):
    return _pkcs7_unpad(text, size)


def generate_key(size=16):
    return os.urandom(size)


def generate_iv(size=16):
    return os.urandom(size)


def generate(size=16):
    return generate_key(size), generate_iv(size)


def split_pad(text: bytes, size=16):
    return [pad(i, size) for i in split(text, size)]


def join(args):
    return b''.join(args)


def encode(text: str, key, iv):  # 提供一个最简单的加密api
    """
    加密函数，提供一个最简单的api加快使用效率
    :param text:
    :param key:
    :param iv:
    :return: bytes
    """
    byte = text.encode('utf-8')
    byte = split_pad(byte)
    crypt_text = aes_encrypt_ls(byte, key, iv, NoIV=True)

    return join(crypt_text)


def decode(crypt_text, key, iv):  # 提供一个最简单的解密api
    """
    解密，提供一个最简单的api加快使用效率
    :param crypt_text:
    :param key:
    :param iv:
    :return: str
    """
    crypt_list = split(crypt_text)
    plain_text = list(aes_detrypt_ls(crypt_list, key, iv))
    for i in range(len(plain_text)):
        plain_text[i] = unpad(plain_text[i])
    return join(plain_text).decode('utf-8')


def encrypt(plain_text, key, iv=None):  # 别名
    return encode(plain_text, key, iv)


def decrypt(crypt_text, key, iv=None):  # 别名
    return decode(crypt_text, key, iv)


zencrypt_logger.debug("Module zencrypt loading ...")
