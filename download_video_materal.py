from concurrent.futures import Future, ThreadPoolExecutor
import os
import queue
import sys
from threading import Lock
import threading
import traceback
import requests
import json

from data_base.download_video_db import video_download_db
from my_log import log
import time_tools


def downlod_from_net(url,need_log=False):
    res = requests.get(url)
    if res.status_code != 200:
        log(f"请求失败，状态码：{res.status_code}")
        log(f"失败原因：{res.text}")
        return None
    result = res.json()
    if need_log:
        log(f"====> url={url}")
        strs = json.dumps(result, ensure_ascii=False, indent=4)
        log(strs)
    return result

def start_download(index):
    url = "https://api.kxzjoker.cn/api/Beautyvideo?type=json"
    dicObj = downlod_from_net(url=url)
    if dicObj is None:
        log(f"index={index} 数据获取失败")
        return "EMPTY",index

    if dicObj.get("code") != 200:
        log(f"index={index} 数据获取失败")
        return "EMPTY",index
    else:
        log(f"index={index} 数据获取成功")
        del dicObj["code"]
        return dicObj,index

def handle_result():
    table_name = "video_material"
    db_class = video_download_db(table_name=table_name)
    while True:
        # 等待结果
        try:
            result,index = result_queue.get(timeout=5)
            if result == "EMPTY":
                log(f"handle_result index={index} 数据获取失败 continue")
                continue
            if result is None:
                break
            log(f"index={index} 返回的结果：\n {json.dumps(result, ensure_ascii=False, indent=4)}")
            # 在这里可以将结果存入数据库
            bool_result=db_class.insert_table(table_name=table_name,data= result)
            log(f"index={index} 数据插入结果： {bool_result}")
        except queue.Empty:
            log(f"没有结果可处理")
            continue
        except Exception as e:
            log(f"处理结果时发生异常: {e}")
            traceback.log_exc()
            continue
result_queue = queue.Queue()
@time_tools.timeCost
def main(count=2):
    # 整数最大值
    log(sys.maxsize)
    # 多线程下载
    # 获取当前CPU核心数
    cpu_count = os.cpu_count()
    log(f"当前CPU核心数：{cpu_count}")
    # 判断任务类型
    is_io_bound = True  # 如果是 I/O 密集型任务，设置为 True

    # 动态设置 max_workers
    max_workers = cpu_count() * 2 if is_io_bound else cpu_count()
    
    ThreadExecutor = ThreadPoolExecutor(max_workers=max_workers)
    futures = []
    thread = threading.Thread(target=handle_result)
    thread.start()
    for i in range(count):
        future = ThreadExecutor.submit(start_download, index=i)
        futures.append(future)
    for i, future in enumerate(futures):
        future:Future
        log(f"第{i}次下载成功")
        result_queue.put(future.result())

    result_queue.put((None,0))  # 结束处理线程

    thread.join()

if __name__ == "__main__":
    main(10_0000)
