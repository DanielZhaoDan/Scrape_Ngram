# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import os, sys
from scraping.utils import post_request_html

cookie = 'datr=PtbnXY4VhzC3ORxIZFyQZLkX; sb=yNvnXS1Y5B51KzRCZXpY8hMy; dpr=2; locale=en_US; c_user=100000028096171; xs=10%3A3CoCL9mOeZ5XtA%3A2%3A1595688072%3A6181%3A9564; fr=00b9BjLp9YpJZJ1dF.AWXf-ahkv_QPByimlTr7hv-n78U.Bd35LM.nu.AAA.0.0.BfHESH.AWUnTMam; spin=r.1002419897_b.trunk_t.1595688073_s.1_v.2_; presence=EDvF3EtimeF1595688081EuserFA21BB28096171A2EstateFDutF1595688077322CEchF_7bCC; wd=1390x346; act=1595688572901%2F47'

url_base = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQwDIx2AYByWYySMACGCacExLAQEGnAxKRnbuDFTE19dNQ%3AAQxgoMTlSb7xJMfc-elrAaPybvLtdMbV_kzn2tX0HY9PVQ&metrics[0]={}'
url_base += '&admarket_id=23842889858960749&fb_dtsg_ag=AQw40ueOpC_tZkaYBbt4-YNYhiw30eNfTd-rsYZkiTXuCw%3AAQzJ9LLD1lgnyJERxtU0ltx_7Hgw05dEd7FjqN_eB8axyA'

param_list = [
    # ('ID_1', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=ID&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'ID', 'MEN', '18-25'),
    # ('ID_2', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=ID&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'ID', 'WOMEN', '18-25'),
    # ('ID_3', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=ID&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'ID', 'MEN', '26-35'),
    # ('ID_4', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=ID&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'ID', 'WOMEN', '26-35'),
    # ('ID_5', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=ID&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'ID', 'MEN', '18-25'),
    # ('ID_6', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=ID&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'ID', 'WOMEN', '18-25'),
    # ('ID_7', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=ID&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'ID', 'MEN', '26-35'),
    # ('ID_8', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=ID&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'ID', 'WOMEN', '26-35'),
    # ('ID_1', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=TR&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'TR', 'MEN', '18-25'),
    # ('ID_2', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=TR&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'TR', 'WOMEN', '18-25'),
    # ('ID_3', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=TR&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'TR', 'MEN', '26-35'),
    # ('ID_4', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=TR&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'TR', 'WOMEN', '26-35'),
    # ('ID_5', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=TR&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'TR', 'MEN', '18-25'),
    # ('ID_6', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=TR&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'TR', 'WOMEN', '18-25'),
    # ('ID_7', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=TR&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'TR', 'MEN', '26-35'),
    # ('ID_8', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=TR&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'TR', 'WOMEN', '26-35'),
    # ('ID_1', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=TH&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'TH', 'MEN', '18-25'),
    # ('ID_2', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=TH&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'TH', 'WOMEN', '18-25'),
    # ('ID_3', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=TH&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'TH', 'MEN', '26-35'),
    # ('ID_4', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=TH&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'TH', 'WOMEN', '26-35'),
    # ('ID_5', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=TH&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'TH', 'MEN', '18-25'),
    # ('ID_6', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=TH&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'TH', 'WOMEN', '18-25'),
    # ('ID_7', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=TH&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'TH', 'MEN', '26-35'),
    # ('ID_8', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=TH&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'TH', 'WOMEN', '26-35'),
    ('ID_1', 'Single',
     'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=BR&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
     'BR', 'MEN', '18-25'),
    # ('ID_2', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=BR&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'BR', 'WOMEN', '18-25'),
    # ('ID_3', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=BR&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'BR', 'MEN', '26-35'),
    # ('ID_4', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=BR&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'BR', 'WOMEN', '26-35'),
    ('ID_5', 'non-Single',
     'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=BR&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
     'BR', 'MEN', '18-25'),
    # ('ID_6', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=BR&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'BR', 'WOMEN', '18-25'),
    # ('ID_7', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=BR&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'BR', 'MEN', '26-35'),
    # ('ID_8', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=BR&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'BR', 'WOMEN', '26-35'),
    # ('ID_1', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=VN&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'VN', 'MEN', '18-25'),
    # ('ID_2', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=VN&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'VN', 'WOMEN', '18-25'),
    # ('ID_3', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=VN&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'VN', 'MEN', '26-35'),
    # ('ID_4', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=VN&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'VN', 'WOMEN', '26-35'),
    # ('ID_5', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=VN&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'VN', 'MEN', '18-25'),
    # ('ID_6', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=VN&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'VN', 'WOMEN', '18-25'),
    # ('ID_7', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=VN&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'VN', 'MEN', '26-35'),
    # ('ID_8', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=VN&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'VN', 'WOMEN', '26-35'),
    # ('ID_1', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=RU&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'RU', 'MEN', '18-25'),
    ('ID_2', 'Single',
     'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=RU&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
     'RU', 'WOMEN', '18-25'),
    # ('ID_3', 'Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=RU&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
    #  'RU', 'MEN', '26-35'),
    ('ID_4', 'Single',
     'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=RU&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672',
     'RU', 'WOMEN', '26-35'),
    # ('ID_5', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=RU&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'RU', 'MEN', '18-25'),
    ('ID_6', 'non-Single',
     'https://www.facebook.com/ads/audience-insights/query/?age[0]=18&age[1]=25&country[0]=RU&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
     'RU', 'WOMEN', '18-25'),
    # ('ID_7', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=RU&gender=2&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'RU', 'MEN', '26-35'),
    # ('ID_8', 'non-Single',
    #  'https://www.facebook.com/ads/audience-insights/query/?age[0]=26&age[1]=35&country[0]=RU&gender=1&relationship[0]=2&relationship[1]=4&relationship[2]=5&metrics[0]=2&interests[0]=6003110325672',
    #  'RU', 'WOMEN', '26-35'),
]

age_list = [
    # ['18', '31'],
    ['18', '40'],
]

gender_list = [
    # '&gender=2', #Men
    '&gender=1'  # Women
]

sheet1 = [
    ['game Id', 'Gender', 'Country', 'Age group', 'category', 'Relevance', 'page name', 'url', 'audience', 'Facebook',
     'Affinity', 'Marital Status']]

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
    url = url_base.format(type)

    res = []
    for age in age_list:
        for gender in gender_list:
            # res.append([url + interest + parse_age_str(age) + gender, 'Men' if '2' in gender else 'Women', '-'.join(age)])
            res.append(
                [url + interest, 'ALL', '18-ANY'])
    return res


def parse_age_str(age):
    return '&age[0]=' + age[0] + '&age[1]=' + age[1]


def parse_from_url(url_obj):
    global sheet1
    g_id, status, url, country, gender, age = url_obj

    # res_json = get_request(url)
    res_json = post_request(url)
    process_json(g_id, res_json, gender, country, age, status)


def post_request(url):
    param = url.split('?')[-1]
    param_l = param.split('&')

    body = {}
    for p in param_l:
        k_v = p.split('=')
        body[k_v[0]] = k_v[1]
    body['admarket_id'] = '23842889858960749'
    body['logger_session_id'] = 'c90abdb40456798f099ca596572e083656381afd'
    body['__user'] = '100000028096171'
    body['__a'] = '1'
    body['__dyn'] = '7xeUmFoO3-SudwCwBzUKFV8-EKnFG5axG2q3uVE98nwYCwqovzEdF8iByFUuxa2e1pzES2S4okBxW3qcw9m4EG6Ehy82mwho3Ywv9E4WUbEqwLgC3mbx-9xm1WxO4Uow9GicwKwAK11xnzoO0iS12Ki8wl8G1uw_wr9E9kbxR12ewi85W1ywLwKG2q4UgwNxq8wio-7EjAw8e0RE4idwmEy9wVwgo6q59o'
    body['__csr'] = ''
    body['__req'] = '3h'
    body['__beoa'] = '0'
    body['__pc'] = 'PHASED:DEFAULT'
    body['dpr'] = '2'
    body['__ccg'] = 'EXCELLENT'
    body['__rev'] = '1002419897'
    body['__s'] = 'p82mh7:uyhu6z:iz0bwg'
    body['__hsi'] = '6853428119464301773-0'
    body['__comet_req'] = '0'
    body['fb_dtsg'] = 'AQEGmXaVzcZT:AQF9gTS80tiF'
    body['jazoest'] = '22057'
    body['__spin_r'] = '1002419897'
    body['__spin_b'] = 'trunk'
    body['__spin_t'] = '1595688073'

    html = post_request_html(url.split('?')[0], cookie=cookie, data=body)
    res = html.replace('for (;;);', '')
    return json.loads(res)


def process_json(g_id, res_json, gender, country, age, status):
    data_list = res_json['payload']['2']['data']
    for category, values in dict(data_list).items():
        for value in values.get('pages'):
            try:
                one_row = [g_id, gender, country, age, category, value.get('rank'), value.get('title'),
                           value.get('url'),
                           value.get('audience'), value.get('benchmark'), int(value.get('affinity')), status]
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
    reg = '<div class="_4bl9 _5m_o">.*?href.*?>(.*?)<'
    data = re.compile(reg).findall(html)

    return 'N/A' if not data else remove_html_tag(data[0])


def scrape_product(start=1):
    res = [[]]
    url_detail = {}
    data = xlrd.open_workbook("data/page_likes.xls", encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):

        row = table.row(i)
        main_url = row[7].value
        try:
            details = url_detail.get(main_url, None)
            if not details:
                details = request_product(main_url + 'about')
                url_detail[main_url] = details
            res.append([main_url, details])
            print details
        except Exception as e:
            print i, e
            res.append([main_url, 'N/A'])
    write_excel('data/product.xls', res)


scrape_from_urls()
write_excel('data/scrape1_TR.xls', sheet1)
# scrape_product()
