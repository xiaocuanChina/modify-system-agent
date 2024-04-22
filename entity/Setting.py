from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.timeout_edit = None
        self.timeout_label = None

        self.initUI()

    def initUI(self):
        self.timeout_label = QLabel(f"超时时间：", self)
        self.timeout_edit = QLineEdit(self)
        self.timeout_edit.setFixedWidth(80)

        main_layout = QVBoxLayout()

        timeout_x_box = QHBoxLayout()
        timeout_x_box.addWidget(self.timeout_label)
        timeout_x_box.addStretch(1)
        timeout_x_box.addWidget(self.timeout_edit)
        main_layout.addLayout(timeout_x_box)

        self.setLayout(main_layout)
