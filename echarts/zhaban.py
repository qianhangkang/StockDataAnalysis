from time import sleep

import pyecharts.options as opts
from pyecharts.charts import Line

from stock_basic import kaipanla2 as kp
from stock_basic import tushare_api as ta


def get_zhaban_Line() -> Line:
    x_data = ta.get_trade_cal()
    x_data.reverse()
    y_data = []
    for trade_date in x_data:
        count = kp.get_zhaban_red_count(trade_date)
        y_data.append(count)
        sleep(0.5)

    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("炸板第二天红盘数", y_data, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="炸板第二天红盘数"))
    )
    return c


def draw_zhaban_line():
    get_zhaban_Line().render("zhaban.html")
