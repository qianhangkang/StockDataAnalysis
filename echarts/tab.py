from pyecharts import options as opts
from pyecharts.charts import Bar, Tab, Page
from pyecharts.faker import Faker

from echarts.fanbao import get_fanbao_dict, get_fanbao_stock_table, get_fanbao_line
from echarts.mood import get_mood_Line
from echarts.zhaban import get_zhaban_Line


def bar_datazoom_slider() -> Bar:
    c = (
        Bar()
            .add_xaxis(Faker.days_attrs)
            .add_yaxis("商家A", Faker.days_values)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-DataZoom（slider-水平）"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return c


def get_fanbao_page() -> Page:
    fanbao_dict = get_fanbao_dict()
    line = get_fanbao_line(fanbao_dict)
    table = get_fanbao_stock_table(fanbao_dict)
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        line,
        table
    )
    return page


def render_tab():
    tab = Tab()
    # pyechats 暂时不支持tab渲染page
    # tab.add(get_fanbao_page(), "图1-反包")
    fanbao_dict = get_fanbao_dict()
    tab.add(get_fanbao_line(fanbao_dict), "图1-反包数量")
    tab.add(get_fanbao_stock_table(fanbao_dict), "图2-反包股票列表")
    tab.add(get_mood_Line(), "图3-涨跌停数量差 & 炸板数")
    tab.add(get_zhaban_Line(), "图4-炸板第二天红盘数")
    tab.render("tab.html")
