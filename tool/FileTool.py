import json


def read_config_json_file(url="data/config.json"):
    # 打开JSON文件
    with open(url, 'r') as f:
        # 从文件中加载JSON数据
        data = json.load(f)
    return data


if __name__ == '__main__':
    print(read_config_json_file("../data/config.json")["testConnectionTimeUrl1"])
