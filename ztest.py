from video_handler.video_processor import probe_duration, probe_video


if __name__ == "__main__":
    # 添加水印
    # add_watermark()
    # 获取视频信息
    file_path = "output.mp4"
    # probe_video(file_path)
    probe_duration(file_path)