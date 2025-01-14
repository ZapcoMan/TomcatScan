# constants.py
# -*- coding: utf-8 -*-
# @Time    : 14 1月 2025 12:55 上午
# @Author  : codervibe
# @File    : constants.py
# @Project : TomcatScan

_, OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK, ACL, REPORT, VERSION_CONTROL, CHECKIN, CHECKOUT, UNCHECKOUT, SEARCH, MKWORKSPACE, UPDATE, LABEL, MERGE, BASELINE_CONTROL, MKACTIVITY = range(28)
REQUEST_METHODS = {'GET': GET, 'POST': POST, 'HEAD': HEAD, 'OPTIONS': OPTIONS, 'PUT': PUT, 'DELETE': DELETE, 'TRACE': TRACE}
SERVER_TO_CONTAINER, CONTAINER_TO_SERVER = range(2)
COMMON_HEADERS = ["SC_REQ_ACCEPT", "SC_REQ_ACCEPT_CHARSET", "SC_REQ_ACCEPT_ENCODING", "SC_REQ_ACCEPT_LANGUAGE", "SC_REQ_AUTHORIZATION", "SC_REQ_CONNECTION", "SC_REQ_CONTENT_TYPE", "SC_REQ_CONTENT_LENGTH", "SC_REQ_COOKIE", "SC_REQ_COOKIE2", "SC_REQ_HOST", "SC_REQ_PRAGMA", "SC_REQ_REFERER", "SC_REQ_USER_AGENT"]
ATTRIBUTES = ["context", "servlet_path", "remote_user", "auth_type", "query_string", "route", "ssl_cert", "ssl_cipher", "ssl_session", "req_attribute", "ssl_key_size", "secret", "stored_method"]

def prepare_ajp_forward_request(target_host, req_uri, method=None):
    """
    准备AJP Forward请求。

    参数:
        target_host: 目标主机
        req_uri: 请求URI
        method: 请求方法，默认为GET
    返回:
        AjpForwardRequest: 准备好的请求对象
    """
    # 绝对导入 AjpForwardRequest 模块
    from model.AjpForwardRequest import GET, AjpForwardRequest

    if method is None:
        method = GET

    # 创建一个AJP Forward请求对象，用于从服务器到容器的通信
    # fr = AjpForwardRequest(AjpForwardRequest.SERVER_TO_CONTAINER)
    # 创建一个AJP Forward请求对象，用于从服务器到容器的通信
    fr = AjpForwardRequest(SERVER_TO_CONTAINER)
    # 设置请求的方法，如GET、POST等
    fr.method = method

    # 设置请求使用的协议版本
    fr.protocol = "HTTP/1.1"

    # 设置请求的统一资源标识符
    fr.req_uri = req_uri

    # 设置目标主机的地址，即请求发送到的地址
    fr.remote_addr = target_host

    # 设置目标主机的主机名，这里选择不设置
    fr.remote_host = None

    # 设置服务器的名称，即请求的目标服务器
    fr.server_name = target_host

    # 设置服务器的端口号，默认为80
    fr.server_port = 80

    # 初始化请求头字典，用于设置HTTP请求的各种头部信息
    fr.request_headers = {
        'SC_REQ_ACCEPT': 'text/html',
        'SC_REQ_CONNECTION': 'keep-alive',
        'SC_REQ_CONTENT_LENGTH': '0',
        'SC_REQ_HOST': target_host,
        'SC_REQ_USER_AGENT': 'Mozilla',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.5',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

    # 设置请求是否通过SSL进行传输
    fr.is_ssl = False

    # 初始化请求的属性列表，用于携带额外的请求信息
    fr.attributes = []

    # 返回配置好的AJP Forward请求对象
    return fr
