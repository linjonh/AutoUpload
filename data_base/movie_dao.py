import json
import os
import sqlite3
import sys

import time_tools

# 获取当前文件所在目录的父目录
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"current_dir={current_dir}")
parent_dir = os.path.dirname(current_dir)
# 将父目录添加到 Python 模块搜索路径中
sys.path.append(parent_dir)


from base_sqlite_db import BaseSqliteDb
from my_log import log


class MovieDb(BaseSqliteDb):
    def __init__(self, db_name="movie.db"):
        super().__init__()
        self.db_name = db_name
        self.data_path = "data/movie/movie.json"
        self.db_connection = self.create_db(self.db_name)

    def create_db(self, db_name: str):
        # 创建sqlite3数据库
        dbconn = sqlite3.connect(db_name)
        return dbconn

    def create_table(self, tabel_name: str, table_fields: tuple[str]):
        # 创建表
        self.db_connection.execute(
            "CREATE TABLE IF NOT EXISTS "
            + tabel_name
            + " ("
            + ",".join(table_fields)
            + ")"
        )
        pass

    def drop_table(self, table_name: str):
        # 删除表
        self.db_connection.execute(f"DROP TABLE IF EXISTS {table_name}")
        pass

    def insert_table(self, table_name: str, data: tuple):
        # 构建占位符
        placeholders = ",".join(["?"] * len(data))
        # 构建 SQL 语句
        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        # 执行插入操作
        self.db_connection.execute(sql, data)

    def update_table(self, table_name: str, data: tuple):
        pass

    def delete_table(self, table_name: str, data: tuple):
        pass

    def select_table(self, table_name: str, data: tuple):
        pass


# 电影数据处理,解析电影数据，插入数据库
# 先各自保存各自数据库，后序用sql语句查询合并各个数据库
@time_tools.time_cost
def handle_data(db_name="data_base/movie.db"):
    # 创建数据库
    movie_class = MovieDb(db_name)

    def create_table():
        # 创建表
        movie_class.create_table(
            "movie",
            (
                "movie_id INTEGER PRIMARY KEY AUTOINCREMENT",
                "type TEXT",
                "movie_name TEXT",
                "author TEXT",
                "director TEXT",
                "scenarist TEXT",
                "actors TEXT",
                "main_actor TEXT",
                "brief TEXT",
                "tags TEXT",
                "url TEXT",
                "cover_image TEXT",
                "landscape_img TEXT",
                "episode_count INTEGER",
                "duration INTEGER",
                "year TEXT",
                "area TEXT",
                "language TEXT",
                "sort_type TEXT",
                "update_time TEXT",
                "showtime TEXT",
            ),
        )
        movie_class.create_table(
            "movie_urls",
            (
                "movie_id INTEGER",
                "movie_name TEXT",
                "src_title TEXT",
                "episode_name TEXT",
                "url TEXT",
                "duration INTEGER",
                "year TEXT",
                "area TEXT",
                "language TEXT",
                "sort_type TEXT",
            ),
        )
        pass

    def insert_netflix_movie_data():
        if config.get("drop_netflix_movie_data", False):
            # 删除表
            movie_class.drop_table("movie")
            movie_class.drop_table("movie_urls")
            movie_class.db_connection.commit()
            create_table()
        idx = 1
        # 插入数据
        file_array = [
            "data/netflixgc/video_items_1_o2.json",
            "data/netflixgc/video_items_1_origin.json",
            "data/netflixgc/video_items_1.json",
            "data/netflixgc/video_items_2.json",
            "data/netflixgc/video_items_3_o1.json",
            "data/netflixgc/video_items_3_o2.json",
            "data/netflixgc/video_items_3_o3.json",
            "data/netflixgc/video_items_4.json",
            "data/netflixgc/video_items_23.json",
            "data/netflixgc/vod_item_2_tmp.json",
            "data/netflixgc/vod_item_30.json",
        ]

        for file in file_array:
            movie_class.data_path = file
            log(f"parse file={file}")
            parsed_vod_ids = []
            with open(movie_class.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for index, item in enumerate(data):
                    log(f"idx={idx} index={index} parse item={item}")
                    item: dict
                    item_id = item["vod_id"]
                    # 先判断是否已经解析过了，有相同的id就跳过
                    if item_id in parsed_vod_ids:
                        log(
                            f"item_id={item_id} name={item['vod_name']} has been parsed!,already insert!"
                        )
                        continue
                    else:
                        parsed_vod_ids.append(item_id)
                        idx += 1  # 电影id，不重复才加1

                    vod_info: list[str] = item["vod_info"]
                    """                  "vod_info": [
                    "片名：小岛惊魂",
                    "状态：正片",
                    "主演：妮可·基德曼 菲奥纽拉·弗拉纳根 ",
                    "导演：未知",
                    "年份：2001",
                    "地区：未知",
                    "类型：剧情 悬疑 恐怖 ",
                    "频道：内详",
                    "上映：2001",
                    "语言：内详",
                    "更新：2024-12-22 17:38",
                    "简介：暂无简介"
                    ]
                    解析出电影信息，循环遍历匹配中文字符确定是急什么字段"""
                    (
                        type,
                        author,
                        main_actor,
                        director,
                        scenarist,
                        actors,
                        area,
                        year,
                        tags,
                        update_time,
                        showtime,
                        language,
                        brief,
                    ) = parse_netflixgc_movie_info(vod_info)
                    duration = item.get("duration", 0)
                    vod_urls_arr = item["vod_urls"]
                    episode_count = 1
                    url_src_names = ""
                    if len(vod_urls_arr) > 0:
                        max = 0
                        for vod_url in vod_urls_arr:
                            url_src_names += vod_url["src_title"] + ","
                            episode_count = len(vod_url["src_urls"])
                            if max < episode_count:
                                max = episode_count
                        episode_count = max
                    movie_class.insert_table(
                        "movie",
                        (
                            idx,  # "movie_id",
                            type,
                            item["vod_name"],
                            author,
                            director,
                            scenarist,  # 编剧
                            actors,
                            main_actor,
                            brief,
                            tags,
                            url_src_names,  # "url"
                            item.get("cover_image", ""),
                            item.get("landscape_img", ""),
                            episode_count,
                            duration,
                            year,
                            area,
                            language,
                            item.get("sort_type", ""),
                            update_time,
                            showtime,
                        ),
                    )
                    # 解析出电影的播放地址
                    vod_urls_arr
                    for vod_url in vod_urls_arr:
                        for src_url in vod_url["src_urls"]:
                            src_title = vod_url["src_title"]
                            episode_name = src_url["title"]
                            url = src_url["url"]
                            movie_class.insert_table(
                                "movie_urls",
                                (
                                    idx,  # "movie_id",
                                    item["vod_name"],
                                    src_title,
                                    episode_name,
                                    url,
                                    duration,
                                    year,
                                    area,
                                    language,
                                    item.get("sort_type", ""),
                                ),
                            )
            pass
            movie_class.db_connection.commit()
        return

    create_table()
    # 插入奈飞工厂数据
    insert_netflix_movie_data()
    # TODO:插入其他网站电影数据

    return movie_class


def parse_netflixgc_movie_info(vod_info):
    # 解析电影信息
    # type,author, main_actor, director, scenarist, actors, area, year, tags, update_time, showtime, language, brief
    # 电影类型,作者,主演,导演,编剧,演员,地区,年份,类型,更新时间,上映时间,语言,简介
    # 先初始化变量
    type = ""
    author = ""
    main_actor = ""
    director = ""
    scenarist = ""
    actors = ""
    area = ""
    year = ""
    tags = ""
    update_time = ""
    showtime = ""
    language = ""
    brief = ""
    for info in vod_info:
        if "状态" in info:
            type = info.split("：")[1]
        elif "作者" in info:
            author = info.split("：")[1]
        elif "主演" in info:
            main_actor = info.split("：")[1]
        elif "导演" in info:
            director = info.split("：")[1]
        elif "编剧" in info:
            scenarist = info.split("：")[1]
        elif "演员" in info:
            actors = info.split("：")[1]
        elif "地区" in info:
            area = info.split("：")[1]
        elif "年份" in info:
            year = info.split("：")[1]
        elif "类型" in info:
            tags = info.split("：")[1]
        elif "频道" in info:
            # main_actor = info.split("：")[1]
            pass
        elif "更新" in info:
            update_time = info.split("：")[1]
        elif "上映" in info:
            showtime = info.split("：")[1]
        elif "语言" in info:
            language = info.split("：")[1]
        elif "简介" in info:
            brief = info.split("：")[1]
    return (
        type,
        author,
        main_actor,
        director,
        scenarist,
        actors,
        area,
        year,
        tags,
        update_time,
        showtime,
        language,
        brief,
    )


def test():
    vod_info = [
        "片名：哥哥太爱我了怎么办",
        "状态：正片",
        "主演：土屋太凤 片寄凉太 千叶雄大 草川拓弥 杉野遥亮 ",
        "导演：未知",
        "年份：2017",
        "地区：未知",
        "类型：喜剧 爱情 ",
        "频道：内详",
        "上映：2017",
        "语言：内详",
        "更新：2024-12-22 17:36",
        "简介：暂无简介",
    ]
    print(parse_netflixgc_movie_info(vod_info))
    pass


config = {
    "drop_netflix_movie_data": True,
}
keys = ["movie_id", "type", "movie_name", "main_actor", "tags", "area", "year", "url"]


def keys_to_string(keys: list[str]):
    # 把keys转换为字符串
    keys_str = ",".join(keys)
    return keys_str


def query_one_movie(movie_id):
    # 查询一部电影
    db = MovieDb()
    data = db.db_connection.execute(
        f"SELECT {keys_to_string(keys)} FROM movie WHERE movie_id=?",
        (movie_id,),
    )
    data = data.fetchone()
    if not data:
        return None
    # 把data 转换为字典
    data_dict = dict(zip(keys, data))
    return data_dict


def query_more_movie(limit, page_num):
    # 查询多部电影
    db = MovieDb()
    data = db.db_connection.execute(
        f"SELECT {keys_to_string(keys)} FROM movie LIMIT ? OFFSET ?",
        (limit, page_num * limit),
    )
    data = data.fetchall()
    if not data:
        return None
    # 把data 转换为字典
    data_list = [dict(zip(keys, item)) for item in data]
    return data_list


if __name__ == "__main__":

    handle_data()
