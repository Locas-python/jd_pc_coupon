import requests
import random
from datetime import datetime
import pymysql

# 将浏览器中复制的的 cookies 字符串，转为字典
make_cookies = lambda cookies:dict([c.split('=') for c in cookies.split('; ')])

# 每次请求中需要携带的 callback 的值（模拟京东 js） 
# -- 它是随机生成的，所以可以直接复制浏览器的结果，但是这样更为真实
def get_query(): return "jQuery" + str(int(random.random() * 1e7))

# 每次请求中需要携带的 _ 的值（模拟京东 js） -- 时间截
def get_timestamp(): return int(datetime.timestamp(datetime.now()) * 1000)




headers = {
    'Host': 'a.jd.com',
    'Referer': 'http://a.jd.com/',
    'User-Agent': 'Mozilla/5.0User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'DNT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    }



def request(cookies = {}):
    s = requests.Session()
    s.headers.update(headers)
   # s.cookies.update(cookies)
    return s


# mysql
# 现需要设置 mysql 用户名/密码
host = 'localhost'
user = ''
password = ''
database = 'jd'

def get_db():
    connect = pymysql.connect(host, user, password, database)
    return connect