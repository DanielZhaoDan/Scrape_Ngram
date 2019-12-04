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

url_base = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQwDIx2AYByWYySMACGCacExLAQEGnAxKRnbuDFTE19dNQ%3AAQxgoMTlSb7xJMfc-elrAaPybvLtdMbV_kzn2tX0HY9PVQ&&country[0]={}&metrics[0]={}'
url_base += '&admarket_id=6017625189745&logger_session_id=39ec19890689a469299448b958e6792a4d47c63a&__user=100006957738125&__a=1&__dyn=7xeUmFoO3-SudwCwBzUKFVedzFuCEkG11wTKq2i5U4e1Fx-ewSAxam4EuwSwmoWdwJx659ouwxxicwko42EiyEqx60DU4m0nCq1eK2W6EbQ9wRyUvyolyU6W78jxe0DV8O2W2y11xnzoO0iS12Ki8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUkyojAw&__csr=&__req=v&__be=1&__pc=PHASED%3ADEFAULT&dpr=2&__rev=1001210818&__s=%3A1on733%3Aqd3rnq&__hsi=6740431404189962938-0&jazoest=28040&__spin_r=1001210818&__spin_b=trunk&__spin_t=1569339982'

param_list = [
    ('ID_1', 'AI', '&interests[0]=6002898176962', 'SG'),
]

age_list = [
    ['18', '29'],
    ['30', '44'],
    ['45', '65'],
]

gender_list = [
    '&gender=2', #Men
    '&gender=1' #Women
]

sheet1 = [['Interest', 'Age', 'Gender', 'Job Title', 'Selected Audience %', 'Compare %']]

age_group = ['18-29', '30-44', '45-65+']
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

    res = []
    for age in age_list:
        for gender in gender_list:
            res.append([url + interest + parse_age_str(age) + gender, 'Men' if '2' in gender else 'Women', '-'.join(age)])

    return res


def parse_age_str(age):
    return '&age[0]=' + age[0] + '&age[1]=' + age[1]


def parse_demographics(url_obj):
    global sheet1
    g_id, name, interest, country = url_obj
    job_url_list = generate_url(country, '15', interest)

    for job_entry in job_url_list:

        job_url, gender, age = job_entry

        total_html = get_request(job_url)

        gender_reg = 'audience.*?ratio":(.*?)}.*?benchmark.*?ratio":(.*?)}.*?title":"(.*?)"'

        data_list = re.compile(gender_reg).findall(total_html)

        for data in data_list:
            selected = float(data[0])
            benchmark = float(data[1])
            one_row = [name, age, gender, data[2], selected, '%.2f' % ((selected - benchmark) / benchmark) ]
            sheet1.append(one_row)
            print one_row


scrape_from_urls()
write_excel('data/job_title.xls', sheet1)