import os
from influxdb import DataFrameClient
import pandas as pd    #'0.22.0'
from sklearn.externals import joblib             #The scikit-learn version is 0.19.1.
from flask import Flask, jsonify, request         #'0.12.2'
from flask import render_template
import requests
import json
from datetime import datetime, timedelta
#source ~/venvs/flaskproj/bin/activate
import numpy as np
from predict_client.prod_client import ProdClient

####Upload data to database ##########

host = '192.168.4.33'

port = 8086

user = ''

password = ''

db_name = 'Online_Classification'

####Upload data to database ##########

writer_client = DataFrameClient(host, port, user, password, db_name)

HOST = 'localhost:9000'
MODEL_NAME = 'test'
MODEL_VERSION = 1


app = Flask(__name__)

predicted_values_for_linear_regression = [ 0, 0, 0]

list_of_users = list()

dict_to_check = dict()

dict_to_check['check'] = 0

client = ProdClient(HOST, MODEL_NAME, MODEL_VERSION)

def convert_data(raw_data):

    return np.array(raw_data, dtype=np.float32)

def get_prediction_from_model(data):

    req_data = [{'in_tensor_name': 'inputs', 'in_tensor_dtype': 'DT_FLOAT', 'data': data}]

    prediction = client.predict(req_data, request_timeout=10)

    return prediction



#sudo docker run -it -p 9000:9000 --name tf-serve -v /home/user/Documents/tf_model/serve/:/serve/ epigramai/model-server:light --port=9000 --model_name=test --model_base_path=./serve/test

def comparator(data):

    if data > 30:

        return 1

    else:

        return 0

def difference(a, b):

    return ( a - b)


##############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!###############################

@app.route('/predict', methods=['POST'])

def apicall_ddd(responses2 = None):

    """API Call

    Pandas dataframe (sent as a payload) from API Call
    """
    try:

        test_json = request.get_json()

        test = pd.read_json(test_json, orient='records')


        query_df = pd.DataFrame(test.NPT)

        print(query_df)

        #query_df = test.set_index('index')

        #current_value = pd.DataFrame(test.'udelnyirashod')

        current_value = pd.DataFrame(test.FLOW)

        print(current_value)


        print("Input variables:")


        #print(query_df)

        #print(type(test))

        print(test)





    except Exception as e:

        raise e

    clf = 'lin_reg_model.pkl'

    if test.empty:

        return(bad_request())

    else:

        #Load the saved model
        #print("Loading the model...")

        lin_reg_model = None

        with open(clf,'rb') as f:

            lin_reg_model = joblib.load(f)

       # lin_reg_model = joblib.load('/home/q/new_project/models/kmeans_model.pkl')

        #print("The model has been loaded...doing predictions now...")

        predictions = lin_reg_model.predict(query_df)

        print("Last predicted value: " ,predictions)

        my_list = map(lambda x: x[0], predictions)

        print(predictions)

        armani = comparator(difference(current_value.values, predictions))

        #df_armani = pd.DataFrame({'Anomaly': armani}, index = query_df.index)

        #upload_armani = writer_client.write_points(df_armani, 'Status')

        if dict_to_check['check'] < armani:

            for k in list_of_users:

                response = requests.post(
                        url='https://api.telegram.org/bot{0}/{1}'.format("550975271:AAEXbwI63saLUWdXanZbn8KKDyu-UOGgmTc",
                                                                 "sendMessage"),
                        data={'chat_id': k, 'text': "Повышенный расход топливного газа ГПА1"}).json()

        if dict_to_check['check'] > armani:

            for k in list_of_users:
                response = requests.post(
                    url='https://api.telegram.org/bot{0}/{1}'.format(
                        "550975271:AAEXbwI63saLUWdXanZbn8KKDyu-UOGgmTc",
                        "sendMessage"),
                    data={'chat_id': k, 'text': "Проблема решена по топливному газу ГПА1"}).json()

        dict_to_check['check'] = armani




                        #350191272



        print("Anomaly is :", armani)


        #predicted_values_for_linear_regression.append(predictions)




        """Add the predictions as Series to a new pandas dataframe
                                OR
           Depending on the use-case, the entire test data appended with the new files
        """
        prediction_series = list(pd.Series(my_list))

        final_predictions = pd.DataFrame(list(zip(prediction_series)))

        """We can be as creative in sending the responses.
           But we need to send the response codes as well.
        """
        responses2 = jsonify(predictions=final_predictions.to_json(orient="records"))

        #print(final_predictions.to_json(orient="records"))

        responses2.status_code = 200

        return (responses2)



#################################################!!!!!!!!!!!!!!!!!!!!!THE FRONTEND OF LINEAR REGRESSION!!!!!!!!!!!!!!!!!!!!!!!!!!!!############################################################

@app.route('/lin-reg', methods=['GET'])

def show_lin_reg():

    return render_template('linear_regression.html', predictions=predicted_values_for_linear_regression[len(predicted_values_for_linear_regression)-1:len(predicted_values_for_linear_regression)])


#https://api.telegram.org/bot545571831:AAGpLH6S0g5ZkSVtzc6M2QHAXYwN6x0Mg04/sendMessage?chat_id=571471242&text=hello-world


#https://api.telegram.org/bot$TOKEN/sendMessage?chat_id=12345&text=Hello+World


@app.route('/users', methods=['POST'])

def register():

    """API Call

    Pandas dataframe (sent as a payload) from API Call
    """

    test_json = request.get_json()

    #test = pd.read_json(test_json, orient='records')

    #query_df = pd.DataFrame(test)

    loaded_r = json.loads(test_json)

    print(loaded_r)



    if loaded_r['Status'] == 1:

        if not loaded_r['User'] in list_of_users:

            list_of_users.append(loaded_r['User'])

        #list_of_users.append(loaded_r['User'])



        #for i in list_of_users:
         #   if i != loaded_r['User']:
          #      list_of_users.append(loaded_r['User'])

    else:
        list_of_users.remove(loaded_r['User'])

    return "done"



@app.route('/show-u', methods=['GET'])

def users():
    return render_template('users.html', users = list_of_users)

@app.route("/tf", methods=['POST'])

def get_prediction():

    req_data = request.get_json()

    the_data = json.loads(req_data)

    print(the_data)

    raw_data = the_data["data"]

    data = convert_data(raw_data)

    print(data)

    prediction = get_prediction_from_model(data)

    print("Prediction: ", prediction)

    # ndarray cannot be converted to JSON
    return jsonify({ 'predictions': prediction['outputs'].tolist() })

if __name__ == '__main__':
    app.run(host="0.0.0.0")





        #print("Input variables:")


   # print(query_df)


