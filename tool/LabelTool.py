import os
from datetime import datetime

from PyQt5.QtGui import QIcon

from tool.IPTool import get_IPv4_path
from tool.FileTool import read_config_json_file
from tool.proxyTool import get_local_proxy_windows, get_agent_status
from tool.strTool import get_package_icon_path, split_string_by_length


def set_proxy_server_info_label(label):
    """
    修改代理服务器label内容
    """
    server, port = get_local_proxy_windows()
    label.setText(f"代理服务器信息: {server}:{port}")
    # return server, port


def set_simple_label(title_and_content, label):
    """
    修改显示IPv4地址label内容
    :param title_and_content: 标题以及内容
    :param label: 按钮对象
    """
    label.setText(f"{title_and_content}")


def set_ipv4_add_str_label(label):
    """
    修改显示IPv4地址label内容
    """
    ipv4_add = get_IPv4_path()
    label.setText(f"本机IPv4地址: {ipv4_add}")


def set_agent_state_label(label):
    """
    修改代理状态的label内容
    """
    state = get_agent_status()
    label.setText(f'当前代理状态：{state}')


def set_refresh_btn_label(label):
    """
    修改刷新时间的label内容
    """
    curr_time = datetime.now()
    refresh_time = curr_time.strftime("%H:%M:%S")
    show_time_str = f' {refresh_time}.{curr_time.microsecond // 1000}'
    label.setText(show_time_str)
    label.setIcon(QIcon(get_package_icon_path('data/image/刷新时间.png')))
    label.setToolTip(split_string_by_length("上次刷新的时间"))


def update_connection_time_tip_test_url():
    """
    修改【测试连接时长】tip文字
    """
    config_content = read_config_json_file()
    local_configuration_file_path = config_content["localJsonConfigurationFileURL"]
    test_url = config_content["testConnectionTimeUrl"]
    if os.path.exists(local_configuration_file_path):
        # 将变量名解析为字典键
        key_list = config_content["localJsonConfigurationItem"].split('.')
        current_data = read_config_json_file(local_configuration_file_path)
        for key in key_list:
            current_data = current_data.get(key)
        test_url = current_data

    get_connection_time_tip = (f"当前检验的URL为：<br/>"
                               f"{test_url}<br/>"
                               f"如需修改，请修改data目录下的config.json<br/>"
                               f"testConnectionTimeUrl的值<br/>"
                               f"连接速度不是延迟速度，连接指的是你访问网址从加载到使用的时间")
    return test_url, get_connection_time_tip


def set_agent_status_label():
    agent_status = get_agent_status()
    if agent_status:
        return "<span style='color:#51c259;'>开启</span>"
    else:
        return "<span style='color:#fc1e1e;'>关闭</span>"
