from easy_daily_picture.util.util_base.db import get_db
from easy_daily_picture.util.util_base.db_util import get_multi_data


class FutureBSData:
    def __init__(self):
        self._session = get_db()

    def buy(self, strategy_code, date):
        sql = """
        select a.ts_code, b.name from strategy_result a inner join future_basic_info_data b
        on a.ts_code=b.ts_code
        where a.bs_flag='B' and a.date=(select max(date) from strategy_result where strategy_code=:strategy_code and date <= :date) 
        and strategy_code=:strategy_code order by a.ts_code
        """
        args = {"date": date, "strategy_code": strategy_code}
        result = get_multi_data(self._session, sql, args)

        return result

    def sell(self, strategy_code, date):
        sql = """
        select a.ts_code, b.name from strategy_result a inner join future_basic_info_data b
        on a.ts_code=b.ts_code
        where a.bs_flag='S' and a.date=(select max(date) from strategy_result where strategy_code=:strategy_code and date <= :date) 
        and strategy_code=:strategy_code order by a.ts_code
        """
        args = {"date": date, "strategy_code": strategy_code}
        result = get_multi_data(self._session, sql, args)

        return result
