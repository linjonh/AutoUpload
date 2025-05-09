import sqlite3
import os

from data_base.base_sqlite_db import BaseSqliteDb
from my_log import log


class video_download_db(BaseSqliteDb):
    def __init__(
        self, db_name: str = "video_download.db", table_name: str = "video_material"
    ):
        """初始化数据库类"""
        super().__init__()
        self.db_name = db_name
        self.table_name = table_name
        self.data_path = os.path.join("data_base/data/", self.db_name)
        self.db_connection = None
        self.create_db(self.db_name)
        self.create_table(
            table_name=table_name,
            table_fields={
                "video_id": "INTEGER PRIMARY KEY",
                "video_title": "TEXT",
                "download_url": "TEXT",
                "image_url": "TEXT",
                "video_number": "INTEGER",
                "Video_platform": "TEXT",
                "time": "TEXT",
                "tips": "TEXT",
            },
        )

    def create_db(self, db_name: str):
        """创建数据库"""
        self.db_name = db_name
        dir = os.path.dirname(self.data_path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.db_connection = sqlite3.connect(self.data_path)
        return self.db_connection

    def drop_db(self, db_name: str):
        """删除数据库"""
        if os.path.exists(self.data_path):
            os.remove(self.data_path)
        else:
            print("数据库不存在")

    def drop_table(self, table_name: str):
        """删除表"""
        cursor = self.db_connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.db_connection.commit()
        cursor.close()

    def create_table(self, table_name: str, table_fields: dict):
        """创建表"""
        cursor = self.db_connection.cursor()
        fields = ", ".join([f"{k} {v}" for k, v in table_fields.items()])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})")
        self.db_connection.commit()
        cursor.close()

    def insert_table(self, table_name: str, data: dict):
        """插入数据"""
        cursor = self.db_connection.cursor()
        id = data["video_id"]
        download_url: str = data["download_url"]
        image_url: str = data["image_url"]
        download_url = download_url[download_url.find(".com") + 4 :]
        image_url = image_url[image_url.find(".com") + 4 :]
        # print(f"id={id} type={type(id)}")
        query = cursor.execute(
            f"select download_url,video_id from {table_name} where video_id=? OR download_url like ? OR image_url like ?",
            (id, f"%{download_url}%", f"%{image_url}%"),
        ).fetchone()
        if query is not None:
            log(f"insert_table: 数据已存在{query}")
            cursor.close()
            return False
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        result = cursor.execute(sql, tuple(data.values()))
        self.db_connection.commit()
        log(f"插入数据成功，结果lastrowid={result.lastrowid}")
        cursor.close()
        return True

    def update_table(self, table_name: str, data: dict):
        """更新数据"""
        cursor = self.db_connection.cursor()
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE video_id = ?"
        cursor.execute(sql, tuple(data.values()) + (data["video_id"],))
        self.db_connection.commit()
        cursor.close()
        return True

    def delete_table(self, table_name: str, video_id: str):
        """删除数据"""
        cursor = self.db_connection.cursor()
        sql = f"DELETE FROM {table_name} WHERE video_id = ?"
        cursor.execute(sql, (video_id,))
        self.db_connection.commit()
        cursor.close()
        return True

    def fech_one_video(self, table_name: str, video_id: str) -> dict:
        """查询数据"""
        cursor = self.db_connection.cursor()
        sql = f"SELECT * FROM {table_name} WHERE video_id = ?"
        cursor.execute(sql, (video_id,))
        result = cursor.fetchone()
        cursor.close()
        return self.transform_tuple_to_dict(result) if result else None

    # 分页插叙数据
    def fech_videos_by_page(self, table_name: str, page_num: int, page_size: int):
        """分页查询数据"""
        cursor = self.db_connection.cursor()
        offset = (page_num - 1) * page_size
        sql = f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        # 转换为字典列表
        result = [
            self.transform_tuple_to_dict(row) for row in result
        ]
        return result
    def transform_tuple_to_dict(self, data: tuple) -> dict:
        """将元组转换为字典"""
        keys = [
            "video_id",
            "video_title",
            "download_url",
            "image_url",
            "video_number",
            "Video_platform",
            "time",
            "tips",
        ]
        return dict(zip(keys, data))
    def close_db(self):
        """关闭数据库"""
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None
        else:
            print("数据库未打开或已关闭")

    def __del__(self):
        """析构函数"""
        self.close_db()


if __name__ == "__main__":
    db = video_download_db()
    # db.create_db("test.db")
    # db.create_table("test_table", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    # db.insert_table("test_table", {"id": 1, "name": "test"})
    # print(db.select_table("test_table", 1))
    # db.update_table("test_table", {"id": 1, "name": "test_updated"})
    # print(db.select_table("test_table", 1))
    # db.delete_table("test_table", 1)
    # print(db.select_table("test_table", 1))
    # db.drop_table("test_table")
    # db.drop_db("test.db")
