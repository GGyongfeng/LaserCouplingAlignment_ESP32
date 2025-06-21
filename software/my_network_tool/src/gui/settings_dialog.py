from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                                 QLabel, QComboBox, QPushButton, QGroupBox)
from PySide6.QtCore import Signal

class SettingsDialog(QDialog):
    """设置对话框"""
    settings_changed = Signal(dict)  # 设置变更信号

    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setMinimumWidth(400)
        self.current_settings = current_settings
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # 主题设置组
        theme_group = QGroupBox("主题设置")
        theme_layout = QVBoxLayout()
        
        theme_row = QHBoxLayout()
        theme_label = QLabel("选择主题：")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["暗色主题", "亮色主题", "蓝色主题"])
        current_theme = self.current_settings.get("theme", "暗色主题")
        self.theme_combo.setCurrentText(current_theme)
        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.theme_combo)
        theme_layout.addLayout(theme_row)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # 扫描设置组
        scan_group = QGroupBox("扫描设置")
        scan_layout = QVBoxLayout()
        
        thread_row = QHBoxLayout()
        thread_label = QLabel("扫描线程数：")
        self.thread_combo = QComboBox()
        self.thread_combo.addItems(["8", "16", "32", "64"])
        current_threads = str(self.current_settings.get("scan_threads", 32))
        self.thread_combo.setCurrentText(current_threads)
        thread_row.addWidget(thread_label)
        thread_row.addWidget(self.thread_combo)
        scan_layout.addLayout(thread_row)
        scan_group.setLayout(scan_layout)
        layout.addWidget(scan_group)

        # 按钮
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("取消")
        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def save_settings(self):
        settings = {
            "theme": self.theme_combo.currentText(),
            "scan_threads": int(self.thread_combo.currentText())
        }
        self.settings_changed.emit(settings)
        self.accept() 