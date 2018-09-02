import json, re, time, random, sys
from urllib.parse import urlencode
import jd_tools

# 优惠券列表 url
coupon_list_url = 'https://a.jd.com/indexAjax/getCouponListByCatalogId.html'

coupon_list_params = {
    #'catalogId': '15',
    'page': 1,
    'pageSize': 9,
    #'callback': 'jQuery507301',
    #'_': 1535724273490
 }



# 领取某一张优惠券的地址
get_a_coupon_url = 'https://a.jd.com/indexAjax/getCoupon.html'
get_a_coupon_params = {
    'type': 1,
}




def get_coupon(category):
    coupon_list_params = {
    #'catalogId': '15',
    'page': 1,
    'pageSize': 9,
    #'callback': 'jQuery507301',
    #'_': 1535724273490
    }

    request = jd_tools.request()
    request.headers.update({'Referer': f'https://a.jd.com/?cateId={category["categoryId"]}'})
    coupon_list_params['catalogId'] = category['categoryId']
    print('开始爬目录 -->', category['categoryName'])
    while True:
        coupon_list_params['_'] = jd_tools.get_timestamp()
        coupon_list_params['callback'] = jd_tools.get_query()
        res = request.get(coupon_list_url, params=coupon_list_params)
        #print(res.text)
        #print(res.text); exit()
        json_data = re.search(r'\{.*\}', res.text, re.S).group()
        #print(json_data); exit()
        couponList = json.loads(json_data).get('couponList')
        #pprint(couponList); exit()
        if not couponList:
            print(res.text)
            print(category)
            print('page: ', coupon_list_params['page'])
            break       
        for coupon in json.loads(json_data)['couponList']:
            store = coupon['limitStr']
            quota = coupon['quota']
            denomination = coupon["denomination"]
            farewall = f'满{quota}减{denomination}'
            print(store, '->', farewall)

            endDataTime = coupon['endTime']  # 优惠券过期时间
            rate = coupon['rate'] # 已经抢了和优惠券总数的百分比
            ruleKey = coupon['ruleKey']
            # 生成优惠卷链接； 访问时需要设置 referer 参数
            get_a_coupon_params['callback'] = jd_tools.get_query() # 取出来使用时再加上这2个参数
            get_a_coupon_params['_'] = jd_tools.get_timestamp()
            get_a_coupon_params['key'] = ruleKey
            coupon_url = get_a_coupon_url + '?' + urlencode(get_a_coupon_params)
            print(coupon_url)
            print('-' * 79)

            sql = 'insert into coupon (category, category_id, store, quota, denomination, expire, rate, ruleKey, url) values\
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            try:
                conn = jd_tools.get_db()
                with conn.cursor() as cursor:
                    cursor.execute(sql, (category['categoryName'], category['categoryId'], store, quota, denomination, endDataTime, rate, 
                    ruleKey, coupon_url ))
                    conn.commit()
            finally:
                conn.close()


        coupon_list_params['page'] += 1
        time.sleep(random.randint(2, 4))

 
# https://a.jd.com/indexAjax/getCoupon.html?callback=jQuery5001204&key=858f2f12edb377eaef3c481b6b5d3a22b03972cefb6df231678df2ed8f945632efbde386139c9c86de7b25e017ebc71f&type=1&_=1535766078195



    