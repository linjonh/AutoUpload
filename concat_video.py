import os
import subprocess

import my_log

folder_path = [
    # f"G:{os.sep}360AutoRec{os.sep}SECVIDEO",
    f"G:{os.sep}360AutoRec{os.sep}REC",
    f"G:{os.sep}360AutoRec{os.sep}EMERGENCY",
]
names = [
    # "SECVIDEO_list.txt",
    "REC_list.txt",
    "EMERGENCY_list.txt",
]


def save_file_list(folder_path: str, file_name: str):
    files = sorted(
        os.listdir(folder_path),
        key=lambda f: os.path.getmtime(os.path.join(folder_path, f)),
    )
    with open(file_name, "w") as f:
        for file in files:
            if file.lower().endswith(".mp4"):
                if "_out" in file:
                    continue
                file_path = os.path.join(folder_path, file)
                f.write(f"file '{file_path}'\n")
    return file_name


def concat_video(dir_file_name: str):
    dir = dir_file_name.replace(".txt", "")
    os.makedirs(dir, exist_ok=True)
    parent_dir = f"{dir}{os.sep}"
    
    
    with open(dir_file_name, "r") as f:
        lines = f.readlines()
    with open("progres.txt", "r") as f:
        progres = f.read()
    my_log.log(len(lines))
    for i in range(0, len(lines), 5):
        if lines[i].strip() in progres:
            my_log.log(f"已合并{i}个视频")
            continue
        # tmp_ts: list[str] = []
        with open("tmp_concat_list.txt", "w") as f:
            for j in range(i, i + 5):
                if j < len(lines):
                    f.write(lines[j])
                    # file_path = lines[j].strip()
                    # input = file_path.replace("file '", "").replace("'", "")
                    # # 先转换为ts
                    # output_tmp = parent_dir+input[input.rfind(os.sep) + 1:].replace(".MP4", "")
                    # cmd = f"ffmpeg -hide_banner -i {input} -c copy -bsf:v h264_mp4toannexb -f mpegts -y {output_tmp}.ts"
                    # my_log.log(f"转换为ts:{cmd}")
                    # result = subprocess.run(cmd, shell=True)
                    # if result.returncode != 0:
                    #     my_log.log("error", result.stderr)
                    # else:
                    #     f.write(f"file '{output_tmp}.ts'\n")
                    #     my_log.log("success:result", result.stdout)
       
          
        output_file_name = (
            lines[i].replace(".MP4", "_out").replace("'", "").split(" ")[1].strip()
        )
        # index = output_file_name.rfind(os.sep)
        # output_file_name = parent_dir + output_file_name[index + 1 :]

        cmd = f"ffmpeg -hide_banner -f concat -safe 0 -thread_queue_size 512 -i tmp_concat_list.txt -c copy  -threads 12 -y {output_file_name}.mp4"
        # cmd = f"ffmpeg -hide_banner -f concat -safe 0 -thread_queue_size 512 -i tmp_concat_list.txt -c copy -bsf:a aac_adtstoasc -threads 12 -y {output_file_name}.mp4"
        my_log.log(f"合并视频:{cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            my_log.log("error", result.stderr)
        else:
            my_log.log("success:result", result.stdout)
            # 记录已经合并的文件
            with open("progres.txt", "a") as f:
                with open("tmp_concat_list.txt", "r") as fr:    
                    tmp_lines=fr.readlines()
                    f.writelines(tmp_lines)
                    # for tl in tmp_lines:
                    #     ts_video = tl.strip().replace("file '", "").replace("'", "")
                    #     my_log.log(f"删除ts文件:{ts_video}")
                    #     try:
                    #         os.remove(ts_video)
                    #     except Exception as e:
                    #         my_log.log(f"删除文件失败:{ts_video} {e}")
                    my_log.log(f"合并视频成功:{output_file_name}")
            # 先删除除文件，再删除记录
            for j in range(i, i + 5):
                if j < len(lines):
                    video = lines[j].strip().replace("file '", "").replace("'", "")
                    my_log.log(f"删除文件:{video}")
                    try:
                        os.remove(video)
                    except Exception as e:
                        my_log.log(f"删除文件失败:{video} {e}")
            # 删除已经合成文件记录
            with open(dir_file_name, "w") as fw:
                for j in range(i, i + 5):
                    if j < len(lines):
                        lines[j] = ""
                fw.writelines(lines)
        break


if __name__ == "__main__":
    for i, name in enumerate(names):
        dir = save_file_list(folder_path[i], name)
        # my_log.log(f"开始合并{name}")
        # concat_video(name)
    pass
