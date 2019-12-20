import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import talib as ta

from easy_daily_picture.util.util_data.future_data import FutureData
from flask import current_app

def get_future_interval_point_data(ts_code, start_date, end_date):
    point_result = FutureData().get_future_interval_point_data(ts_code, start_date, end_date)

    point_result["sma_data_5"] = ta.MA(point_result["close"], timeperiod=5, matype=0)
    point_result["sma_data_10"] = ta.MA(point_result["close"], timeperiod=10, matype=0)
    point_result["sma_data_30"] = ta.MA(point_result["close"], timeperiod=30, matype=0)

    return point_result


def plot_future_big_picture_data(ts_code, point_data, image_name):
    sns.set()
    sns.set_palette(sns.color_palette('dark'))

    def _calc_the_last_sma_data_sloop(point_data):
        sma_5_point_n_1, sma_5_point_n_2 = point_data["sma_data_5"].iloc[-1], point_data["sma_data_5"].iloc[-2]
        sma_30_point_n_1, sma_30_point_n_2 = point_data["sma_data_30"].iloc[-1], point_data["sma_data_30"].iloc[-2]

        sma_data_5_sloop = round((sma_5_point_n_1 - sma_5_point_n_2) / sma_5_point_n_2, 5)
        sma_data_30_sloop = round((sma_30_point_n_1 - sma_30_point_n_2) / sma_30_point_n_2, 5)

        return sma_data_5_sloop, sma_data_30_sloop

    point_data['xticks_int_index'] = [i for i in range(len(point_data["trade_date"]))]
    xticks_index_map = point_data["trade_date"].apply(lambda x: x.strftime("%Y-%m-%d"))

    def format_date(x, pos=None):
        if x < 0 or x > len(xticks_index_map) - 1:
            return ''
        return xticks_index_map.iloc[int(x)]

    fig = plt.figure(figsize=(16, 9))
    sma_data_5_sloop, sma_data_30_sloop = _calc_the_last_sma_data_sloop(point_data)

    ax1 = plt.axes([0, 0.1, 0.85, 0.9])
    ax1.plot(point_data["xticks_int_index"], point_data["close"], ls="-", lw=1, color='k')
    ax1.plot(point_data["xticks_int_index"], point_data["sma_data_30"], ls="-", lw=1, color='g')
    ax1.plot(point_data["xticks_int_index"], point_data["sma_data_5"], ls="-", lw=1, color='r')

    ax1.annotate(s=sma_data_5_sloop,
                 xy=(point_data["xticks_int_index"].iloc[-1], point_data["sma_data_5"].iloc[-1]),
                 xytext=(point_data["xticks_int_index"].iloc[-1] + 1, point_data["sma_data_5"].iloc[-1]),
                 weight='bold')
    ax1.annotate(s=sma_data_30_sloop,
                 xy=(point_data["xticks_int_index"].iloc[-1], point_data["sma_data_30"].iloc[-1]),
                 xytext=(point_data["xticks_int_index"].iloc[-1] + 1, point_data["sma_data_30"].iloc[-1]),
                 weight='bold')
    ax1.annotate(s=point_data["close"].iloc[-1],
                 xy=(point_data["xticks_int_index"].iloc[-1], point_data["close"].iloc[-1]),
                 xytext=(point_data["xticks_int_index"].iloc[-1] + 12, point_data["close"].iloc[-1]),
                 weight='bold')
    ax1.annotate(s=point_data['trade_date'].iloc[-1],
                 xy=(point_data["xticks_int_index"].iloc[-1], point_data["close"].iloc[-1]),
                 xytext=(point_data["xticks_int_index"].iloc[-1] + 12, min(point_data["close"])),
                 weight='bold')

    labels = ['close point', "sma_30", "sma_5"]
    ax1.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title=ts_code, shadow=True, fancybox=True, labels=labels)
    ax1.grid(True)

    ax1.xaxis.set_major_locator(ticker.MultipleLocator(3))  # 来强制指定每隔5个刻度，设定一个主刻度
    # 原始数据中日期是不连续的, 反应到x轴的刻度上, x轴会默认补全所有日期, 所以有的日期就会没数据, 这个方法可以去掉没有数据的日期
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    plt.xticks(rotation=90)

    plt.savefig(os.path.join(current_app.image_dir, image_name))


def plot_future_interval_point_data_by_code(ts_code, start_date, end_date, image_name):
    ts_code_point_data = get_future_interval_point_data(ts_code, start_date, end_date)
    plot_future_big_picture_data(ts_code, ts_code_point_data, image_name)
