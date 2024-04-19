import re
import socket

import aiohttp
import requests
import geoip2.database

from tool.FileTool import read_config_json_file
from tool.proxyTool import get_local_proxy_windows


def get_IPv4_path():
    """
        获取本机IP
        return: 本机IPv4地址
    """
    #
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def get_target_server_ip():
    """
    获取当前代理IP
    return: 127.0.*.*这样的ip地址
    """
    server, port = get_local_proxy_windows()
    # 代理服务器地址
    proxy_url = f"{server}:{port}"
    # 目标服务器地址
    target_url = 'https://httpbin.org/ip'
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    try:
        config_json = read_config_json_file()
        timeout = config_json["timeout"]
        response = requests.get(target_url, proxies=proxies, timeout=timeout)
        # 从响应中获取目标服务器的 IP 地址
        target_ip = response.json()['origin']
        return target_ip
    except Exception as e:
        # print("Error:", e)
        return None


async def fetch_data(target_url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), trust_env=True) as session:
        async with session.get(target_url) as response:
            return await response.json()


def get_proxy_location(proxy_ip, fileish="data/GeoLite2-City.mmdb"):
    """
    获取代理服务器地址

    return: 国家, 城市（如果查不到数据则返回Unknown，Unknown）
    """
    # 载入 GeoIP2 数据库
    reader = geoip2.database.Reader(fileish=fileish, locales=["zh-CN"])
    # proxy_ip = get_target_server_ip()
    try:
        if proxy_ip:
            # 查询 IP 地址的地理位置信息
            response = reader.city(proxy_ip)
            country = response.country.name
            city = response.city.name
            return country, city
        else:
            return "<font color='#FF0000'>连接", "超时</font>"
    except geoip2.errors.AddressNotFoundError:
        return "Unknown", "Unknown"
    finally:
        reader.close()


def get_connection_time(url):
    """
    获取网址的连接时间
    :param url: 网址URL
    """
    try:
        config_json = read_config_json_file()
        timeout = config_json["timeout"]
        response = requests.get(url, timeout=timeout)
        return f"{(response.elapsed.total_seconds() * 1000):.2f}"  # 将响应时间转换为毫秒
    except requests.exceptions.RequestException as e:
        return -1


def get_curr_ip_fraud_score(ip):
    """
    获得IP的欺诈分值
    """
    # ip = get_target_server_ip()
    url = f'https://scamalytics.com/ip/{ip}'

    response = requests.get(url)

    if response.status_code == 200:
        # 使用正则表达式匹配Fraud Score的分数部分
        match = re.search(r'Fraud Score:\s*(\d+)', response.text)
        if match:
            fraud_score = match.group(1)
            return fraud_score
    return -1


if __name__ == '__main__':
    # print(get_proxy_location("../data/GeoLite2-City.mmdb"))

    # target_url = 'https://chat.openai.com/c/8a31e7d8-437a-48af-a836-8eacea680fb5'
    # latency = get_connection_time(target_url)
    # if latency is not None:
    #     print(f"连接到 {target_url} 大约需要 {latency} 毫秒")
    # else:
    #     print(f"无法获取到 {target_url} 的延迟")
    print(get_curr_ip_fraud_score())
