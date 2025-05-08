from io import TextIOWrapper
import os
import re
import sqlite3
import threading

from my_log import log


def connectOrCreateDb(name: str = "default.db"):
    # 连接或自动创建数据库
    dbcon = sqlite3.connect(name)
    return dbcon


def createTable(dbcon: sqlite3.Connection):

    # 游标
    cur = dbcon.cursor()
    # 模特表
    result = cur.execute(
        "CREATE TABLE model(model_id UNIQUE,name UNIQUE,tags,description,birthday)"
    )
    print(f"create model={result}")
    # 专辑表
    result = cur.execute(
        "CREATE TABLE album(album_id UNIQUE,model_id,title,photo_count,photo_time,group_name)"
    )
    print(f"create album={result}")

    # 图片地址表
    result = cur.execute(
        "CREATE TABLE photo_urls(photo_id UNIQUE,album_id,model_id,title,url UNIQUE)"
    )
    print(f"create photo_urls={result}")


def selectTable(dbcon: sqlite3.Connection):
    res = dbcon.execute("SELECT * from sqlite_master")
    list = res.fetchall()
    for i in list:
        print(i)


async def insertIntoTable(
    dbcon: sqlite3.Connection, file: TextIOWrapper, group_name: str
):
    with file as f:
        date = ""
        title = ""
        cur = dbcon.cursor()
        model_id = (
            dbcon.cursor().execute("select count(rowid)-1 FROM model").fetchone()[0]
        )
        album_id = (
            dbcon.cursor().execute("select count(rowid)-1 FROM album").fetchone()[0]
        )
        photo_id = (
            dbcon.cursor()
            .execute("select count(rowid)-1 FROM photo_urls")
            .fetchone()[0]
        )
        log(f"model_id={model_id},album_id={album_id},photo_id={photo_id}")
        for line in f.readlines():
            if line.startswith("date") or line.startswith("item"):
                info = line.replace("\n", "").split("title")
                date = info[0].replace("date=", "").strip()
                index = date.find("=")
                if index != -1:
                    date = date[date.find("=") + 1 :].strip()
                title = info[1].replace("=", "")
                log(f"date={date},name={title}")
                # album_id,model_id,title,photo_count,photo_time,group_name
                query_title = cur.execute(
                    "select title FROM album WHERE title=?", (title,)
                ).fetchone()
                if query_title is not None:
                    continue
                album_id += 1
                cur.execute(
                    "INSERT INTO album VALUES(?,?,?,?,?,?)",
                    (album_id, 0, title, 0, date, group_name),
                )
                log(f"INSERT INTO album: {info}")
            elif line.startswith("http"):
                # photo_id,album_id,model_id,title,url
                url = line.replace("\n", "")
                # 查询是否重复url
                query_url = cur.execute(
                    "select url FROM photo_urls WHERE url=?", (url,)
                ).fetchone()
                if query_url is not None:
                    continue
                photo_id += 1
                cur.execute(
                    "INSERT INTO photo_urls VALUES(?,?,?,?,?)",
                    (photo_id, album_id, 0, title, url),
                )
                log(f"INSERT INTO photo_urls: {url}")
        dbcon.commit()


async def insertModelIntoTable(
    db: sqlite3.Connection, count, file: TextIOWrapper, group_name, lock
):
    cursor = db.cursor()
    birthday = ""
    for line in file:
        if line.startswith("pageIndex"):
            continue
        if line.startswith("Model:"):
            model_name = line.replace("Model:", "").strip()
        if line.startswith("Info:"):
            info = line.replace("Info:", "").strip()
            if info != "":
                log(f"{model_name},{info}")
                if "|" in info:
                    arr = info.split("|")
                    for i in arr:
                        if i.startswith("生"):
                            birthday = i.split("：")[1].strip()
                            find = re.findall(r"\d{4}-\d{2}-\d{2}", birthday)
                            log(f"birthday={birthday} find={find}")

                            if len(find) > 0:
                                birthday = find[0]
                            else:
                                find = re.findall(r"\d{4}年\d{2}月\d{2}日", birthday)
                                if len(find) > 0:
                                    birthday = (
                                        find[0]
                                        .replace("年", "-")
                                        .replace("月", "-")
                                        .replace("日", "")
                                    )
                                else:
                                    birthday = ""
                            break
            else:
                birthday = ""
            # model(model_id UNIQUE,name UNIQUE,tags,description,birthday)
            # sqlite3.IntegrityError: UNIQUE constraint failed: model.model_id
            with lock:
                # 查询数据库是否有重复的模特
                query = cursor.execute(
                    "select name FROM model WHERE name=?", (model_name,)
                ).fetchone()
                if query is not None:
                    # 变为更新
                    cursor.execute(
                        "UPDATE model SET description=?, birthday=? WHERE name=?",
                        (info, birthday, model_name),
                    )
                else:
                    cursor.execute(
                        "INSERT INTO model (model_id,name, description, birthday) VALUES (?,?, ?, ?)",
                        (count, model_name, info, birthday),
                    )
                    count += 1
    db.commit()
    return count


def query_mei_data_base(
    table_name: str = "photo_urls", db_name="meirentu.db", page_num=0, limit=1000
):
    # 查询数据
    path = os.path.join(os.path.dirname(__file__),"data" ,db_name)
    dbcon = connectOrCreateDb(path)
    res = dbcon.cursor().execute(
        f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {page_num * limit}"
    )
    datas = res.fetchall()
    # 把datas的 photo_id ,album_id,model_id,title,url 转换为字典
    data_list = [transform_tuple_to_dict(data) for data in datas]
    return data_list
def query_mei_image_data_base(
    table_name: str = "photo_urls", db_name="meirentu.db", photo_id=0
):
    # 查询数据
    path = os.path.join(os.path.dirname(__file__),"data" ,db_name)
    dbcon = connectOrCreateDb(path)
    res = dbcon.cursor().execute(
        f"SELECT * FROM {table_name} WHERE photo_id=?", (photo_id,)
    )
    data = res.fetchone()
    if data is None:
        return None
    # 把datas的 photo_id ,album_id,model_id,title,url 转换为字典
    data_dict = transform_tuple_to_dict(data)
    return data_dict

def transform_tuple_to_dict(data: tuple) -> dict:
    """将元组转换为字典"""
    keys = [
        "photo_id",
        "album_id",
        "model_id",
        "title",
        "url",
    ]
    return dict(zip(keys, data))


if __name__ == "__main__":
    # dbcon = connectOrCreateDb("../meirentu.db")
    # # createTable(dbcon=dbcon)
    # # selectTable(dbcon=dbcon)
    # # insertIntoTable()
    # res = dbcon.cursor().execute("select rowid FROM album")
    # print(type(res))

    pass
