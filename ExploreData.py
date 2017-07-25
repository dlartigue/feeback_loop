import pandas as pd

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from data import Base


class ExploreData(object):

    def __init__(self, db_connection):
        self.engine = create_engine(db_connection)
        Base.metadata.bind = self.engine
        self.session = sessionmaker(bind=self.engine)
        self.s = self.session()

    def get_last_n_rows(self, table, n):
        # test = db.s.query(table).order_by(table.date.desc()).limit(n)
        table_name = table.__table__.name
        value_list = []

        if table_name == 'weight':
            value_col = 'weight'
        elif table_name == 'energy':
            value_col = 'calories'

        query = (select([table.date, getattr(table, value_col)])
                 .order_by(table.date.desc())
                 .limit(n))

        result_proxy = self.s.execute(query)
        query_results = result_proxy.fetchall()

        for row in query_results:
            value_list.append([row[0], row[1]])

        result = pd.DataFrame(value_list, columns=['date', value_col])
        result['date'] = pd.to_datetime(result['date'],
                                        format="%Y-%m-%d")
        result = result.set_index(pd.DatetimeIndex(result['date']))
        result = result.drop(['date'], axis=1)

        return(result)

    def filter_by_dow(self, data, dow):
        dow_list = data.index.dayofweek
        filtered = data.loc[data.index[dow_list == dow]][0:2]
        return(filtered)

    def __exit__(self, type, value, traceback):
        self.s.close()


if __name__ == '__main__':
    from data import weight, energy
    from auth import DB_CONNECTION
    db = ExploreData(DB_CONNECTION)
    t = db.get_last_n_rows(weight, 7)
    print(db.get_last_n_rows(energy, 7))
    print(t.index.strftime("%w"))
    # test = db.s.query(weight).order_by(weight.date.desc()).limit(7)
    # weight_list = []
    # # print(test.calories)
    # for row in test:
    #     weight_list.append((row.date, row.weight))
    # print(pd.DataFrame(weight_list))
