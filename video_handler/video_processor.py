import os
import sys

# 暴露 my_log 路径给运行时
current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
print("current:", current)
print("parent:", parent)
sys.path.append(parent)

from my_log import log
def get_xfade():
    #随机获取一个xfade 特效 滤镜指令，1秒中的
    import random
    xfade = [
        "fade",
        "wipeleft",
        "wiperight",
        "wipeup",
        "wipedown",
        "slideleft",
        "slideright",
        "slideup",
        "slidedown",
        "circleopen",
        "circleclose",
        # "boxopen",
        # "boxclose",
    ]
    return random.choice(xfade)
def add_watermark(
    input="input.mp4",
    output="output.mp4",
    duration1="0:6",
    duration2="6:12",
    fontsize=40,
    fontcolor="white",
    text="@爵醒影视",
    gap_x=20,
    gap_y=20,
):
    """
    添加水印到视频
    :param input: 输入视频文件路径
    :param output: 输出视频文件路径
    :param duration1: 水印持续时间1
    :param duration2: 水印持续时间2
    :param fontsize: 字体大小
    :param fontcolor: 字体颜色
    :param text: 水印文本
    :param gap_x: 水印横向间距
    :param gap_y: 水印纵向间距
    :return: 运行结果
    """
    # 修改时间
    dur = probe_duration(input)
    mid = dur/2
    duration1 = f"0:{mid}"
    duration2 = f"{mid}:{dur}"
    log("Adding watermark to video...")
    # 使用ffmpeg添加水印，水印隔一段时间出现在不同位置
    # 合并为一条指令，前半段视频水印左上角，后半段水印在右下角

    cmd = (
        f'ffmpeg -y -i {input} -filter_complex "[0:v]split=2[v1][v2];'
        + f"[v1]trim={duration1},setpts=PTS-STARTPTS,fps=30,drawtext=fontfile='simhei.ttf':fontsize={fontsize}:fontcolor={fontcolor}:text='{text}':x={gap_x}:y={gap_y}[v1out];"
        + f"[v2]trim={duration2},setpts=PTS-STARTPTS,fps=30,drawtext=fontfile='simhei.ttf':fontsize={fontsize}:fontcolor={fontcolor}:text='{text}':x=w-tw-{gap_x}:y=h-th-{gap_y}[v2out];"
        # +f'[v1out][v2out]concat=n=2:v=1:a=0[outv]" -map [outv] -map 0:a -c:a aac {output}')
        + f'[v1out][v2out]xfade=transition={get_xfade()}:duration=1:offset={mid-1}[outv]" -map [outv] -map 0:a -c:v libx264 -c:a libmp3lame {output}'
    )
    log(f"Running command: {cmd}")
    code = os.system(cmd)
    log(f"run cmd result code: {code}")
    return code


def probe_video(file_path):
    """
    获取视频文件的信息
    :param file_path: 视频文件路径
    :return: 视频信息字典
    """
    log("Probing video file...")
    cmd = f"ffprobe -v error -show_format -show_streams -of json {file_path}"
    result = os.popen(cmd).read()
    log(f"Probe result: {result}")
    return result


def probe_duration(file_path):
    """
    获取视频文件的时长
    :return: 视频时长
    """
    log("Probing video duration...")
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 {file_path}"
    result = os.popen(cmd).read()
    log(f"Probe result: {result}")
    return float(result.strip().split("=")[1])


if __name__ == "__main__":
    # 添加水印
    add_watermark()
    # 获取视频信息
    # file_path = "output.mp4"
    # probe_video(file_path)
    # probe_duration(file_path)
