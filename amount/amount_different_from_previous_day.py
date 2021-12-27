import pandas as pd
import tushare as ts

from stock_basic import tushare_api
from stock_basic.basic import get_stock_basic_df

pro = ts.pro_api("4e8cf3debc133f549e0bb20a0f68baeb267947b2d099b4d17c94f923")
# pandas 输出对齐
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


def pretty_print_all(stock_merge_data_frame, number):
    sorted_df_all = stock_merge_data_frame.sort_values(by='amount_difference_absolute', ascending=False)
    sorted_df_inflow = sorted_df_all[sorted_df_all.amount_difference > 0]
    sorted_df_outflow = sorted_df_all[sorted_df_all.amount_difference < 0]
    print("\n\n")
    print("===" * 5 + "根据净变动成交量降序" + "===" * 5)
    print(format_data_frame(sorted_df_all, number))
    # format_data_frame(sorted_df_all).plot()
    # plt.show()
    print("\n\n")
    print("===" * 5 + "根据成交量净增加降序" + "===" * 5)
    print(format_data_frame(sorted_df_inflow, number))
    print("\n\n")
    print("===" * 5 + "根据成交量净减少降序" + "===" * 5)
    print(format_data_frame(sorted_df_outflow, number))


def format_data_frame(data_frame, number):
    data_frame_head = data_frame.head(number)
    df1 = pd.DataFrame()
    df1['股票代码'] = data_frame_head['ts_code']
    df1['股票名称'] = data_frame_head['name']
    df1['上一个交易日成交量（千元）'] = data_frame_head['amount_x']
    df1['当前交易日成交量（千元）'] = data_frame_head['amount_y']
    df1['相对于上一个交易日的成交额变动（千元）'] = data_frame_head['amount_difference']
    df1['当日涨跌幅（未复权）'] = data_frame_head['pct_chg_y']
    # df1['上一个交易日成交量（千元）'] = data_frame_head['amount_x'].map(lambda x: format(x * 1000, ','))
    # df1['当前交易日成交量（千元）'] = data_frame_head['amount_y'].map(lambda x: format(x * 1000, ','))
    # df1['相对于上一个交易日的成交额变动（千元）'] = data_frame_head['amount_difference'].map(lambda x: format(x * 1000, ','))
    return df1.reset_index(drop=True)


def get_merge_data_frame(df_previous, df_current):
    df_merge = pd.merge(df_previous, df_current, on="ts_code", how="left")
    # 当前交易日 - 上一个交易日
    amount_difference = df_merge['amount_y'] - df_merge['amount_x']
    df_merge['amount_difference'] = amount_difference
    df_merge['amount_difference_absolute'] = abs(amount_difference)
    stock_basic_data = get_stock_basic_df()
    return pd.merge(df_merge, stock_basic_data, on="ts_code", how="left")


def print_daily_amount_difference(trade_date, number):
    previous_trade_cal = tushare_api.get_previous_trade_cal(end_date=trade_date)
    df_previous = tushare_api.get_daily(trade_date=previous_trade_cal)
    df_current = tushare_api.get_daily(trade_date=trade_date)
    df_merge_data = get_merge_data_frame(df_previous, df_current)
    pretty_print_all(df_merge_data, number)
