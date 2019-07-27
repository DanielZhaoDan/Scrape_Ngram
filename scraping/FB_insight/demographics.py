# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import os, sys

cookie = 'datr=RKzWW_1NuhIxB9RG7RUemqv0; sb=ovjqW-tww_Qe7OR39cZQ91wp; c_user=100006957738125; xs=204%3AxJOImzLFdPhW1A%3A2%3A1546597455%3A20772%3A8703; ; act=1562565332845%2F5; fr=0mVSQPNFOoV7LvCYc.AWVThUfa65qq7ZUHAA1jwC3vBZE.Bb0aQ1.Cv.Fyn.0.0.BdLT8j.; spin=r.1000990842_b.trunk_t.1564192415_s.1_v.2_; presence=EDvF3EtimeF1564192427EuserFA21B06957738125A2EstateFDt3F_5b_5dElm3FA2user_3a175814135854019A2Eutc3F1551963747010G564192427191CEchFDp_5f1B06957738125F1CC; wd=1394x433; pnl_data2=eyJhIjoib25hZnRlcmxvYWQiLCJjIjoiWEFkc0tlcGxlckNvbnRyb2xsZXIiLCJiIjpmYWxzZSwiZCI6Ii9hZHMvYXVkaWVuY2UtaW5zaWdodHMvcGVvcGxlIiwiZSI6W119'

url_base = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQyV01ZGWRUvK-yhHeE2DjYFnotXCO_ZDdXf6JwGChURcw%3AAQwVh_SPtXVuiqTP2CNpuqccwJfopUFdcJS9Xj4vyMRD0w&age[0]=18&age[1]=-1&country[0]={}&interests[0]={}&metrics[0]={}&admarket_id=6017625189745&logger_session_id=124e692f3d09c6c08c3d1c26179e72d0ea711d6f&__user=100006957738125&__a=1&__dyn=7xeUmFoO3yqSudwCwBzUKFVe79uCEkG11wTKq2i5Uf9E29zEdF8iByFUuwSwmoWdwJx659o4258O1hwgaxaaxG4oy0w8lwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe4U2vAz8bEa8465uaGcw5MKi8wl8G1uw_wr9E9kbxR1-18wnE2iwKG2q4U4a5E&__req=27&__be=1&__pc=PHASED%3Aufi_home_page_pkg&dpr=1&__rev=1000990842&__s=%3Appaagk%3A6hnj79&jazoest=28201&__spin_r=1000990842&__spin_b=trunk&__spin_t=1564192415'

param_list = [
    ('ID_1', 'AMD Gaming', '6011835283233', 'ID'),
    ('ID_2', 'Intel', '6003233117498', 'ID'),
    ('ID_3', 'AMD Gaming', '6011835283233', 'IN'),
    ('ID_4', 'Intel', '6003233117498', 'IN'),
    ('ID_5', 'AMD Gaming', '6011835283233', 'KR'),
    ('ID_6', 'Intel', '6003233117498', 'KR'),
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


def parse_demographics(url_obj):
    global sheet1
    g_id, name, interest, country = url_obj
    gender_url = url_base.format(country, interest, '3')
    total_url = url_base.format(country, interest, '30')

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