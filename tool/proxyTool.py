import winreg
import time

import requests

from tool.FileTool import read_config_json_file, verify_if_the_json_hierarchy_exists


def get_agent_status():
    """
    获得代理状态
    """
    # 获取注册表中的key
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
    proxy_enable, _ = winreg.QueryValueEx(key, 'ProxyEnable')
    winreg.CloseKey(key)
    return proxy_enable


def set_agent_status(agent_status):
    """
    设置代理状态
    :param agent_status: 代理状态
        - True: 开启代理
        - False: 关闭代理
    :return: None
    """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
    # 设置状态
    # 打开代理设置的注册表键
    setting_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0,
                                 winreg.KEY_SET_VALUE)
    # 将 ProxyEnable 设置为 1，启用代理
    winreg.SetValueEx(setting_key, 'ProxyEnable', 0, winreg.REG_DWORD, int(agent_status))

    winreg.CloseKey(key)

    return get_agent_status()


def get_proxies():
    """
    用于网络请求时的代理服务器
    """
    server, port = get_local_proxy_windows()
    # 代理服务器地址
    proxy_url = f"{server}:{port}"
    return {
        'http': proxy_url,
        'https': proxy_url
    }


def get_local_proxy_windows():
    """
    获取本地使用的代理服务器 IP 和端口 (Windows)

    Returns:
        正常状态：代理服务器 IP 和端口，例如 ("127.0.0.1", 8080)
        异常状态：返回参数均为None
    """
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    key_name = "ProxyServer"
    # key_name = "ProxyServerTest"

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
    try:
        proxy_server, proxy_enable = winreg.QueryValueEx(key, key_name)
        if proxy_enable == 1:
            server_and_port_info = proxy_server.split(":")
            if len(server_and_port_info) == 2:
                server = server_and_port_info[0]
                port = server_and_port_info[1]
                return server, port
            return None, None
    except FileNotFoundError:
        try:
            # 打开注册表项
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
                # 设置字符串值
                winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, "")
            return None, None

        except Exception as e:
            print("出现错误:", e)
    finally:
        winreg.CloseKey(key)


def set_local_proxy_windows(server, proxy):
    """
    设置本机系统代理服务器
    @param server: 代理服务器 IP
    @param proxy: 代理服务器端口
    """
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    key_name = "ProxyServer"
    # key_name = "ProxyServerTest"
    new_value = f"{server}:{proxy}"

    try:
        # 打开注册表项
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
            # 修改指定键的值
            winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, new_value)
    except Exception as e:
        print("出现错误:", e)
        return False
    return True


def test_proxy_latency():
    """
    测试代理服务器与指定地址的延时
    """
    file = read_config_json_file()
    item_url = verify_if_the_json_hierarchy_exists()
    test_url = file["testConnectionTimeUrl"]
    if item_url:
        test_url = item_url
    number_of_test_delays = file["number_of_test_delays"]

    latency_sum = 0

    for i in range(number_of_test_delays):
        try:
            start_time = time.time()
            # start_time = datetime.timestamp(datetime.now())
            # print(f"start_time:{start_time}")
            requests.get(test_url, proxies=get_proxies(), timeout=2.5)
            end_time = time.time()
            latency_sum = latency_sum + (end_time - start_time)
            # # end_time = datetime.timestamp(datetime.now())
            # print(f"end_time:{end_time}")
        except Exception as e:
            print(f"代理服务器 测试失败: {str(e)}")
            return -1
    return int(latency_sum / number_of_test_delays * 1000)


if __name__ == '__main__':
    print(get_agent_status())
