# -*- coding: utf-8 -*-
# @Time    : 13 1月 2025 11:58 下午
# @Author  : codervibe
# @File    : AjpBodyRequest.py
# @Project : TomcatScan
import struct

from . import AjpResponse


class AjpBodyRequest:
    """
    AJP Body 请求类。
    """
    SERVER_TO_CONTAINER, CONTAINER_TO_SERVER = range(2)
    MAX_REQUEST_LENGTH = 8186

    def __init__(self, data_stream, data_len, data_direction=None):
        """
        初始化AjpBodyRequest对象。

        参数:
            data_stream: 数据流对象
            data_len: 数据长度
            data_direction: 数据方向，默认为None
        """
        self.data_stream = data_stream
        self.data_len = data_len
        self.data_direction = data_direction

    def serialize(self):
        """
        序列化数据。

        返回:
            bytes: 序列化后的数据
        """
        data = self.data_stream.read(AjpBodyRequest.MAX_REQUEST_LENGTH)
        if len(data) == 0:
            return struct.pack(">bbH", 0x12, 0x34, 0x00)
        else:
            res = struct.pack(">H", len(data))
            res += data
        if self.data_direction == AjpBodyRequest.SERVER_TO_CONTAINER:
            header = struct.pack(">bbH", 0x12, 0x34, len(res))
        else:
            header = struct.pack(">bbH", 0x41, 0x42, len(res))
        return header + res

    def send_and_receive(self, socket, stream):
        """
        发送数据并接收响应。

        参数:
            socket: 套接字对象
            stream: 数据流对象
        """
        while True:
            data = self.serialize()
            socket.send(data)
            r = AjpResponse.receive(stream)
            while r.prefix_code != AjpResponse.GET_BODY_CHUNK and r.prefix_code != AjpResponse.SEND_HEADERS:
                r = AjpResponse.receive(stream)

            if r.prefix_code == AjpResponse.SEND_HEADERS or len(data) == 4:
                break