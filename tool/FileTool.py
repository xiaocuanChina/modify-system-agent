import json
import os
from datetime import datetime
from urllib.parse import quote

import pyperclip

from tool.strTool import update_source_vmess


def read_config_json_file(url="data/config.json"):
    # 打开JSON文件
    with open(url, 'r') as f:
        # 从文件中加载JSON数据
        data = json.load(f)
    return data


def verify_if_the_json_hierarchy_exists():
    """
    验证json文件的层级是否存在
    并且获取配置文件内中最新的URL
    :return
        目录存在：json指定层级下的value
        目录不存在：None
    """
    config_content = read_config_json_file()
    local_configuration_file_path = config_content["localJsonConfigurationFileURL"]
    current_data = None
    if os.path.exists(local_configuration_file_path):
        # 将变量名解析为字典键
        key_list = config_content["localJsonConfigurationItem"].split('.')
        current_data = read_config_json_file(local_configuration_file_path)
        for key in key_list:
            current_data = current_data.get(key)
    if current_data:
        return current_data
    else:
        return config_content["testConnectionTimeUrl"]


def main_update(file_url, replace_text, replacement_content=""):
    """
    读取文件并替换服务器名称的主方法
    :param file_url: 文件路径
    :param replace_text: 需要被替换的文本（旧）
    :param replacement_content: 替换的内容（新）
    """
    node_list = []
    # 适用于直接替换地址就可以改变名称的服务器 quote：将汉字转码 unquote：将码转汉字
    directly_replace_characters = quote(replace_text)
    item_replacement_content = quote(replacement_content)
    with open(file_url, 'r', encoding='utf-8') as file:
        for line in file:
            if "vmess" in line:
                # 处理每一行的内容
                line = update_source_vmess(replace_text, line)
                if line is None:
                    continue
            elif "vless" in line or "trojan" or "ss" in line:
                line = line.replace(directly_replace_characters, item_replacement_content)
            else:
                # line = f"当前服务器无法解析{line}"
                continue
            node_list.append(line)
    # 将处理好的数据写入到新文件中
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    add_file_catalogue = "./data/nodeMsgs/"
    new_file_name = f"nodeMsg_{formatted_time}.txt"

    with open(f'{add_file_catalogue}{new_file_name}', 'w', encoding='utf-8') as new_file:
        for line in node_list:
            new_file.write(line)
    set_str = '\n'.join(node_list)
    # 将字符串复制到剪贴板
    pyperclip.copy(set_str)

    delete_excess_files(add_file_catalogue)


def delete_excess_files(directory):
    """
    移除多余的文件
    :param directory: 目录地址
    :return delete_num 删除文件的数量
    """
    # 获取目录下的所有文件
    files = [os.path.join(directory, file) for file in os.listdir(directory) if
             os.path.isfile(os.path.join(directory, file))]

    # 按照文件创建时间进行排序
    files.sort(key=os.path.getctime)
    delete_num = 0
    config_content = read_config_json_file()
    delete_file_num_positive = config_content["numberOfReservedNodeFiles"]
    delete_file_num_negative = -delete_file_num_positive
    # 如果文件数量超过 5 个，删除多余的文件
    if len(files) > delete_file_num_positive:
        files_to_delete = files[:delete_file_num_negative]  # 获取需要删除的文件列表
        for file in files_to_delete:
            delete_num += 1
            os.remove(file)
    return delete_num


# def get_new_config_url():
#     """
#     获取配置文件内中最新的URL
#     """
#     json_directory_address = verify_if_the_json_hierarchy_exists()
#     if json_directory_address:
#         config_url = json_directory_address
#     else:
#         config_content = read_config_json_file()
#         config_url = config_content["testConnectionTimeUrl"]
#     return config_url


if __name__ == '__main__':
    # print(read_config_json_file("../data/config.json")["testConnectionTimeUrl1"])
    print(verify_if_the_json_hierarchy_exists())
