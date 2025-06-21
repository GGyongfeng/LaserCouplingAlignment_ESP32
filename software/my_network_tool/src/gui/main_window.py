from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                 QHBoxLayout, QPushButton, QLabel, 
                                 QLineEdit, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction, QPainter
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtCore import QDateTime
import os
import sys
from datetime import datetime

# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.network.ip_scanner import get_local_ip
from src.network.tcp_client import TCPClient
from src.gui.settings_dialog import SettingsDialog
from src.gui.scan_window import ScanWindow
from src.style.theme_manager import ThemeManager
from src.data.history_manager import HistoryManager
from src.network.middleware import MiddlewareManager, LoggingMiddleware, StatusMiddleware

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("激光耦合对准工具")
        self.setMinimumSize(900, 700)  # 增加窗口高度以容纳图表
        
        # 初始化设置
        self.settings = {
            "theme": "亮色主题",
        }
        
        # 初始化中间件管理器
        self.middleware_manager = MiddlewareManager()
        self.middleware_manager.add_middleware(LoggingMiddleware())
        self.middleware_manager.add_middleware(StatusMiddleware())
        
        # 初始化TCP客户端
        self.tcp_client = TCPClient()
        self.tcp_client.response_received.connect(self.on_response_received)
        self.tcp_client.error_occurred.connect(self.show_error_message)
        self.tcp_client.connected.connect(self.on_connection_status_changed)
        
        # 初始化历史数据管理器
        self.history_manager = HistoryManager()
        
        # 加载样式表
        self.load_theme()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title = QLabel("激光耦合对准工具")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # IP地址部分
        ip_container = QHBoxLayout()
        self.get_ip_button = QPushButton("获取本机IP")
        self.get_ip_button.clicked.connect(self.on_get_ip_click)
        self.ip_label = QLabel("")
        ip_container.addWidget(self.get_ip_button)
        ip_container.addWidget(self.ip_label)
        ip_container.addStretch()
        layout.addLayout(ip_container)
        
        # ESP32连接部分
        esp32_container = QHBoxLayout()
        self.esp32_ip_input = QLineEdit()
        self.esp32_ip_input.setPlaceholderText("输入ESP32的IP地址")
        self.connect_button = QPushButton("连接ESP32")
        self.connect_button.clicked.connect(self.on_connect_click)
        self.connection_status = QLabel("未连接")
        esp32_container.addWidget(self.esp32_ip_input)
        esp32_container.addWidget(self.connect_button)
        esp32_container.addWidget(self.connection_status)
        layout.addLayout(esp32_container)
        
        # 位移测量部分
        displacement_container = QHBoxLayout()
        self.measure_button = QPushButton("测量位移")
        self.measure_button.clicked.connect(self.on_measure_click)
        self.displacement_label = QLabel("位移: --")
        displacement_container.addWidget(self.measure_button)
        displacement_container.addWidget(self.displacement_label)
        displacement_container.addStretch()
        layout.addLayout(displacement_container)
        
        # 禁用控制按钮，直到连接成功
        self.measure_button.setEnabled(False)
        
        # 创建图表
        self.create_chart()
        layout.addWidget(self.chart_view)
        
        # 添加状态栏
        self.statusBar().showMessage("就绪")
        
        # 设置窗口图标
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                "assets", "icons", "app.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        # 扫描窗口实例
        self.scan_window = None
        
        # 加载历史数据到图表
        self.update_chart()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        export_menu = file_menu.addMenu("导出数据")
        export_json_action = QAction("导出为JSON", self)
        export_json_action.triggered.connect(self.export_json)
        export_csv_action = QAction("导出为CSV", self)
        export_csv_action.triggered.connect(self.export_csv)
        export_menu.addAction(export_json_action)
        export_menu.addAction(export_csv_action)
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu("工具")
        scan_action = QAction("网络扫描", self)
        scan_action.triggered.connect(self.show_scan_window)
        tools_menu.addAction(scan_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_scan_window(self):
        """显示扫描窗口"""
        if not self.scan_window:
            self.scan_window = ScanWindow(self)
        self.scan_window.show()
    
    def export_json(self):
        """导出JSON数据"""
        from PySide6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "导出JSON数据", "", "JSON文件 (*.json)"
        )
        if filepath:
            self.history_manager.export_to_json(filepath)
            self.statusBar().showMessage("数据导出成功")
    
    def export_csv(self):
        """导出CSV数据"""
        from PySide6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "导出CSV数据", "", "CSV文件 (*.csv)"
        )
        if filepath:
            self.history_manager.export_to_csv(filepath)
            self.statusBar().showMessage("数据导出成功")
    
    def on_measure_click(self):
        """处理测量按钮点击事件"""
        cmd = "READ_DIST_1"
        request = {
            "cmd": cmd,
            "data": {},
            "seq": self.tcp_client.seq + 1
        }
        # 使用中间件处理请求
        request = self.middleware_manager.process_request(request)
        # 保存当前命令类型
        self.current_cmd = cmd
        self.tcp_client.send_command(cmd)
        self.statusBar().showMessage("正在测量...")
        
    def on_response_received(self, response):
        """处理收到的响应"""
        print("\n=== 开始处理响应 ===")
        print(f"原始响应数据: {response}")
        
        # 使用中间件处理响应
        response = self.middleware_manager.process_response(response)
        print(f"中间件处理后的响应: {response}")
        
        # 使用当前命令类型进行匹配
        if hasattr(self, 'current_cmd') and self.current_cmd == "READ_DIST_1":
            print("检测到 READ_DIST_1 命令")
            # 检查响应状态码
            if response.get("code") == 0:
                print("响应状态码为 0 (成功)")
                data = response.get("data", {})
                print(f"响应数据: {data}")
                
                if data.get("success", False):
                    print("data.success 为 True")
                    displacement = data.get("displacement")
                    print(f"获取到的位移值: {displacement}")
                    
                    if displacement is not None:
                        print("位移值不为空，更新显示")
                        # 更新位移显示
                        self.displacement_label.setText(f"位移: {displacement:.4f} mm")
                        self.statusBar().showMessage("测量成功")
                        # 保存到历史记录
                        self.history_manager.add_record(
                            displacement=displacement,
                            success=True
                        )
                        # 更新图表
                        self.update_chart()
                    else:
                        print("警告：位移值为空")
                        self.show_error_message("未收到位移数据")
                else:
                    print(f"data.success 为 False")
                    error_msg = response.get("msg", "测量失败")
                    self.displacement_label.setText("位移: --")
                    self.statusBar().showMessage(f"测量失败: {error_msg}")
                    # 保存错误记录
                    self.history_manager.add_record(
                        success=False,
                        error_message=error_msg
                    )
            else:
                print(f"响应状态码不为 0: {response.get('code')}")
                error_msg = response.get("msg", "未知错误")
                self.displacement_label.setText("位移: --")
                self.statusBar().showMessage(f"错误: {error_msg} (错误码: {response.get('code')})")
                # 保存错误记录
                self.history_manager.add_record(
                    success=False,
                    error_message=error_msg
                )
        else:
            print(f"收到未知命令: {response.get('cmd')}")
        
        print("=== 响应处理完成 ===\n")
    
    def load_theme(self):
        """加载主题"""
        style = ThemeManager.load_theme(self.settings["theme"])
        self.setStyleSheet(style)
    
    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self.settings, self)
        dialog.settings_changed.connect(self.apply_settings)
        dialog.exec()
    
    def apply_settings(self, new_settings):
        """应用新设置"""
        self.settings.update(new_settings)
        self.load_theme()
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于",
                         "激光耦合对准工具 v1.0\n\n"
                         "用于激光器耦合过程中的位移测量和数据记录")
    
    def on_get_ip_click(self):
        ip = get_local_ip()
        self.ip_label.setText(f"本机IP地址: {ip}")
    
    def on_connect_click(self):
        """处理连接按钮点击事件"""
        if not self.tcp_client.is_connected:
            ip = self.esp32_ip_input.text().strip()
            if not ip:
                self.show_error_message("请输入ESP32的IP地址")
                return
            
            # 添加简单的IP地址格式验证
            ip_parts = ip.split('.')
            if len(ip_parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_parts):
                self.show_error_message("请输入有效的IP地址格式（例如：192.168.1.100）")
                return
                
            self.tcp_client.set_host(ip)
            self.connect_button.setEnabled(False)  # 禁用按钮防止重复点击
            self.connection_status.setText("正在连接...")
            self.statusBar().showMessage("正在连接到ESP32...")
            
            try:
                if self.tcp_client.connect_to_server():
                    self.connect_button.setText("断开连接")
                    self.statusBar().showMessage("连接成功")
            except Exception as e:
                self.show_error_message(str(e))
                self.connection_status.setText("未连接")
                self.statusBar().showMessage("连接失败")
        else:
            self.tcp_client.disconnect_from_server()
            self.connect_button.setText("连接ESP32")
            self.statusBar().showMessage("已断开连接")
        
        self.connect_button.setEnabled(True)
    
    def on_connection_status_changed(self, connected):
        """处理连接状态变化"""
        self.measure_button.setEnabled(connected)
        self.connection_status.setText("已连接" if connected else "未连接")
        if not connected:
            self.connect_button.setText("连接ESP32")
            self.connect_button.setEnabled(True)
            self.displacement_label.setText("位移: --")
    
    def show_error_message(self, message):
        """显示错误消息"""
        QMessageBox.warning(self, "错误", message)
        self.statusBar().showMessage(f"错误: {message}")
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.tcp_client:
            self.tcp_client.stop()
        super().closeEvent(event)
    
    def create_chart(self):
        """创建图表"""
        # 创建图表
        self.chart = QChart()
        self.chart.setTitle("位移历史数据")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # 创建数据系列
        self.series = QLineSeries()
        self.series.setName("位移")
        self.chart.addSeries(self.series)
        
        # 创建坐标轴
        self.axis_x = QDateTimeAxis()
        self.axis_x.setTitleText("时间")
        self.axis_x.setFormat("HH:mm:ss")
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axis_x)
        
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("位移 (mm)")
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axis_y)
        
        # 创建图表视图
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setMinimumHeight(200)
        
    def update_chart(self):
        """更新图表数据"""
        # 获取历史数据
        records = self.history_manager.get_latest_records(100)  # 获取最新的100条记录
        
        # 清空现有数据
        self.series.clear()
        
        # 添加数据点
        for record in records:
            if record.get("success") and record.get("displacement") is not None:
                # 将Python datetime转换为QDateTime
                timestamp = datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
                # 使用当前时间作为基准，只保留时分秒信息
                current_time = QDateTime.currentDateTime()
                current_time.setTime(timestamp.time())
                displacement = record["displacement"]
                self.series.append(current_time.toMSecsSinceEpoch(), displacement)
        
        # 调整坐标轴范围
        if self.series.count() > 0:
            # 获取当前时间
            current_time = QDateTime.currentDateTime()
            # 设置时间范围为当前时间前后30分钟
            start_time = current_time.addSecs(-1800)  # 30分钟前
            end_time = current_time.addSecs(1800)     # 30分钟后
            
            self.axis_x.setRange(start_time, end_time)
            
            # 计算Y轴范围，留出一些边距
            y_min = min(point.y() for point in self.series.points())
            y_max = max(point.y() for point in self.series.points())
            y_range = y_max - y_min
            margin = y_range * 0.1
            self.axis_y.setRange(y_min - margin, y_max + margin) 