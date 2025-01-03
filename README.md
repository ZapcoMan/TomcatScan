# TomcatWeakPasswordDetectionTool
* Tomcat 弱密码检测工具

## 简介
`Tomcat弱密码检测工具` 是一个用于检测Tomcat管理界面是否存在弱密码问题的Python脚本。通过命令行参数接收输入，尝试不同的用户名和密码组合来检测弱密码。

## 安装依赖
确保你已经安装了Python环境，并且安装了所需的依赖库。你可以使用以下命令安装依赖：
~~~bash
 pip install -r requirements.txt
~~~
## 使用方法
### 命令行参数
该工具通过命令行参数接收输入，以下是可用的参数：

| 参数名 | 类型 | 是否必填 | 描述 |
| ------ | ---- | -------- | ---- |
| `-url` | `str` | 是 | Tomcat管理界面的URL |
| `-username_file` | `str` | 否 | 用户名字典文件的路径，默认使用内置用户名列表 |
| `-password_file` | `str` | 否 | 密码字典文件的路径，默认使用内置密码列表 |

### 示例
1. **使用默认用户名和密码列表检测**
~~~bash
python tool.py -url http://example.com:8080/manager/html
~~~
2. **使用自定义用户名和密码字典文件检测**
~~~bash 
python tool.py -url http://example.com:8080/manager/html -username_file usernames.txt -password_file passwords.txt
~~~
## 内置的用户名和密码列表
如果未提供用户名字典文件或密码字典文件，工具将使用内置的默认用户名和密码列表：

- **默认用户名列表**：`["user", "test", "admin", "tom", "keep"]`
- **默认密码列表**：`["admin", "password", "123456"]`

## 输出结果
工具会遍历所有用户名和密码的组合，尝试登录Tomcat管理界面。如果检测到弱密码，将输出相关信息：
~~~plaintext
 Trying username: admin, password: admin 检测到弱密码。用户名: admin, 密码: admin
~~~
## 注意事项
- 确保提供的URL是正确的Tomcat管理界面地址。
- 自定义的用户名和密码字典文件应为纯文本文件，每行一个用户名或密码。
- 使用此工具时，请遵守相关法律法规，仅在授权的情况下进行测试。

## 联系方式
如需帮助或有任何问题，请联系作者：codervibe
