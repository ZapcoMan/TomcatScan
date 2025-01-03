# -*- coding: utf-8 -*-
# @Time    : 03 1月 2025 2:10 下午
# @Author  : codervibe
# @File    : tool.py
# @Project : TomcatWeakPasswordDetectionTool
import argparse
import os

from tomcatWeakPassword import TomcatWeakPasswordDetector

# 内置的用户名和密码列表
default_username_list = ["user", "test", "admin", "tom", "keep"]
default_password_list = ["admin", "password", "123456"]

# 创建ArgumentParser对象
parser = argparse.ArgumentParser(description="Tomcat弱密码检测工具")
parser.add_argument("-url", type=str, required=True, help="Tomcat管理界面的URL")
parser.add_argument("-username_file", type=str, help="用户名字典文件的路径")
parser.add_argument("-password_file", type=str, help="密码字典文件的路径")

# 解析命令行参数
args = parser.parse_args()
custom_url = args.url
username_file = args.username_file
password_file = args.password_file

# 读取用户名字典文件或使用内置的用户名列表
if username_file and os.path.isfile(username_file):
    with open(username_file, 'r', encoding='utf-8') as file:
        username_list = [line.strip() for line in file]
else:
    username_list = default_username_list

# 读取密码字典文件或使用内置的密码列表
if password_file and os.path.isfile(password_file):
    with open(password_file, 'r', encoding='utf-8') as file:
        password_list = [line.strip() for line in file]
else:
    password_list = default_password_list

detector = TomcatWeakPasswordDetector(base_url=custom_url)

for username in username_list:
    for password in password_list:
        print(f"Trying username: {username}, password: {password}")
        is_weak = detector.check_weak_password(username, password)
        if is_weak:
            print(f"\033[34m检测到弱密码。用户名: {username}, 密码: {password}\033[0m")
        # else:
        #     print(f"密码错误或认证失败。用户名: {username}, 密码: {password}")
