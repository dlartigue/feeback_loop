
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from ExistConnection import ExistConnection
from data import Base, weight, energy


class UpdateData(object):

    def __init__(self, exist_user, exist_key, db_connection):
        self.exist = ExistConnection(exist_user, exist_key)
        self.engine = create_engine(db_connection)
        Base.metadata.bind = self.engine
        self.session = sessionmaker(bind=self.engine)
        self.s = self.session()

    def get_data(self, data_type):
        return(self.exist.get_data(data_type))

    def most_recent_entry(self, table):
        try:
            recent = (self.s.query(table)
                      .order_by(table.date.desc())
                      .first())
        except InvalidRequestError:
            return('bad request')
        if recent is None:
            return('no data found')
        return(recent.date)

    def populate_table(self, table, data_type):
        if data_type == 'energy':
            col_name = 'calories'
        elif data_type == 'weight':
            col_name = 'weight'
        last_date = self.most_recent_entry(table)
        data = self.get_data(data_type)
        if (last_date != 'no data found') & (last_date != 'bad request'):
            data = data[:str(last_date)]
        dts = data.index.tolist()
        data = data[data.sort_index().diff() != 0]
        if len(dts) == 1:
            self.update_table(table, col_name, dts[0], data.loc[dts[0]][0])
        for dt in dts:
            row_value = data.loc[dt][0]
            try:
                new_row = table(**{'date': dt, col_name: row_value})
                self.s.add(new_row)
                self.s.commit()
            except (InvalidRequestError, IntegrityError):
                try:
                    self.s.rollback()
                    new_row = table(**{'date': dt, col_name: row_value})
                    self.s.add(new_row)
                    self.s.commit()
                except IntegrityError:
                    pass

    def update_table(self, table, col_name, date, data):
        ups = (update(table)
               .where(table.date == date)
               .values(**{col_name: data}))
        self.s.execute(ups)
        self.s.commit()

    def update_all_data(self):
        self.populate_table(weight, 'weight')
        self.populate_table(energy, 'energy')

    def __exit__(self, type, value, traceback):
        self.s.close()


if __name__ == '__main__':
    from auth import DB_CONNECTION, EXIST_USER, EXIST_KEY
    updates = UpdateData(EXIST_USER, EXIST_KEY, DB_CONNECTION)
    updates.update_all_data()
    updates.s.close()
    # print(updates.most_recent_entry(energy))
    # updates.populate_weight_table(weight, 'weight')
    # updates.populate_energy_table()
    # print(test)
    # print(update_object.get_data('energy'))
