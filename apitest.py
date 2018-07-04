from apiclass import *


query_body = """
SELECT  npt, ngp,t5_average_temperature,engine_pcd ,t1_temperature, turb_air_inlet_filter_dp,gas_fuel_flow_x

FROM Unit1 ORDER BY time DESC LIMIT 1

"""



########The database to retrieve data from ML######################

zhost = '192.168.4.33'

zport = 8086

zuser = ''

zpassword = ''

zdb_name = 'Labview'

writer_client = DataFrameClient(zhost, zport, zuser, zpassword, zdb_name)

starttime=time.time()

while True:

    predictor = Online_predictor(zhost, zport, zuser, zpassword, zdb_name,query_body)

    predictor.get_data_from_influx()

    predictor.read_data()

    df = predictor.prepare_data()

    udelnyi_rashod_gaza = df['gas_fuel_flow_x']

    df = df.set_index('index')

    data = df.to_json(orient='records')

    #print(data)

    resp = requests.post(" http://192.168.1.37:5000/predict", \
                         data=json.dumps(data), \
                         headers=header)

    resp.status_code

    json_clasified = resp.json()

    for k in json_clasified:
        needed_data = json_clasified[k]

    print(needed_data)

    final_data = float(needed_data[6:15])

    print('Predicted from model: ', final_data)

    print('Actual value of gas flow: ', predictor.show())

    predicted_udelnyiRashodGaza = pd.DataFrame({'gas_fuel_flow_y': final_data}, index=df.index)

    #upload_udelnyi_rashod_gaza = writer_client.write_points(predicted_udelnyiRashodGaza, 'unit1')

    time.sleep(20.0 - ((time.time() - starttime) % 20.0))












