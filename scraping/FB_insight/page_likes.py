# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import os, sys

cookie = 'datr=RKzWW_1NuhIxB9RG7RUemqv0; sb=ovjqW-tww_Qe7OR39cZQ91wp; c_user=100006957738125; xs=204%3AxJOImzLFdPhW1A%3A2%3A1546597455%3A20772%3A8703; fr=0mVSQPNFOoV7LvCYc.AWXamP8Ag4Yu_zgArwvpNP0gJpo.Bb0aQ1.Cv.F2A.0.0.BditFT.AWUknhrQ; spin=r.1001266026_b.trunk_t.1570529080_s.1_v.2_; presence=EDvF3EtimeF1570529929EuserFA21B06957738125A2EstateFDutF1570529929756CEchFDp_5f1B06957738125F1CC; wd=1647x541; act=1570530170543%2F9; pnl_data2=eyJhIjoib25hZnRlcmxvYWQiLCJjIjoiWEFkc0tlcGxlckNvbnRyb2xsZXIiLCJiIjpmYWxzZSwiZCI6Ii9hZHMvYXVkaWVuY2UtaW5zaWdodHMvaW50ZXJlc3RzIiwiZSI6W119'

url_base = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQwDIx2AYByWYySMACGCacExLAQEGnAxKRnbuDFTE19dNQ%3AAQxgoMTlSb7xJMfc-elrAaPybvLtdMbV_kzn2tX0HY9PVQ&city[0]={}&metrics[0]={}'
url_base += '&admarket_id=6017625189745&logger_session_id=ef675544a3427aa08790fc71c423af75b797087c&__user=100006957738125&__a=1&__dyn=7xeUmFoO3-SudwCwBzUKFVedzFuCEkG11wTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwxxicwko42EiyEqx68w9q15w5VCwjHwKxG2Z2odoK7UC5oK1KxO4Ujw9-icwKwEwgolUScw4JwgHAy85iawnEfU6Oq2l2Utgvx-2y1uw9a2WE9EjwgEmwkE-58C4V8&__csr=&__req=1q&__be=1&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001266026&__s=%3Ayrvwm7%3Ak7ofa5&__hsi=6745374670875311486-0&jazoest=27854&__spin_r=1001266026&__spin_b=trunk&__spin_t=1570529080'

param_list = [
    # ('ID_1', 'Boost Mobile, Digital Wallet, Go-jek', '&interests[0]=6003149389749&interests[1]=6003280248159&interests[2]=977370282327350', '1002881', 'Yogykarta'),
    # ('ID_2', 'Boost Mobile, Digital Wallet, Go-jek', '&interests[0]=6003149389749&interests[1]=6003280248159&interests[2]=977370282327350', '989399', 'Semarang'),
    ('ID_3', 'Boost Mobile, Digital Wallet, Go-jek', '&interests[0]=6003149389749&interests[1]=6003280248159&interests[2]=977370282327350', '992961', 'Surakarta'),
]

age_list = [
    # ['18', '31'],
    ['18', '40'],
]

gender_list = [
    # '&gender=2', #Men
    '&gender=1' #Women
]

sheet1 = [['game Id', 'Gender', 'Country', 'Age group', 'category', 'Relevance', 'page name', 'url', 'audience', 'Facebook', 'Affinity']]

age_group = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+', 'Total']
gender_group = ['Men', 'Women', 'All']


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
    try:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', ori)
        return str(HTMLParser.HTMLParser().unescape(dd)).strip()
    except:
        return HTMLParser.HTMLParser().unescape(dd)


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
    return json.loads(res)


def get_html(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
        'accept': '*/*',
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content.replace("\n", "").replace('\t', '')
    return res


def scrape_from_urls():
    for param in param_list:
        try:
            parse_from_url(param)
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


def parse_from_url(url_obj):
    global sheet1
    g_id, name, interest, country, country_name = url_obj
    job_url_list = generate_url(country, '2', interest)

    for url_entry in job_url_list:
        url, gender, age = url_entry

        res_json = get_request(url)
        process_json(g_id, res_json, gender, country_name, age)


def process_json(g_id, res_json, gender, country, age):
    data_list = res_json['payload']['2']['data']
    for category, values in dict(data_list).items():
        for value in values.get('pages'):
            try:
                one_row = [g_id, gender, country, age, category, value.get('rank'), value.get('title'), value.get('url'),
                           value.get('audience'), value.get('benchmark'), int(value.get('affinity'))]
                print one_row
                sheet1.append(one_row)
            except Exception as e:
                print('ERR-row: ', value, e)


def scrape_from_files():
    genders = ['Men', 'Women']
    for param in param_list:
        for gender in genders:
            filename = 'source/' + param[1] + '_' + gender + '.html'
            parse_from_file(filename, param, gender)


def request_product(url):
    html = get_html(url)
    reg = '<div class="_50f4">Products</div>(.*?)See more'
    data = re.compile(reg).findall(html)

    return 'N/A' if not data else remove_html_tag(data[0])


def scrape_product(start=1):
    res = [[]]
    url_detail = {}
    data = xlrd.open_workbook("data/FB Insights.xls", encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):

        row = table.row(i)
        main_url = row[7].value
        try:
            details = url_detail.get(main_url, None)
            if not details:
                details = request_product(main_url+'about')
                url_detail[main_url] = details
            res.append([main_url, details])
            print details
        except Exception as e:
            print i, e
            res.append([main_url, 'N/A'])
    write_excel('data/product.xls', res)


scrape_from_urls()
write_excel('data/page_likes.xls', sheet1)
scrape_product()