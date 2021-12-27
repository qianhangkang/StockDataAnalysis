import time

from stock_basic import tushare_api as pro

if __name__ == '__main__':
    print(pro.get_previous_trade_cal(int(time.strftime('%Y%m%d', time.localtime(time.time())))))
