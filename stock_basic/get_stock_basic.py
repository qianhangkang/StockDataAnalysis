import os

import pandas as pd
import tushare as ts

pro = ts.pro_api("4e8cf3debc133f549e0bb20a0f68baeb267947b2d099b4d17c94f923")

"""
先从本地data文件夹中获取
获取不到再请求远程数据源
"""


def get_stock_basic_df(path='stock_basic.csv'):
    try:
        if os.path.exists(path):
            df_stock_basic = pd.read_csv(path, engine='python')
            if not df_stock_basic.empty:
                return df_stock_basic
    except Exception:
        print("读入本地数据异常，直接请求远程数据")

    # 文件不存在或者为空
    df_stock_basic = pro.stock_basic(list_status='L')
    print(path)
    df_stock_basic.to_csv(path, index=None)
    return df_stock_basic
