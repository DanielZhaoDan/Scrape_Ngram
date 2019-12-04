# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import os, sys

cookie = 'datr=RKzWW_1NuhIxB9RG7RUemqv0; sb=ovjqW-tww_Qe7OR39cZQ91wp; c_user=100006957738125; xs=204%3AxJOImzLFdPhW1A%3A2%3A1546597455%3A20772%3A8703; ; fr=0mVSQPNFOoV7LvCYc.AWUvbhXxVSvGgNeRpWC3jlm-3zc.Bb0aQ1.Cv.Fyn.0.0.BdS4B7.AWXVNuAZ; act=1565229224169%2F4; spin=r.1001072277_b.trunk_t.1566104867_s.1_v.2_; wd=1873x292; presence=EDvF3EtimeF1566106310EuserFA21B06957738125A2EstateFDt3F_5b_5dElm3FA2user_3a175814135854019A2Eutc3F1551963747010G566106310257CEchFDp_5f1B06957738125F1CC; pnl_data2=eyJhIjoib25hZnRlcmxvYWQiLCJjIjoiWEFkc0tlcGxlckNvbnRyb2xsZXIiLCJiIjpmYWxzZSwiZCI6Ii9hZHMvYXVkaWVuY2UtaW5zaWdodHMvaW50ZXJlc3RzIiwiZSI6W119'

url_base = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQwSdRuRhiC1lNIvyECY_Ynj4LhESEdEMMwj8nfknlwhkg%3AAQxgl5v5XoAyP045VCl-kwTKx46m2tu-j7hwDEiktpVvAA&age[0]=18&age[1]=-1&country[0]={}&&metrics[0]={}&admarket_id=6017625189745&logger_session_id=537caf7b5b241f661817b68e6625f457b1d0c007&__user=100006957738125&__a=1&__dyn=7xeUmFoO3yqSudwCwBzUKFVe79uCEkG11wTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwxxicwko42EiyEqx68w825o4m0nCq1eK2W6EbQ9wRyUvyolyU6W78jxe0DV8O2W2y11xnyGz81bo4aV8y1kyE5W3-1PwBgK7k7UvwEwnE2iwKG2q4U4a5E5afxi&__req=k&__be=1&__pc=PHASED%3Aufi_home_page_pkg&dpr=1&__rev=1001072277&__s=2woygf%3A1dlwd5%3Al9zr5s&__hsi=6726375366434162411-0&jazoest=28230&__spin_r=1001072277&__spin_b=trunk&__spin_t=1566104867'

param_list = [
    ('ID_1', 'AMD', '&interests[0]=6003060775932&interests[1]=6003507858586&interests[2]=6003506463031&interests[3]=6011835283233&interests[4]=6004144552809&interests[5]=6003110510235&interests[6]=6016289746149', 'KR'),
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
    url = url_base.format(country, type)

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