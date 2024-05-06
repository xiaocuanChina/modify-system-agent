import os
import re
import sys
import base64
import json
from urllib.parse import quote

import pyperclip
from PyQt5.QtGui import QIcon


def get_package_icon_path(path):
    """
    打包使用的绝对路径
    """
    if getattr(sys, 'frozen', False):
        # 如果是PyInstaller打包的程序
        base_path = sys._MEIPASS
    else:
        # 如果是直接运行的脚本
        base_path = os.path.abspath(".")

    icon_path = os.path.join(base_path, path)
    return icon_path


# def copy_str(s):
#     # 获取剪贴板实例
#     clipboard = QGuiApplication.clipboard()
#     # 设置剪贴板内容
#     clipboard.setText(s)


def copy_str_and_set_btn(s, my_btn):
    """
    复制内容到粘贴板并修改按钮内容
    :param s: 需要复制的文本内容
    :param my_btn: 按钮对象
    :return: None
    """
    # 将字符串复制到剪贴板
    pyperclip.copy(s)
    # 更新复制按钮的文本和图标
    my_btn.setText("复制成功")
    my_btn.setIcon(QIcon(get_package_icon_path('data/image/成功.png')))


def split_string_by_length(text, max_length=None):
    """
    将字符按照自定长度进行分割（忽略h5标签）
    """
    if max_length:
        # 使用正则表达式捕获HTML标签
        html_tag_regex = re.compile(r'<\/?[a-z][^>]*>')
        tags = html_tag_regex.findall(text)

        # 去除HTML标签,并将文本分割成多个段落
        clean_text = html_tag_regex.sub('', text)
        chunks = [clean_text[i:i + max_length] for i in range(0, len(clean_text), max_length)]

        # 重新插入HTML标签
        result = []
        tag_index = 0
        text_index = 0
        for chunk in chunks:
            result.append(chunk)
            while tag_index < len(tags) and text.find(tags[tag_index], text_index) < text_index + len(chunk):
                tag = tags[tag_index]
                position = text.find(tag, text_index) - text_index
                result[-1] = result[-1][:position] + tag + result[-1][position:]
                tag_index += 1
                text_index += position + len(tag)
            text_index += len(chunk)
        return '\n'.join(result)
        # return '<br/>'.join(result)
    else:
        return text


def update_source_vmess(replace_text, vmess_info, replacement_content=""):
    """
    解析并替换vmess服务器地址
    :param replace_text: 需要被替换的文本（旧）
    :param vmess_info: 服务器地址
    :param replacement_content: 替换的内容（新）
    :return:
    """
    # 进行Base64解码
    decoded_info = base64.urlsafe_b64decode(vmess_info[len("vmess://"):]).decode('utf-8')
    # 解析JSON格式
    vmess_data = json.loads(decoded_info)
    # 修改服务器地址和端口
    name = vmess_data['ps']
    vmess_data['ps'] = name.replace(replace_text, replacement_content)
    # 将修改后的数据转换回JSON字符串
    modified_vmess_info = json.dumps(vmess_data, separators=(',', ':'), ensure_ascii=False)
    # 进行Base64编码
    encoded_modified_info = base64.urlsafe_b64encode(modified_vmess_info.encode('utf-8')).decode('utf-8').rstrip("=")

    return f"vmess://{encoded_modified_info}\n"


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
            elif "vless" in line or "trojan" or "ss" in line:
                line = line.replace(directly_replace_characters, item_replacement_content)
            else:
                # line = f"当前服务器无法解析{line}"
                continue
            node_list.append(line)
    # 将处理好的数据写入到新文件中
    with open('./data/new.txt', 'w', encoding='utf-8') as new_file:
        for line in node_list:
            new_file.write(line)
    set_str = '\n'.join(node_list)
    # 将字符串复制到剪贴板
    pyperclip.copy(set_str)


if __name__ == '__main__':
    # print(get_package_icon_path(""))
    s = "如需要设置默认代理服务器请执行以下步骤：<ul><li>找到文件根目录</li><li>进入data目录</li><li>修改config.json的default_proxy_server和default_proxy_proxy【：】后面的值</li></ul>"
    print(split_string_by_length(s, 8))
