# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import os, sys

cookie = 'datr=PtbnXY4VhzC3ORxIZFyQZLkX; sb=yNvnXS1Y5B51KzRCZXpY8hMy; c_user=100044116672366; xs=43%3AO3CPKtJnpU-Rlg%3A2%3A1575484489%3A-1%3A-1; fr=00b9BjLp9YpJZJ1dF.AWWBoZVnMnfayKew9ta3T_9YheM.Bd35LM.nu.F4G.0.0.BeKS3-.; ; spin=r.1001666243_b.trunk_t.1580528507_s.1_v.2_; presence=EDvF3EtimeF1580528647EuserFA21B44116672366A2EstateFDutF1580528647612CEchFDp_5f1B44116672366F0CC; act=1580528783585%2F5; wd=1390x300'

url_base = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzlMD3AwbVpXqt9UQ5s2WV_7Vaunusbjbejfy7XBf1h1w%3AAQy6oZYYGaZgKkcWrFNgx03WSUxJyf6TAUDJwu8M9zCkug&age[0]=18&age[1]=-1&metrics[0]={}&admarket_id=23844093502180140&logger_session_id=ea4d9ae31995c5bf3b4118f11f360643632b0531&__user=100044116672366&__a=1&__dyn=7xeXxaBz8fXpUS2q2mfyWDAUsBWqxiEqwCwTKq2i5U4e1Fx-ewSAxam4Euxa2e1pzES2S4okBxW3qcw9aEiyEqx60DU4m0nCq1eK2W6EbQ9wRyUvyolyU6W78jwbeicwKwEwgolUScw4JwgHAy85iawnEfU7e2l2Utgvx-2y1uw9a2WE9Ejx2365E5afxW4V8&__csr=&__req=28&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001666243&__s=5a7hs2%3A3gkisx%3A8pi171&__hsi=6788318344457357401-0&jazoest=28254&__spin_r=1001666243&__spin_b=trunk&__spin_t=1580528507'

param_list = [
    ('ID_1', 'CLEAR', '&country[0]=ID&interests[0]=6003547497642&interests[1]=6002970347721&interests[2]=6003423248519', 'Indonesia'),
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