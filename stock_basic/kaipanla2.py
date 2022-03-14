import time

import requests
from dateutil import parser

headers_history = {
    'Host': 'apphis.longhuvip.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'Accept': '*/*',
    'User-Agent': 'lhb/5.4.0 (com.kaipanla.www; build:0; iOS 15.3.1) Alamofire/5.4.0',
    'Accept-Language': 'zh-Hans-CN;q=1.0, en-CN;q=0.9',
}

headers_today = {
    'Host': 'apphq.longhuvip.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'Accept': '*/*',
    'User-Agent': 'lhb/5.4.0 (com.kaipanla.www; build:0; iOS 15.3.1) Alamofire/5.4.0',
    'Accept-Language': 'zh-Hans-CN;q=1.0, en-CN;q=0.9',
}


def get_zhaban_red_count(trade_date='', page_size=200):
    print(f'正在获取炸板红盘股票数量,date={trade_date}')
    date = str(parser.parse(trade_date).strftime('%Y-%m-%d'))
    data = 'Date=' + date + '&Index=0&IsZZ=0&Order=1&PhoneOSNew=2&PlateID=801903&Token=0&Type=6&UserID=0&VerSion=5.2.1.0&a=ZhiShuStockList_W8&apiv=w28&c=ZhiShuRanking&old=1&st=' + str(
        page_size)
    headers = headers_today if int(trade_date) == int(
        time.strftime('%Y%m%d', time.localtime(time.time()))) else headers_history
    host = headers['Host']
    response = requests.post(f'https://{host}/w1/api/index.php', headers=headers, data=data)
    try:
        j = response.json()
        res = j['list']
        ps = j['Count']
        if ps <= page_size:
            s = sum(obj[6] > 0 for obj in res)
            print(f'{trade_date}炸板第二天红盘数量={s}')
            return s
        else:
            print(f'ps={ps}，重新获取...')
            get_zhaban_red_count(trade_date, ps)
    except Exception:
        print(f'获取炸板列表异常，response={response.content}')
        return 0
