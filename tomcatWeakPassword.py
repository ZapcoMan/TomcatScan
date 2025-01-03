# -*- coding: utf-8 -*-
# @Time    : 03 1月 2025 2:11 下午
# @Author  : codervibe
# @File    : tomcatWeakPassword.py
# @Project : TomcatWeakPasswordDetectionTool

import requests
from requests.auth import HTTPBasicAuth


class TomcatWeakPasswordDetector:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '"Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

    def check_weak_password(self, username, password):
        auth = HTTPBasicAuth(username=username, password=password)
        try:
            response = requests.get(self.base_url, headers=self.headers, auth=auth)
            # print("Response Status Code:", response.status_code)
            # print("Response Content:", response.text)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print("HTTP Request failed:", e)
            return False
