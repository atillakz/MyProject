from unitclass import *

user = "userzsse"

password = "Zeinet8sse"

host = "80.241.40.230"

database = "zsse"

query_for_agp = (
    "SELECT id,unit_notready, unit_stdby,unit_run,unit_loaded, emerg_stop_blow_cnt,emrg_stop_cnt, gas_fuel_flow,hpc_flow_act,ufoh, unit_attempts, start_count FROM zsse.Unit3_Labview ORDER BY id DESC LIMIT 1")

starttime = time.time()

id_to_check = dict()

id_to_check['check'] = 0

query_insert_for_agp_one = (
    "INSERT INTO Unit3_metrics (dateandtime,USI,USC,UPPT,UFTI,UAI,USRI,URRI,UAH) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")

while True:
    print(datetime.now())

    estimator = Compute_parameters_for_unit(user, password, host, database, query_for_agp)

    estimator.connect_to_sql()

    id = estimator.prepare_data()

    dateandtime = estimator.date()

    if id_to_check['check'] != id:

        USI = estimator.usi()

        USC = estimator.usc()

        UPPT = estimator.uppt()

        UFTI = estimator.ufti()

        UAI = estimator.uai()

        USRI = estimator.usri()

        URRI = estimator.urri()

        UAH = estimator.uah()

        print(USI, USC, UPPT, UFTI, UAI, USRI, URRI, UAH)

        cnx_insert = mysql.connector.connect(user=user, password=password, host=host,
                                             database=database)
        cursor_insert = cnx_insert.cursor()

        print("ID : ", id)

        print("Data inserted into Unit3_metrics")
        print(USI, USC, UPPT, UFTI, UAI, USRI, URRI, UAH)

        cursor_insert.execute(query_insert_for_agp_one, (dateandtime, USI, USC, UPPT, UFTI, UAI, USRI, URRI, UAH))

        cnx_insert.commit()

        cnx_insert.close()

    else:
        USI = estimator.nan()

        USC = estimator.nan()

        UPPT = estimator.nan()

        UFTI = estimator.nan()

        UAI = estimator.nan()

        USRI = estimator.nan()

        URRI = estimator.nan()

        UAH = estimator.nan()

        print("Data inserted into Unit3_metrics")
        print(USI, USC, UPPT, UFTI, UAI, USRI, URRI, UAH)
        print("ID : ", id)
        # cnx_insert.commit()
        # cnx_insert.close()

    id_to_check['check'] = id

    time.sleep(35.0 - ((time.time() - starttime) % 35.0))







