from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QLabel, 
                              QTableWidget, QTableWidgetItem, QHeaderView,
                              QProgressBar, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
import os

from src.network.ip_scanner import scan_network_devices
from src.gui.context_menu import DeviceContextMenu

class ScanWorker(QThread):
    """扫描工作线程"""
    progress_updated = Signal(int)  # 进度信号
    scan_completed = Signal(list)   # 完成信号

    def __init__(self, thread_count=32):
        super().__init__()
        self.is_running = True
        self.thread_count = thread_count

    def run(self):
        def progress_callback():
            self.progress_count += 1
            progress = int((self.progress_count / 254) * 100)
            self.progress_updated.emit(progress)

        self.progress_count = 0
        devices = scan_network_devices(progress_callback=progress_callback)
        if self.is_running:  # 只有在没有被停止的情况下才发送结果
            self.scan_completed.emit(devices)

    def stop(self):
        self.is_running = False

class ScanWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("网络设备扫描")
        self.setMinimumSize(800, 600)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 扫描控制部分
        scan_control = QHBoxLayout()
        self.scan_button = QPushButton("开始扫描")
        self.scan_button.clicked.connect(self.on_scan_click)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        scan_control.addWidget(self.scan_button)
        scan_control.addWidget(self.progress_bar)
        scan_control.addStretch()
        layout.addLayout(scan_control)
        
        # 设备列表表格
        self.table = QTableWidget()
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['IP地址', '主机名', 'MAC地址', '状态'])
        # 设置表格列宽自动调整
        header = self.table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        # 初始化扫描相关变量
        self.scanning = False
        self.scan_worker = None
        
    def on_scan_click(self):
        if not self.scanning:
            # 开始扫描
            self.scanning = True
            self.scan_button.setText("停止扫描")
            self.progress_bar.setValue(0)
            self.table.setRowCount(0)
            
            # 创建并启动扫描线程
            self.scan_worker = ScanWorker()
            self.scan_worker.progress_updated.connect(self.update_progress)
            self.scan_worker.scan_completed.connect(self.scan_complete)
            self.scan_worker.start()
        else:
            # 停止扫描
            self.scanning = False
            self.scan_button.setText("开始扫描")
            if self.scan_worker:
                self.scan_worker.stop()
                self.scan_worker.wait()
    
    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
    
    def scan_complete(self, devices):
        self.scanning = False
        self.scan_button.setText("开始扫描")
        
        # 更新设备表格
        self.table.setRowCount(0)
        sorted_devices = sorted(devices, key=lambda x: [int(i) for i in x['ip'].split('.')])
        
        for dev in sorted_devices:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(dev['ip']))
            self.table.setItem(row, 1, QTableWidgetItem(dev['hostname']))
            self.table.setItem(row, 2, QTableWidgetItem(dev['mac']))
            self.table.setItem(row, 3, QTableWidgetItem(dev['status']))
            
            # 设置单元格文本居中对齐
            for col in range(4):
                item = self.table.item(row, col)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def show_context_menu(self, pos):
        """显示右键菜单"""
        item = self.table.itemAt(pos)
        if item is None:
            return
            
        row = item.row()
        ip = self.table.item(row, 0).text()
        hostname = self.table.item(row, 1).text()
        
        menu = DeviceContextMenu(ip, hostname, self)
        menu.ping_device.connect(self.ping_device)
        menu.copy_ip.connect(self.copy_to_clipboard)
        menu.copy_hostname.connect(self.copy_to_clipboard)
        menu.exec(self.table.viewport().mapToGlobal(pos))
    
    def ping_device(self, ip):
        """Ping设备"""
        from src.network.ip_scanner import ping
        if ping(ip):
            QMessageBox.information(self, "Ping结果", f"{ip} 可以访问")
        else:
            QMessageBox.warning(self, "Ping结果", f"{ip} 无法访问")
    
    def copy_to_clipboard(self, text):
        """复制文本到剪贴板"""
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(text)
        
    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.scan_worker:
            self.scan_worker.stop()
            self.scan_worker.wait()
        super().closeEvent(event) 