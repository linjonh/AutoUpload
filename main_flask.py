from flask import Flask, render_template, request, jsonify

from data_base.download_video_db import video_download_db
from my_log import log

app = Flask(__name__)
PAGE_SIZE = 1000

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    # Process the data here
    # For example, just echoing it back
    return jsonify(data)


def query_data_base(page_num: int = 1, page_size: int = PAGE_SIZE):
    db = video_download_db(table_name="video_material")
    
    lists = db.fech_videos_by_page(
        table_name="video_material",
        page_num=page_num,
        page_size=page_size,
    )
    db.close_db()
    # 转换为字典列表
    # "video_id": "INTEGER PRIMARY KEY",
    # "video_title": "TEXT",
    # "download_url": "TEXT",
    # "image_url": "TEXT",
    # "video_number": "INTEGER",
    # "Video_platform": "TEXT",
    # "time": "TEXT",
    # "tips": "TEXT",
    
    videos = [{'video_id': row[0],
               'video_title': row[1],
               'download_url': row[2],
               'image_url': row[3],
               'video_number': row[4],
               'Video_platform': row[5],
               'time': row[6],
               'tips': row[7]               
               } for row in lists]
    return videos
def query_data_base_one(video_id):
    db = video_download_db(table_name="video_material")
    data:tuple = db.fech_one_video(
        table_name="video_material",
        video_id=video_id,
    )
    db.close_db()
    # 转换为字典列表
    # "video_id": "INTEGER PRIMARY KEY",
    # "video_title": "TEXT",
    # "download_url": "TEXT",
    # "image_url": "TEXT",
    # "video_number": "INTEGER",
    # "Video_platform": "TEXT",
    # "time": "TEXT",
    # "tips": "TEXT",
    # 开始把data的tuple对象转化为字典
    result = {
        'video_id': data[0],
        'video_title': data[1],
        'download_url': data[2],
        'image_url': data[3],
        'video_number': data[4],
        'Video_platform': data[5],
        'time': data[6],
        'tips': data[7]
    }   
    
    return result


@app.route("/", methods=["GET"])
def home():
    datas = query_data_base(page_num=1, page_size=PAGE_SIZE)
    return render_template("index.html", videos=datas, page=1, total_pages=10)


@app.route("/page=<int:page_num>", methods=["GET"])
def index(page_num: int):
    if page_num < 1:
        page_num = 1
    if page_num > 10:
        page_num = 10
    datas = query_data_base(page_num=page_num, page_size=PAGE_SIZE)
    return render_template("index.html", videos=datas, page=page_num, total_pages=10)

@app.route("/video_id=<int:video_id>", methods=["GET"])
def video_detail(video_id: int):
    data=query_data_base_one(video_id)
    if not data:
        return jsonify({"error": "Video not found"}), 404
    return render_template("video_detail.html", video=data)
