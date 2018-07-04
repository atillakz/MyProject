from apiclass import *

waterwash_check = dict()

waterwash_check['status'] = 0

last_value_loss_index = dict()

last_value_loss_index['last_value'] = 0

cycles_left_waterwash = 0

time_start_waterwash = dict()

time_start_waterwash['start'] = 0

time_finish_waterwash = dict()

time_finish_waterwash['finish'] = 0

def index_loss(a, b):

    return (a/b) *100

def comparator_for_index(x):

    if x >= 102.0408:

        return 1

    else:

        return 0

def time_to_waterwash(y):

    return int(abs(2/y))

def comparator_for_flow(data):

    if data > 30:

        return 1

    else:

        return 0

def difference(a, b):
    return (a - b)


def days_hours_minutes(td):
    days = td.days * 24
    hours = td.seconds / 3600
    total = days + hours
    return total.values


########The database to upload data from ML######################
host = '192.168.4.33'

port = 8086

user = ''

password = ''

db_name = 'Online_Classification' #metricdata

########The database to retrieve data from ML######################

zhost = '192.168.4.33'

zport = 8086

zuser = ''

zpassword = ''

zdb_name = 'Labview'

query_body = """
SELECT power_c,gas_fuel_flow, gas_fuel_flow_y, gas_fuel_flow_x

FROM Unit1 ORDER BY time DESC LIMIT 1

"""
writer_client = DataFrameClient(host, port, user, password, db_name)

starttime = time.time()

while True:

    predictor = Online_predictor(zhost, zport, zuser, zpassword, zdb_name,query_body)

    predictor.get_data_from_influx()

    predictor.read_data()

    df = predictor.prepare_data()

    print(df.columns)
    mownost_nagnetatelya = df['power_c']

    actual_gas_fuel_flow = df['gas_fuel_flow_x']

    gtg = df['gas_fuel_flow']

    predicted_gas_fuel_flow = df['gas_fuel_flow_y']

    turbine_power = gtg / predicted_gas_fuel_flow

    predicted_turbine_power = pd.DataFrame({'power' : turbine_power}, index=df.index)

    armani = comparator_for_flow(difference(actual_gas_fuel_flow, predicted_gas_fuel_flow))

    #armani_pd = pd.DataFrame({'status_flow' : armani}, index=df.index)

    index_poteri = index_loss(mownost_nagnetatelya, turbine_power)

    #predicted_index_poteri = pd.DataFrame({'loss_index': index_poteri}, index = df.index)

    waterwash = comparator_for_index(index_poteri.values)

    if waterwash_check['status'] < waterwash:

        time_start_waterwash['start'] = df.index

    if waterwash_check['status'] == 1 and waterwash == 1:

        time_start_waterwash['next_start'] = df.index

        vremya_alert_waterwash = days_hours_minutes(time_start_waterwash['next_start'] - time_start_waterwash['start'])

    if  waterwash_check['status'] > waterwash:

        time_finish_waterwash['finish'] = df.index

        whole_time_waterwash_alert = days_hours_minutes(time_finish_waterwash['finish'] - time_start_waterwash['start'])

        pd_whole_time_waterwash_alert = pd.DataFrame({'whole_time': whole_time_waterwash_alert}, index=df.index)

        upload_whole_time_waterwash_alert = writer_client.write_points(pd_whole_time_waterwash_alert, 'vremya_waterwash_alert')

    waterwash_check['status'] = waterwash

    #predicted_index_poteri = pd.DataFrame({'waterwash_status': waterwash}, index = df.index)

    acc_loss_index = difference(index_poteri,last_value_loss_index['last_value'])

    if acc_loss_index > 0:

        cycles_left_waterwash = time_to_waterwash(acc_loss_index)

    last_value_loss_index['last_value'] = index_poteri.values

    print(last_value_loss_index['last_value'])

    print(acc_loss_index)

    print("Turbine Power : ", turbine_power.values)

    print("Index Lost : ", index_poteri.values)

    print("Waterwash : ", waterwash)

    print("Cycles left to waterwash : ", cycles_left_waterwash)

    print("Waterwash alert : ", vremya_alert_waterwash)

    #predicted_cycles_left = pd.DataFrame({'waterwash_time' : cycles_left_waterwash}, index=df.index)

    #predicted_udelnyiRashodGaza = pd.DataFrame({'flow': final_data}, index=df.index)

    data_to_influx = pd.DataFrame({'power_e':turbine_power.values,

                                   'loss_index': index_poteri.values,

                                   'waterwash_status': waterwash,

                                   'status_flow': armani,

                                   'waterwash_time': cycles_left_waterwash,

                                   'vremya_waterwash_alert': vremya_alert_waterwash


                                   }, index=df.index)


   # upload_data_to_influx = writer_client.write_points(data_to_influx, 'unit_1')

    #upload_udelnyi_rashod_gaza = writer_client.write_points(predicted_udelnyiRashodGaza, 'udelnyi_rashod_predicted')

    #upload_turbine_power = writer_client.write_points(predicted_turbine_power, 'mownost_turbiny')

   # upload_index_poteri = writer_client.write_points(predicted_index_poteri, 'index_loss')

    #upload_cycles_left_waterwash = writer_client.write_points(predicted_cycles_left, 'cycles_left')

    time.sleep(20.0 - ((time.time() - starttime) % 20.0))












