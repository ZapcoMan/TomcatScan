# AjpForwardRequest.py
# -*- coding: utf-8 -*-
# @Time    : 13 1月 2025 11:54 下午
# @Author  : codervibe
# @File    : AjpForwardRequest.py
# @Project : TomcatScan
import struct
from io import BytesIO as StringIO

from common.common import pack_string, unpack, unpack_string
from model.AjpResponse import AjpResponse

# 定义HTTP请求方法的常量
_, OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK, ACL, REPORT, VERSION_CONTROL, CHECKIN, CHECKOUT, UNCHECKOUT, SEARCH, MKWORKSPACE, UPDATE, LABEL, MERGE, BASELINE_CONTROL, MKACTIVITY = range(28)

# 创建一个映射，将HTTP请求方法字符串映射到相应的常量
REQUEST_METHODS = {'GET': GET, 'POST': POST, 'HEAD': HEAD, 'OPTIONS': OPTIONS, 'PUT': PUT, 'DELETE': DELETE, 'TRACE': TRACE}

# 定义数据传输方向的常量
SERVER_TO_CONTAINER, CONTAINER_TO_SERVER = range(2)

# 定义常见的HTTP请求头的常量
COMMON_HEADERS = [
    "SC_REQ_ACCEPT",
    "SC_REQ_ACCEPT_CHARSET", "SC_REQ_ACCEPT_ENCODING", "SC_REQ_ACCEPT_LANGUAGE",
    "SC_REQ_AUTHORIZATION",
    "SC_REQ_CONNECTION", "SC_REQ_CONTENT_TYPE", "SC_REQ_CONTENT_LENGTH", "SC_REQ_COOKIE",
    "SC_REQ_COOKIE2",
    "SC_REQ_HOST", "SC_REQ_PRAGMA", "SC_REQ_REFERER", "SC_REQ_USER_AGENT"
]

# 定义请求属性的常量
ATTRIBUTES = [
    "context", "servlet_path", "remote_user", "auth_type", "query_string", "route", "ssl_cert",
    "ssl_cipher", "ssl_session", "req_attribute", "ssl_key_size", "secret", "stored_method"
]

class AjpForwardRequest:
    """
    AJP Forward 请求类。
    """

    def __init__(self, data_direction=None):
        """
        初始化AjpForwardRequest对象。

        参数:
            data_direction: 数据方向，默认为None
        """
        self.headers = {}
        self.prefix_code = 0x02
        self.method = None
        self.protocol = None
        self.req_uri = None
        self.remote_addr = None
        self.remote_host = None
        self.server_name = None
        self.server_port = None
        self.is_ssl = None
        self.num_headers = None
        self.request_headers = None
        self.attributes = None
        self.data_direction = data_direction

    def pack_headers(self):
        """
        打包请求头。

        返回:
            bytes: 打包后的请求头数据
        """
        self.num_headers = len(self.request_headers)
        res = struct.pack(">h", self.num_headers)
        for h_name in self.request_headers:
            if h_name.startswith("SC_REQ"):
                code = COMMON_HEADERS.index(h_name) + 1
                res += struct.pack("BB", 0xA0, code)
            else:
                res += pack_string(h_name)

            res += pack_string(self.request_headers[h_name])
        return res

    def pack_attributes(self):
        """
        打包属性。

        返回:
            bytes: 打包后的属性数据
        """
        res = b""
        for attr in self.attributes:
            a_name = attr['name']
            code = ATTRIBUTES.index(a_name) + 1
            res += struct.pack("b", code)
            if a_name == "req_attribute":
                aa_name, a_value = attr['value']
                res += pack_string(aa_name)
                res += pack_string(a_value)
            else:
                res += pack_string(attr['value'])
        res += struct.pack("B", 0xFF)
        return res

    def serialize(self):
        """
        序列化请求。

        返回:
            bytes: 序列化后的请求数据
        """
        res = struct.pack("bb", self.prefix_code, self.method)
        res += pack_string(self.protocol)
        res += pack_string(self.req_uri)
        res += pack_string(self.remote_addr)
        res += pack_string(self.remote_host)
        res += pack_string(self.server_name)
        res += struct.pack(">h", self.server_port)
        res += struct.pack("?", self.is_ssl)
        res += self.pack_headers()
        res += self.pack_attributes()
        if self.data_direction == SERVER_TO_CONTAINER:
            header = struct.pack(">bbh", 0x12, 0x34, len(res))
        else:
            header = struct.pack(">bbh", 0x41, 0x42, len(res))
        return header + res

    def parse(self, raw_packet):
        """
        解析原始数据包。

        参数:
            raw_packet: 原始数据包
        """
        stream = StringIO(raw_packet)
        self.magic1, self.magic2, data_len = unpack(stream, "bbH")
        self.prefix_code, self.method = unpack(stream, "bb")
        self.protocol = unpack_string(stream)
        self.req_uri = unpack_string(stream)
        self.remote_addr = unpack_string(stream)
        self.remote_host = unpack_string(stream)
        self.server_name = unpack_string(stream)
        self.server_port = unpack(stream, ">h")
        self.is_ssl = unpack(stream, "?")
        self.num_headers, = unpack(stream, ">H")
        self.request_headers = {}
        for i in range(self.num_headers):
            code, = unpack(stream, ">H")
            if code > 0xA000:
                h_name = COMMON_HEADERS[code - 0xA001]
            else:
                h_name = unpack(stream, "%ds" % code)
                stream.read(1)  # \0
            h_value = unpack_string(stream)
            self.request_headers[h_name] = h_value

    def send_and_receive(self, socket, stream, save_cookies=False):
        """
        发送请求并接收响应。

        参数:
            socket: 套接字对象
            stream: 数据流对象
            save_cookies: 是否保存cookie，默认为False
        返回:
            list: 响应数据列表
        """
        res = []
        i = socket.sendall(self.serialize())
        if self.method == POST:
            return res

        r = AjpResponse.receive(stream)
        assert r.prefix_code == AjpResponse.SEND_HEADERS
        res.append(r)
        if save_cookies and 'Set-Cookie' in r.response_headers:
            self.headers['SC_REQ_COOKIE'] = r.response_headers['Set-Cookie']

        # read body chunks and end response packets
        while True:
            r = AjpResponse.receive(stream)
            res.append(r)
            if r.prefix_code == AjpResponse.END_RESPONSE:
                break
            elif r.prefix_code == AjpResponse.SEND_BODY_CHUNK:
                continue
            else:
                raise NotImplementedError
                break

        return res
