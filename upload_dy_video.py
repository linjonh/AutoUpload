import json
import os
import traceback
import selenium
from selenium import webdriver
import pathlib
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeService
from selenium.webdriver.remote.webelement import WebElement

from data_base.download_video_db import video_download_db
from main_flask import query_data_base
from my_log import log
import my_log
from video_handler.save_download_video import save_download_video
from video_handler.video_processor import add_watermark


def input_brife(driver, describe=""):
    print("输入视频简单描述。。")
    # tag = driver.find_element(
    #     by=By.CSS_SELECTOR, value="div.outerdocbody.editor-kit-outer-container"
    # )
    innerTag = driver.find_element(
        by=By.CSS_SELECTOR,
        value="div.zone-container.editor-kit-container.editor.editor-comp-publish.notranslate.chrome.window.chrome88",
    )
    data = describe
    # inputEvent = """{
    #     "isTrusted": true,
    #     "inputType": "insertCompositionText",
    #     "type": "input",
    #     "bubbles": true,
    #     "composed": true,
    #     "returnValue": true,
    #     "srcElement":"div.zone-container.editor-kit-container.editor.editor-comp-publish.notranslate.chrome.window.chrome88",
    #     "target":"div.zone-container.editor-kit-container.editor.editor-comp-publish.notranslate.chrome.window.chrome88",
    #     "isComposing": true,
    #     "isComposition": true
    # }"""
    # obj: dict = json.loads(inputEvent)
    # obj.update(
    #     {
    #         "data": data,
    #         "timeStamp": int(time.time())
    #     }
    # )

    # json_val = json.dumps(obj,ensure_ascii=False)
    # print(json_val)
    # driver.execute_script(        f"arguments[0].dispatchEvent(new InputEvent('input', {json_val}));", tag    )
    driver.execute_script(f"arguments[0].innerText = '{data}';", innerTag)


publish_file = []


def publish_douyin(
    driver: webdriver.Chrome, path_mp4, describe_title, describe, collection=None
):
    """
    作用：发布抖音视频
    """
    driver.find_element(by=By.XPATH, value='//*[text()="发布视频"]').click()
    time.sleep(2)
    driver.find_element(by=By.XPATH, value='//input[@type="file"]').send_keys(path_mp4)

    # 等待视频上传完成
    print("视频还在上传中···")
    time.sleep(1)
    while True:
        time.sleep(5)
        try:
            driver.find_element(by=By.XPATH, value='//*[text()="重新上传"]')
            break
        except Exception as e:
            pass
    print("视频已上传完成！")

    # 封面地址获取
    # path_cover = ""
    # for i in path.iterdir():
    #     if(".png" in str(i) or ".jpg" in str(i)):
    #         path_cover = str(i);
    #         break;

    # if(path_cover != ""):
    #     print("检查到封面路径：" + path_cover)
    # else:
    #     print("未检查到封面路径，程序终止！")
    #     exit()

    # 添加封面
    # driver.find_element(by=By.XPATH,value='//*[text()="编辑封面"]').click()
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//div[text()="上传封面"]').click()
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//input[@type="file"]').send_keys(path_cover)
    # time.sleep(3)
    # driver.find_element(by=By.XPATH,value='//*[text()="裁剪封面"]/..//*[text()="确定"]').click()
    # time.sleep(3)
    # driver.find_element(by=By.XPATH,value='//*[text()="设置封面"]/..//*[contains(@class,"upload")]//*[text()="确定"]').click()

    # 封面选择
    driver.find_element(by=By.CSS_SELECTOR, value="div.recommendCover-vWWsHB").click()
    while True:
        time.sleep(2)
        try:
            driver.find_element(
                by=By.CSS_SELECTOR,
                value="div.semi-modal-confirm button.semi-button.semi-button-primary",
            ).click()
            print("封面确定完成！")
            break
        except Exception as e:
            print("封面确定失败！")
    time.sleep(1)
    # 输入视频描述
    print("输入视频描述title···")
    data = describe

    driver.find_element(
        by=By.CSS_SELECTOR, value="input.semi-input.semi-input-default"
    ).send_keys(describe_title)
    print("输入视频描述title完成！")
    time.sleep(1)

    input_brife(driver, describe)
    # 选择合集

    time.sleep(1)
    try:
        print("选择合集")
        driver.find_element(
            by=By.CSS_SELECTOR,
            value="div.semi-select.select-collection-nkL6sA.semi-select-single",
        ).click()
        time.sleep(1)
        print("选择合集第一个")
        if collection == None:
            driver.find_elements(
                by=By.CSS_SELECTOR, value="div.semi-select-option.collection-option"
            )[2].click()
        else:
            els = driver.find_elements(
                by=By.CSS_SELECTOR, value="div.semi-select-option.collection-option"
            )
            for el in els:
                if collection in el.text:
                    el.click()
                    break
    except Exception as e:
        print("选择合集出错")

    # 设置选项
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//*[@class="radio--4Gpx6"]').click()
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//*[@class="semi-select-selection"]//span[contains(text(),"输入")]').click()
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//*[@class="semi-select-selection"]//input').send_keys("中关村人工智能科技")
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//*[@class="semi-select-selection"]//input').send_keys("园")
    # time.sleep(5)
    # driver.find_element(by=By.XPATH,value='//*[@class="semi-popover-content"]//*[text()="中关村人工智能科技园"]').click()

    # 同步到西瓜视频
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//div[@class="preview--27Xrt"]//input').click()   # 默认启用一次后，后面默认启用了。
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//*[@class="card-pen--2P8rh"]').click()
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//*[@class="DraftEditor-root"]//br').send_keys(describe + " #上热门")
    # time.sleep(1)
    # driver.find_element(by=By.XPATH,value='//button[text()="确定"]').click()

    time.sleep(1)
    # 选择保密性选项
    driver.find_elements(by=By.CSS_SELECTOR, value="div label.radio-d4zkru")[0].click()

    time.sleep(1)

    # 人工进行检查并发布
    # time.sleep(3)
    # # 点击发布
    print("点击发布")
    driver.find_element(by=By.XPATH, value='//button[text()="发布"]').click()
    count = 0
    while True:
        time.sleep(0.3)
        try:
            el = driver.find_element(by=By.CSS_SELECTOR, value="div.semi-toast-content")
            if "发布成功" in el.text:
                my_log.log(el.text)
                return True, el.text
            else:
                my_log.log(el.text)
                return False, el.text
        except Exception as e:
            count += 1
            if count > 7:
                break
            pass
    return True, "发布成功！"


def upload(
    driver: webdriver.Chrome,
    folder_path=None,
    describe_title=None,
    describe=None,
    collection=None,
    publish_file_name="publish_file.txt",
):
    # 基本信息
    if folder_path is None:
        # 视频存放路径
        folder_path = f"G:{os.sep}360AutoRec{os.sep}SECVIDEO"
    if describe_title is None:
        # 视频描述
        describe_title = f"行车记录仪,记录生活"
    if describe is None:
        describe = f"#行车记录仪"

    # path = pathlib.Path(folder_path)

    # 视频地址获取
    # path_mp4 = "C:\\Users\\Administrator\\Videos\\黑神话：悟空 - VS石猿战死1.mp4"
    # 获取文件列表并按修改时间排序
    files = sorted(
        os.listdir(folder_path),
        key=lambda f: os.path.getmtime(os.path.join(folder_path, f)),
    )
    if os.path.exists(publish_file_name):
        with open(publish_file_name, "r", encoding="utf-8") as f:
            publish_file = f.read().split("\n")
            print(f"publish_file size={len(publish_file)}")
    else:
        publish_file = []

    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:5003")

    time.sleep(2)
    count = 0
    for i in range(len(files)):
        if i >= len(files):
            break
        file = files[i]
        print(f"{i} : {file}")
        if ".mp4" in str(file).lower():
            path_mp4 = os.path.join(folder_path, file)
        if path_mp4 != "":
            print("检查到视频路径：" + path_mp4)
        else:
            print("未检查到视频路径，程序终止！")
            exit()
        try:
            new_path = (
                path_mp4.replace("_out", "").replace(".mp4", "").replace(".MP4", "")
            )
            new_path = new_path[new_path.rfind(os.sep) + 1 :]
            my_log.log(f"new_path={new_path}")
            flag = False
            for publish in publish_file:
                if new_path in publish:
                    print(f"已发布过该视频，跳过！{path_mp4}")
                    flag = True
                    break
            if flag:
                continue
            else:
                my_log.log(f"{path_mp4} 该视频未發佈,开始发布视频！")
            tuple_result = publish_douyin(
                driver=driver,
                path_mp4=path_mp4,
                describe_title=describe_title,
                describe=describe,
                collection=collection,
            )
            my_log.log(f"发布结果：{tuple_result}")
            result, text = tuple_result
            if result:
                publish_file.append(path_mp4)
                my_log.log("发布成功！size=", len(publish_file))
                count += 1
                with open(publish_file_name, "a", encoding="utf-8") as f:
                    f.write(f"{path_mp4}\n")
            else:
                my_log.log(f"发布失败！{text}")
                break
            # if count>=70:
            #     my_log.log("发布视频数量已达到70个，程序终止！")
            #     break
        except Exception as e:
            print(e)
            traceback.print_exc()
            my_log.log("发布失败！")
        time.sleep(2)
    my_log.log(f"已发布{count}个视频")

    with open(publish_file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(publish_file))


def test():
    print("test")
    driver = setup_driver()
    print(type(driver))
    driver.get(
        "https://creator.douyin.com/creator-micro/content/manage?enter_from=publish"
    )
    # driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    title = driver.title
    print(title)
    driver.implicitly_wait(3)
    # text_box = driver.find_element(by=By.NAME, value="my-text")
    # submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    # text_box.send_keys("Selenium")
    # submit_button.click()

    input("Press Enter to close...")  # 保持窗口打开


def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("")
    # options.add_experimental_option("debuggerAddress", "localhost:5003")
    # options.add_argument("--remote-debugging-port=5003")  # 允许调试
    # options.add_argument("--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data")  # 设置用户数据目录
    options.add_argument("--user-data-dir=C:\\Py_selenium\\auto")  # 设置用户数据目录
    options.add_argument("--proxy-server=http://localhost:7890")  # 设置代理
    options.binary_location = (
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    )
    driver = webdriver.Chrome(
        options=options,
        service=ChromeService(executable_path="G:\\chromedriver.exe"),
    )
    return driver


def auto_upload(driver:webdriver.Chrome):
    # 查询数据库
    table_name = "video_material"
    db = video_download_db(table_name=table_name)
    # 读取json配置文件获取最后执行的page_num,page_size
    # 需要检查是否存在config.json文件
    if not os.path.exists("config.json"):
        # 如果不存在，则创建一个新的config.json文件
        config = {
            "page_num": 1,
            "page_size": 10,
        }
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
    with open("config.json", "r") as f:
        config = json.load(f)
        page_num = config.get("page_num", 1)
        page_size = config.get("page_size", 2)
    list_videos = query_data_base(page_num=page_num, page_size=page_size)
    for video in list_videos[2:]:
        video_id = video["video_id"]
        video_title: str = video["video_title"]
        download_url = video["download_url"]
        image_url = video["image_url"]
        video_number = video["video_number"]
        Video_platform = video["Video_platform"]
        time = video["time"]
        tips = video["tips"]
        # 下载好视频
        path = save_download_video(video_id, download_url)
        # 添加水印
        code = add_watermark(input=path, output=f"temp/video_{video_id}_out.mp4")
        os.remove(path)
        if code != 0:
            print("添加水印失败！")
            continue
        # 准备好文案
        describe_title, describe = handle_pub_txt(video_title)
        # 发布视频
        dir = os.path.dirname(os.path.abspath(path))
        
        upload(
            driver=driver,
            folder_path=dir,
            describe_title=describe_title,
            describe=describe,
            collection="人间值得",
            publish_file_name="kuaishou_to_dy_pub.txt",
        )
        # break
    # 清理temp文件夹
    for file in os.listdir("temp"):
        if file.endswith(".mp4") or file.endswith(".jpg"):
            os.remove(os.path.join("temp", file))
    # 保存最后执行的page_num,page_size 到json文件
    log(f"保存最后执行的page_num={page_num} page_size={page_size} 到config.json")
    with open("config.json", "w") as f:
        config["page_num"] = page_num+1  #for next page
        config["page_size"] = page_size
        json.dump(config, f, indent=4)
    pass


def handle_pub_txt(video_title: str):
    log(f"原始={video_title}")
    arry = video_title.replace("\\n", " ").split(" ")
    describe_title = ""
    topic = ""
    for string in arry:
        if string.startswith("@"):
            # 去除@人名
            continue
        if string.startswith("#"):
            topic += string + " "
            pass
        elif "..." in string:
            continue
        elif string.find("@") != -1:
            # 去除@人名
            name = string[string.find("@")+1 :]
            string = string[: string.find("@")]
            while True:
                if name.find("@") == -1:
                    break
                string += name[: name.find("@")]
                name = name[name.find("@")+1 :]
            describe_title += string
        else:
            describe_title +=string.strip()+" "
    if topic.strip() == "":
        topic = "#小姐姐 #可爱 #美女 #记录美好生活"
    if describe_title.strip() == "":
        describe_title = "小姐姐"
    describe = f"{describe_title}{topic}"

    log(f"处理后={describe}")

    return describe_title, describe


if __name__ == "__main__":

    # 开始执行视频发布
    # upload(
    #     folder_path="temp",
    #     # folder_path="E:\\360CARDVR\\REC",
    #     describe_title="行车记录仪,记录生活",
    #     describe="#行车记录仪",
    #     collection="行驶",
    # )
    def test_handle_text():
        db = video_download_db()
        data = db.fech_one_video(table_name=db.table_name, video_id="13")
        list = db.fech_videos_by_page(table_name=db.table_name, page_num=1, page_size=100)

        title = data["video_title"]
        handle_pub_txt(title)
        for i in list:
            # print(i)
            print(i["video_id"])
            handle_pub_txt(i["video_title"])
    driver = setup_driver()
    # 进入创作者页面，并上传视频
    driver.get("https://creator.douyin.com/creator-micro/home")
    
    auto_upload(driver)
    input("Press Enter to close...")  # 保持窗口打开

    # test()
