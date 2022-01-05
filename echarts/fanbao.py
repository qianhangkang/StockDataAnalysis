import time
from time import sleep

from pyecharts import options as opts
from pyecharts.charts import Line, Page
from pyecharts.components import Table

from stock_basic import basic
from stock_basic import east_assert as eas
from stock_basic import tushare_api as ta


def get_fanbao_dict():
    tc_list = ta.get_trade_cal(1)
    tc_list_len = len(tc_list)
    stock_dict = {}
    # 获取涨停
    for date in tc_list:
        stock_df = eas.get_top(date)
        stock_dict[date] = list(stock_df['c'].values)
        sleep(0.3)

    fanbao_dict = {}
    for index in range(tc_list_len):
        if index + 2 > tc_list_len - 1:
            break
        s1 = set(stock_dict[tc_list[index]])
        s2 = set(stock_dict[tc_list[index + 2]])
        # 当前交易日与上上个交易日的交集
        s3 = s1.intersection(s2)
        # 中间这个交易日涨停的股票列表
        s_middle = set(stock_dict[tc_list[index + 1]])

        # 在中间这个交易日不涨停
        # 即s3中的元素不能在s_middle里
        res = s3.difference(s_middle)
        fanbao_dict[tc_list[index]] = res
        print(f'交易日期为{tc_list[index]}的反包股票个数为{len(res)}，代码为{str(res)}')

    return fanbao_dict


def line_smooth(fanbao_dict: dict) -> Line:
    x_data = []
    y_data = []
    for k, v in fanbao_dict.items():
        x_data.append(k)
        y_data.append(len(v))

    x_data.reverse()
    y_data.reverse()

    c = (
        Line()
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis("反包股票个数", y_data, is_smooth=True)
            .set_series_opts()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Line-smooth"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True)))
        # .render("line_smooth.html")
    )

    return c


def table_fanbao(fanbao_dict: dict) -> Table:
    table = Table()

    # 每周一强制更新一次
    reload = int(time.strftime('%Y%m%d', time.localtime(time.time()))) % 7 == 1
    df_stock = basic.get_stock_basic_df(reload=reload)

    headers = ["日期", "股票代码"]
    rows = []
    # type of v is a set
    for k, v in fanbao_dict.items():
        code_with_name_set = set()
        for code in v:
            query_str = f'symbol=="{code}"'
            res = df_stock.query(query_str)
            code_with_name = f'{code}'
            if len(res) > 0:
                name = str(res.head(1)['name'].values[0])
                code_with_name = f'{code_with_name}({name})'
            code_with_name_set.add(code_with_name)
        code = ','.join(code_with_name_set)
        item = [k, code]
        rows.append(item)

    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="Table")
    )
    return table


def draw_charts(fanbao_dict: dict):
    line = line_smooth(fanbao_dict)
    table = table_fanbao(fanbao_dict)
    print("draw chrats...")

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        line,
        table
    )
    page.render('line_smooth.html')

    print("done ...")
