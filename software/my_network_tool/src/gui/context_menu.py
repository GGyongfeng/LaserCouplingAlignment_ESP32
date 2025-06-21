from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal

class DeviceContextMenu(QMenu):
    """设备列表右键菜单"""
    ping_device = Signal(str)  # Ping设备信号
    copy_ip = Signal(str)      # 复制IP信号
    copy_hostname = Signal(str) # 复制主机名信号

    def __init__(self, ip, hostname, parent=None):
        super().__init__(parent)
        self.ip = ip
        self.hostname = hostname
        self.setup_menu()

    def setup_menu(self):
        # Ping设备
        ping_action = self.addAction(f"Ping {self.ip}")
        ping_action.triggered.connect(lambda: self.ping_device.emit(self.ip))

        self.addSeparator()

        # 复制IP
        copy_ip_action = self.addAction("复制IP地址")
        copy_ip_action.triggered.connect(lambda: self.copy_ip.emit(self.ip))

        # 复制主机名
        if self.hostname != "Unknown":
            copy_hostname_action = self.addAction("复制主机名")
            copy_hostname_action.triggered.connect(
                lambda: self.copy_hostname.emit(self.hostname)
            ) 