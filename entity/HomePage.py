from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QApplication

from tool.LabelTool import set_proxy_server_info_label, \
    set_refresh_btn_label, update_connection_time_tip_test_url, set_agent_status_label
from tool.IPTool import get_IPv4_path, get_proxy_location, get_connection_time, get_target_server_ip, \
    get_curr_ip_fraud_score
from tool.FileTool import read_config_json_file
from tool.strTool import *
from tool.proxyTool import *

"""
我想换UI！！！
来个人教教我把！！
我想换UI！！！
来个人教教我把！！
我想换UI！！！
来个人教教我把！！
我想换UI！！！
来个人教教我把！！
我想换UI！！！
来个人教教我把！！
"""


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        # 初始化组件
        self.default_server_btn = None
        self.start_btn = None
        self.get_fraud_score_btn = None
        self.fraud_score_label = None
        self.agent_server_ip_refresh_btn = None
        self.agent_server_ip_copy_btn = None
        self.agent_server_ip_label = None
        self.get_connection_time_btn = None
        self.get_connection_time_label = None
        self.get_server_ip_msg_btn = None
        self.server_ip_str = None
        self.server_ip_position_label = None
        self.server_ip_position_str = None
        self.edit_server_btn = None
        self.show_text_edit = None
        self.separate_text_edit = None
        self.port_text_edit = None
        self.server_text_edit = None
        self.ipv4_add_str_label = None
        self.proxy_server_info_str_label = None
        self.copy_server_btn = None
        self.refresh_btn = None
        self.copy_ip_btn = None
        self.agent_state_label = None
        self.refresh_time = None
        self.windows_top_btn = None

        # 初始化参数
        # 代理IP地址
        self.agent_server_ip = None
        self.config_content = read_config_json_file()

        self.get_connection_time_title = "连接时长为："
        self.get_connection_time_content = "None（点击按钮获取）"

        self.agent_server_ip_label_title = "服务器IP："
        self.agent_server_ip_label_content = "None（点击按钮获取）"

        self.fraud_score_label_title = "欺诈分值："
        self.fraud_score_label_content = "-1（点击按钮获取）"

        self.server_ip_position_title = "服务器地理位置："
        self.server_ip_position_content = "None None（点击按钮获取）"

        self.ipv4_add_str_title = "本机IPv4地址："
        self.ipv4_add_str_content = get_IPv4_path()

        self.proxy_server_info_str_title1 = "代理服务器信息："
        self.proxy_server_info_str_title2 = "请设置代理服务器信息: "
        local_server, local_port = get_local_proxy_windows()
        self.proxy_server_info_str_content = f"{local_server}:{local_port}"

        self.agent_state_label_title = "当前代理状态："
        self.agent_state_label_content = set_agent_status_label()

        # 文本宽度（一行数量）
        self.TEXT_WIDTH = 17

        self.initUI()

    # noinspection PyUnresolvedReferences
    def initUI(self):

        # 构建网络代理.png的绝对路径
        window_icon_path = get_package_icon_path("data/image/网络代理.png")
        self.setWindowIcon(QIcon(window_icon_path))

        test_url, get_connection_time_tip = update_connection_time_tip_test_url()
        self.get_connection_time_label = QLabel(self.get_connection_time_title + self.get_connection_time_content)
        self.get_connection_time_btn = QPushButton("测试连接速度")
        self.get_connection_time_btn.setToolTip(get_connection_time_tip)
        self.get_connection_time_btn.setIcon(QIcon(get_package_icon_path("data/image/连接时长.png")))
        self.get_connection_time_btn.clicked.connect(self.get_connection_time_fn)

        self.agent_server_ip_label = QLabel(f"{self.agent_server_ip_label_title}{self.agent_server_ip_label_content}",
                                            self)
        self.agent_server_ip_copy_btn = QPushButton('复制IP地址', self)
        self.agent_server_ip_copy_btn.setIcon(QIcon(get_package_icon_path("data/image/复制.png")))
        self.agent_server_ip_copy_btn.clicked.connect(self.agent_server_ip_copy_fn)
        self.agent_server_ip_refresh_btn = QPushButton('刷新IP地址', self)
        # self.agent_server_ip_refresh_btn.setIcon(QIcon(get_package_icon_path("data/image/ipAddress.png")))
        self.agent_server_ip_refresh_btn.setIcon(QIcon(get_package_icon_path("data/image/IP地址.png")))
        self.agent_server_ip_refresh_btn.clicked.connect(self.agent_server_ip_refresh_fn)

        self.fraud_score_label = QLabel(f"{self.fraud_score_label_title}{self.fraud_score_label_content}")
        self.get_fraud_score_btn = QPushButton('获取欺诈分值', self)
        fraud_score_tip = "什么是欺诈分值？<br/>欺诈分值通常是一个0到100的范围内的分数，分数越高表示越高的欺诈风险。"
        self.get_fraud_score_btn.setToolTip(split_string_by_length(fraud_score_tip, self.TEXT_WIDTH))
        self.get_fraud_score_btn.setIcon(QIcon(get_package_icon_path("data/image/得分.png")))
        self.get_fraud_score_btn.clicked.connect(self.get_fraud_score_fn)

        self.server_ip_position_label = QLabel(self.server_ip_position_title + self.server_ip_position_content, self)
        # self.server_ip_label = QLabel(f"服务器IP: {get_target_server_ip()}", self)
        # self.server_ip_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.get_server_ip_msg_btn = QPushButton('获取服务器信息', self)
        self.get_server_ip_msg_btn.setIcon(QIcon(get_package_icon_path("data/image/服务器地址.png")))
        tip_str2 = "点击后会隐藏按钮，防止多次点击导致程序卡死，而且一开始就加载的地址的话，如果你的节点延时过高的话，启动就会很慢，而且你选的服务器和具体的位置大差不差"
        self.get_server_ip_msg_btn.setToolTip(split_string_by_length(tip_str2, self.TEXT_WIDTH))
        self.get_server_ip_msg_btn.clicked.connect(self.get_server_ip_msg_fn)

        # self.ipv4_add_str_content = get_IPv4_path()
        self.ipv4_add_str_label = QLabel(self.ipv4_add_str_title + self.ipv4_add_str_content, self)

        # 代理服务器信息
        # 如何配置代理服务器喝配置代理服务器的分别显示见【刷新按钮】附近的if判断
        # ------- 代理服务器信息 -------
        local_server, local_port = get_local_proxy_windows()
        self.proxy_server_info_str_label = QLabel(
            self.proxy_server_info_str_title1 + self.proxy_server_info_str_content,
            self)
        self.copy_server_btn = QPushButton('复制本地地址', self)
        tip_str = "复制的代理服务器地址仅在本机使用，如果需要获取局域网内可使用的服务器ip以及端口请查看自己代理软件的配置对应端口"
        self.copy_server_btn.setToolTip(split_string_by_length(tip_str, self.TEXT_WIDTH))
        self.copy_server_btn.setIcon(QIcon(get_package_icon_path('data/image/复制.png')))  # 替换为你的图标文件路径
        self.copy_server_btn.clicked.connect(self.copy_proxy_server_address)
        self.edit_server_btn = QPushButton('调整代理服务器', self)
        self.edit_server_btn.setIcon(QIcon(get_package_icon_path('data/image/编辑.png')))  # 替换为你的图标文件路径
        self.edit_server_btn.clicked.connect(self.edit_server_info)
        self.default_server_btn = QPushButton("恢复为默认服务器")
        self.default_server_btn.setIcon(QIcon(get_package_icon_path('data/image/恢复默认服务器.png')))  # 替换为你的图标文件路径

        # ------- 配置代理服务器 -------
        # tip_str = "输入完代理服务器地址之后<span style='color:red;'>点击刷新</span>即可自动为您配置代理服务器地址"
        self.server_text_edit = QLineEdit(self)
        self.server_text_edit.setPlaceholderText("请输入服务器")  # 设置背景文字
        self.separate_text_edit = QLabel(f":", self)
        self.port_text_edit = QLineEdit(self)
        self.port_text_edit.setPlaceholderText("请输入端口号")  # 设置背景文字

        # self.copy_server_btn = QPushButton('复制局域网', self)
        # self.copy_server_btn.setToolTip('复制（局域网）代理服务器地址到剪贴板')
        # self.copy_server_btn.setIcon(QIcon(get_package_icon_path('data/image/复制.png')))  # 替换为你的图标文件路径
        # item_copy_str = f"{server}:{port}"
        # self.copy_server_btn.clicked.connect(lambda: self.copy_str(item_copy_str, self.copy_server_btn))

        # IPv4地址信息
        self.copy_ip_btn = QPushButton('一键复制', self)
        self.copy_ip_btn.setToolTip('仅复制IPv4地址')
        self.copy_ip_btn.setIcon(QIcon(get_package_icon_path('data/image/复制.png')))
        self.copy_ip_btn.clicked.connect(self.copy_ipv4_address)

        # 代理状态
        self.agent_state_label = QLabel(self.agent_state_label_title + self.agent_state_label_content, self)
        self.refresh_time = QLabel('', self)
        self.refresh_time.hide()

        self.start_btn = QPushButton('开启代理', self)
        if not get_agent_status():
            self.start_btn.hide()
        self.start_btn.setIcon(QIcon(get_package_icon_path('data/image/开启.png')))  # 替换为你的图标文件路径
        self.start_btn.clicked.connect(self.enable_proxy)

        self.stop_btn = QPushButton('关闭代理', self)
        if get_agent_status():
            self.stop_btn.hide()
        self.stop_btn.setIcon(QIcon(get_package_icon_path('data/image/关闭.png')))
        self.stop_btn.clicked.connect(self.close_agent)

        # 功能按钮
        exit_btn = QPushButton('退出', self)
        exit_btn.setIcon(QIcon(get_package_icon_path('data/image/退出.png')))
        exit_btn.clicked.connect(lambda: QApplication.quit())

        self.refresh_btn = QPushButton('刷新', self)
        self.refresh_btn.setIcon(QIcon(get_package_icon_path('data/image/刷新时间.png')))
        self.refresh_btn.clicked.connect(self.refresh)

        self.windows_top_btn = QPushButton('点我置顶', self)
        self.windows_top_btn.setIcon(QIcon(get_package_icon_path('data/image/置顶-false.png')))
        self.windows_top_btn.clicked.connect(self.set_windows_top)

        if local_server and local_port:
            self.show_text_edit = False
            self.server_text_edit.hide()
            self.port_text_edit.hide()
            self.separate_text_edit.hide()
        else:
            self.show_text_edit = True
            self.refresh_btn.setText("点我保存")
            self.refresh_btn.setIcon(QIcon(get_package_icon_path('data/image/保存.png')))
            self.proxy_server_info_str_label.setText(self.proxy_server_info_str_title2)
            self.copy_server_btn.hide()
            self.edit_server_btn.hide()

        # 创建垂直布局，并将文本标签和按钮添加到布局中
        y_box = QVBoxLayout()

        # ipv4布局
        ipv4_add_x_box = QHBoxLayout()
        ipv4_add_x_box.addWidget(self.ipv4_add_str_label)
        ipv4_add_x_box.addWidget(self.copy_ip_btn)
        y_box.addLayout(ipv4_add_x_box)

        # 代理服务器信息布局
        proxy_server_x_box = QHBoxLayout()  # 创建水平布局
        proxy_server_x_box.addWidget(self.proxy_server_info_str_label)
        proxy_server_x_box.addWidget(self.copy_server_btn)
        proxy_server_x_box.addWidget(self.edit_server_btn)

        proxy_server_x_box.addWidget(self.server_text_edit)
        proxy_server_x_box.addWidget(self.separate_text_edit)
        proxy_server_x_box.addWidget(self.port_text_edit)

        y_box.addLayout(proxy_server_x_box)

        # 代理状态布局
        agent_state_x_box = QHBoxLayout()  # 创建水平布局
        agent_state_x_box.addWidget(self.agent_state_label)
        agent_state_x_box.addWidget(self.start_btn)
        agent_state_x_box.addWidget(self.stop_btn)
        agent_state_x_box.addWidget(self.default_server_btn)
        y_box.addLayout(agent_state_x_box)

        # 功能按钮布局
        function_but_x_box = QHBoxLayout()  # 创建水平布局
        function_but_x_box.addWidget(self.windows_top_btn)
        function_but_x_box.addWidget(self.refresh_btn)
        function_but_x_box.addWidget(exit_btn)
        y_box.addLayout(function_but_x_box)

        # 显示IP布局
        server_ip_x_box = QHBoxLayout()
        server_ip_x_box.addWidget(self.agent_server_ip_label)
        server_ip_x_box.addWidget(self.agent_server_ip_copy_btn)
        server_ip_x_box.addWidget(self.agent_server_ip_refresh_btn)
        y_box.addLayout(server_ip_x_box)

        # 欺诈分值布局
        fraud_score_x_box = QHBoxLayout()
        fraud_score_x_box.addWidget(self.fraud_score_label)
        fraud_score_x_box.addWidget(self.get_fraud_score_btn)
        y_box.addLayout(fraud_score_x_box)

        # 显示地址布局
        server_ip_position_x_box = QHBoxLayout()
        server_ip_position_x_box.addWidget(self.server_ip_position_label)
        server_ip_position_x_box.addWidget(self.get_server_ip_msg_btn)
        y_box.addLayout(server_ip_position_x_box)

        # 获取连接时长的布局
        connection_time_x_box = QHBoxLayout()
        connection_time_x_box.addWidget(self.get_connection_time_label)
        connection_time_x_box.addWidget(self.get_connection_time_btn)
        y_box.addLayout(connection_time_x_box)

        # y_box.addWidget(self.get_server_ip_msg_btn)

        # 设置窗口布局
        self.setLayout(y_box)

    def enable_proxy(self):
        """
        开启代理
        """
        self.stop_btn.show()
        self.start_btn.hide()
        set_agent_status(True)
        self.refresh()

    def close_agent(self):
        """
        关闭代理
        """
        self.stop_btn.hide()
        self.start_btn.show()
        set_agent_status(False)
        self.refresh()

    def refresh(self):
        """
        刷新的方法
        """
        # 刷新IPv4的地址
        self.ipv4_add_str_content = get_IPv4_path()
        self.ipv4_add_str_label.setText(self.ipv4_add_str_title + self.ipv4_add_str_content)

        # 如果设置代理服务器的文本框内容不为空
        validate_server = self.server_text_edit.text()
        validate_port = self.port_text_edit.text()
        if validate_server and validate_port:
            set_local_proxy_windows(validate_server, validate_port)
            self.server_text_edit.hide()
            self.port_text_edit.hide()
            self.separate_text_edit.hide()

            self.copy_server_btn.show()
            self.edit_server_btn.show()

        # 刷新服务器地址
        set_proxy_server_info_label(self.proxy_server_info_str_label)
        local_server, local_port = get_local_proxy_windows()
        self.proxy_server_info_str_content = f"{local_server}:{local_port}"
        self.proxy_server_info_str_label.setText(
            self.proxy_server_info_str_title1 + self.proxy_server_info_str_content)

        # 刷新代理状态
        self.agent_state_label_content = set_agent_status_label()
        self.agent_state_label.setText(self.agent_state_label_title + self.agent_state_label_content)

        # 设置按钮刷新时间
        set_refresh_btn_label(self.refresh_btn)

    def set_windows_top(self):
        """
        设置窗口置顶
        :return:
        """
        # 获取窗口标志
        flags = self.windowFlags()

        # 检查窗口是否置顶
        if flags & QtCore.Qt.WindowStaysOnTopHint:
            self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, False)
            self.windows_top_btn.setIcon(QIcon(get_package_icon_path('data/image/置顶-false.png')))
        else:
            self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.windows_top_btn.setIcon(QIcon(get_package_icon_path('data/image/置顶-true.png')))
        self.show()

    def copy_proxy_server_address(self):
        """
        需要复制的代理服务器地址
        """
        copy_server, copy_port = get_local_proxy_windows()
        proxy_server_address = f"https://{copy_server}:{copy_port}"
        copy_str_and_set_btn(proxy_server_address, self.copy_server_btn)

    def copy_ipv4_address(self):
        """
        复制ipv4地址的方法
        """
        copy_str_and_set_btn(self.ipv4_add_str_content, self.copy_ip_btn)

    def get_server_ip_msg_fn(self):
        """
        获取服务器地理位置的方法
        """
        self.get_server_ip_msg_btn.hide()
        QApplication.processEvents()
        # print("--")
        if self.agent_server_ip:
            self.server_ip_position_content = get_proxy_location(self.agent_server_ip)
            # self.server_ip_position_content = f"{country} {city}"
            self.server_ip_position_label.setText(self.server_ip_position_title + self.server_ip_position_content)
            self.get_server_ip_msg_btn.show()
        else:
            self.agent_server_ip_refresh_fn()
            if self.agent_server_ip:
                self.get_server_ip_msg_fn()

        self.get_server_ip_msg_btn.show()

    def edit_server_info(self):
        """
        修改代理服务器配置
        """
        # 核心代码 设置不同组件的显隐藏
        self.copy_server_btn.hide()
        self.edit_server_btn.hide()
        self.server_text_edit.show()
        self.separate_text_edit.show()
        self.port_text_edit.show()

        # 获取默认的代理服务器信息
        default_server, default_port = get_local_proxy_windows()
        self.server_text_edit.setText(default_server)
        self.port_text_edit.setText(default_port)

        # 设置在“修改服务器状态”下的显示的内容
        self.proxy_server_info_str_label.setText("请设置代理服务器信息: ")
        self.refresh_btn.setText("点我保存")
        self.refresh_btn.setIcon(QIcon(get_package_icon_path('data/image/保存.png')))
        # self.proxy_server_info_str_label.setText("请设置代理服务器信息: ")

    def get_connection_time_fn(self):
        """
        获取连接速度
        """
        self.get_connection_time_btn.hide()
        QApplication.processEvents()
        test_url, get_connection_time_tip = update_connection_time_tip_test_url()
        latency = get_connection_time(test_url)
        # font_color = "#22B14C"
        if float(latency) >= 1900:
            font_color = "#ED1C24"
        elif float(latency) == -1:
            font_color = "#FF0000"
        else:
            font_color = "#22B14C"
        self.get_connection_time_content = f"<font color='{font_color}'>{latency}ms</font>"
        self.get_connection_time_label.setText(self.get_connection_time_title + self.get_connection_time_content)
        self.get_connection_time_btn.setToolTip(get_connection_time_tip)
        self.get_connection_time_btn.show()

    def agent_server_ip_copy_fn(self):
        """
        复制IP地址
        """
        if self.agent_server_ip:
            copy_str_and_set_btn(self.agent_server_ip, self.agent_server_ip_copy_btn)
        else:
            self.agent_server_ip_refresh_fn()
            if self.agent_server_ip:
                self.agent_server_ip_copy_fn()

    def agent_server_ip_refresh_fn(self):
        """
        刷新IP地址
        """
        self.agent_server_ip_refresh_btn.hide()
        self.agent_server_ip_copy_btn.hide()
        QApplication.processEvents()
        self.agent_server_ip = get_target_server_ip()
        self.agent_server_ip_label_content = self.agent_server_ip

        self.agent_server_ip_label.setText(f"{self.agent_server_ip_label_title}{self.agent_server_ip_label_content}")

        self.agent_server_ip_refresh_btn.show()
        self.agent_server_ip_copy_btn.show()

        # return self.agent_server_ip

    def get_fraud_score_fn(self):
        """
        获取欺诈分值
        """
        self.get_fraud_score_btn.hide()
        QApplication.processEvents()
        if self.agent_server_ip:
            self.fraud_score_label_content = get_curr_ip_fraud_score(self.agent_server_ip)
            font_color = "#009A60"
            if int(self.fraud_score_label_content) <= 20:
                font_color = "#4AA84E"
            elif int(self.fraud_score_label_content) <= 30:
                font_color = "#92B73A"
            elif int(self.fraud_score_label_content) <= 40:
                font_color = "#C6BF22"
            elif int(self.fraud_score_label_content) <= 50:
                font_color = "#EDBD02"
            elif int(self.fraud_score_label_content) <= 60:
                font_color = "#FFAD00"
            elif int(self.fraud_score_label_content) <= 70:
                font_color = "#FF8C00"
            elif int(self.fraud_score_label_content) <= 80:
                font_color = "#FC6114"
            elif int(self.fraud_score_label_content) <= 90:
                font_color = "#F43021"
            elif int(self.fraud_score_label_content) <= 100:
                font_color = "#ED0022"

            self.fraud_score_label.setText(
                f"{self.fraud_score_label_title}"
                f"<font color ='{font_color}'>{self.fraud_score_label_content}</font>")
        else:
            self.agent_server_ip_refresh_fn()
            if self.agent_server_ip:
                self.get_fraud_score_fn()
        self.get_fraud_score_btn.show()
