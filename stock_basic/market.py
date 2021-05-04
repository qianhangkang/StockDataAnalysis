import time

import pandas as pd
import requests

KLINE_URL = "https://stock.xueqiu.com/v5/stock/chart/kline.json"


def get_snowball_cookie():
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://xueqiu.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    res = requests.get('https://xueqiu.com/', headers=headers)
    cookie = res.cookies.get('xq_a_token')
    if not cookie:
        print(res.cookies)
        raise Exception('获取雪球cookie异常')
    return cookie


def get_snowball_headers():
    cookie = get_snowball_cookie()
    headers = {
        'authority': 'stock.xueqiu.com',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'origin': 'https://xueqiu.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://xueqiu.com/S/SH000001',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'xq_a_token=' + cookie,
    }
    return headers


def get_market_volume(symbol, count):
    params = {
        "symbol": symbol,
        "begin": int(round(time.time() * 1000)),
        "period": "day",
        "type": "before",
        "count": -count
    }
    response = requests.get(KLINE_URL, params=params, headers=get_snowball_headers())
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        raise Exception('获取json失败')


def convert_json_to_df(json):
    df_data_item = pd.DataFrame(json['data']['item'])
    df = pd.DataFrame()
    df['date'] = df_data_item[0]
    # df['date'] = pd.to_datetime(df_data_item[0], unit='ms').dt.strftime('%Y-%m-%d')
    df['volume'] = df_data_item[9]
    return df


def get_two_cities_volume(count):
    """
    获取两市成交额
    :return: DataFrame
    """
    json_sh = get_market_volume('SH000001', count)
    json_sz = get_market_volume('SZ399001', count)
    df_sh = convert_json_to_df(json_sh)
    df_sz = convert_json_to_df(json_sz)
    df_merge = pd.merge(df_sh, df_sz, on='date', how='inner')
    df = pd.DataFrame()
    # 日期为时间戳
    df['date'] = df_merge['date']
    df['上交所成交额'] = df_merge['volume_x']
    df['深交所成交额'] = df_merge['volume_y']
    df['两市成交额'] = df_merge['volume_x'] + df_merge['volume_y']
    return df


def kline(symbol, count):
    params = (
        ('symbol', symbol),
        ('begin', int(round(time.time() * 1000))),
        ('period', 'day'),
        ('type', 'before'),
        ('count', -count),
        ('indicator', 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'),
    )

    response = requests.get('https://stock.xueqiu.com/v5/stock/chart/kline.json', headers=get_snowball_headers(),
                            params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        raise Exception('获取json失败')
