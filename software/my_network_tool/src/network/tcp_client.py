import socket
import json
from PySide6.QtCore import QThread, Signal

class TCPClient(QThread):
    response_received = Signal(dict)  # 信号：发送解析后的响应数据
    error_occurred = Signal(str)      # 信号：发送错误信息
    connected = Signal(bool)          # 信号：连接状态
    
    def __init__(self, host=None, port=8888):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None
        self.seq = 0
        self._is_connected = False

    @property
    def is_connected(self):
        return self._is_connected

    def run(self):
        """线程主函数"""
        while self._is_connected:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                try:
                    response_data = json.loads(data.decode())
                    self.response_received.emit(response_data)
                except json.JSONDecodeError:
                    self.error_occurred.emit("收到无效的响应数据")
            except Exception as e:
                self.error_occurred.emit(f"接收数据错误: {str(e)}")
                break
        
        self._is_connected = False
        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected.emit(False)

    def connect_to_server(self):
        """启动线程连接"""
        if not self.host:
            raise ValueError("未设置服务器地址")
        
        # 确保之前的连接已关闭
        self.disconnect_from_server()
            
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # 设置5秒超时
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(None)  # 恢复正常模式
            self._is_connected = True
            self.connected.emit(True)
            self.start()  # 启动监听线程
            return True
        except socket.timeout:
            if self.socket:
                self.socket.close()
                self.socket = None
            raise TimeoutError("连接超时，请检查ESP32是否开启或网络是否正常")
        except ConnectionRefusedError:
            if self.socket:
                self.socket.close()
                self.socket = None
            raise ConnectionRefusedError("连接被拒绝，请检查ESP32是否正确运行")
        except Exception as e:
            if self.socket:
                self.socket.close()
                self.socket = None
            raise Exception(f"连接失败: {str(e)}")

    def disconnect_from_server(self):
        """断开与服务器的连接"""
        self._is_connected = False
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.socket.close()
            self.socket = None
        self.connected.emit(False)
        self.wait()  # 等待线程结束

    def send_command(self, cmd, data=None):
        """发送命令"""
        if not self.is_connected or not self.socket:
            self.error_occurred.emit("未连接到服务器")
            return
            
        self.seq += 1
        request = {
            "cmd": cmd,
            "data": data or {},
            "seq": self.seq
        }
        
        try:
            self.socket.sendall((json.dumps(request) + "\n").encode())
        except Exception as e:
            self.error_occurred.emit(f"发送命令失败: {str(e)}")
            self.disconnect_from_server()

    def set_host(self, host):
        """设置服务器主机地址"""
        self.host = host

    def stop(self):
        """停止线程"""
        self.disconnect_from_server()