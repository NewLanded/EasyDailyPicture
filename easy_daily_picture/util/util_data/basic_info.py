from easy_daily_picture.util.util_base.db import get_db
from easy_daily_picture.util.util_base.db_util import get_multi_data

from itertools import count


class BasicInfo:
    def __init__(self):
        self._session = get_db()

    def get_future_info_by_symbol(self, symbol_code_list):
        index_dict = dict(zip([i for i in symbol_code_list], count()))

        sql = """
        select ts_code, name from  future_basic_info_data 
        where symbol in ({0})
        """.format("'" + "','".join(symbol_code_list) + "'")
        args = {}
        result = get_multi_data(self._session, sql, args)

        result = sorted(result, key=lambda x: index_dict[x[0].split('.')[0]])

        return result
