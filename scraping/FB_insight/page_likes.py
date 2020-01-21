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

url_base = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQwDIx2AYByWYySMACGCacExLAQEGnAxKRnbuDFTE19dNQ%3AAQxgoMTlSb7xJMfc-elrAaPybvLtdMbV_kzn2tX0HY9PVQ&metrics[0]={}'
url_base += '&admarket_id=6017625189745&logger_session_id=ef675544a3427aa08790fc71c423af75b797087c&__user=100006957738125&__a=1&__dyn=7xeUmFoO3-SudwCwBzUKFVedzFuCEkG11wTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwxxicwko42EiyEqx68w9q15w5VCwjHwKxG2Z2odoK7UC5oK1KxO4Ujw9-icwKwEwgolUScw4JwgHAy85iawnEfU6Oq2l2Utgvx-2y1uw9a2WE9EjwgEmwkE-58C4V8&__csr=&__req=1q&__be=1&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001266026&__s=%3Ayrvwm7%3Ak7ofa5&__hsi=6745374670875311486-0&jazoest=27854&__spin_r=1001266026&__spin_b=trunk&__spin_t=1570529080'

param_list = [
    ('ID_1', 'HP', 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzji92kJsPhk0fSKeFCKVJcTqkcIaZk4QvWRP4M_nISYA%3AAQwYXhyv5SBwveT2-Yx7lHPGxgQ7Uz20HgrkRCDNLxFDIg&age[0]=18&age[1]=19&country[0]=BR&country[1]=FR&country[2]=DE&country[3]=IN&country[4]=MX&country[5]=RU&country[6]=US&country[7]=GB&interests[0]=6003200182684&interests[1]=6003533303598&interests[2]=6006406219142&interests[3]=6002925240321&interests[4]=6003154042305&interests[5]=6003196812767&metrics[0]=2&admarket_id=23844093502180140&logger_session_id=10482f9d47c8b294337c801ce11e8b8ab6f961ea&__user=100044116672366&__a=1&__dyn=7xeUmFoO3-SudwCwBybGbGujxOnFG5awgodXCwAxu3Oq1Fx-ewSAxamaDxW4E8U5Cezobohxim7E8okz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0n2V8y1kyE5W3-1ICwBgK7k7UvwEwnE2iwKG2q4U4a5E5afxW4V8&__csr=&__req=2k&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001494170&__s=10ehry%3Ae29d83%3A6fccjp&__hsi=6766832954723853906-0&jazoest=27989&__spin_r=1001494170&__spin_b=trunk&__spin_t=1575484490', '', 'ALL', '18-19'),
    ('ID_2', 'HP', 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzji92kJsPhk0fSKeFCKVJcTqkcIaZk4QvWRP4M_nISYA%3AAQwYXhyv5SBwveT2-Yx7lHPGxgQ7Uz20HgrkRCDNLxFDIg&age[0]=20&age[1]=24&country[0]=BR&country[1]=DE&country[2]=FR&country[3]=GB&country[4]=IN&country[5]=MX&country[6]=RU&country[7]=US&education[0]=4&interests[0]=6003200182684&interests[1]=6003533303598&interests[2]=6006406219142&interests[3]=6002925240321&interests[4]=6003154042305&interests[5]=6003196812767&metrics[0]=2&admarket_id=23844093502180140&logger_session_id&__user=100044116672366&__a=1&__dyn=7xeUmFoO3-SudwCwBybGbGujxOnFG5awgodXCwAxu13wqovzEdF8iBxa7EiwzwmoWdwJx659ouwxxicw9aEiyEqx60DU4m0nCq1eK2W6EbQ9wRyUvyolyU6W78jwbeicwKwEwgolUScw5MKi8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei&__csr=&__req=4&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001494170&__s=xub0tz%3Ae29d83%3Arzee8i&__hsi=6766838907222854163-0&jazoest=27989&__spin_r=1001494170&__spin_b=trunk&__spin_t=1575484490', '', 'ALL', '20-24'),
    ('ID_3', 'HP', 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzji92kJsPhk0fSKeFCKVJcTqkcIaZk4QvWRP4M_nISYA%3AAQwYXhyv5SBwveT2-Yx7lHPGxgQ7Uz20HgrkRCDNLxFDIg&age[0]=25&age[1]=34&country[0]=BR&country[1]=DE&country[2]=FR&country[3]=GB&country[4]=IN&country[5]=MX&country[6]=RU&country[7]=US&education[0]=4&interests[0]=6003200182684&interests[1]=6003533303598&interests[2]=6006406219142&interests[3]=6002925240321&interests[4]=6003154042305&interests[5]=6003196812767&family_statuses[0]=6002714398372&metrics[0]=2&admarket_id=23844093502180140&logger_session_id=5ae7fd9a981014b429a4eed28fa0afacf11d756a&__user=100044116672366&__a=1&__dyn=7xeUmFoO3-SudwCwBybGbGujxOnFG5awgodXCwAxu3Oq1Fx-ewSAxamaDxW4E8U5Cezobohxim7E8okz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0n2V8y1kyE5W3-1PwBgK7k7UvwEwnE2iwKG2q4U4a5E5afxW4V8&__csr=&__req=l&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001494170&__s=kbjnee%3Ae29d83%3Arzee8i&__hsi=6766838907222854163-0&jazoest=27989&__spin_r=1001494170&__spin_b=trunk&__spin_t=1575484490', '', 'ALL', '25-34'),
    ('ID_4', 'HP', 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzji92kJsPhk0fSKeFCKVJcTqkcIaZk4QvWRP4M_nISYA%3AAQwYXhyv5SBwveT2-Yx7lHPGxgQ7Uz20HgrkRCDNLxFDIg&age[0]=35&age[1]=44&country[0]=BR&country[1]=DE&country[2]=FR&country[3]=GB&country[4]=IN&country[5]=MX&country[6]=RU&country[7]=US&education[0]=4&interests[0]=6003200182684&interests[1]=6003533303598&interests[2]=6006406219142&interests[3]=6002925240321&interests[4]=6003154042305&interests[5]=6003196812767&family_statuses[0]=6002714398372&metrics[0]=2&admarket_id=23844093502180140&logger_session_id=5ae7fd9a981014b429a4eed28fa0afacf11d756a&__user=100044116672366&__a=1&__dyn=7xeUmFoO3-SudwCwBybGbGujxOnFG5awgodXCwAxu3Oq1Fx-ewSAxamaDxW4E8U5Cezobohxim7E8okz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0n2V8y1kyE5W3-1PwBgK7k7UvwEwnE2iwKG2q4U4a5E5afxW4V8&__csr=&__req=l&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001494170&__s=kbjnee%3Ae29d83%3Arzee8i&__hsi=6766838907222854163-0&jazoest=27989&__spin_r=1001494170&__spin_b=trunk&__spin_t=1575484490', '', 'ALL', '35-44'),
    ('ID_5', 'HP', 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzji92kJsPhk0fSKeFCKVJcTqkcIaZk4QvWRP4M_nISYA%3AAQwYXhyv5SBwveT2-Yx7lHPGxgQ7Uz20HgrkRCDNLxFDIg&age[0]=45&age[1]=54&country[0]=BR&country[1]=DE&country[2]=FR&country[3]=GB&country[4]=IN&country[5]=MX&country[6]=RU&country[7]=US&education[0]=4&interests[0]=6003200182684&interests[1]=6003533303598&interests[2]=6006406219142&interests[3]=6002925240321&interests[4]=6003154042305&interests[5]=6003196812767&family_statuses[0]=6002714398372&metrics[0]=2&admarket_id=23844093502180140&logger_session_id=5ae7fd9a981014b429a4eed28fa0afacf11d756a&__user=100044116672366&__a=1&__dyn=7xeUmFoO3-SudwCwBybGbGujxOnFG5awgodXCwAxu3Oq1Fx-ewSAxamaDxW4E8U5Cezobohxim7E8okz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0n2V8y1kyE5W3-1PwBgK7k7UvwEwnE2iwKG2q4U4a5E5afxW4V8&__csr=&__req=l&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001494170&__s=kbjnee%3Ae29d83%3Arzee8i&__hsi=6766838907222854163-0&jazoest=27989&__spin_r=1001494170&__spin_b=trunk&__spin_t=1575484490', '', 'ALL', '45-54'),
    ('ID_5', 'HP', 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzji92kJsPhk0fSKeFCKVJcTqkcIaZk4QvWRP4M_nISYA%3AAQwYXhyv5SBwveT2-Yx7lHPGxgQ7Uz20HgrkRCDNLxFDIg&age[0]=55&age[1]=64&country[0]=BR&country[1]=DE&country[2]=FR&country[3]=GB&country[4]=IN&country[5]=MX&country[6]=RU&country[7]=US&education[0]=4&interests[0]=6003200182684&interests[1]=6003533303598&interests[2]=6006406219142&interests[3]=6002925240321&interests[4]=6003154042305&interests[5]=6003196812767&family_statuses[0]=6002714398372&metrics[0]=2&admarket_id=23844093502180140&logger_session_id=5ae7fd9a981014b429a4eed28fa0afacf11d756a&__user=100044116672366&__a=1&__dyn=7xeUmFoO3-SudwCwBybGbGujxOnFG5awgodXCwAxu3Oq1Fx-ewSAxamaDxW4E8U5Cezobohxim7E8okz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0n2V8y1kyE5W3-1PwBgK7k7UvwEwnE2iwKG2q4U4a5E5afxW4V8&__csr=&__req=l&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001494170&__s=kbjnee%3Ae29d83%3Arzee8i&__hsi=6766838907222854163-0&jazoest=27989&__spin_r=1001494170&__spin_b=trunk&__spin_t=1575484490', '', 'ALL', '55-64'),
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
    g_id, name, url, country_name, gender, age = url_obj

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