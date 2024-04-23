import json
import os


def read_config_json_file(url="data/config.json"):
    # 打开JSON文件
    with open(url, 'r') as f:
        # 从文件中加载JSON数据
        data = json.load(f)
    return data


def verify_if_the_json_hierarchy_exists():
    """
    验证json文件的层级是否存在
    :return
        目录存在：json指定层级下的value
        目录不存在：None
    """
    config_content = read_config_json_file()
    local_configuration_file_path = config_content["localJsonConfigurationFileURL"]
    if os.path.exists(local_configuration_file_path):
        # 将变量名解析为字典键
        key_list = config_content["localJsonConfigurationItem"].split('.')
        current_data = read_config_json_file(local_configuration_file_path)
        for key in key_list:
            current_data = current_data.get(key)
        return current_data
    return None


if __name__ == '__main__':
    # print(read_config_json_file("../data/config.json")["testConnectionTimeUrl1"])
    print(verify_if_the_json_hierarchy_exists())
