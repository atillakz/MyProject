import json
import requests
header = {'Content-Type': 'application/json', \
                  'Accept': 'application/json'}

import pandas as pd

import pandas as pd
from influxdb import DataFrameClient
from sklearn.externals import joblib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
query_body = """

SELECT npt, gas_fuel_flow
FROM Unit1
WHERE time > \'2018-05-10T12:00:00Z\'

"""
# AND
# time < \'2018-04-12T06:10:00Z\'

host = '192.168.4.33'

port = 8086

user = ''

password = ''

db_name = 'Online_Classification'


zhost = '192.168.4.33'

zport = 8086

zuser = ''

zpassword = ''

zdb_name = 'Labview'

starttime=time.time()

while True:

    class Online_predictor():

        def __init__(self, zhost, zport, zuser, zpassword, zdb_name):

            self.zhost = zhost

            self.zport = zport

            self.zuser = zuser

            self.zpassword = zpassword

            self.zdb_name = zdb_name

        def get_data_from_influx(self):

            self.client = DataFrameClient(self.zhost, self.zport, self.zuser, self.zpassword, self.zdb_name)

            self.data = self.client.query(query_body)

        def read_data(self):

            self.new_data = dict(self.data)

            for i in self.new_data:
                self.my_data = self.new_data[i]

        def prepare_data(self):

            self.my_data = self.my_data.reset_index()

            self.my_data = self.my_data.dropna()

            self.my_data.columns = ['date', 'FLOW', 'NPT']

            self.current_flow = self.my_data['FLOW']

            # self.my_data.drop('FLOW', axis = 1, inplace = True)

            self.my_data = self.my_data.set_index('date')

            self.last_value = self.my_data[len(self.my_data) - 1:len(self.my_data)]

            self.last_value_for_flow = self.current_flow[len(self.current_flow) - 1:len(self.current_flow)]

            return self.last_value

        def comparator(self, data):

            if data > 30:

                return 1

            else:

                return 0

        def difference(self, value):

            return (self.last_value_for_flow.values - value)

        def show(self):

            return (self.last_value_for_flow.values)


    if __name__ == '__main__':

        predictor = Online_predictor(zhost, zport, zuser, zpassword, zdb_name)

        predictor.get_data_from_influx()

        predictor.read_data()

        df = predictor.prepare_data()

        # print(df)

        data = df.to_json(orient='records')

        print(data)

        # print(dt)

        # print(data)


        resp = requests.post(" http://127.0.0.1:5000/predict", \
                             data=json.dumps(data), \
                             headers=header)

        resp.status_code

        json_clasified = resp.json()

        for k in json_clasified:
            needed_data = json_clasified[k]

        final_data = float(needed_data[6:15])

        print('Predicted from model: ', final_data)

        print('Actual value of gas flow: ', predictor.show())

        armani = predictor.comparator(predictor.difference(final_data))

        print("Delta:", predictor.difference(final_data))

        data_to_send = pd.DataFrame({'predicted': armani}, index=df.index)

        final_data_to_send = pd.DataFrame({'model-value': final_data}, index=df.index)

        writer_client = DataFrameClient(host, port, user, password, db_name)

        uploaded_data = writer_client.write_points(data_to_send, 'telegram')

        uploaded_data_for_flow = writer_client.write_points(final_data_to_send, 'lin-reg')

        print(data_to_send)

    time.sleep(20.0 - ((time.time() - starttime) % 20.0))


