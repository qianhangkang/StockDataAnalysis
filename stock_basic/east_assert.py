import time

import pandas as pd
import requests

cookies = {
    'em_hq_fls': 'old',
    'qgqp_b_id': '2ccf9bd36f9ed3d52cb8a42d438ba85e',
    'em-quote-version': 'topspeed',
    '_qddaz': 'QD.yn2ykp.d505fb.kuqb9b6f',
    'st_si': '52915734976991',
    'cowCookie': 'true',
    'intellpositionL': '588px',
    'intellpositionT': '455px',
    'HAList': 'ty-90-BK0815-%u6628%u65E5%u6DA8%u505C%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-600309-%u4E07%u534E%u5316%u5B66%2Ca-sz-300146-%u6C64%u81E3%u500D%u5065%2Ca-sh-601990-%u5357%u4EAC%u8BC1%u5238%2Ca-sh-601279-%u82F1%u5229%u6C7D%u8F66%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570',
    'st_asi': 'delete',
    'st_pvi': '32992069072691',
    'st_sp': '2020-01-30%2021%3A05%3A24',
    'st_inirUrl': 'https%3A%2F%2Fwww.google.com%2F',
    'st_sn': '178',
    'st_psi': '20211226110657960-113200304537-4702778063',
}

headers = {
    'Proxy-Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://quote.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

"""
获取涨跌停股票dataframe
不对交易日期做校验，若传入非交易日期将会获取到空白列表
@:param zt 1涨停（默认），0跌停
"""


def get_top(trade_date=''):
    print(f'正在获取交易日期为{trade_date}的涨跌股票列表...')
    # 默认拿涨停的，跌停的获取不了数据，要用到时再debug
    zt = 1
    s = 'ZT' if zt > 0 else 'DT'
    sort = 'fbt:asc' if zt > 0 else 'fund%3A+asc'
    url = f'http://push2ex.eastmoney.com/getTopic{s}Pool'
    params = (
        ('ut', '7eea3edcaed734bea9cbfc24409ed989'),
        ('dpt', 'wz.ztzt'),
        ('Pageindex', '0'),
        ('pagesize', '10'),
        ('sort', sort),
        ('date', str(trade_date)),
    )
    pool = {}
    try:
        response = requests.get(url, headers=headers, params=params,
                                cookies=cookies, verify=False)
        if response.status_code != 200:
            print("获取东方财富涨跌停列表失败，errorCode=" + response.status_code)
            return None
        json = response.json()['data']
        if json is None:
            print("当前日期=" + trade_date + "不存在涨跌停股票")
            return None
        total_count = json['tc']
        pool = json['pool']
        pool_count = len(pool)
        # 该交易日涨停数量大于当前获取到的数量，重新修改pagesize获取全部
        if pool_count < total_count:
            params = (
                ('ut', '7eea3edcaed734bea9cbfc24409ed989'),
                ('dpt', 'wz.ztzt'),
                ('Pageindex', '0'),
                ('pagesize', total_count),
                ('sort', 'fbt:asc'),
                ('date', str(trade_date)),
            )
            time.sleep(1)
            response = requests.get('http://push2ex.eastmoney.com/getTopicZTPool', headers=headers, params=params,
                                    cookies=cookies, verify=False)
            if response.status_code != 200:
                print("获取东方财富涨跌停列表失败...errorCode=" + response.status_code)
                return None
            json = response.json()['data']
            pool = json['pool']
    except Exception:
        print("error")
        print(Exception)

    # 格式化pool
    # 代码、名称、股价(20110->20.11)、涨幅(10.010940551757812->10.01)
    return pd.DataFrame(pool, columns=['c', 'n', 'p', 'zdp'])


"""
获取涨跌停股票数量
@:param zt 1涨停（默认），0跌停
"""


def get_count(trade_date='', zt=1):
    # http://push2ex.eastmoney.com/getTopicDTPool?&sort=fund%3Aasc&date=20220310&_=1646899011773
    print(f'正在获取{trade_date}涨跌停数量...')
    s = 'ZT' if zt > 0 else 'DT'
    sort = 'fbt:asc' if zt > 0 else 'fund:asc'
    url = f'http://push2ex.eastmoney.com/getTopic{s}Pool'
    params = (
        ('ut', '7eea3edcaed734bea9cbfc24409ed989'),
        ('dpt', 'wz.ztzt'),
        ('Pageindex', '0'),
        ('pagesize', '20'),
        ('sort', sort),
        ('date', str(trade_date)),
    )
    try:
        response = requests.get(url, headers=headers, params=params,
                                cookies=cookies, verify=False)
        if response.status_code != 200:
            print("获取东方财富涨跌停列表失败，errorCode=" + response.status_code)
            return None

        json = response.json()
        data = json['data']
        if data is None:
            print("data is None")
            print(response.content)
            return 0

        c = data['tc']
        print(f'{s}的数量为{c}')
        return c

    except Exception:
        print("error")
        return None


"""
获取炸板股数量
"""


def get_zhaban_count(trade_date=''):
    print(f'正在获取日期={trade_date}的炸板股数量...')
    params = (
        ('ut', '7eea3edcaed734bea9cbfc24409ed989'),
        ('dpt', 'wz.ztzt'),
        ('Pageindex', '0'),
        ('pagesize', '20'),
        ('sort', 'fbt:asc'),
        ('date', str(trade_date)),
        ('_', '1647250510597'),
    )
    response = requests.get('http://push2ex.eastmoney.com/getTopicZBPool', headers=headers, params=params,
                            cookies=cookies, verify=False)
    try:
        j = response.json()
        d = j['data']
        c = d['tc']
        print(f'炸板股数量={c}')
        return c
    except Exception:
        print(f'获取失败，content={response.content}')
        return 0
