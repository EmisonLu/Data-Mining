import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import queue
from time import sleep
import random

# the path of the crawled image stored locally
PATH = "/Users/emisonlu/Desktop/photo/"

# queue for storing second-level access URLs
q = queue.Queue()

# content crawled on the first level
result_layer1 = {
    "name": [],
    "director": [],
    "year": [],
    "countries": [],
    "types": [],
    "rating_num": [],
    "evaluator": [],
    "evaluation": []
}

# content crawled on the second level
result_layer2 = {
    "name": [],
    "comment": [],
}

# the first layer of data crawling
def spider_layer1(cookies):

    header = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }

    # a total of 10 pages, paged crawling
    pages = ["0", "25", "50", "75", "100", "125", "150", "175", "200", "225"]
    for page in pages:
        sleep(0.1)
        url = "https://movie.douban.com/top250?start=" + page + "&filter="

        response = requests.get(url, cookies=cookies, headers=header)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

        # get the first page list information
        all_movies = soup.find('div', id="content")
        for each_movie in all_movies.find_all('div', class_="item"):
            all_span_tag = each_movie.find_all('span')
            all_p_tag = each_movie.find_all('p')
            all_a_tag = each_movie.find_all('a')

            # store the URL of each movie in the first layer into the queue for the second layer to crawl
            url_deep = all_a_tag[0]['href']
            q.put(url_deep)

            # get the name, rating_num, evaluator, evaluation of each movie
            name = all_span_tag[0].text
            rating_num = all_span_tag[-4].text
            evaluator = all_span_tag[-2].text
            evaluation = all_span_tag[-1].text

            # get the director, year, countries, types of each movie
            str_list = all_p_tag[0].text.split()
            director, year, countries, types = handle_str(str_list)
            
            # store the above information in a dictionary
            result_layer1["name"].append(name)
            result_layer1["director"].append(director)
            result_layer1["year"].append(year)
            result_layer1["countries"].append(countries)
            result_layer1["types"].append(types)
            result_layer1["rating_num"].append(rating_num)
            result_layer1["evaluator"].append(evaluator)
            result_layer1["evaluation"].append(evaluation)

            # get the cover of every movie
            movie_pic = each_movie.find('img')['src']
            img_name = movie_pic[movie_pic.rfind('/')+1:]
            r = requests.get(movie_pic)

            # store the picture locally
            with open(PATH+img_name, 'wb') as f:
                f.write(r.content)
                f.close()

    # store the information crawled on the first layer in csv format locally
    df = pd.DataFrame(result_layer1)
    df.to_csv("layer1.csv", encoding="utf-8_sig")

# process the string to get the director, year, countries, types of each movie
def handle_str(str_list):
    # get the director
    director = str_list[1]

    # get the types
    i = len(str_list)-1
    j = i
    while True:
        if str_list[i] == '/':
            break
        i = i-1
    string = str_list[i+1]
    for s in range(i+2, j+1):
        string = string + ' ' + str_list[s]
    types = string

    # get the countries
    j = i
    while True:
        i = i-1
        if str_list[i] == '/':
            break
    string = str_list[i+1]
    for s in range(i+2, j):
        string = string + ' ' + str_list[s]
    countries = string

    # get the year
    year = str_list[i-1]

    return director, year, countries, types

# the second layer of data crawling
def spider_layer2(cookies):
    header = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }

    # remove the URL from the queue and crawl until the queue is empty
    while q.empty() == False:
        sleep(0.1)
        url = q.get()

        response = requests.get(url, cookies=cookies, headers=header)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

        contents = soup.find('div', id="content")
        # get the name of the movie
        name = contents.find('h1').find_all('span')[0].text.split()[0]
        print(name)

        # get short comments of the movie
        comments = contents.find('div', id="hot-comments")
        for each_comment in comments.find_all('div', class_="comment-item"):
            all_span_tag = each_comment.find_all('span')
            comment = all_span_tag[-1].text
            print(comment)
            # store the above information in a dictionary
            result_layer2["name"].append(name)
            result_layer2["comment"].append(comment)

        result_layer2["name"].append("")
        result_layer2["comment"].append("")

    # store the information crawled on the first layer in csv format locally
    df = pd.DataFrame(result_layer2)
    df.to_csv("layer2.csv", encoding="utf-8_sig")

# simulate user login
def login(username, password):
    url = 'https://accounts.douban.com/j/mobile/login/basic'
    header = {
        'user-agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
        'Origin': 'https://accounts.douban.com',
        'content-Type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'connection': 'keep-alive',
        'Host': 'accounts.douban.com'
    }

    # parameters required for login
    data = {
        'ck': '',
        'name': '',
        'password': '',
        'remember': 'false',
        'ticket': ''
    }
    data['name'] = username
    data['password'] = password
    data = urllib.parse.urlencode(data)

    # send post package to simulate login
    req = requests.post(url, headers=header, data=data, verify=False)
    cookies = requests.utils.dict_from_cookiejar(req.cookies)
    return cookies


if __name__ == '__main__':
    # get user account and password
    username = input('输入账号：')
    password = input('输入密码：')
    cookies = login(username, password)

    # the first level of crawling
    spider_layer1(cookies)

    # the second level of crawling
    spider_layer2(cookies)
