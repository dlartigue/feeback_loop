import requests
import json
from pandas import DataFrame

from auth import EXIST_USER, EXIST_KEY


class ExistConnection(object):
    '''
    KJ_to_KCAL = 0.2390
    KG_to_LBS = 2.204623
    '''

    def __init__(self, user_name, key):
        self.name = user_name
        attribute_url = "https://exist.io/api/1/users/%s/attributes/%s/"
        self.url = attribute_url % (user_name, '%s')
        # self.weight_url = self.attribute_url % (user_name, 'weight')
        # self.energy_url = self.attribute_url % (user_name, 'energy')
        self.auth_header = {'Authorization': 'Bearer %s' % key}
        self.conversions = {'energy': 0.2390, 'weight': 2.204623}

    def get_data(self, data_type):
        i = 0

        try:
            conversion = self.conversions[data_type]
        except KeyError:
            conversion = 1

        try:
            r = requests.get(self.url % data_type, headers=self.auth_header)
            if r.status_code == 200:
                r = json.loads(r.text)
                for result in r['results']:
                    r['results'][i]['value'] = (result['value'] * conversion)
                    i = i + 1
                df = DataFrame.from_records(r['results'], index='date')
                return(df)
            else:
                print("Request returned status code %s" % r.status_code)
        except requests.exceptions.RequestException:
            print("connection failed!!")


if __name__ == '__main__':
    test = ExistConnection(EXIST_USER, EXIST_KEY)
    weight_data = test.get_data('weight')
    print(weight_data)
    energy_data = test.get_data('energy')
    print(energy_data)
