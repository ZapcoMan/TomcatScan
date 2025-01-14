# -*- coding: utf-8 -*-
# @Time    : 13 1月 2025 11:56 下午
# @Author  : codervibe
# @File    : AjpResponse.py
# @Project : TomcatScan

from . import AjpResponse
from common.common import unpack, unpack_string


class AjpResponse:
    """
    AJP 响应类。
    """
    _, _, _, SEND_BODY_CHUNK, SEND_HEADERS, END_RESPONSE, GET_BODY_CHUNK = range(7)
    COMMON_SEND_HEADERS = [
        "Content-Type", "Content-Language", "Content-Length", "Date", "Last-Modified",
        "Location", "Set-Cookie", "Set-Cookie2", "Servlet-Engine", "Status", "WWW-Authenticate"
    ]

    def parse(self, stream):
        """
        解析响应数据。

        参数:
            stream: 数据流对象
        """
        self.magic, self.data_length, self.prefix_code = unpack(stream, ">HHb")

        if self.prefix_code == AjpResponse.SEND_HEADERS:
            self.parse_send_headers(stream)
        elif self.prefix_code == AjpResponse.SEND_BODY_CHUNK:
            self.parse_send_body_chunk(stream)
        elif self.prefix_code == AjpResponse.END_RESPONSE:
            self.parse_end_response(stream)
        elif self.prefix_code == AjpResponse.GET_BODY_CHUNK:
            self.parse_get_body_chunk(stream)
        else:
            raise NotImplementedError

    def parse_send_headers(self, stream):
        """
        解析发送的响应头。
        """
        self.http_status_code, = unpack(stream, ">H")
        self.http_status_msg = unpack_string(stream)
        self.num_headers, = unpack(stream, ">H")
        self.response_headers = {}
        for i in range(self.num_headers):
            code, = unpack(stream, ">H")
            if code <= 0xA000:  # custom header
                h_name, = unpack(stream, "%ds" % code)
                stream.read(1)  # \0
                h_value = unpack_string(stream)
            else:
                h_name = AjpResponse.COMMON_SEND_HEADERS[code - 0xA001]
                h_value = unpack_string(stream)
            self.response_headers[h_name] = h_value

    def parse_send_body_chunk(self, stream):
        """
        解析发送的响应体块。
        """
        self.data_length, = unpack(stream, ">H")
        self.data = stream.read(self.data_length + 1)

    def parse_end_response(self, stream):
        """
        解析结束响应。
        """
        self.reuse, = unpack(stream, "b")

    def parse_get_body_chunk(self, stream):
        """
        解析获取的响应体块。
        """
        rlen, = unpack(stream, ">H")
        return rlen

    @staticmethod
    def receive(stream):
        """
        接收并解析数据。

        参数:
            stream: 数据流对象
        返回:
            AjpResponse: 解析后的响应对象
        """
        r = AjpResponse()
        r.parse(stream)
        return r
