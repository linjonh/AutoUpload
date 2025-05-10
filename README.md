- 抖音 web 端自动上传视频脚本。
- 基于 selenium 框架，python 编写脚本。
- 需要 chromeDriver 驱动程序，可以在 chromeLab 的 test 官网下载。


# 视频素材下载工具[download_video_materal.py](download_video_materal.py)


# flask网页服务启动

```bash
flask --app  main_flask.py run --debug  
```
`--debug`选项是为了可以热加载

# 获取ip
地址：http://ip-api.com/json
```json
{
  "status": "success",
  "country": "Taiwan",
  "countryCode": "TW",
  "region": "TPE",
  "regionName": "Taipei City",
  "city": "Taipei",
  "zip": "",
  "lat": 25.053,
  "lon": 121.5259,
  "timezone": "Asia/Taipei",
  "isp": "Chunghwa Telecom Co., Ltd.",
  "org": "Chunghwa Telecom Co. Ltd.",
  "as": "AS3462 Data Communication Business Group",
  "query": "111.243.78.91"
}
```