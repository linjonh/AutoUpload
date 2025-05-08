import json
from urllib.parse import unquote


class MovieInfo:
    def __init__(self):
        self.type = ""  # 电影类型
        self.name = ""  # 电影名
        self.author = ""  # 作者
        self.director = ""  # 导演
        self.scenarist = ""  # 编剧
        self.actors = ""  # 演员
        self.main_actor = ""  # 主演
        self.brief = ""  # 简介
        self.tags = []  # 标签
        self.url = []  # 播放地址 {1：url,2:url}
        self.cover_image = ""  # 封面图片
        self.landscape_img = ""  # 横屏图片
        self.episode_count = 0  # 集数
        self.duration = 0  # 时长

        self.year = ""  # 年份
        self.area = ""  # 地区
        self.language = ""  # 语言
        self.sort_type = ""  # 排序方式
        self.update_time = ""  # 更新时间
        self.showtime = ""  # 上映时间
        pass


if __name__ == "__main__":

    info = MovieInfo()
    json = json.dumps(info.__dict__, indent=4, ensure_ascii=False)
    print(json)
    
    url="%68%74%74%70%73%3A%2F%2F%76%31%30%2E%64%69%6F%75%73%2E%63%63%2F%32%30%32%34%30%38%30%39%2F%66%73%5A%66%59%4A%50%51%2F%69%6E%64%65%78%2E%6D%33%75%38%26%64%6F%6E%67%6D%61%6E%26%6E%65%78%74%3D%68%74%74%70%3A%2F%2F%77%77%77%2E%64%61%6E%64%61%6E%7A%61%6E%35%2E%63%6F%6D%2F%70%6C%61%79%2F%31%33%37%39%36%37%2D%31%2D%33%2F"
    url_next="%68%74%74%70%73%3A%2F%2F%76%31%30%2E%64%69%6F%75%73%2E%63%63%2F%32%30%32%34%30%38%31%30%2F%5A%34%68%51%6D%35%4A%34%2F%69%6E%64%65%78%2E%6D%33%75%38"
    print(unquote(url))
    print(unquote(url_next))
