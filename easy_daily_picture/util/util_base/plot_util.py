import os

import matplotlib.pyplot as plt
import seaborn as sns
import talib as ta
import numpy as np
from flask import current_app

from easy_daily_picture.util.util_data.future_data import FutureData


def get_future_interval_point_data(ts_code, start_date, end_date):
    point_result = FutureData().get_future_interval_point_data(ts_code, start_date, end_date)
    point_result.dropna(subset=['close'], inplace=True)

    point_result["sma_data_5"] = ta.MA(point_result["close"], timeperiod=5, matype=0)
    point_result["sma_data_30"] = ta.MA(point_result["close"], timeperiod=30, matype=0)

    point_result["sma_data_20"] = ta.MA(point_result["close"], timeperiod=20, matype=0)
    point_result["sma_data_40"] = ta.MA(point_result["close"], timeperiod=40, matype=0)

    point_result["ema_data_5"] = ta.MA(point_result["close"], timeperiod=5, matype=1)

    point_result["bias_20"] = (point_result["close"] - point_result["sma_data_20"]) / point_result["sma_data_20"] * 100

    point_result["sma_standard"] = point_result[['sma_data_20', 'sma_data_30', 'sma_data_40']].apply(np.std, ddof=0, axis=1)
    point_result["sma_cov"] = point_result["sma_standard"] / point_result[['sma_data_20', 'sma_data_30', 'sma_data_40']].apply(np.mean,
                                                                                                                               axis=1)

    point_result_all_date = FutureData().get_future_interval_point_data_by_main_code(ts_code, end_date)
    point_result_all_date.dropna(subset=['close'], inplace=True)
    point_result_max_date = point_result['trade_date'].max()
    point_result_all_date = point_result_all_date[point_result_all_date['trade_date'] <= point_result_max_date]

    contract_list = point_result_all_date['ts_code'].unique()
    for contract in contract_list:
        point_result_all_date[contract] = point_result_all_date[point_result_all_date['ts_code'] == contract]['close']

    return point_result, point_result_all_date


def plot_future_big_picture_data(ts_code, point_data, point_result_all_date, image_name):
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

    fig = plt.figure(figsize=(16, 24))  # 16, 18
    ax4 = plt.axes([0.05, 0.1, 0.85, 0.08])

    ax4.bar(point_data["xticks_int_index"], point_data["bias_20"], ls="-", lw=1, color='k')

    labels = ['bias']
    ax4.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title=ts_code, shadow=True, fancybox=True, labels=labels)

    import matplotlib.ticker as ticker
    ax4.xaxis.set_major_locator(ticker.MultipleLocator(3))  # 来强制指定每隔5个刻度，设定一个主刻度
    # 原始数据中日期是不连续的, 反应到x轴的刻度上, x轴会默认补全所有日期, 所以有的日期就会没数据, 这个方法可以去掉没有数据的日期
    ax4.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    plt.xticks(rotation=90)

    #####################################
    ax3 = plt.axes([0.05, 0.18, 0.85, 0.04], sharex=ax4)
    plt.setp(ax3.get_xticklabels(), visible=False)

    ax3.bar(point_data["xticks_int_index"], point_data["sma_cov"], ls="-", lw=1, color='k')

    labels = ['sma_cov']
    ax3.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title=ts_code, shadow=True, fancybox=True, labels=labels)

    #####################################
    ax2 = plt.axes([0.05, 0.22, 0.85, 0.26], sharex=ax3)
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax2.plot(point_data["xticks_int_index"], point_data["close"], ls="-", lw=1, color='k')
    ax2.plot(point_data["xticks_int_index"], point_data["sma_data_20"], ls="-", lw=1, color='r')
    ax2.plot(point_data["xticks_int_index"], point_data["sma_data_30"], ls="-", lw=1, color='g')
    ax2.plot(point_data["xticks_int_index"], point_data["sma_data_40"], ls="-", lw=1, color='b')

    labels = ['close point', "sma_20", "sma_30", "ema_40"]
    ax2.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title=ts_code, shadow=True, fancybox=True, labels=labels)

    #####################################
    ax1 = plt.axes([0.05, 0.48, 0.85, 0.26], sharex=ax2)
    plt.setp(ax1.get_xticklabels(), visible=False)

    sma_data_5_sloop, sma_data_30_sloop = _calc_the_last_sma_data_sloop(point_data)
    ax1.plot(point_data["xticks_int_index"], point_data["close"], ls="-", lw=1, color='k')
    ax1.plot(point_data["xticks_int_index"], point_data["sma_data_30"], ls="-", lw=1, color='g')
    ax1.plot(point_data["xticks_int_index"], point_data["sma_data_5"], ls="-", lw=1, color='r')
    ax1.plot(point_data["xticks_int_index"], point_data["ema_data_5"], ls="-", lw=1, color='darkblue')

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

    labels = ['close point', "sma_30", "sma_5", "ema_5"]
    ax1.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title=ts_code, shadow=True, fancybox=True, labels=labels)

    #####################################
    ax0 = plt.axes([0.05, 0.74, 0.85, 0.26])
    plt.setp(ax0.get_xticklabels(), visible=False)

    contract_list = point_result_all_date['ts_code'].unique()
    for contract in contract_list:
        ax0.plot(point_result_all_date["trade_date"], point_result_all_date[contract], ls="-", lw=1, color='k')

    ax0.legend(loc="upper left", title='just OK for newest futures contract', shadow=True, fancybox=True, labels=[])

    #####################################
    ax1.grid(True)
    ax2.grid(True)

    plt.savefig(os.path.join(current_app.image_dir, image_name))
    # plt.show()


def plot_future_interval_point_data_by_code(ts_code, start_date, end_date, image_name):
    ts_code_point_data, point_result_all_date = get_future_interval_point_data(ts_code, start_date, end_date)
    plot_future_big_picture_data(ts_code, ts_code_point_data, point_result_all_date, image_name)


if __name__ == '__main__':
    import datetime

    from easy_daily_picture import create_app
    app = create_app()
    with app.test_request_context():
        plot_future_interval_point_data_by_code('CS2005.DCE', datetime.datetime(2019, 1, 1), datetime.datetime(2020, 2, 5), 'aaaa.png')
