import json
import os
import time
import requests

from utils import timeCost

data = """---
title: Community
nav_order: 3
---
# Community
---
Have a question that you can't find answer to in the [Rhino faq](./docs/faq.md)? Here are some additional resources for help:

## Mailing List

Rhino discussions happen on the [mozilla-rhino](https://groups.google.com/group/mozilla-rhino) group on Google Groups.

There is a much older group, [mozilla.dev.tech.js-engine.rhino](news://news.mozilla.org/mozilla.dev.tech.js-engine.rhino), that is no longer actively used. Please use the new group instead, but the old one may be of historical interest.

The [mozilla.dev.tech.js-engine](news://news.mozilla.org/mozilla.dev.tech.js-engine) newsgroup answers questions about the C implementation of JavaScript, and was also used for answering questions about Rhino until September 27, 2007. To view archived messages _earlier than_ September 27, 2007, try [Google group for the earlier newsgroup](https://groups.google.com/group/mozilla.dev.tech.js-engine/topics).

## Bug System

The best way to enter Rhino bugs to enter an [issue in GitHub.](https://github.com/mozilla/rhino/issues)

If you have the inclination to fix it, you are also encouraged to fix it and submit a [pull request](https://github.com/mozilla/rhino/pulls).

Many older Rhino issues were logged in [Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Rhino). There may be some bugs there of historical interest. Note that Rhino has its own product category.
"""

data = """
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
"""


def stream_api(data_str: str = data,callback=None):
    """使用流式API"""
    # 1. 创建一个请求，设置请求方法、URL和请求体
    # 2. 使用requests库发送请求，并获取响应流
    # 3. 遍历响应流，逐块读取数据并处理
    # 4. 如果接收到的块数据为空，则退出循环

    # 发送POST请求，设置流式传输
    # 注意：这里的URL需要替换为实际的API地址
    response_stream = requests.request(
        method="POST",
        url="http://localhost:11434/api/generate",
        data=None,
        json={
            "model": "deepseek-r1:8B",
            "prompt": f"帮我翻译一下markdow文件成中文,注意front matter字段名称不要翻译：{data_str}",
            "stream": True,
        },
        stream=True,
    ).iter_content(chunk_size=None)
    for chunk in response_stream:
        if chunk:
            response = chunk.decode("utf-8")
            dict_str: dict = json.loads(response)
            if dict_str.get("done") == True:
                break
            # time.sleep(0.1)
            print(dict_str.get("response"), end="", flush=True)
            if callback:
                callback(dict_str.get("response"))


@timeCost
def sync_api(data_str: str = data):
    """使用同步API"""
    # 1. 创建一个请求，设置请求方法、URL和请求体
    # 2. 使用requests库发送请求，并获取响应
    # 3. 处理响应数据

    # 发送POST请求，获取响应
    response = requests.request(
        method="POST",
        url="http://localhost:11434/api/generate",
        data=None,
        json={
            "model": "deepseek-r1:8B",
            "prompt": f"帮我翻译一下markdow文件成中文,注意front matter字段名称不要翻译：{data_str}",
            "stream": False,
        },
    )
    dict_str: dict = json.loads(response.text)
    result: str = dict_str.get("response")
    index = result.find("</think>") + len("</think>")
    string: str = result[index:]
    response = string.strip()
    print(response)
    # with open("test.md", "w", encoding="utf-8") as f:
    #     f.write(string.strip())
    return response


if __name__ == "__main__":
    i18n = "i18n/en/docusaurus-plugin-content-docs/current"
    for root, dirs, files in os.walk(f"../rhino-doc/{i18n}/"):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                print(f"正在翻译文件：{path}")
                with open(path, "r", encoding="utf-8") as f:
                    data = f.read()
                response = sync_api(data)

                with open(path.replace(i18n, "docs"), "w", encoding="utf-8") as f:
                    f.write(response)
            # break
        # break
