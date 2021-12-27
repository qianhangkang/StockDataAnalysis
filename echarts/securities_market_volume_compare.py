import datetime as dt

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Kline, Bar, Grid

from stock_basic import market


def get_data(count):
    json = market.kline('BK0057', count)
    df_data_securities = pd.DataFrame(json['data']['item'])
    df_data_volume = market.get_two_cities_volume(count)
    df_merge = pd.merge(df_data_securities, df_data_volume, left_on=0, right_on='date', how='inner')
    return df_merge


def draw_charts():
    df_merge = get_data(3000)
    kline_data = pd.DataFrame(df_merge, columns=[2, 5, 4, 3]).values.tolist()
    xaxis = pd.to_datetime(df_merge[0], unit='ms').dt.strftime('%Y-%m-%d').to_list()

    kline = (
        Kline()
            .add_xaxis(xaxis_data=xaxis)
            .add_yaxis(
            series_name="证券板块指数",
            y_axis=kline_data,
            itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c"),
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(
                is_show=False, pos_bottom=10, pos_left="center"
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False,
                    type_="inside",
                    xaxis_index=[0, 1],
                    range_start=0,
                    range_end=100,
                ),
                opts.DataZoomOpts(
                    is_show=True,
                    xaxis_index=[0, 1],
                    type_="slider",
                    pos_top="85%",
                    range_start=0,
                    range_end=100,
                ),
            ],
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color="rgba(245, 245, 245, 0.8)",
                border_width=1,
                border_color="#ccc",
                textstyle_opts=opts.TextStyleOpts(color="#000"),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                dimension=2,
                series_index=5,
                is_piecewise=True,
                pieces=[
                    {"value": 1, "color": "#00da3c"},
                    {"value": -1, "color": "#ec0000"},
                ],
            ),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                link=[{"xAxisIndex": "all"}],
                label=opts.LabelOpts(background_color="#777"),
            ),
            brush_opts=opts.BrushOpts(
                x_axis_index="all",
                brush_link="all",
                out_of_brush={"colorAlpha": 0.1},
                brush_type="lineX",
            ),
        )
    )

    array_volume = df_merge['两市成交额'].values.tolist()
    bar_yaxis = [round(i / 100000000, 1) for i in array_volume]
    bar = (
        Bar()
            .add_xaxis(xaxis_data=xaxis)
            .add_yaxis(
            series_name="两市成交量（亿元）",
            y_axis=bar_yaxis,
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                grid_index=1,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=1,
                is_scale=True,
                split_number=3,
                axislabel_opts=opts.LabelOpts(is_show=True),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="证券板块与两市成交量（亿元）对比")
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(y=10000), opts.MarkLineItem(y=15000)]
            )
        )
    )

    # Grid Overlap + Bar
    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="1000px",
            height="800px",
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    grid_chart.add(
        kline,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
    )
    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="63%", height="16%"
        ),
    )

    title = '证券-两市成交额对比' + str(dt.date.today()) + '.html'
    grid_chart.render(title)
    print("done")


if __name__ == '__main__':
    draw_charts()
