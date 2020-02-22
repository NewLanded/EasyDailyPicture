import datetime

from flask import Blueprint, jsonify, request, send_from_directory, current_app

from easy_daily_picture.util.util_base.date_util import convert_datetime_to_str, convert_str_to_datetime
from easy_daily_picture.util.util_base.plot_util import plot_future_interval_point_data_by_code
from easy_daily_picture.util.util_data.basic_info import BasicInfo

# from easy_daily_picture.util.util_data.future_bs_data import FutureBSData

bp = Blueprint('future', __name__, url_prefix='/future')


# @bp.route('/buy_result', methods=('GET',))
# def buy_result():
#     date = datetime.datetime.now()
#     strategy_code = "future_bs_when_trend_start"
#
#     result = FutureBSData().buy(strategy_code, date)
#
#     return jsonify(result)
#
#
# @bp.route('/sell_result', methods=('GET',))
# def sell_result():
#     date = datetime.datetime.now()
#     strategy_code = "future_bs_when_trend_start"
#
#     result = FutureBSData().sell(strategy_code, date)
#
#     return jsonify(result)


@bp.route('/holding_info/', methods=('GET',))
def holding_info():
    symbol = request.args.get('symbol', '')
    result = BasicInfo().get_future_info_by_symbol([symbol])

    return jsonify(result)


@bp.route('/get_next_trade_day/', methods=('GET',))
def get_next_trade_day():
    data_date = request.args.get('data_date', None)
    if not data_date:
        raise ValueError("data_date not found")

    data_date = convert_str_to_datetime(data_date)
    next_trade_day = BasicInfo().get_next_trade_day(data_date)
    next_trade_day = convert_datetime_to_str(next_trade_day)

    return jsonify(next_trade_day)


@bp.route('/plot_future_interval_point_data_by_ts_code/', methods=('GET',))
def plot_future_interval_point_data_by_ts_code():
    ts_code = request.args.get('ts_code', None)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)

    if not ts_code:
        raise ValueError("ts_code not found")

    if not end_date:
        end_date = datetime.datetime.now()
    end_date = convert_str_to_datetime(end_date)

    if not start_date:
        start_date = end_date - datetime.timedelta(days=365)
    start_date = convert_str_to_datetime(start_date)

    image_name = ts_code + "_" + convert_datetime_to_str(start_date) + "_" + convert_datetime_to_str(end_date) + ".png"
    plot_future_interval_point_data_by_code(ts_code, start_date, end_date, image_name)
    return jsonify(current_app.config['OUTGOING_IMAGE_URI'] + image_name)


@bp.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(current_app.image_dir, filename)
