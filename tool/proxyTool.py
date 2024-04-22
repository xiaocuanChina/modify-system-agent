import winreg


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


if __name__ == '__main__':
    server, port = get_local_proxy_windows()
    item_copy_str = f"https://{server}:{port}"
    print(item_copy_str)
