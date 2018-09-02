import json, re, time, random, os
import jd_tools
from get_coupon import get_coupon
from queue import Queue
from threading import Thread
from multiprocessing import pool
# PC端 京东优惠券

# 优惠券目录
## 参数 callback
## 参数 _
coupon_category_url = 'https://a.jd.com/indexAjax/getCatalogList.html'



# 获取优惠券目录
coupon_category_params = {
    'callback': jd_tools.get_query(),
    '_': jd_tools.get_timestamp(),
}

request = jd_tools.request()

res = request.get(coupon_category_url, params=coupon_category_params)
json_data  = re.search(r'\{.*\}', res.text, re.S).group()
coupon_category = json.loads(json_data)['catalogList']




for category in coupon_category:
    get_coupon(category)
    time.sleep(3)

