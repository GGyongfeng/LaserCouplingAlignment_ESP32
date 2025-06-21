from typing import Dict, List, Callable
import json
from datetime import datetime

class Middleware:
    """中间件基类"""
    def process_request(self, request: Dict) -> Dict:
        """处理请求"""
        return request
        
    def process_response(self, response: Dict) -> Dict:
        """处理响应"""
        return response

class LoggingMiddleware(Middleware):
    """日志中间件"""
    def process_request(self, request: Dict) -> Dict:
        print(f"\n[{datetime.now()}] 发送请求:")
        print(json.dumps(request, ensure_ascii=False, indent=2))
        return request
        
    def process_response(self, response: Dict) -> Dict:
        print(f"\n[{datetime.now()}] 收到响应:")
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return response

class StatusMiddleware(Middleware):
    """状态处理中间件"""
    def process_response(self, response: Dict) -> Dict:
        if response.get("code") == 0:
            print(f"\n✅ 请求成功: {response.get('msg', '操作成功')}")
        else:
            print(f"\n❌ 请求失败: {response.get('msg', '未知错误')} (错误码: {response.get('code')})")
        return response

class MiddlewareManager:
    """中间件管理器"""
    def __init__(self):
        self.middlewares: List[Middleware] = []
        
    def add_middleware(self, middleware: Middleware):
        """添加中间件"""
        self.middlewares.append(middleware)
        
    def process_request(self, request: Dict) -> Dict:
        """处理请求"""
        for middleware in self.middlewares:
            request = middleware.process_request(request)
        return request
        
    def process_response(self, response: Dict) -> Dict:
        """处理响应"""
        for middleware in reversed(self.middlewares):
            response = middleware.process_response(response)
        return response 