import datetime

from easy_daily_picture.util.util_base.db import get_db
from easy_daily_picture.util.util_base.db_util import get_multi_data
import pandas as pd


class FutureData:
    def __init__(self):
        self._session = get_db()

    def get_future_interval_point_data(self, ts_code, start_date, end_date):
        sql = '''
        select ts_code, trade_date, `open`, high, low, close, settle, change1, change2, vol, amount from future_daily_point_data where 
        ts_code = :ts_code and trade_date >= :start_date and trade_date <= :end_date
        order by trade_date
        '''
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        result = get_multi_data(self._session, sql, args)

        result = pd.DataFrame(result,
                              columns=['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'settle', 'change1', 'change2', 'vol',
                                       'amount'])

        return result

    def get_future_interval_point_data_by_main_code(self, ts_code, end_date):
        sql = """select a.close, a.trade_date, b.mapping_ts_code as ts_code from 
        future_daily_point_data a inner join
        (select trade_date, mapping_ts_code from future_main_code_data where ts_code=(
        select ts_code from future_main_code_data where mapping_ts_code= :ts_code limit 1)) b 
        on a.ts_code=b.mapping_ts_code and a.trade_date=b.trade_date
        where a.trade_date >= :start_date and a.trade_date <= :end_date
        order by a.trade_date"""

        args = {"ts_code": ts_code, "start_date": end_date - datetime.timedelta(days=1800), "end_date": end_date}
        result = get_multi_data(self._session, sql, args)

        result = pd.DataFrame(result, columns=['close', 'trade_date', 'ts_code'])

        return result
