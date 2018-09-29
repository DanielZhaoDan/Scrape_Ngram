# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import sys
from datetime import datetime
import HTMLParser
import os
from urlparse import urlparse
import time
import random

age_list = [
    ('18', '24'),
    ('24', '35'),
]
location_list = ['ID', 'VN', 'TH']
gender_list = ['1', '2']
interest_list = ['none', '6003423248519']
url_list = []
cookie = 'sb=yduuW7d6pqOtCHmB1YcewWHo; datr=yduuW6OgolGqlgqUYD0MX3_A; dpr=2; c_user=100006957738125; xs=9%3AFG6N33zFCc9wcQ%3A2%3A1538186190%3A20772%3A8703; pl=n; spin=r.4365232_b.trunk_t.1538186191_s.1_v.2_; act=1538186424671%2F6; fr=0oCaHd4goT2ZSs7jt.AWUW-sfWPyP8YFA75or50tEToWk.Bbe6u2.t7.Fuu.0.0.Bbrw_V.AWUn0tkb; presence=EDvF3EtimeF1538199509EuserFA21B06957738125A2EstateFDutF1538199509994CEchFDp_5f1B06957738125F16CC; wd=1385x371; pnl_data2=eyJhIjoib25hZnRlcmxvYWQiLCJjIjoiWEFkc0tlcGxlckNvbnRyb2xsZXIiLCJiIjpmYWxzZSwiZCI6Ii9hZHMvYXVkaWVuY2UtaW5zaWdodHMvaW50ZXJlc3RzIiwiZSI6W119'
base_url = 'https://www.facebook.com/ads/audience-insights/query/?dpr=2&age[0]=%s&age[1]=%s&country[0]=%s&gender=%s&metrics[0]=2&admarket_id=6017625189745&logger_session_id=e5b149d85c0a18f176bc40e58fad23e6f2b61fc0&__user=100006957738125&__a=1&__dyn=5V8WUmFoO3yqSudg9odoKFVe8UhBWqxiF88ooUdXCwAy8WqErxSawmWx-ex2axuF8iBAzouxa2e6FQ3mcUS2S4og-m10xicx21hwEyoC8yEqx6cw9a15UnDxm5EK10wOwRxeaCwjHGbwLghKbm7Qpy9US252odoKUryolyU6W78hDzo23xKicDwCx-mE465uaG4Hx63e0z8S15w_Ki8xWbwFyFE-17xS&__req=n&__be=1&__rev=4365232&__spin_r=4365232&__spin_b=trunk&__spin_t=1538186191'

def compose_urls() :
    for age in age_list:
        for location in location_list:
            for gender in gender_list:
                for interest in interest_list:
                    url = base_url % (age[0], age[1], location, gender)
                    if interest != 'none':
                        url  = url + '&interests[0]:' + interest
                    url_list.append(url)


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


def read_excel(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows - 1):
        row = table.row(i)
        try:
            main_url = row[7].value
            publisher = row[6].value
            article_url = row[4].value
            country = row[1].value
            details = request_sheet2(main_url)
            if not details:
                i -= 1
                continue
            one_row = [publisher, main_url, article_url, country] + details
            print(one_row)
            sheet2_data.append(one_row)
        except:
            print(i)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_date(ori):
    ori = ori.replace('Mei', 'May')
    if 'hour' in ori:
        return datetime.now().strftime('%d/%m/%Y')
    try:
        date = datetime.strptime(ori, '%b %d, %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': random.choice(cookie),
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res

compose_urls()
for url in url_list:
    print url