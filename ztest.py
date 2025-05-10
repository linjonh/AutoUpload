import os
import time_tools
from video_handler.video_processor import probe_duration, probe_video

text = ("\"#随笔段子"
+"其实吧生活就是很捉摸不透，因为没有人会在乎你，正如你就像发光的金子放在沙漠里，可有可无一样，一眼望去全是沙漠🏜️，谁又能在茫茫沙漠里找到你这埋藏在沙漠里的细粒沙金呢？大家都只是过客，来也匆匆，去也匆匆，谁又会为你而停留呢？也就好像这条动态也不会有人看，也不会有点赞，也不会有评论一样，甚至手一滑屏幕，如火箭🚀升空般划过你的眼睛！因而渐渐的，渐渐的，大家变得沉默，不再愿意发动态，也不愿意去透露自己生活，更不愿意展现自己！久而久之，你会发现朋友圈的质量其实没有什么可看的，也不愿意每天花时间去看别人芝麻大点事，要么几天几周不看，要么几个月才偶尔记得了打开刷几条，要么干脆把朋友圈功能也都关了。大家似乎都很懂得无用社交，对于自己没有利益的不回复不主动，对于自己不感兴趣的不回复不主动，对于自己不关心的不回复不主动，对于自己弊大于利的避而远之……似乎成了成人间的交往准则。"
+"当你工作了多年以后，你也会发现各自成家的成家，唯独自己剩下了，与他们格格不入，渐渐的你习惯了一个人的生活，不想为了迎合别人而委屈自己，已所不欲也勿施于人。你学会了一个人高兴，一个人忧伤，一个人承受，一个人痛苦。一个人欣赏周星驰，慢慢体会到他的心酸苦楚凄凉，一个人走来，辉煌过，灿烂过，也开怀大笑过，最后慢慢的一个人老去，头发变得花白，脸上的皱纹清晰可见，看到此，你内心是否也很难平静？"
+"\"")


def test_tts():
    tts_names = [
        "zh-CN-XiaoxiaoNeural",  # Female    News, Novel            Warm
        "zh-CN-XiaoyiNeural",  # Female    Cartoon, Novel         Lively
        "zh-CN-YunjianNeural",  # Male      Sports, Novel          Passion
        "zh-CN-YunxiNeural",  # Male      Novel                  Lively, Sunshine
        "zh-CN-YunxiaNeural",  # Male      Cartoon, Novel         Cute
        "zh-CN-YunyangNeural",  # Male      News                   Professional, Reliable
        "zh-CN-liaoning-XiaobeiNeural",  # Female    Dialect                Humorous
        "zh-CN-shaanxi-XiaoniNeural",  # Female    Dialect                Bright
        "zh-HK-HiuGaaiNeural",  # Female    General                Friendly, Positive
        "zh-HK-HiuMaanNeural",  # Female    General                Friendly, Positive
        "zh-HK-WanLungNeural",  # Male      General                Friendly, Positive
        "zh-TW-HsiaoChenNeural",  # Female    General                Friendly, Positive
        "zh-TW-HsiaoYuNeural",  # Female    General                Friendly, Positive
        "zh-TW-YunJheNeural",  # Male      General                Friendly, Positive
    ]
    for i in tts_names:
        # 生成语音
        cmd = [
            "edge-tts",
            f"-t {text}",
            f"-v {i}",
            f"--write-media {i}.mp3",
        ]
        cmd_str = " ".join(cmd)
        # print(cmd_str)
        print(f"正在生成语音：{i}")
        run_cmd(cmd_str)
        # break


@time_tools.timeCost
def run_cmd(cmd_str):
    os.system(cmd_str)


def concat_images():
    cmd=f"ffmpeg -hide_banner -y -i {input} -vf "
    


if __name__ == "__main__":
    # 添加水印
    # add_watermark()
    # 获取视频信息
    # file_path = "output.mp4"
    # probe_video(file_path)
    # probe_duration(file_path)
    test_tts()
