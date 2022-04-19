import datetime
import time

import tushare as ts
from dateutil.relativedelta import relativedelta

pro = ts.pro_api("4e8cf3debc133f549e0bb20a0f68baeb267947b2d099b4d17c94f923")

"""
日线行情
"""


def get_daily(ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = pro.daily(ts_code=ts_code, trade_date=trade_date)
            else:
                df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df


"""
周线行情
"""


def get_weekly(ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = pro.weekly(ts_code=ts_code, trade_date=trade_date)
            else:
                df = pro.weekly(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df


"""
获取上一个交易日日期，以字符串的形式返回
ex:20210101
"""


def get_previous_trade_cal(end_date=''):
    if int(end_date) <= 20210101:
        print("仅支持20210101后的日期")
        exit(0)

    if int(end_date) > int(time.strftime('%Y%m%d', time.localtime(time.time()))):
        print("日期不能超过今天")
        exit(0)

    df_tc = pro.trade_cal(start_date='20210101', end_date=end_date, is_open=1)
    # 获取当前的日期和上一个交易日
    trade_date_list = df_tc[-2:]['cal_date'].values
    # if trade_date_list[1] != end_date:
    #     print("当前日期不是交易日")
    #     exit(0)
    return trade_date_list[0]


"""
获取交易日期df
@:param duration 交易天数
"""


def get_trade_cal(month_duration=1):
    d = datetime.date.today() - relativedelta(months=month_duration + 2)
    sd = int(d.strftime('%Y%m%d'))
    df_tc = pro.trade_cal(start_date=str(sd), end_date=int(time.strftime('%Y%m%d', time.localtime(time.time()))),
                          is_open=1)
    # 从最后开始截取
    # 返回从当前日期降序的交易日期
    res = list(df_tc[-month_duration * 30:]['cal_date'].values)
    res.reverse()
    return res


"""
获取交易日期列表(降序)
ex['20220314','20220311','20220310]
"""


def get_trade_date_list(month_duration=1):
    x_data = get_trade_cal(month_duration)
    x_data.reverse()
    return x_data
