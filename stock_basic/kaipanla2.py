import requests
from dateutil import parser

headers = {
    'Host': 'apphis.longhuvip.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'Accept': '*/*',
    'User-Agent': 'lhb/5.2.10 (com.kaipanla.www; build:0; iOS 15.3.1) Alamofire/5.2.10',
    'Accept-Language': 'zh-Hans-CN;q=1.0, en-CN;q=0.9',
}


def get_zhaban_red_count(trade_date=''):
    print(f'正在获取炸板红盘股票数量,date={trade_date}')
    date = str(parser.parse(trade_date).strftime('%Y-%m-%d'))
    data = 'Date=' + date + '&Index=0&IsZZ=0&Order=1&PhoneOSNew=2&PlateID=801903&Token=0&Type=6&UserID=0&VerSion=5.2.1.0&a=ZhiShuStockList_W8&apiv=w28&c=ZhiShuRanking&old=1&st=100'
    response = requests.post('https://apphis.longhuvip.com/w1/api/index.php', headers=headers, data=data)
    try:
        j = response.json()
        res = j['list']
        s = sum(obj[6] > 0 for obj in res)
        return s
    except Exception:
        return 0
