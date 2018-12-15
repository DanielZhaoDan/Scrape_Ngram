# -*- coding: utf-8 -*-
import re
import xlwt
from datetime import datetime
import html
import os
import sys
import xlrd
import requests
import time
import operator

P_ID = 1

sheet1_data = [['Name', 'ER', 'Main age - Followers', 'Main Gender', 'Audience Interests', 'Share', 'URL']]

cookie = '__cfduid=d1c8aa2b8f54c02adf8e5d42efad75cf41542108389; _ga=GA1.2.1373599352.1542108398; _gid=GA1.2.833929376.1542108398; __hstc=148432680.47ca0e17df99336bf5bc85c4480263b3.1542108400178.1542108400178.1542108400178.1; __hssrc=1; hubspotutk=47ca0e17df99336bf5bc85c4480263b3; intercom-id-tznjiue2=7475e61d-a793-48d4-8b02-50b71f2c5869; previewExitIntentPopup=1; fs_inited=1; fs_uid=rs.fullstory.com`8MY4Y`5183839853871104:5629499534213120; _dc_gtm_UA-97700016-3=1; __hssc=148432680.20.1542108400179; amplitude_id_fdb01fff6a804dba1f464a3e9942cfb6hypeauditor.com=eyJkZXZpY2VJZCI6ImM5MThjN2JlLTlkMmQtNGVlYi05ZGEwLWQzYmI3NWZlZDNiMVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU0MjEwODM5NzQ3NiwibGFzdEV2ZW50VGltZSI6MTU0MjExMDkwODA3NywiZXZlbnRJZCI6NDYsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjo0Nn0='


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
        'refer': 'https://hypeauditor.com/preview/yuyacst/?ref=top',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    }, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    return {}


def get_request(url):
    header = {
        'cookie': cookie,
    }
    res_data = requests.get(url, headers=header, timeout=10)
    res = res_data.content
    res = res.decode('ascii', 'ignore').replace('\t', '').replace('\r', '').replace('\n', '')
    return res


def request_details(user_name, url):
    res = []
    json_url = 'https://hypeauditor.com/checkPreview/?username=%s&v=2' % user_name

    json_obj = get_json_resp(json_url)
    ER = json_obj['data']['preview']['blogger']['er']['value']
    age_group = json_obj['data']['preview']['report']['demography_core_age_group']
    demography_list = json_obj['data']['preview']['report']['demography']

    max_age = 'Female'
    percentage = float(demography_list[0]['prc'])
    if percentage > 50:
        max_age = 'Male'

    audience_thematics = json_obj['data']['preview']['report']['audience_thematics']
    for audience in audience_thematics[:3]:
        res.append([user_name, ER, age_group, max_age, audience[0], round(audience[1]*100, 0), url])

    return res


def request_list(url):
    global sheet1_data
    html = get_request(url)
    reg = 'class="kyb-ellipsis" href="(.*?)".*?@(.*?)<'

    name_list = re.compile(reg).findall(html)

    for name in name_list:
        url = 'https://hypeauditor.com' + name[0].split('&')[0]
        user_name = name[1]
        try:
            details_list = request_details(user_name, url)
            for details in details_list:
                print(details)
                sheet1_data.append(details)
        except:
            print('EXCEPT: ', name)


request_list('https://hypeauditor.com/top-instagram/beauty-fashion/mexico/?p=1')
request_list('https://hypeauditor.com/top-instagram/beauty-fashion/mexico/?p=2')
write_excel('data/1.sheet', sheet1_data)