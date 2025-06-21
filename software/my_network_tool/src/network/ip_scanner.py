import socket
import subprocess
import platform
import threading
from queue import Queue
import time

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def ping(host: str) -> bool:
    """使用ping命令检测主机是否在线"""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def get_hostname(ip: str) -> str:
    """获取主机名"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return "Unknown"

def worker(queue: Queue, results: list, progress_callback=None):
    """工作线程函数"""
    while True:
        ip = queue.get()
        if ip is None:
            break
        if ping(ip):
            hostname = get_hostname(ip)
            mac = "N/A"  # MAC地址获取需要管理员权限，这里暂时不实现
            results.append({
                'ip': ip,
                'hostname': hostname,
                'mac': mac,
                'status': '在线'
            })
        if progress_callback:
            progress_callback()
        queue.task_done()

def scan_network_devices(progress_callback=None) -> list:
    """扫描局域网内的设备
    
    Args:
        progress_callback: 进度回调函数
        
    Returns:
        list: 包含在线设备信息的列表
    """
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        return []
    
    # 获取网段
    ip_parts = local_ip.split('.')
    network = '.'.join(ip_parts[:-1])
    
    # 创建工作队列
    queue = Queue()
    results = []
    
    # 添加所有可能的IP到队列
    for i in range(1, 255):
        queue.put(f"{network}.{i}")
    
    # 创建工作线程
    threads = []
    thread_count = min(32, queue.qsize())  # 最多32个线程
    for _ in range(thread_count):
        t = threading.Thread(
            target=worker,
            args=(queue, results, progress_callback)
        )
        t.daemon = True
        t.start()
        threads.append(t)
    
    # 等待所有IP扫描完成
    queue.join()
    
    # 停止所有线程
    for _ in range(thread_count):
        queue.put(None)
    for t in threads:
        t.join()
    
    return sorted(results, key=lambda x: [int(i) for i in x['ip'].split('.')]) 