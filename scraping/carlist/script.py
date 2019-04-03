# -*- coding: utf-8 -*-
import re
import xlwt
from datetime import datetime
import html
import os
import xlrd
import requests
import time
import operator

P_ID = 1
PAGE_SIZE = 26
PRINT_DETAIL = False

sheet1_data = [['UID', 'Card url', 'Brand', 'Make', 'Model',  'Variant', 'Year of Make', 'Engine Capacity', 'Transmission', 'Seat Capacity',
      'Mileage', 'Resale Price (RM)', 'Colour']]
sheet2_data = [['UID', 'Air Conditioning', 'Interior Lighting', 'Power Driver Seat', 'Power Steering', 'Sunroof', 'Other']]
sheet3_data = [['UID', 'Auto Wipers', 'Cruise Control', 'Engine Start', 'Hill Start Assist', 'Navigation', 'Parking Brake', 'Parking Sensor', 'Steering Wheel Control', 'Other']]
sheet4_data = [['UID', 'AUX', 'Bluetooth', 'Radio', 'Other']]
sheet5_data = [['UID', 'ABS/SBD', 'Curtain Airbags', 'Front Airbags', 'Stability Control', 'Other']]

cookie = '_csrf=P1qIMBendS3J6ZzotwkgXeQy0RrmxxVF; _ga=GA1.2.1957316965.1553824904; _gcl_au=1.1.807367197.1553824905; visitorTrackingId=7717dfcd-5bc6-4fc1-8e7e-65fed034c2ab; visitorSessionId=4b8b9539-9ceb-449c-920f-e36fb0397334; cto_lwid=fe9cb052-688f-4fd7-a7d8-bdbf24bb2f0c; G_ENABLED_IDPS=google; _gid=GA1.2.1527615779.1553943435; recentView_car=%5B%225627129%22%5D; _gaexp=GAX1.2.URLeoZMdSAGkowcjnIwSyw.18069.0; noLanguageRedirect=true'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)

    i = 0
    while len(alldata) > 65500:
        _filename = filename.replace('.xls', '_%s.xls' % i)
        start_index = 0
        end_index = 65500
        data = alldata[start_index:end_index]
        alldata = alldata[end_index:]
        w = xlwt.Workbook(encoding='utf-8')
        ws = w.add_sheet('old', cell_overwrite_ok=True)
        for row in range(0, len(data)):
            one_row = data[row]
            for col in range(0, len(one_row)):
                try:
                    ws.write(row, col, one_row[col][:32766])
                except:
                    try:
                        ws.write(row, col, one_row[col])
                    except:
                        print('===Write excel ERROR===' + str(one_row[col]))
        w.save(_filename)
        print("%s===========over============%d" % (_filename, len(data)))
        i += 1
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col][:32766])
            except:
                try:
                    ws.write(row, col, one_row[col])
                except:
                    print('===Write excel ERROR===' + str(one_row[col]))
    w.save(filename)
    print("%s===========over============%d" % (filename, len(alldata)))


def request_sheet1(url):
    reg = 'js-ellipsize-text".*? href="(.*?)".*?listing__price.*?">(.*?)<'
    html = get_request(url)
    data_list = re.compile(reg).findall(html)

    for data in data_list:
        url = data[0]
        price = data[1]
        request_sheet2(url, price)


def request_sheet2(url, price):
    global P_ID
    try:
        headline_Reg = 'h1 class="headline.*?>(.*?)</h1.*?listing__section--key-details(.*?)seven-tenths'
        detail_reg = 'h3 class="specifications__title.*?>(.*?)</h3(.*?)/div> *?</div'
        html = get_request(url)

        headline_data = re.compile(headline_Reg).findall(html)
        headline = remove_html_tag(headline_data[0][0])
        detail_raw = headline_data[0][1]
        get_detail(url, price, headline, detail_raw)

        detail_list = re.compile(detail_reg).findall(html)
        for detail in detail_list:
            if detail[0] == 'Comfort':
                get_comfort(detail[1])
            elif detail[0] == 'Convenience':
                get_convenience(detail[1])
            elif detail[0] == 'Entertainment':
                get_entertainment(detail[1])
            elif detail[0] == 'Safety':
                get_safety(detail[1])

        P_ID += 1
    except Exception as e:
        print('EXP-2', url, e)


def get_comfort(html):
    global sheet2_data, P_ID
    item_list = get_item_detail(html)

    # [['UID', 'Air Conditioning', 'Interior Lighting', 'Power Driver Seat', 'Power Steering', 'Sunroof']]
    Air_conditioning = 'N/A'
    Interior_Lighting = 'N/A'
    Power_driver_seat = 'N/A'
    power_steeting = 'N/A'
    sun_roof = 'N/A'
    others = []

    for item in item_list:
        if item[0] == 'Air-conditioning':
            Air_conditioning = item[1]
        elif item[0] == 'Interior lighting':
            Interior_Lighting = item[1]
        elif item[0] == 'Power steering':
            power_steeting = item[1]
        elif item[0] == 'Power driver seat':
            Power_driver_seat = item[1]
        elif item[0] == 'Sunroof':
            sun_roof = item[1]
        else:
            others.append(item[1])

    for other in others:
        one_row = ['MZ-%d' % P_ID, Air_conditioning, Interior_Lighting, Power_driver_seat, power_steeting, sun_roof, other]
        sheet2_data.append(one_row)
        if PRINT_DETAIL:
            print(one_row)


def get_convenience(html):
    global sheet3_data, P_ID
    item_list = get_item_detail(html)

    # [['UID', 'Auto Wipers', 'Cruise Control', 'Engine Start', 'Hill Start Assist', 'Navigation', 'Parking Brake', 'Parking Sensor', 'Steering Wheel Control', 'Other']]
    auto_wipers = 'N/A'
    cruise_control = 'N/A'
    engine_start = 'N/A'
    hill_start = 'N/A'
    navigation = 'N/A'
    parking_brake = 'N/A'
    parking_sensor = 'N/A'
    steering = 'N/A'
    others = []

    for item in item_list:
        if item[0] == 'Auto wipers':
            auto_wipers = item[1]
        elif item[0] == 'Cruise control':
            cruise_control = item[1]
        elif item[0] == 'Engine start':
            engine_start = item[1]
        elif item[0] == 'Parking sensor':
            parking_sensor = item[1]
        elif item[0] == 'Steering wheel controls':
            steering = item[1]
        elif item[0] == 'Navigation':
            navigation = item[1]
        elif item[0] == 'Parking brake':
            parking_brake = item[1]
        elif item[0] == 'Hill start assist':
            hill_start = item[1]
        else:
            others.append(item[1])

    for other in others:
        one_row = ['MZ-%d' % P_ID, auto_wipers, cruise_control, engine_start, hill_start, navigation, parking_brake, parking_sensor, steering, other]
        sheet3_data.append(one_row)
        if PRINT_DETAIL:
            print(one_row)


def get_entertainment(html):
    global sheet4_data, P_ID
    item_list = get_item_detail(html)

    # [['UID', 'AUX', 'Bluetooth', 'Radio']]
    AUX = 'N/A'
    Bluetooth = 'N/A'
    Radio = 'N/A'
    others = []

    for item in item_list:
        if item[0] == 'Aux':
            AUX = item[1]
        elif item[0] == 'Bluetooth':
            Bluetooth = item[1]
        elif item[0] == 'Radio':
            Radio = item[1]
        else:
            others.append(item[1])

    for other in others:
        one_row = ['MZ-%d' % P_ID, AUX, Bluetooth, Radio, other]
        sheet4_data.append(one_row)
        if PRINT_DETAIL:
            print(one_row)


def get_safety(html):
    global sheet5_data, P_ID
    item_list = get_item_detail(html)

    # [['UID', 'ABS/SBD', 'Curtain Airbags', 'Front Airbags', 'Stability Control', 'Other']]
    abs_sbd = 'N/A'
    curtain_airbags = 'N/A'
    front_airbags = 'N/A'
    stability = 'N/A'

    others = []

    for item in item_list:
        if item[0] == 'ABS/EBD':
            abs_sbd = item[1]
        elif item[0] == 'Front Airbags':
            front_airbags = item[1]
        elif item[0] == 'Stability control':
            stability = item[1]
        elif item[0] == 'Curtain Airbags':
            curtain_airbags = item[1]
        else:
            others.append(item[1])

    for other in others:
        one_row = ['MZ-%d' % P_ID, abs_sbd, curtain_airbags, front_airbags, stability, other]
        sheet5_data.append(one_row)
        if PRINT_DETAIL:
            print(one_row)


def get_detail(url, price, headline, html):
    global sheet1_data, P_ID
    item_list = get_item_detail(html)

    one_row = ['N/A' for i in range(13)]
    one_row[0] = 'MZ-%d' % P_ID
    one_row[1] = url
    one_row[3] = headline
    one_row[-2] = price

    # [['UID', 'Card url', 'Brand', 'Make', 'Model', 'Variant', 'Year of Make', 'Engine Capacity', 'Transmission',
    # 'Seat Capacity', 'Mileage', 'Resale Price (RM)', 'Colour']]

    for item in item_list:
        if item[0] == 'Make':
            one_row[2] = item[1]
        elif item[0] == 'Model':
            one_row[4] = item[1]
        elif item[0] == 'Variant':
            one_row[5] = item[1]
        elif item[0] == 'Year':
            one_row[6] = item[1]
        elif item[0] == 'Engine Capacity':
            one_row[7] = item[1]
        elif item[0] == 'Transmission':
            one_row[8] = item[1]
        elif item[0] == 'Seat Capacity':
            one_row[9] = item[1]
        elif item[0] == 'Mileage':
            one_row[10] = item[1]
        elif item[0] == 'Colour':
            one_row[-1] = item[1]

    sheet1_data.append(one_row)
    print(one_row)


def get_item_detail(html):
    reg = 'class="list-item.*?span.*?>(.*?)<.*?<span.*?>(.*?)<'
    item_list = re.compile(reg).findall(html)

    return item_list


def get_date(ori_str):
    try:
        timestamp = int(time.mktime(datetime.strptime(ori_str, "%Y-%m-%d").timetuple()))
        ret = datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
        return ret
    except:
        return 'N/A'


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(html.unescape(dd))


def get_json_resp(url):
    resp = requests.get(url, headers={
        'Cookie': cookie,
        'Accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    }, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    return {}


def get_request(url):
    header = {
        'cookie': cookie,
        'referer': 'https://www.carlist.my/used-cars-for-sale/malaysia?min_year=2012&max_year=2018',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    res_data = requests.get(url, headers=header, timeout=10)
    return str(res_data.content).replace('\\t', '').replace('\\r', '').replace('\\n', '')


def request_sheet3(filename, start=1):
    print('process -> ' + filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            profile_id = row[0].value
            name = row[1].value
            c_id = row[9].value
            request_portfolio(profile_id, c_id, name)
        except Exception as e:
            print(str(i) + ' -> ' + str(e))
    write_excel('data/sheet3.xls', sheet3_data)

for i in range(1, 1110):
    url = 'https://www.carlist.my/used-cars-for-sale/malaysia?min_year=2012&max_year=2018&page_number=%d&page_size=25' % i
    try:
        print(url)
        request_sheet1(url)
    except Exception as e:
        print('EXP-1', url, e)
write_excel('data/sheet1.xls', sheet1_data)
write_excel('data/sheet2.xls', sheet2_data)
write_excel('data/sheet3.xls', sheet3_data)
write_excel('data/sheet4.xls', sheet4_data)
write_excel('data/sheet5.xls', sheet5_data)