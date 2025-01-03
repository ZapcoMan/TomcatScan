# -*- coding: utf-8 -*-
# @Time    : 03 1月 2025 2:11 下午
# @Author  : codervibe
# @File    : tomcatWeakPassword.py
# @Project : TomcatWeakPasswordDetectionTool

import requests
from requests.auth import HTTPBasicAuth


def tomcatWeakPassword(username, password):
    url = "http://localhost:8080/manager/html"
    headers = {
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
    auth = HTTPBasicAuth(username=username, password=username)

    try:
        response = requests.get(url, headers=headers, auth=auth)
        # response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        print("Response Status Code:", response.status_code)
        # print("Response Content:", response.text)
    except requests.exceptions.RequestException as e:
        print("HTTP Request failed:", e)



