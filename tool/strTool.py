import os
import re
import sys

from PyQt5.QtGui import QGuiApplication, QIcon


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
    # 获取剪贴板实例
    clipboard = QGuiApplication.clipboard()
    # 设置剪贴板内容
    clipboard.setText(s)
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


if __name__ == '__main__':
    # print(get_package_icon_path(""))
    s = "如需要设置默认代理服务器请执行以下步骤：<ul><li>找到文件根目录</li><li>进入data目录</li><li>修改config.json的default_proxy_server和default_proxy_proxy【：】后面的值</li></ul>"
    print(split_string_by_length(s, 8))
