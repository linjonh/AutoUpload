import json
import os
import selenium
from selenium import webdriver
import pathlib
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeService

import my_log


def input_brife(driver, describe=""):
    print("输入视频简单描述。。")
    # tag = driver.find_element(
    #     by=By.CSS_SELECTOR, value="div.outerdocbody.editor-kit-outer-container"
    # )
    innerTag = driver.find_element(
        by=By.CSS_SELECTOR,
        value="div.zone-container.editor-kit-container.editor.editor-comp-publish.notranslate.chrome.window.chrome88",
    )
    data = describe + " #上热门 #dou上热门 #我要上热门"
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
def publish_douyin(driver:webdriver.Chrome,path_mp4,describe_title,describe,collection=None):
        """
        作用：发布抖音视频
        """
        driver.find_element(by=By.XPATH, value='//*[text()="发布视频"]').click()
        time.sleep(1)
        driver.find_element(by=By.XPATH, value='//input[@type="file"]').send_keys(
            path_mp4
        )

        # 等待视频上传完成
        print("视频还在上传中···")
        time.sleep(80)
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
        
        #封面选择
        # driver.find_element(
        #     by=By.CSS_SELECTOR, value="div.recommendCover-vWWsHB"
        # ).click()
        # while True:
        #     time.sleep(5)
        #     try:
        #         driver.find_element(
        #             by=By.CSS_SELECTOR,
        #             value="div.semi-modal-confirm button.semi-button.semi-button-primary",
        #         ).click()
        #         print("封面确定完成！")
        #         break
        #     except Exception as e:
        #         print("封面确定失败！")
        time.sleep(1)
        # 输入视频描述
        print("输入视频描述title···")
        data = describe + " #上热门 #dou上热门 #我要上热门"

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
            if collection==None:
                driver.find_elements(
                    by=By.CSS_SELECTOR, value="div.semi-select-option.collection-option"
                )[0].click()
            else:
                els=driver.find_elements(
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

        # 人工进行检查并发布
        # time.sleep(3)
        # # 点击发布
        print("点击发布")
        driver.find_element(by=By.XPATH, value='//button[text()="发布"]').click()
        return True

def upload(folder_path=None, describe_title=None, describe=None,collection=None):
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
    if os.path.exists("publish_file.txt"):
        with open("publish_file.txt", "r") as f:
            publish_file = f.read().split("\n")
            print(f"publish_file size={len(publish_file)}")
    else:
        publish_file = []

    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:5003")
    driver = setup_driver()
    # 进入创作者页面，并上传视频
    driver.get("https://creator.douyin.com/creator-micro/home")
    time.sleep(2)
    count=0
    for i in range(len(files)):
        if i >= len(files):
            break
        file=files[i]
        print(f"{i} : {file}")
        if ".mp4" in str(file).lower():
            path_mp4 = os.path.join(folder_path, file)
        if path_mp4 != "":
            print("检查到视频路径：" + path_mp4)
        else:
            print("未检查到视频路径，程序终止！")
            exit()
        try:
            new_path = path_mp4.replace("_out","").replace(".mp4","").replace(".MP4","")
            new_path=new_path[new_path.rfind(os.sep)+1:]
            my_log.log(f"new_path={new_path}")
            flag = False
            for publish in publish_file:
                if new_path in publish:
                    print(f"已发布过该视频，跳过！{path_mp4}")
                    flag=True
                    break
            if flag:
                continue
            else:
                print(f"{path_mp4} 该视频未發佈,开始发布视频！")
            if publish_douyin(driver=driver, path_mp4=path_mp4, describe_title=describe_title, describe=describe,collection=collection):
                publish_file.append(path_mp4)
                print("发布成功！size=", len(publish_file))
                count+=1
                with open("publish_file.txt", "a") as f:
                    f.write(f"{path_mp4}\n")
            if count>=70:
                my_log.log("发布视频数量已达到70个，程序终止！")
                break
        except Exception as e:
            print(e)
            print("发布失败！")
        time.sleep(2)
    with open("publish_file.txt", "w") as f:
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
        service=ChromeService(
            executable_path="G:\\chromedriver.exe"
        ),
    )
    return driver


if __name__ == "__main__":
    # 开始执行视频发布
    # upload(folder_path="G:\\360AutoRec\\EMERGENCY", describe_title="行车记录仪,记录生活", describe="#行车记录仪",collection="紧急")
    upload(folder_path="G:\\360AutoRec\\REC", describe_title="行车记录仪,记录生活", describe="#行车记录仪",collection="行驶")
    upload(folder_path="G:\\360AutoRec\\rec_有电话", describe_title="行车记录仪,记录生活", describe="#行车记录仪",collection="Self")
    input("Press Enter to close...")  # 保持窗口打开

    # test()
