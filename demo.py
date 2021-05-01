import requests
from bs4 import BeautifulSoup
import pandas as pd
# import os

# 请求网页
url = "https://movie.douban.com/cinema/later/chengdu/"
# 伪装成浏览器的header
fake_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
}
response = requests.get(url, headers=fake_headers)

PATH = "/Users/emisonlu/Desktop/photo/"
# 解析网页
# 初始化BeautifulSoup方法：利用网页字符串自带的编码信息解析网页
soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
all_movies = soup.find('div', id="showing-soon")

result = {
    "name": [],
    "href": [],
    "date": [],
    "type": [],
    "area": [],
    "lovers": []
}
for each_movie in all_movies.find_all('div', class_="item"):
    all_a_tag = each_movie.find_all('a')
    all_li_tag = each_movie.find_all('li')
    movie_name = all_a_tag[1].text
    moive_href = all_a_tag[1]['href']
    movie_date = all_li_tag[0].text
    movie_type = all_li_tag[1].text
    movie_area = all_li_tag[2].text
    movie_lovers = all_li_tag[3].text
    movie_pic = each_movie.find('img')['src']
    # print(movie_pic)

    # 将图片名称提取出来，之所以要‘+1’是为了去掉‘/’,使其不会出现在图片名字中
    img_name = movie_pic[movie_pic.rfind('/')+1:]

    r = requests.get(movie_pic)

    with open(PATH+img_name, 'wb') as f:  # 创建并打开图片文件
        f.write(r.content)  # 将图片内容写入这个文件
        f.close()

    print('名字：{}，链接：{}，日期：{}，类型：{}，地区：{}， 关注者：{}'.format(
        movie_name, moive_href, movie_date, movie_type, movie_area, movie_lovers))

    result["name"].append(movie_name)
    result["href"].append(moive_href)
    result["date"].append(movie_date)
    result["type"].append(movie_type)
    result["area"].append(movie_area)
    result["lovers"].append(movie_lovers)

    df=pd.DataFrame(result)
    df.to_csv("doban.csv", encoding="utf-8_sig")
