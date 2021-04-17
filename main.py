import argparse
import time

from amount.amount_different_from_previous_day import print_daily_amount_difference


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-td", "--trade_date", help="交易日期，ex:20210415", type=int)
    parser.add_argument("-n", "--number", help="显示的数量", type=int)
    args = parser.parse_args()
    trade_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    n = 20
    if args.trade_date:
        trade_date = args.trade_date
    if args.number:
        n = args.number

    print_daily_amount_difference(str(trade_date), n)


if __name__ == '__main__':
    main()
