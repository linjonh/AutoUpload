import json
import math
import time
import volcenginesdkcore
import volcenginesdktranslate20250301


class VolcanTranslate:
    def __init__(self):
        """
        初始化
        """
        # 创建一个配置对象
        # use default configuration
        # Configuration.set_default(configuration)
        self.configuration = volcenginesdkcore.Configuration()
        self.configuration.client_side_validation = True  # 客户端是否进行参数校验
        self.configuration.scheme = "http"  # https or http
        self.configuration.debug = False  # 是否开启调试
        self.configuration.logger_file = "sdk.log"
        with open("volcan_engine_translate.key", "r",encoding="utf-8") as f:
            s = f.read()
            str_dict: dict = json.loads(s)
            self.configuration.ak = str_dict["Access Key ID"]  # 用户的access key
            self.configuration.sk = str_dict["Secret Access Key"]  # 用户的secret key
            self.configuration.region = "cn-shanghai"  # 用户的region
        # 设置默认配置
        volcenginesdkcore.Configuration.set_default(self.configuration)    
        self.api_instnace = self.get_api_instance()

    def get_api_instance(self):
        """
        获取api实例
        :return:
        """
        # 创建一个API实例
        # use global default configuration
        api_instance = volcenginesdktranslate20250301.TRANSLATE20250301Api(
            volcenginesdkcore.ApiClient(self.configuration)
        )
        return api_instance
    def translate_text(self, source_language:str, target_language:str, text_list:list[str]):
        """
        翻译文本
        :param source_language: 源语言
        :param target_language: 目标语言
        :param text_list: 待翻译文本列表
        :return:
        """
        # 创建一个翻译请求对象
        translate_text_request = volcenginesdktranslate20250301.TranslateTextRequest(
            source_language=source_language,
            target_language=target_language,
            text_list=text_list,
        )
        try:
            # 复制代码运行示例，请自行打印API返回值。
            result = self.api_instnace.translate_text(body=translate_text_request)
            # print(result)
            return result
            
        except Exception as e:
            # 复制代码运行示例，请自行打印API错误信息。
            print("Exception when calling api: %s\n" % e)
            return None
    
if __name__ == "__main__":
    volcan_translate = VolcanTranslate()
    
    def translate_text(data:str):
        """
        测试翻译
        :return:
        """
        # 测试翻译
        source_language = "en"
        target_language = "zh"
        text_list = [data]
        result = volcan_translate.translate_text(source_language, target_language, text_list)
        if result is not None:
            print(type(result))
        # 处理返回结果
        if result is None:
            print("没有返回结果")
            return None
        
        
    i18n = "i18n/en/docusaurus-plugin-content-docs/current"
    with open(f"../rhino-doc/{i18n}/docs/scopes_and_contexts.md", "r", encoding="utf-8") as f:
        data = f.read()
        print("正在翻译文件：length:", len(data))
        count=math.ceil(len(data)/ 5000.0)
        for i in range(count):
            sub_data = data[i * 5000: (i + 1) * 5000]
            print(f"正在翻译第{i + 1}段数据 {len(sub_data)}")
            if len(sub_data) == 0:
                continue
            translate_text(sub_data)
            # time.sleep(1)
        print("翻译完成")
        