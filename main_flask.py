import json
from flask import Flask, Response, render_template, request, jsonify

from data_base.download_video_db import video_download_db
from data_base.meirentu_sqlite_db import query_mei_data_base, query_mei_image_data_base
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
    return lists
def query_data_base_one(video_id):
    db = video_download_db(table_name="video_material")
    data = db.fech_one_video(
        table_name="video_material",
        video_id=video_id,
    )
    db.close_db()
    if not data:
        return None    
    return data

@app.route("/pic=<int:page_num>", methods=["GET"])
def meirentu(page_num:int=1):
    # 处理请求参数
    data_list=query_mei_data_base(page_num=page_num, limit=24)
    return render_template("meirentu.html", data_list=data_list, page=page_num, total_pages=10)
@app.route("/pic/id=<id>", methods=["GET"])
def image_detail(id):
    # 处理请求参数
    photo=query_mei_image_data_base(photo_id=id)
    
    return render_template("image_detail.html", photo=photo)

@app.route("/", methods=["GET"])
def home():
    datas = query_data_base(page_num=1, page_size=PAGE_SIZE)
    return render_template("index.html", videos=datas, page=1, total_pages=10)

@app.route("/pic", methods=["GET"])
def pic():
    return meirentu(1)


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

@app.route("/c",methods=["POST"])
def collec():
    log(f"request {request.host_url}")
    for h in request.headers:
        log(f"{h}")
    data=request.get_json(silent=True)
    pretify=json.dumps(data,indent=4,ensure_ascii=False)
    log(f"data={pretify}")
    return Response(response='{"result":"success"}',status=200)