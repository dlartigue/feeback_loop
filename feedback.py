from datetime import datetime

from auth import DB_CONNECTION, EXIST_USER, EXIST_KEY
from UpdateData import UpdateData
from ExploreData import ExploreData

from data import weight, energy


CHECK_IN_DOW = 0  # 0: Monday

current = int(datetime.now().strftime("%w"))

if current == 0:
    today = 6
else:
    today = current - 1


days = 14

ups = UpdateData(EXIST_USER, EXIST_KEY, DB_CONNECTION)
ups.update_all_data()

db = ExploreData(DB_CONNECTION)

weight_data = db.filter_by_dow(
    db.get_last_n_rows(weight, days), today)

energy_data = db.filter_by_dow(
    db.get_last_n_rows(energy, days), today)

# w_dow = weight_data.index.dayofweek
# e_dow = energy_data.index.dayofweek

# filtered = weight_data.loc[weight_data.index[w_dow == today]][0:2]

print(weight_data)
# print(weight_data[])

print(energy_data)
