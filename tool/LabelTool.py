import os
from datetime import datetime

from PyQt5.QtGui import QIcon

from tool.IPTool import get_IPv4_path
from tool.FileTool import read_config_json_file, verify_if_the_json_hierarchy_exists
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
    json_directory_address = verify_if_the_json_hierarchy_exists()
    if json_directory_address:
        test_url = json_directory_address
    else:
        config_content = read_config_json_file()
        test_url = config_content["testConnectionTimeUrl"]

    get_connection_time_tip = (f"连接速度<b>不是延迟速度</b><br/>"
                               f"连接指的是你访问网址从加载到使用的时间<br/>"
                               f"如需修改当前检验的URL，请修改data目录下的config.json<br/>"
                               f"testConnectionTimeUrl的值")
    return test_url, get_connection_time_tip


def set_agent_status_label():
    """
    设置代理状态文字颜色
    """
    agent_status = get_agent_status()
    if agent_status:
        return "<span style='color:#51c259;'>开启</span>"
    else:
        return "<span style='color:#fc1e1e;'>关闭</span>"


def fraud_score_font_color(score):
    """
    设置欺诈分数的颜色
    """
    font_color = "#009A60"
    if int(score) <= 20:
        font_color = "#4AA84E"
    elif int(score) <= 30:
        font_color = "#92B73A"
    elif int(score) <= 40:
        font_color = "#C6BF22"
    elif int(score) <= 50:
        font_color = "#EDBD02"
    elif int(score) <= 60:
        font_color = "#FFAD00"
    elif int(score) <= 70:
        font_color = "#FF8C00"
    elif int(score) <= 80:
        font_color = "#FC6114"
    elif int(score) <= 90:
        font_color = "#F43021"
    elif int(score) <= 100:
        font_color = "#ED0022"
    return font_color


def delayed_font_color(latency_avg):
    """
    绘制延时的字体颜色
    """
    if 0 < latency_avg < 500:
        font_color = "#009A60"
    elif 0 < latency_avg < 900:
        font_color = "#FF8C00"
    else:
        font_color = "#ED0022"
    return font_color
