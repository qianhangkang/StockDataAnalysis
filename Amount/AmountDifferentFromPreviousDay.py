import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import time

pro = ts.pro_api("4e8cf3debc133f549e0bb20a0f68baeb267947b2d099b4d17c94f923")
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


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
    if trade_date_list[1] != end_date:
        print("当前日期不是交易日")
        exit(0)
    return trade_date_list[0]


def pretty_print_all(stock_merge_data_frame):
    sorted_df_all = stock_merge_data_frame.sort_values(by='amount_difference_absolute', ascending=False)
    sorted_df_inflow = sorted_df_all[sorted_df_all.amount_difference > 0]
    sorted_df_outflow = sorted_df_all[sorted_df_all.amount_difference < 0]
    print("===" * 5 + "根据净变动成交量降序" + "===" * 5)
    print(format_data_frame(sorted_df_all))
    # format_data_frame(sorted_df_all).plot()
    # plt.show()
    print("===" * 5 + "根据净流入成交量降序" + "===" * 5)
    print(format_data_frame(sorted_df_inflow))
    print("===" * 5 + "根据净流出成交量降序" + "===" * 5)
    print(format_data_frame(sorted_df_outflow))


def format_data_frame(data_frame):
    data_frame_head = data_frame.head(20)
    df1 = pd.DataFrame()
    df1['股票代码'] = data_frame_head['ts_code']
    df1['股票名称'] = data_frame_head['name']
    df1['上一个交易日成交量（千元）'] = data_frame_head['amount_x']
    df1['当前交易日成交量（千元）'] = data_frame_head['amount_y']
    df1['相对于上一个交易日的成交额变动（千元）'] = data_frame_head['amount_difference']
    # df1['上一个交易日成交量（千元）'] = data_frame_head['amount_x'].map(lambda x: format(x * 1000, ','))
    # df1['当前交易日成交量（千元）'] = data_frame_head['amount_y'].map(lambda x: format(x * 1000, ','))
    # df1['相对于上一个交易日的成交额变动（千元）'] = data_frame_head['amount_difference'].map(lambda x: format(x * 1000, ','))
    return df1.reset_index(drop=True)


def get_merge_data_frame():
    df_merge = pd.merge(df_previous, df_current, on="ts_code", how="left")
    # 当前交易日 - 上一个交易日
    amount_difference = df_merge['amount_y'] - df_merge['amount_x']
    df_merge['amount_difference'] = amount_difference
    df_merge['amount_difference_absolute'] = abs(amount_difference)
    stock_basic_data = pro.stock_basic(list_status='L')
    return pd.merge(df_merge, stock_basic_data, on="ts_code", how="left")


if __name__ == '__main__':
    trade_date = '20210415'
    previous_trade_cal = get_previous_trade_cal(end_date=trade_date)
    df_previous = get_daily(trade_date=previous_trade_cal)
    df_current = get_daily(trade_date=trade_date)
    df_merge_data = get_merge_data_frame()
    pretty_print_all(df_merge_data)
