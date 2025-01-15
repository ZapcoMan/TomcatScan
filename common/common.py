# -*- coding: utf-8 -*-
# @Time    : 14 1月 2025 12:46 上午
# @Author  : codervibe
# @File    : common.py
# @Project : TomcatScan
import random
import secrets
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


def getRandomUserAgent():
    """
    获取随机的User-Agent。

    返回:
        str: 随机的User-Agent
    """
    # 定义一组常见的User-Agent，用于模拟不同的浏览器请求
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    ]
    return secrets.choice(user_agents)
