from time import sleep

import pyecharts.options as opts
from pyecharts.charts import Line

from stock_basic import east_assert as eas
from stock_basic import tushare_api as ta


def get_difference_with_zt_dt_data_list(trade_date_list):
    y_data = []
    for trade_date in trade_date_list:
        zt_count = eas.get_count(str(trade_date), 1)
        if zt_count is None:
            print("zt_count is None")
            return
        dt_count = eas.get_count(str(trade_date), 0)
        if dt_count is None:
            print("dt_count is None")
            return
        y = int(zt_count) - int(dt_count)
        y_data.append(y)
        sleep(0.5)
    return y_data


def get_zhaban_count_data_list(trade_date_list):
    y_data = []
    for trade_date in trade_date_list:
        y = eas.get_zhaban_count(trade_date)
        y_data.append(y)
        sleep(0.5)
    return y_data


def get_mood_Line(yaxis_index=None):
    x_data = ta.get_trade_date_list()
    y1 = get_difference_with_zt_dt_data_list(x_data)
    y2 = get_zhaban_count_data_list(x_data)

    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("涨停数-跌停数", y1, is_smooth=True, yaxis_index=yaxis_index)
            .add_yaxis("炸板数", y2, is_smooth=True, yaxis_index=yaxis_index)
            .set_global_opts(title_opts=opts.TitleOpts(title="情绪指标"))
        # .set_global_opts(title_opts=opts.TitleOpts(title="情绪指标"),
        #                  xaxis_opts=opts.AxisOpts(type_="time"))
    )
    return c


def draw_mood_line():
    get_mood_Line().render("mood.html")
