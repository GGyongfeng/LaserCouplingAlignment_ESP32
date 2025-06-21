import os

class ThemeManager:
    """主题管理器"""
    
    @staticmethod
    def get_theme_path(theme_name: str) -> str:
        """获取主题文件路径"""
        theme_map = {
            "暗色主题": "dark_theme.qss",
            "亮色主题": "light_theme.qss",
            "蓝色主题": "blue_theme.qss"
        }
        
        if theme_name not in theme_map:
            theme_name = "亮色主题"
            
        theme_file = theme_map[theme_name]
        return os.path.join(os.path.dirname(__file__), theme_file)
    
    @staticmethod
    def load_theme(theme_name: str) -> str:
        """加载主题样式"""
        theme_path = ThemeManager.get_theme_path(theme_name)
        if os.path.exists(theme_path):
            with open(theme_path, "r", encoding="utf-8") as f:
                return f.read()
        return "" 