import json
import volcenginesdkcore
import volcenginesdktranslate20250301


configuration = volcenginesdkcore.Configuration()
configuration.client_side_validation = True  # 客户端是否进行参数校验
configuration.scheme = "http"  # https or http
configuration.debug = False  # 是否开启调试
configuration.logger_file = "sdk.log"
with open("volcan_engine_translate.key", "r") as f:
    s = f.read()
    str_dict: dict = json.loads(s)
configuration.ak = str_dict["Access Key ID"]  # 用户的access key
configuration.sk = "Secret Access Key"  # 用户的secret key
configuration.region = "cn-shanghai"  # 用户的region

volcenginesdkcore.Configuration.set_default(configuration)


# use global default configuration
api_instance = volcenginesdktranslate20250301.TRANSLATE20250301Api(
    volcenginesdkcore.ApiClient(configuration)
)
translate_text_request = volcenginesdktranslate20250301.TranslateTextRequest(
    source_language="en",
    target_language="zh",
    text_list=[
        "Hello World!",
        """
---
permalink: /404.html
---
```js
<script>
  /* Redirect links to old, self-hosted JavaDocs to javadoc.io, see https://github.com/mozilla/rhino/pull/1126 */
  const oldPathStart = '/rhino/javadoc/';
  const newJavaDocUrl = 'javadoc.io/doc/org.mozilla/rhino/latest/';
  const loc = window.location;

  if (loc.pathname.startsWith(oldPathStart)) \{
    let origin=loc.host + oldPathStart;
    console.log(origin)
    let url=loc.href.replace(origin, newJavaDocUrl);
    window.location.replace(url);
  }
</script>
```
Oh no! Whatever you were looking for isn't there, sorry about that...
""",
    ],
)
try:
    # 复制代码运行示例，请自行打印API返回值。
    result = api_instance.translate_text(body=translate_text_request)
    print(result)
except Exception as e:
    # 复制代码运行示例，请自行打印API错误信息。
    print("Exception when calling api: %s\n" % e)
    pass
