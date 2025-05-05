#下载视频，并保存到temp文件夹
import os


def save_download_video(video_id,url):
    """
    下载视频，并保存到temp文件夹
    :param url: 视频链接
    :return: 下载的视频文件路径
    """
    # 创建temp文件夹
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # 从网络url下载视频
    # 这里使用requests库下载视频
    import requests
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download video: {response.status_code}")
    # 保存视频到temp文件夹
    with open(os.path.join("temp", f"video_{video_id}.mp4"), "wb") as f:
        f.write(response.content)
    # 获取下载的视频文件路径
    video_file_path = os.path.join("temp", f"video_{video_id}.mp4")
    
    return video_file_path