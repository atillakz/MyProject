# -*- coding: utf-8 -*-
import telebot
from telebot import types
from influxdb import InfluxDBClient, DataFrameClient
import time
import numpy as np
import requests
import json




token = "550975271:AAEXbwI63saLUWdXanZbn8KKDyu-UOGgmTc"

bot = telebot.TeleBot(token, threaded=False)

## Iniatialization of keyboard markups
markup_menu_1 = types.ReplyKeyboardMarkup(row_width=1)
markup_menu_2 = types.ReplyKeyboardMarkup(row_width=1)
markup_menu_3 = types.ReplyKeyboardMarkup(row_width=1)
markup_menu_3_1 = types.ReplyKeyboardMarkup(row_width=1)
markup_menu_4 = types.ReplyKeyboardMarkup(row_width=1)
markup_menu_5 = types.ReplyKeyboardMarkup(row_width=1)
markup_menu_5_1 = types.ReplyKeyboardMarkup(row_width=1)
markup_menu_6 = types.ReplyKeyboardMarkup(row_width=1)
markup_menu_7 = types.ReplyKeyboardMarkup(row_width=1)
markup_menu_7_1 = types.ReplyKeyboardMarkup(row_width=1)

## Buttons
btn_statistics = types.KeyboardButton('Cтатистика')
btn_otchet = types.KeyboardButton('Отчет')
btn_anomalii = types.KeyboardButton('Аномалии')
btn_ks_karaozek_2 = types.KeyboardButton('КС Караозек')
btn_nazad_to_1 = types.KeyboardButton('Назад')
btn_nazad_to_2 = types.KeyboardButton('Назад')
btn_nazad_to_3= types.KeyboardButton('Назад')
btn_nazad_to_4 = types.KeyboardButton('Назад')
btn_nazad_to_5= types.KeyboardButton('Назад')
btn_nazad_to_6 = types.KeyboardButton('Назад')
btn_nazad_to_7= types.KeyboardButton('Назад')
btn_vnachalo = types.KeyboardButton('В начало')
btn_stancia_3 = types.KeyboardButton('Станция')
btn_gpa1_3 = types.KeyboardButton('ГПА 1')
btn_gpa2_3 = types.KeyboardButton('ГПА 2')
btn_gpa3_3 = types.KeyboardButton('ГПА 3')
btn_stancia = types.KeyboardButton('Станция')
btn_ks_karaozek_4 = types.KeyboardButton('КС Караозек')
btn_sutki_5 = types.KeyboardButton('Час')
btn_nedelia_5 = types.KeyboardButton('Сутки')
btn_mesiac_5 = types.KeyboardButton('Неделя')
btn_god_5 = types.KeyboardButton('Месяц')
btn_da_6 = types.KeyboardButton('Да')
btn_net_6 = types.KeyboardButton('Нет')
btn_ks_karaozek_7 = types.KeyboardButton('КС Караозек')
btn_otkaz_podpisok_7_1 = types.KeyboardButton('Отказаться от всех подписок')

## Markup menu
markup_menu_1.add(btn_statistics, btn_otchet, btn_anomalii)
markup_menu_2.add(btn_ks_karaozek_2, btn_nazad_to_1)
markup_menu_3.add(btn_stancia_3, btn_gpa1_3, btn_gpa2_3, btn_gpa3_3, btn_nazad_to_2, btn_vnachalo)
markup_menu_3_1.add(btn_nazad_to_3, btn_vnachalo)
markup_menu_4.add(btn_ks_karaozek_4, btn_nazad_to_1)
markup_menu_5.add(btn_sutki_5, btn_nedelia_5, btn_mesiac_5, btn_god_5, btn_nazad_to_4, btn_vnachalo)
markup_menu_5_1.add(btn_nazad_to_5, btn_vnachalo)
markup_menu_6.add(btn_da_6, btn_net_6, btn_otkaz_podpisok_7_1)
markup_menu_7.add(btn_ks_karaozek_7, btn_nazad_to_6, btn_vnachalo)
markup_menu_7_1.add(btn_nazad_to_7, btn_vnachalo)


user_step = {}

print("Telegram bot is running!")
bot.send_message(350191272, "Server was started. Please /start it.")

def get_user_step(cid):
    if cid in user_step:
        return user_step[cid]
    else:
        user_step[cid] = 1
        return




@bot.message_handler(commands=["start"])
def keyboard (message):
    cid = message.chat.id
    user_step[cid] = 1
    bot.send_message(message.chat.id, "Выберите действие",reply_markup=markup_menu_1)


## Menu when user choose title from main menu
@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1)
def main_menu(message):
    cid = message.chat.id
    if message.text == "Cтатистика":
        user_step[cid] = 2
        bot.send_message(message.chat.id, "Выберите КС", reply_markup=markup_menu_2)
    elif message.text == "Отчет":
        user_step[cid] = 4
        bot.send_message(message.chat.id,"Выберите КС",reply_markup=markup_menu_4)
    elif message.text == "Аномалии":
        user_step[cid] = 6
        bot.send_message(message.chat.id,"Желаете ли Вы подписаться на уведомление аномалий?",reply_markup=markup_menu_6)




## Menu when user choose statistics
@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==2)
def main_menu(message):
    cid = message.chat.id
    if message.text == "КС Караозек":
        user_step[cid] = 3
        bot.send_message(message.chat.id, "Выберите объект", reply_markup=markup_menu_3)
    elif message.text == "Назад":
        user_step[cid] = 1
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_menu_1)



## Menu when user choose statistics/ks karaozek
@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3)
def main_menu(message):
    cid = message.chat.id
    client = InfluxDBClient('192.168.4.33', 8086, 'test', '12345', 'Labview')
    client2 = InfluxDBClient('192.168.4.33', 8086, 'test', '12345', 'metricdata')
    rs = client.query("SELECT * from Unit1 GROUP BY * ORDER BY DESC LIMIT 1;")
    rs_1 = client.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
    rs2 = client2.query("SELECT * from unit1 GROUP BY * ORDER BY DESC LIMIT 1;")
    data1 = list(rs.get_points())
    data2 = list(rs2.get_points())
    data3 =list(rs_1.get_points())
    rs2_stat = client2.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
    data4 = list(rs2_stat.get_points())


    try:
        dict_data = data1[0]
        dict_data_ss = data2[0]
        dict_data_stat = data3[0]
        dict_data_ss_stat = data4[0]
    except:
        dict_data_ss_stat['SAI'] = "No data"
        dict_data_ss_stat['SFTI'] = "No data"
        dict_data_ss_stat['SRRI'] = "No data"
        dict_data_stat['total_unit_run'] = "No data"
        dict_data_stat['press_in'] = "No data"
        press_out = "No data"
        status['choice'] = "No data"
        dict_data['start_count'] = "No data"
        dict_data['engine_fired_hours'] = "No data"
        dict_data['emrg_stop_cnt'] = "No data"
        UAI_CM = "No data"
        dict_data_ss['UFTI'] = "No data"
        dict_data_ss['URRI'] = "No data"
        dict_data_ss['UAH'] = "No data"
        dict_data_ss['URRI'] = "No data"
        dict_data['hpc_eta'] = "No data"
        dict_data['hpc_turndown'] = "No data"



    press_out = round(dict_data_stat['press_out'], 2)
    try:
        UAI_CM = round(dict_data_ss['UAI'], 2)
    except:
        UAI_CM = "No data"
    try:
        UAH_CM = round(dict_data_ss['UAH'], 2)
    except:
        UAH_CM = "No data"

    try:
        URRI_CM = round(dict_data_ss['URRI'], 2)
    except:
        URRI_CM = "No data"

    try:
        SAI_CM = round(dict_data_ss_stat['SAI'], 2)
    except:
        SAI_CM = "No data"

    try:
        SRRI_CM = round(dict_data_ss_stat['SRRI'], 2)
    except:
        SRRI_CM = "No data"

    try:
        URRI_CM = round(dict_data_ss['URRI'], 2)
    except:
        URRI_CM = "No data"


    status = dict()
    status['choice'] = 0


    if message.text == "Станция":
        user_step[cid] = 8
        text_1 = """
        KPI:
        - Готовность станций: *{}%*
        - Производительность станций: *{}%*
        - Надежность станций: *{}%*
        - Количество ГПА в работе: *{}*.
        - Давление на входе станций: *{}МПа*
        - Давление на выходе станций: *{}Мпа*
        """.format(SAI_CM, dict_data_ss_stat['SFTI'], SRRI_CM, dict_data_stat['total_unit_run'], dict_data_stat['press_in'], press_out)
        bot.send_message(message.chat.id, text_1, parse_mode='Markdown', reply_markup=markup_menu_3_1)

    elif message.text == "ГПА 1":
        user_step[cid] = 8

        if dict_data_ss['USI'] == 1:
            status['choice'] = 'Не готов'

        if dict_data_ss['USI'] == 2:
            status['choice'] = 'В резерве'

        if dict_data_ss['USI'] == 3:
            status['choice'] = 'В работе'

        if dict_data_ss['USI'] == 4:
            status['choice'] = 'Магистраль'



        text_2 = """
        ГПА1: {}.
        Счетчики:
        - Количество пусков: *{}*
        - Количество часов: *{}ч.*
        - Количество АО: *{}*
        Эффективность:
        Готовность: *{}%*
        Производительность: *{}%*
        Надежность: *{}%*
        Заплан. время до ТО: *{}ч.*
        КПД(относит.): 30%
        Fuel Transport Index: *{}%*
        HPC Efficiency: *{}%*
        Соотношение ExhaustTT к скорости OK:
        Соотношение темп-ры воздуха (TIT):
        Запас по помпажу (TRD): *{}*
        """.format(status['choice'], dict_data['start_count'], dict_data['engine_fired_hours'], dict_data['emrg_stop_cnt'], UAI_CM, dict_data_ss['UFTI'], URRI_CM, UAH_CM,
                   URRI_CM, dict_data['hpc_eta'], dict_data['hpc_turndown'])
        bot.send_message(message.chat.id, text_2, parse_mode='Markdown', reply_markup=markup_menu_3_1)

    elif message.text == "ГПА 2":
        user_step[cid] = 8

        if dict_data_ss['USI'] == 1:
            status['choice'] = 'Не готов'

        if dict_data_ss['USI'] == 2:
            status['choice'] = 'В резерве'

        if dict_data_ss['USI'] == 3:
            status['choice'] = 'В работе'

        if dict_data_ss['USI'] == 4:
            status['choice'] = 'Магистраль'

        text_3 = """
        ГПА2: {}.
        Счетчики:
        - Количество пусков: *{}*
        - Количество часов: *{}ч.*
        - Количество АО: *{}*
        Эффективность:
        Готовность: *{}%*
        Производительность: *{}%*
        Надежность: *{}%*
        Заплан. время до ТО: *{}ч.*
        КПД(относит.): 30%
        Fuel Transport Index: *{}%*
        HPC Efficiency: *{}%*
        Соотношение ExhaustTT к скорости OK:
        Соотношение темп-ры воздуха (TIT):
        Запас по помпажу (TRD): *{}*
        """.format(status['choice'], dict_data['start_count'], dict_data['engine_fired_hours'], dict_data['emrg_stop_cnt'], UAI_CM, dict_data_ss['UFTI'], URRI_CM, UAH_CM,
                   URRI_CM, dict_data['hpc_eta'], dict_data['hpc_turndown'])
        bot.send_message(message.chat.id, text_3, parse_mode='Markdown', reply_markup=markup_menu_3_1)

    elif message.text == "ГПА 3":
        user_step[cid] = 8

        if dict_data_ss['USI'] == 1:
            status['choice'] = 'Не готов'

        if dict_data_ss['USI'] == 2:
            status['choice'] = 'В резерве'

        if dict_data_ss['USI'] == 3:
            status['choice'] = 'В работе'

        if dict_data_ss['USI'] == 4:
            status['choice'] = 'Магистраль'

        text_4 = """
        ГПА3: {}.
        Счетчики:
        - Количество пусков: *{}*
        - Количество часов: *{}ч.*
        - Количество АО: *{}*
        Эффективность:
        Готовность: *{}%*
        Производительность: *{}%*
        Надежность: *{}%*
        Заплан. время до ТО: *{}ч.*
        КПД(относит.): 30%
        Fuel Transport Index: *{}%*
        HPC Efficiency: *{}%*
        Соотношение ExhaustTT к скорости OK:
        Соотношение темп-ры воздуха (TIT):
        Запас по помпажу (TRD): *{}*
        """.format(status['choice'], dict_data['start_count'], dict_data['engine_fired_hours'], dict_data['emrg_stop_cnt'], UAI_CM, dict_data_ss['UFTI'], URRI_CM, UAH_CM,
                   URRI_CM, dict_data['hpc_eta'], dict_data['hpc_turndown'])
        bot.send_message(message.chat.id, text_4, parse_mode='Markdown', reply_markup=markup_menu_3_1)

    elif message.text == "Назад":
        user_step[cid] = 2
        bot.send_message(message.chat.id, "Выберите КС", reply_markup=markup_menu_2)

    elif message.text == "В начало":
        user_step[cid] = 1
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_menu_1)


## Menu when user choose statistics/stancia or gpa1-3
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 8)
def main_menu(message):
    cid = message.chat.id

    if message.text == "Назад":
        user_step[cid] = 3
        bot.send_message(message.chat.id, "Выберите объект", reply_markup=markup_menu_3)

    elif message.text == "В начало":
        user_step[cid] = 1
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_menu_1)




## Menu when user choose otchet
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 4)
def main_menu(message):
    cid = message.chat.id
    if message.text == "КС Караозек":
        user_step[cid] = 5
        bot.send_message(message.chat.id, "Выберите диапазон времени", reply_markup=markup_menu_5)
    elif message.text == "Назад":
        user_step[cid] = 1
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_menu_1)





## Menu when user choose otchet/ ks karaozek
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 5)
def main_menu(message):
    cid = message.chat.id
    client = InfluxDBClient('192.168.4.33', 8086, 'test', '12345', 'Labview')
    client2 = InfluxDBClient('192.168.4.33', 8086, 'test', '12345', 'metricdata')

    if message.text == "Час":
        user_step[cid] = 9
        rs5 = client.query("SELECT * from station WHERE TIME > now() - 1h;")
        data5 = list(rs5.get_points())
        rs6 = client.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
        data6 = list(rs6.get_points())

        rs7 = client.query("SELECT * from Unit1 WHERE TIME > now() - 1h;")
        data7 = list(rs7.get_points())
        rs8 = client.query("SELECT * from Unit1 GROUP BY * ORDER BY DESC LIMIT 1;")
        data8 = list(rs8.get_points())
        rs_ss_1 = client2.query("SELECT * from station WHERE TIME > now() - 1h;")
        data9 = list(rs_ss_1.get_points())
        rs_ss_2 = client2.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
        data10 = list(rs_ss_2.get_points())



        try:
            dict_data_day_before = data5[0]
            dict_data_current = data6[0]
        except:
            pass

        try:
            dict_data_day_before_stat_ss = data9[0]
            dict_data_current_stat_ss = data10[0]
        except:
            pass

        try:
            dict_data_day_before_u1 = data7[0]
            dict_data_current_u1 = data8[0]
        except:
            pass




        try:
            gas_common = round(dict_data_current['gas_common'] - dict_data_day_before['gas_common'], 2)
        except:
            gas_common = 'NO data'

        try:
            gas_losses = round(dict_data_current['gas_losses'] - dict_data_day_before['gas_losses'], 2)
        except:
            gas_losses = 'NO data'

        try:
            fuel_gas_common = round(dict_data_current['fuel_gas_common'] - dict_data_day_before['fuel_gas_common'], 2)
        except:
            fuel_gas_common = 'NO data'

        try:
            power_com = round(dict_data_current['power_com'] - dict_data_day_before['power_com'], 2)
        except:
            power_com = 'NO data'




        try:
            gas_total_u1 = round(dict_data_current_u1['gas_total'] - dict_data_day_before_u1['gas_total'], 2)
            fuel_gas_total_u1 = round(dict_data_current_u1['fuel_gas_total'] - dict_data_day_before_u1['fuel_gas_total'], 2)
            gas_spent_total_u1 = round(dict_data_current_u1['gas_spent_total'] - dict_data_day_before_u1['gas_spent_total'], 2)
        except:
            gas_total_u1 = 'NO data'
            fuel_gas_total_u1 = 'NO data'
            gas_spent_total_u1 = 'NO data'


        try:
            ssd = dict_data_current_stat_ss['SSD'] - dict_data_day_before_stat_ss['SSD']
        except:
            ssd = 'NO data'



        text_1 = """
        Станция:
        - Транспорт газа: *{} млн м3*
        - Потребление газа: *{} м3*
        - Потери техн. газа: *{} м3*
        - Потребление электроэнерг.: *{}* MW
        - Аварийные остановы: *{}*

        ГПА 1
        - Транспорт газа: *{} млн м3*
        - Потребление газа: *{} м3*
        - Потери техн. газа: *{} м3*

        ГПА 2
        - Транспорт газа: xxx млн м3
        - Потребление газа: xxx м3
        - Потери техн. газа: xxx м3

        ГПА 3
        - Транспорт газа: xxx млн м3
        - Потребление газа: xxx м3
        - Потери техн. газа: xxx м3
        """.format(gas_common, fuel_gas_common, gas_losses, power_com, ssd,  gas_total_u1, fuel_gas_total_u1, gas_spent_total_u1)
        bot.send_message(message.chat.id, text_1, parse_mode='Markdown', reply_markup=markup_menu_5_1)

    elif message.text == "Сутки":
        user_step[cid] = 9
        rs5 = client.query("SELECT * from station WHERE TIME > now() - 1d;")
        data5 = list(rs5.get_points())
        rs6 = client.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
        data6 = list(rs6.get_points())

        rs7 = client.query("SELECT * from Unit1 WHERE TIME > now() - 1d;")
        data7 = list(rs7.get_points())
        rs8 = client.query("SELECT * from Unit1 GROUP BY * ORDER BY DESC LIMIT 1;")
        data8 = list(rs8.get_points())
        rs_ss_1 = client2.query("SELECT * from station WHERE TIME > now() - 1d;")
        data9 = list(rs_ss_1.get_points())
        rs_ss_2 = client2.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
        data10 = list(rs_ss_2.get_points())

        try:
            dict_data_day_before = data5[0]
            dict_data_current = data6[0]
        except:
            pass

        try:
            dict_data_day_before_stat_ss = data9[0]
            dict_data_current_stat_ss = data10[0]
        except:
            pass

        try:
            dict_data_day_before_u1 = data7[0]
            dict_data_current_u1 = data8[0]
        except:
            pass


## Catch exception when on of get data as none
        try:
            gas_common = round(dict_data_current['gas_common'] - dict_data_day_before['gas_common'], 2)
        except:
            gas_common = 'NO data'

        try:
            gas_losses = round(dict_data_current['gas_losses'] - dict_data_day_before['gas_losses'], 2)
        except:
            gas_losses = 'NO data'

        try:
            fuel_gas_common = round(dict_data_current['fuel_gas_common'] - dict_data_day_before['fuel_gas_common'], 2)
        except:
            fuel_gas_common = 'NO data'

        try:
            power_com = round(dict_data_current['power_com'] - dict_data_day_before['power_com'], 2)
        except:
            power_com = 'NO data'


        try:
            gas_total_u1 = round(dict_data_current_u1['gas_total'] - dict_data_day_before_u1['gas_total'], 2)
            fuel_gas_total_u1 = round(
                dict_data_current_u1['fuel_gas_total'] - dict_data_day_before_u1['fuel_gas_total'], 2)
            gas_spent_total_u1 = round(
                dict_data_current_u1['gas_spent_total'] - dict_data_day_before_u1['gas_spent_total'], 2)
        except:
            gas_total_u1 = 'NO data'
            fuel_gas_total_u1 = 'NO data'
            gas_spent_total_u1 = 'NO data'

        try:
            ssd = dict_data_current_stat_ss['SSD'] - dict_data_day_before_stat_ss['SSD']
        except:
            ssd = 'NO data'


        text_3 = """
        Станция:
        - Транспорт газа: *{} млн м3*
        - Потребление газа: *{} м3*
        - Потери техн. газа: *{} м3*
        - Потребление электроэнерг.: *{}* MW
        - Аварийные остановы: *{}*

        ГПА 1
        - Транспорт газа: *{} млн м3*
        - Потребление газа: *{} м3*
        - Потери техн. газа: *{} м3*

        ГПА 2
        - Транспорт газа: xxx млн м3
        - Потребление газа: xxx м3
        - Потери техн. газа: xxx м3

        ГПА 3
        - Транспорт газа: xxx млн м3
        - Потребление газа: xxx м3
        - Потери техн. газа: xxx м3
        """.format(gas_common, fuel_gas_common, gas_losses, power_com, ssd, gas_total_u1, fuel_gas_total_u1,
                   gas_spent_total_u1)
        bot.send_message(message.chat.id, text_3, parse_mode='Markdown', reply_markup=markup_menu_5_1)

    elif message.text == "Неделя":
        user_step[cid] = 9
        rs5 = client.query("SELECT * from station WHERE TIME > now() - 1w;")
        data5 = list(rs5.get_points())
        rs6 = client.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
        data6 = list(rs6.get_points())

        rs7 = client.query("SELECT * from Unit1 WHERE TIME > now() - 1w;")
        data7 = list(rs7.get_points())
        rs8 = client.query("SELECT * from Unit1 GROUP BY * ORDER BY DESC LIMIT 1;")
        data8 = list(rs8.get_points())
        rs_ss_1 = client2.query("SELECT * from station WHERE TIME > now() - 1w;")
        data9 = list(rs_ss_1.get_points())
        rs_ss_2 = client2.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
        data10 = list(rs_ss_2.get_points())

        try:
            dict_data_day_before = data5[0]
            dict_data_current = data6[0]
        except:
            pass

        try:
            dict_data_day_before_stat_ss = data9[0]
            dict_data_current_stat_ss = data10[0]
        except:
            pass

        try:
            dict_data_day_before_u1 = data7[0]
            dict_data_current_u1 = data8[0]
        except:
            pass

        try:
            gas_common = round(dict_data_current['gas_common'] - dict_data_day_before['gas_common'], 2)
        except:
            gas_common = 'NO data'

        try:
            gas_losses = round(dict_data_current['gas_losses'] - dict_data_day_before['gas_losses'], 2)
        except:
            gas_losses = 'NO data'

        try:
            fuel_gas_common = round(dict_data_current['fuel_gas_common'] - dict_data_day_before['fuel_gas_common'], 2)
        except:
            fuel_gas_common = 'NO data'

        try:
            power_com = round(dict_data_current['power_com'] - dict_data_day_before['power_com'], 2)
        except:
            power_com = 'NO data'



        try:
            gas_total_u1 = round(dict_data_current_u1['gas_total'] - dict_data_day_before_u1['gas_total'], 2)
            fuel_gas_total_u1 = round(
                dict_data_current_u1['fuel_gas_total'] - dict_data_day_before_u1['fuel_gas_total'], 2)
            gas_spent_total_u1 = round(
                dict_data_current_u1['gas_spent_total'] - dict_data_day_before_u1['gas_spent_total'], 2)
        except:
            gas_total_u1 = 'NO data'
            fuel_gas_total_u1 = 'NO data'
            gas_spent_total_u1 = 'NO data'

        try:
            ssd = dict_data_current_stat_ss['SSD'] - dict_data_day_before_stat_ss['SSD']
        except:
            ssd = 'NO data'

        text_4 = """
        Станция:
        - Транспорт газа: *{} млн м3*
        - Потребление газа: *{} м3*
        - Потери техн. газа: *{} м3*
        - Потребление электроэнерг.: *{}* MW
        - Аварийные остановы: *{}*

        ГПА 1
        - Транспорт газа: *{} млн м3*
        - Потребление газа: *{} м3*
        - Потери техн. газа: *{} м3*

        ГПА 2
        - Транспорт газа: xxx млн м3
        - Потребление газа: xxx м3
        - Потери техн. газа: xxx м3

        ГПА 3
        - Транспорт газа: xxx млн м3
        - Потребление газа: xxx м3
        - Потери техн. газа: xxx м3
        """.format(gas_common, fuel_gas_common, gas_losses, power_com, ssd, gas_total_u1, fuel_gas_total_u1,
                   gas_spent_total_u1)
        bot.send_message(message.chat.id, text_4, parse_mode='Markdown', reply_markup=markup_menu_5_1)

    elif message.text == "Месяц":
        user_step[cid] = 9
        rs5 = client.query("SELECT * from station WHERE TIME > now() - 1m;")
        data5 = list(rs5.get_points())
        rs6 = client.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
        data6 = list(rs6.get_points())

        rs7 = client.query("SELECT * from Unit1 WHERE TIME > now() - 1m;")
        data7 = list(rs7.get_points())
        rs8 = client.query("SELECT * from Unit1 GROUP BY * ORDER BY DESC LIMIT 1;")
        data8 = list(rs8.get_points())
        rs_ss_1 = client2.query("SELECT * from station WHERE TIME > now() - 1m;")
        data9 = list(rs_ss_1.get_points())
        rs_ss_2 = client2.query("SELECT * from station GROUP BY * ORDER BY DESC LIMIT 1;")
        data10 = list(rs_ss_2.get_points())

        try:
            dict_data_day_before = data5[0]
            dict_data_current = data6[0]
        except:
            pass

        try:
            dict_data_day_before_stat_ss = data9[0]
            dict_data_current_stat_ss = data10[0]
        except:
            pass

        try:
            dict_data_day_before_u1 = data7[0]
            dict_data_current_u1 = data8[0]
        except:
            pass

        ## Catch exception when on of get data as none
        try:
            gas_common = round(dict_data_current['gas_common'] - dict_data_day_before['gas_common'], 2)
        except:
            gas_common = 'NO data'

        try:
            gas_losses = round(dict_data_current['gas_losses'] - dict_data_day_before['gas_losses'], 2)
        except:
            gas_losses = 'NO data'

        try:
            fuel_gas_common = round(dict_data_current['fuel_gas_common'] - dict_data_day_before['fuel_gas_common'],
                                    2)
        except:
            fuel_gas_common = 'NO data'

        try:
            power_com = round(dict_data_current['power_com'] - dict_data_day_before['power_com'], 2)
        except:
            power_com = 'NO data'

        try:
            gas_total_u1 = round(dict_data_current_u1['gas_total'] - dict_data_day_before_u1['gas_total'], 2)
            fuel_gas_total_u1 = round(
                dict_data_current_u1['fuel_gas_total'] - dict_data_day_before_u1['fuel_gas_total'], 2)
            gas_spent_total_u1 = round(
                dict_data_current_u1['gas_spent_total'] - dict_data_day_before_u1['gas_spent_total'], 2)
        except:
            gas_total_u1 = 'NO data'
            fuel_gas_total_u1 = 'NO data'
            gas_spent_total_u1 = 'NO data'

        try:
            ssd = dict_data_current_stat_ss['SSD'] - dict_data_day_before_stat_ss['SSD']
        except:
            ssd = 'NO data'



        text_5 = """
        Станция:
        - Транспорт газа: *{} млн м3*
        - Потребление газа: *{} м3*
        - Потери техн. газа: *{} м3*
        - Потребление электроэнерг.: *{}* MW
        - Аварийные остановы: *{}*

        ГПА 1
        - Транспорт газа: *{} млн м3*
        - Потребление газа: *{} м3*
        - Потери техн. газа: *{} м3*

        ГПА 2
        - Транспорт газа: xxx млн м3
        - Потребление газа: xxx м3
        - Потери техн. газа: xxx м3

        ГПА 3
        - Транспорт газа: xxx млн м3
        - Потребление газа: xxx м3
        - Потери техн. газа: xxx м3
        """.format(gas_common, fuel_gas_common, gas_losses, power_com, ssd, gas_total_u1, fuel_gas_total_u1,
                   gas_spent_total_u1)
        bot.send_message(message.chat.id, text_5, parse_mode='Markdown', reply_markup=markup_menu_5_1)

    elif message.text == "Назад":
        user_step[cid] = 4
        bot.send_message(message.chat.id, "Выберите КС", reply_markup=markup_menu_4)

    elif message.text == "В начало":
        user_step[cid] = 1
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_menu_1)



## Menu when user choose otchet/ ks karaozek / den - god
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 9)
def main_menu(message):
    cid = message.chat.id

    if message.text == "Назад":
        user_step[cid] = 5
        bot.send_message(message.chat.id, "Выберите диапазон времени", reply_markup=markup_menu_5)

    elif message.text == "В начало":
        user_step[cid] = 1
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_menu_1)




## Menu when user choose anomalii
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 6)
def main_menu(message):
    cid = message.chat.id
    last_name = message.chat.last_name
    first_name = message.chat.first_name
    if message.text == "Да":
        user_step[cid] = 7
        text_1 = """
                Выберите КС
                """
        bot.send_message(message.chat.id, text_1, reply_markup=markup_menu_7)

    elif message.text == "Отказаться от всех подписок":

        header = {'Content-Type': 'application/json',

                  'Accept': 'application/json'}

        data1 = {}

        data1['User'] = cid

        data1['Status'] = 0

        data2 = json.dumps(data1)
        print(str(first_name) + " " + str(last_name) + " unsubscribed from anomaly")
        try:
            response = requests.post(
            url='http://localhost:5000/users',
            data=json.dumps(data2), headers=header)

        except:
            print('Print host can not connect')
            pass

        user_step[cid] = 1
        bot.send_message(message.chat.id, "Вы отписались!", reply_markup=markup_menu_1)


    elif message.text == "Нет":
            user_step[cid] = 1
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_menu_1)


## Menu when user choose anomalii/ da
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 7)
def main_menu(message):
    cid = message.chat.id
    last_name = message.chat.last_name
    first_name = message.chat.first_name
    if message.text == "КС Караозек":

        header = {'Content-Type': 'application/json',
                  'Accept': 'application/json'}
        data1 = dict()
        data1['User'] = cid
        data1['Status'] = 1
        data2 = json.dumps(data1)
        print(str(first_name)+" "+str(last_name)+" subscribed to anomaly")
        try:
            response = requests.post(
            url='http://localhost:5000/users',
            data=json.dumps(data2), headers=header)
        except:
            print('Print host can not connect')
            pass
        user_step[cid] = 10
        text_1 = """
                Вы оформили подписку и будете получать уведомление по аномалиям КС Караозек.
                """
        bot.send_message(message.chat.id, text_1, reply_markup=markup_menu_7_1)

    elif message.text == "Назад":
        user_step[cid] = 6
        bot.send_message(message.chat.id, "Желаете ли Вы подписаться на уведомление аномалий?", reply_markup=markup_menu_6)

    elif message.text == "В начало":
        user_step[cid] = 1
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_menu_1)



## Menu when user choose anomalii/ da /
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 10)
def main_menu(message):
    cid = message.chat.id

    if message.text == "Назад":
        user_step[cid] = 6
        bot.send_message(message.chat.id, "Желаете ли Вы подписаться на уведомление аномалий?", reply_markup=markup_menu_6)

    elif message.text == "В начало":
        user_step[cid] = 1
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_menu_1)



if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, timeout = 300)
        except Exception as e:
            print(e)
            time.sleep(5)
# bot.polling(none_stop=True, interval = 0, timeout = 180)





