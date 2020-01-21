# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import os, sys

cookie = 'datr=PtbnXY4VhzC3ORxIZFyQZLkX; sb=yNvnXS1Y5B51KzRCZXpY8hMy; locale=en_GB; c_user=100044116672366; xs=43%3AO3CPKtJnpU-Rlg%3A2%3A1575484489%3A-1%3A-1; fr=00b9BjLp9YpJZJ1dF.AWUvlIHgYzV7iZtqqgJBcWKhU9k.Bd35LM.nu.AAA.0.0.Bd5_xJ.AWU8k8Vq; spin=r.1001494170_b.trunk_t.1575484490_s.1_v.2_; wd=1779x578; presence=EDvF3EtimeF1575484828EuserFA21B44116672366A2EstateFDutF1575484505253CEchFDp_5f1B44116672366F0CC; pnl_data2=eyJhIjoiYWxsX3BhZ2VsZXRzX2Rpc3BsYXllZCIsImMiOiJYQWRzS2VwbGVyQ29udHJvbGxlciIsImIiOmZhbHNlLCJkIjoiL2Fkcy9hdWRpZW5jZS1pbnNpZ2h0cy9wZW9wbGUiLCJlIjpbXX0%3D'

url_base = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQyFRbBit5KBs93Gmepxo4HPUivsyIurje_0uqeXxyJSTg%3AAQxD8h9XnwiiPheGLHU6wWsSoBslmR4qGRcTYir45POJJg&age[0]=18&age[1]=-1&metrics[0]={}&admarket_id=23844093502180140&logger_session_id&__user=100044116672366&__a=1&__dyn=7xeUmFoO3-SudwCwBybGbGujxOnFG5awgodXCwAxu13wqovzEdF8iBxa7EiwzwmoWdwJx659ouwxxicw9aEiyEqx60DU4m0nCq1eK2W6EbQ9wRyUvyolyU6W78jwbeicwKwEwgolUScw5MKi8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei&__csr=&__req=7&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001494170&__s=eelzzs%3A1fpzv9%3Abi3ysp&__hsi=6766655804713496006-0&jazoest=28349&__spin_r=1001494170&__spin_b=trunk&__spin_t=1575484490'

param_list = [
    ('ID_1', 'HP', '&interests[0]=6003200182684&interests[1]=6003293850143&interests[2]=6003533303598&interests[3]=6006406219142', 'ALL'),
]

sheet1 = [['Game ID', 'Name', 'Country', 'Gender', 'Age range', 'Percentage', 'Max New Audience']]

age_group = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+', 'Total']
gender_group = ['Men', 'Women']


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
    print(filename + "===========over============")


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
        'accept': '*/*',
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content.replace('for (;;);', '')
    return res


def scrape_from_urls():
    for param in param_list:
        try:
            parse_demographics(param)
        except Exception as e:
            print('ERR-parse: ', param, e)


def generate_url(country, type, interest):
    url = url_base.format(type)

    return url + interest


def parse_demographics(url_obj):
    global sheet1
    g_id, name, interest, country = url_obj
    gender_url = generate_url(country, '3', interest)
    total_url = generate_url(country, '30', interest)

    print gender_url

    gender_html = get_request(gender_url)
    total_html = get_request(total_url)

    gender_reg = 'audience.*?ratio":(.*?)}.*?benchmark.*?ratio":(.*?)}'

    gender_data = re.compile(gender_reg).findall(gender_html)

    total_reg = '\[.*?,(.*?)\]'
    total_data = re.compile(total_reg).findall(total_html)

    i = 0

    for gender in gender_group:
        for age in age_group:
            if age == 'Total':
                one_row = [g_id, name, country, gender, age, '%.0f' % (float(gender_data[i][0]) * 100) + '%', total_data[0]]
            else:
                one_row = [g_id, name, country, gender, age, '%.0f' % (float(gender_data[i][1]) * 100) + '%', total_data[0]]
            print one_row
            sheet1.append(one_row)
            i += 1


scrape_from_urls()
write_excel('data/demographics.xls', sheet1)