import os
import json
import datetime
import sqlite3
from typing import List, Dict, Optional

class HistoryManager:
    def __init__(self, db_path: str = "data/history.db"):
        self.db_path = db_path
        self._ensure_db_dir()
        self._init_db()
        
    def _ensure_db_dir(self):
        """确保数据库目录存在"""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
    def _init_db(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 创建位移数据表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS displacement_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    displacement REAL,
                    success BOOLEAN,
                    error_message TEXT
                )
            ''')
            conn.commit()
            
    def add_record(self, displacement: float = None, success: bool = True, error_message: str = None):
        """添加一条记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO displacement_history (displacement, success, error_message) VALUES (?, ?, ?)',
                (displacement, success, error_message)
            )
            conn.commit()
            
    def get_latest_records(self, limit: int = 100) -> List[Dict]:
        """获取最新的记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM displacement_history ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]
            
    def get_records_by_date_range(self, start_date: datetime.date, end_date: datetime.date) -> List[Dict]:
        """按日期范围获取记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT * FROM displacement_history 
                   WHERE date(timestamp) BETWEEN date(?) AND date(?)
                   ORDER BY timestamp DESC''',
                (start_date.isoformat(), end_date.isoformat())
            )
            return [dict(row) for row in cursor.fetchall()]
            
    def get_statistics(self, start_date: Optional[datetime.date] = None, 
                      end_date: Optional[datetime.date] = None) -> Dict:
        """获取统计数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            where_clause = ""
            params = []
            
            if start_date and end_date:
                where_clause = "WHERE date(timestamp) BETWEEN date(?) AND date(?)"
                params = [start_date.isoformat(), end_date.isoformat()]
            
            query = f'''
                SELECT 
                    COUNT(*) as total_count,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count,
                    AVG(CASE WHEN success = 1 THEN displacement ELSE NULL END) as avg_displacement,
                    MIN(CASE WHEN success = 1 THEN displacement ELSE NULL END) as min_displacement,
                    MAX(CASE WHEN success = 1 THEN displacement ELSE NULL END) as max_displacement
                FROM displacement_history
                {where_clause}
            '''
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            return {
                "total_count": result[0],
                "success_count": result[1],
                "avg_displacement": result[2],
                "min_displacement": result[3],
                "max_displacement": result[4]
            }
            
    def export_to_json(self, filepath: str, start_date: Optional[datetime.date] = None,
                      end_date: Optional[datetime.date] = None):
        """导出数据到JSON文件"""
        records = self.get_records_by_date_range(start_date, end_date) if start_date and end_date \
                 else self.get_latest_records(1000000)  # 设置一个较大的限制
                 
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
            
    def export_to_csv(self, filepath: str, start_date: Optional[datetime.date] = None,
                     end_date: Optional[datetime.date] = None):
        """导出数据到CSV文件"""
        import csv
        records = self.get_records_by_date_range(start_date, end_date) if start_date and end_date \
                 else self.get_latest_records(1000000)
                 
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'timestamp', 'displacement', 'success', 'error_message'])
            writer.writeheader()
            writer.writerows(records) 