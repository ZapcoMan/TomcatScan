# -*- coding: utf-8 -*-
# @Time    : 03 1月 2025 2:11 下午
# @Author  : codervibe
# @File    : tomcatWeakPassword.py
# @Project : TomcatWeakPasswordDetectionTool
import requests
from requests.auth import HTTPBasicAuth
import random

class TomcatWeakPasswordDetector:
    """
    Tomcat弱密码检测器类，用于检测Tomcat服务器是否存在弱密码安全问题。

    初始化时接收一个基础URL，用于后续的认证尝试。
    """
    def __init__(self, base_url):
        self.base_url = base_url
        # 定义一组常见的用户代理，用于模拟不同浏览器的请求
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"
        ]
        # 定义请求头，以模拟真实浏览器的请求
        self.headers = {
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '"Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

    def check_weak_password(self, username, password):
        """
        尝试使用给定的用户名和密码认证Tomcat服务器。

        参数:
        username (str): 用户名
        password (str): 密码

        返回:
        bool: 如果认证成功则返回True，否则返回False。
        """
        # 随机选择一个用户代理，以避免被服务器识别出扫描行为
        self.headers["User-Agent"] = random.choice(self.user_agents)
        # 创建HTTP基本认证对象
        auth = HTTPBasicAuth(username=username, password=password)
        try:
            # 发送认证请求
            response = requests.get(self.base_url, headers=self.headers, auth=auth)
            # 根据响应状态码判断认证是否成功
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            # 处理请求异常
            print("HTTP Request failed:", e)
            return False
