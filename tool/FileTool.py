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
