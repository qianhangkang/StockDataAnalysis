from stock_basic.tushare_api import get_trade_cal

if __name__ == '__main__':
    # df = ea.get_top('20211227')
    # print(len(df))
    # print(df.head())
    trade_df = get_trade_cal()
    print(trade_df)
