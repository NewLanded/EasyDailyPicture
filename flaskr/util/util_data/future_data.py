from flaskr.util.util_base.db import get_db
from flaskr.util.util_base.db_util import get_multi_data
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

        result = pd.DataFrame(result, columns=['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'settle', 'change1', 'change2', 'vol', 'amount'])

        return result
