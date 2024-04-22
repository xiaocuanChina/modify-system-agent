import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QAction, QStackedWidget, QMainWindow, QApplication

from HomePage import HomePage
from Setting import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 获取主屏幕对象
        screen = QGuiApplication.primaryScreen()
        # 从主屏幕对象获取屏幕几何信息(包括屏幕分辨率)
        screen_geometry = screen.geometry()
        # 从屏幕几何信息中获取屏幕宽度
        screen_width = screen_geometry.width()
        # 从屏幕几何信息中获取屏幕高度
        screen_height = screen_geometry.height()

        # 窗口宽度
        self.WIDGET_WIDTH = 434
        # 窗口高度
        self.WIDGET_HEIGHT = 257
        # 窗口默认x轴
        self.WINDOW_X = (screen_width - self.WIDGET_WIDTH) // 2
        # 窗口默认y轴
        self.WINDOW_Y = (screen_height - self.WIDGET_HEIGHT) // 2
        # 设置标题
        self.TITLE = '系统代理信息'

        # 设置窗口的基本属性
        self.setGeometry(self.WINDOW_X, self.WINDOW_Y, self.WIDGET_WIDTH, self.WIDGET_HEIGHT)
        self.setWindowTitle(self.TITLE)

        self.initUI()

    def initUI(self):
        # 禁用最小化、最大化和关闭按钮
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        # 创建菜单栏
        menubar = self.menuBar()

        # 添加首页和设置菜单
        home_menu = QAction("主页", self)
        home_menu.triggered.connect(self.show_home_page)
        menubar.addAction(home_menu)

        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings_page)
        menubar.addAction(settings_action)

        # 创建页面管理器
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 添加首页和设置页面
        self.home_page = HomePage()
        self.stacked_widget.addWidget(self.home_page)

        self.settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.settings_page)

    def show_settings_page(self):
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
