# -*- coding: utf-8 -*-
# @Time    : 14 1月 2025 12:46 上午
# @Author  : codervibe
# @File    : common.py
# @Project : TomcatScan
import struct


def unpack(stream, fmt):
    """
    解包字节流。

    参数:
        stream (io.BytesIO): 字节流
        fmt (str): 解包格式

    返回:
        tuple: 解包后的数据
    """
    size = struct.calcsize(fmt)
    buf = stream.read(size)
    return struct.unpack(fmt, buf)


def unpack_string(stream):
    """
    解包字符串。

    参数:
        stream (io.BytesIO): 字节流

    返回:
        str: 解包后的字符串
    """
    size, = unpack(stream, ">h")
    if size == -1:  # null string
        return None
    res, = unpack(stream, "%ds" % size)
    stream.read(1)  # \0
    return res


def pack_string(s):
    """
    打包字符串，添加长度信息。

    参数:
        s (str): 输入字符串

    返回:
        bytes: 打包后的字节数据
    """
    if s is None:
        return struct.pack(">h", -1)
    l = len(s)
    return struct.pack(">H%dsb" % l, l, s.encode('utf8'), 0)

