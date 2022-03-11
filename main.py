import argparse
import time

from amount.amount_different_from_previous_day import print_daily_amount_difference
from echarts.fanbao import draw_charts, get_fanbao_dict
from echarts.zhaban import draw_zhaban_line


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-td", "--trade_date", help="交易日期，ex:20210415", type=int)
    parser.add_argument("-n", "--number", help="显示的数量", type=int)
    parser.add_argument("--fanbao", help="反包股票数量", action="store_true")
    parser.add_argument("--zhaban", help="炸板第二天红盘数量", action="store_true")
    args = parser.parse_args()
    trade_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    n = 20
    if args.zhaban:
        draw_zhaban_line()
        exit(0)
    if args.trade_date:
        trade_date = args.trade_date
    if args.number:
        n = args.number
    if args.fanbao:
        draw_charts(get_fanbao_dict())
        exit(0)

    print_daily_amount_difference(str(trade_date), n)


if __name__ == '__main__':
    main()
