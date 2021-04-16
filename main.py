import argparse
import time

from amount import amount_different_from_previous_day


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-td", "--trade_date", help="交易日期，ex:20210415", type=int)
    args = parser.parse_args()

    trade_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    if args.trade_date:
        trade_date = args.trade_date

    amount_different_from_previous_day.print_daily_amount_difference(str(trade_date))


if __name__ == '__main__':
    main()
