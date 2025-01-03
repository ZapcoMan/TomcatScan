# -*- coding: utf-8 -*-
# @Time    : 03 1月 2025 2:10 下午
# @Author  : codervibe
# @File    : tool.py
# @Project : TomcatWeakPasswordDetectionTool
from tomcatWeakPassword import TomcatWeakPasswordDetector

# 用户名和密码列表
username_list = ["admin", "user", "test"]
password_list = ["admin", "password", "123456"]



# 指定URL
custom_url = "http://localhost:8080/manager/html"
detector = TomcatWeakPasswordDetector(base_url=custom_url)

for username in username_list:
    for password in password_list:
        # print(f"Trying username: {username}, password: {password}")
        is_weak = detector.check_weak_password(username, password)
        if is_weak:
            print(f"\033[34m检测到弱密码。用户名: {username}, 密码: {password}\033[34m")
