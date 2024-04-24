import re
import socket

import aiohttp
import requests
import geoip2.database

from tool.FileTool import read_config_json_file
from tool.proxyTool import get_proxies


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
    # 目标服务器地址
    target_url = 'https://httpbin.org/ip'
    try:
        config_json = read_config_json_file()
        timeout = config_json["timeout"]
        response = requests.get(target_url, proxies=get_proxies(), timeout=timeout)
        # 从响应中获取目标服务器的 IP 地址
        target_ip = response.json()['origin']
        return target_ip
    except Exception as e:
        print("Error:", e)
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
    print(reader)
    # proxy_ip = get_target_server_ip()
    try:
        if proxy_ip:
            item = ""
            # 查询 IP 地址的地理位置信息
            response = reader.city(proxy_ip)
            country = response.country.name
            item += f'{country} '
            for subdivision in response.subdivisions:
                if subdivision.name:
                    item += f'{subdivision.name} '
            city = response.city.name
            item += f'{city} '
            return item
            # return country, city
        else:
            return "<font color='#FF0000'>连接", "超时</font>"
    except geoip2.errors.AddressNotFoundError:
        return "Unknown Unknown"
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
        response = requests.get(url, proxies=get_proxies(), timeout=timeout)
        return f"{(response.elapsed.total_seconds() * 1000):.2f}"  # 将响应时间转换为毫秒
    except requests.exceptions.RequestException as e:
        return -1


def get_curr_ip_fraud_score(ip):
    """
    获得IP的欺诈分值

    IP就要从参数中传，速度会快一点
    """
    url = f'https://scamalytics.com/ip/{ip}'

    config_json = read_config_json_file()
    timeout = config_json["timeout"]
    response = requests.get(url, proxies=get_proxies(), timeout=timeout)

    if response.status_code == 200:
        # 使用正则表达式匹配Fraud Score的分数部分
        match = re.search(r'Fraud Score:\s*(\d+)', response.text)
        if match:
            fraud_score = match.group(1)
            return fraud_score
    return -1


def get_curr_ip_fraud_score_use_api(username, key, ip):
    """
    使用官方api获取欺诈分值
    IP就要从参数中传，速度会快一点

    return:
        score：欺诈分数
        remaining：剩余额度
    """
    url = f"https://api11.scamalytics.com/{username}/?key={key}&ip={ip}"

    config_json = read_config_json_file()
    timeout = config_json["timeout"]
    # 主要是查询ip的数据，因此这里不需要启动代理
    response = requests.get(url, timeout=timeout)
    json = response.json()
    # 分数
    score = json["score"]
    credits = json["credits"]
    # 已使用
    used = credits["used"]
    # 剩余额度
    remaining = credits["remaining"]

    return score, remaining


if __name__ == '__main__':
    get_curr_ip_fraud_score_use_api("18175931941", "d549482711fe87378bfd13225da384ed15e1e2aee0a2396651b749527d65787d")
