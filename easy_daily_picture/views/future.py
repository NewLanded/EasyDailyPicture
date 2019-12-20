import datetime

from flask import Blueprint, jsonify, request

from easy_daily_picture.util.util_base.date_util import convert_datetime_to_str
from easy_daily_picture.util.util_base.plot_util import plot_future_interval_point_data_by_code
from easy_daily_picture.util.util_data.basic_info import BasicInfo
from easy_daily_picture.util.util_data.future_bs_data import FutureBSData

bp = Blueprint('future', __name__, url_prefix='/future')


@bp.route('/buy_result', methods=('GET',))
def buy_result():
    date = datetime.datetime.now()
    strategy_code = "future_bs_when_trend_start"

    result = FutureBSData().buy(strategy_code, date)

    return jsonify(result)


@bp.route('/sell_result', methods=('GET',))
def sell_result():
    date = datetime.datetime.now()
    strategy_code = "future_bs_when_trend_start"

    result = FutureBSData().sell(strategy_code, date)

    return jsonify(result)


@bp.route('/holding_info', methods=('GET',))
def holding_info():
    symbol_list = request.args.get('symbol_list', '')
    symbol_list = symbol_list.replace(' ', '').replace('\t', '').replace('\n', '').split(',')

    result = BasicInfo().get_future_info_by_symbol(symbol_list)

    return jsonify(result)


@bp.route('/plot_future_interval_point_data_by_ts_code', methods=('GET',))
def plot_future_interval_point_data_by_ts_code():
    ts_code = request.args.get('ts_code', None)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)

    if not ts_code:
        raise ValueError("ts_code not found")

    if not end_date:
        end_date = datetime.datetime.now()

    if not start_date:
        start_date = end_date - datetime.timedelta(days=365)

    image_name = ts_code + "_" + convert_datetime_to_str(start_date) + "_" + convert_datetime_to_str(end_date) + ".png"
    plot_future_interval_point_data_by_code(ts_code, start_date, end_date, image_name)
    return jsonify({"image_name": image_name})
