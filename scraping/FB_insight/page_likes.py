# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import os, sys

cookie = 'datr=PtbnXY4VhzC3ORxIZFyQZLkX; sb=yNvnXS1Y5B51KzRCZXpY8hMy; c_user=100044116672366; xs=43%3AO3CPKtJnpU-Rlg%3A2%3A1575484489%3A-1%3A-1; fr=00b9BjLp9YpJZJ1dF.AWVA5nlYFzJGjn27TDQcaqYhpDQ.Bd35LM.nu.F4G.0.0.BeS8nu.AWURaZ56; spin=r.1001794891_b.trunk_t.1583406679_s.1_v.2_; wd=1691x551; presence=EDvF3EtimeF1583406692EuserFA21B44116672366A2EstateFDutF0CEchF_7bCC'

url_base = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQwDIx2AYByWYySMACGCacExLAQEGnAxKRnbuDFTE19dNQ%3AAQxgoMTlSb7xJMfc-elrAaPybvLtdMbV_kzn2tX0HY9PVQ&metrics[0]={}'
url_base += '&admarket_id=6017625189745&logger_session_id=ef675544a3427aa08790fc71c423af75b797087c&__user=100006957738125&__a=1&__dyn=7xeUmFoO3-SudwCwBzUKFVedzFuCEkG11wTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwxxicwko42EiyEqx68w9q15w5VCwjHwKxG2Z2odoK7UC5oK1KxO4Ujw9-icwKwEwgolUScw4JwgHAy85iawnEfU6Oq2l2Utgvx-2y1uw9a2WE9EjwgEmwkE-58C4V8&__csr=&__req=1q&__be=1&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001266026&__s=%3Ayrvwm7%3Ak7ofa5&__hsi=6745374670875311486-0&jazoest=27854&__spin_r=1001266026&__spin_b=BRunk&__spin_t=1570529080'

param_list = [
    ('ID_1', 'Single',
     'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzyY4Ti3f5VO7odh1deurAdeD_Jbhei5dzTOLC0NQTA-g:AQxGbE1WIbHxueCF6J1FEx2NBuoBT0aorIDyFrd6SRm6Ww&age[0]=18&age[1]=25&country[0]=TR&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003110325672&interests[1]=6002970347721&interests[2]=6003423248519&admarket_id=23844093502180140&logger_session_id=ba53e88e6c56b3530792301c62cb696bbe33082c&__user=100044116672366&__a=1&__dyn=7xeXxaBz8fXpUS2q2mfyWDAUsBWqxiEqwCwTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwSz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0iS12Ki8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei0i61dw&__csr=&__req=1z&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=2&__rev=1001722648&__s=fava9d%3Avaybue%3A9f00qf&__hsi=6794739195959889700-0&__comet_req=0&jazoest=28193&__spin_r=1001722648&__spin_b=trunk&__spin_t=1582021532',
     'TR', 'MEN', '18-25'),
    ('ID_2', 'Single',
     'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzyY4Ti3f5VO7odh1deurAdeD_Jbhei5dzTOLC0NQTA-g:AQxGbE1WIbHxueCF6J1FEx2NBuoBT0aorIDyFrd6SRm6Ww&age[0]=18&age[1]=25&country[0]=TR&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003547497642&interests[1]=6002970347721&interests[2]=6003423248519&admarket_id=23844093502180140&logger_session_id=ba53e88e6c56b3530792301c62cb696bbe33082c&__user=100044116672366&__a=1&__dyn=7xeXxaBz8fXpUS2q2mfyWDAUsBWqxiEqwCwTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwSz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0iS12Ki8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei0i61dw&__csr=&__req=22&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=2&__rev=1001722648&__s=hsd98z%3Avaybue%3A9f00qf&__hsi=6794739195959889700-0&__comet_req=0&jazoest=28193&__spin_r=1001722648&__spin_b=trunk&__spin_t=1582021532',
     'TR', 'WOMEN', '18-25'),
    ('ID_3', 'Single',
     'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzyY4Ti3f5VO7odh1deurAdeD_Jbhei5dzTOLC0NQTA-g:AQxGbE1WIbHxueCF6J1FEx2NBuoBT0aorIDyFrd6SRm6Ww&age[0]=26&age[1]=35&country[0]=TR&gender=2&relationship[0]=1&metrics[0]=2&interests[0]=6003547497642&interests[1]=6002970347721&interests[2]=6003423248519&admarket_id=23844093502180140&logger_session_id=ba53e88e6c56b3530792301c62cb696bbe33082c&__user=100044116672366&__a=1&__dyn=7xeXxaBz8fXpUS2q2mfyWDAUsBWqxiEqwCwTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwSz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0iS12Ki8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei0i61dw&__csr=&__req=1z&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=2&__rev=1001722648&__s=fava9d%3Avaybue%3A9f00qf&__hsi=6794739195959889700-0&__comet_req=0&jazoest=28193&__spin_r=1001722648&__spin_b=trunk&__spin_t=1582021532',
     'TR', 'MEN', '26-35'),
    ('ID_4', 'Single',
     'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzyY4Ti3f5VO7odh1deurAdeD_Jbhei5dzTOLC0NQTA-g:AQxGbE1WIbHxueCF6J1FEx2NBuoBT0aorIDyFrd6SRm6Ww&age[0]=26&age[1]=35&country[0]=TR&gender=1&relationship[0]=1&metrics[0]=2&interests[0]=6003547497642&interests[1]=6002970347721&interests[2]=6003423248519&admarket_id=23844093502180140&logger_session_id=ba53e88e6c56b3530792301c62cb696bbe33082c&__user=100044116672366&__a=1&__dyn=7xeXxaBz8fXpUS2q2mfyWDAUsBWqxiEqwCwTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwSz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0iS12Ki8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei0i61dw&__csr=&__req=22&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=2&__rev=1001722648&__s=hsd98z%3Avaybue%3A9f00qf&__hsi=6794739195959889700-0&__comet_req=0&jazoest=28193&__spin_r=1001722648&__spin_b=trunk&__spin_t=1582021532',
     'TR', 'WOMEN', '26-35'),
    ('ID_5', 'non-Single',
     'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzyY4Ti3f5VO7odh1deurAdeD_Jbhei5dzTOLC0NQTA-g:AQxGbE1WIbHxueCF6J1FEx2NBuoBT0aorIDyFrd6SRm6Ww&age[0]=18&age[1]=25&country[0]=TR&gender=2&relationship[0]=0&relationship[2]=2&relationship[3]=4&relationship[4]=5&metrics[0]=2&interests[0]=6003547497642&interests[1]=6002970347721&interests[2]=6003423248519&admarket_id=23844093502180140&logger_session_id=ba53e88e6c56b3530792301c62cb696bbe33082c&__user=100044116672366&__a=1&__dyn=7xeXxaBz8fXpUS2q2mfyWDAUsBWqxiEqwCwTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwSz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0iS12Ki8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei0i61dw&__csr=&__req=2v&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=2&__rev=1001722648&__s=fu1ab4%3Avaybue%3A9f00qf&__hsi=6794739195959889700-0&__comet_req=0&jazoest=28193&__spin_r=1001722648&__spin_b=trunk&__spin_t=1582021532',
     'TR', 'MEN', '18-25'),
    ('ID_6', 'non-Single',
     'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzyY4Ti3f5VO7odh1deurAdeD_Jbhei5dzTOLC0NQTA-g:AQxGbE1WIbHxueCF6J1FEx2NBuoBT0aorIDyFrd6SRm6Ww&age[0]=18&age[1]=25&country[0]=TR&interests[0]=6003547497642&interests[1]=6002970347721&interests[2]=6003423248519&gender=1&relationship[0]=0&relationship[2]=2&relationship[3]=4&relationship[4]=5&metrics[0]=2&admarket_id=23844093502180140&logger_session_id=ba53e88e6c56b3530792301c62cb696bbe33082c&__user=100044116672366&__a=1&__dyn=7xeXxaBz8fXpUS2q2mfyWDAUsBWqxiEqwCwTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwSz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0iS12Ki8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei0i61dw&__csr=&__req=2v&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=2&__rev=1001722648&__s=fu1ab4%3Avaybue%3A9f00qf&__hsi=6794739195959889700-0&__comet_req=0&jazoest=28193&__spin_r=1001722648&__spin_b=trunk&__spin_t=1582021532',
     'TR', 'WOMEN', '18-25'),
    ('ID_7', 'non-Single',
     'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzyY4Ti3f5VO7odh1deurAdeD_Jbhei5dzTOLC0NQTA-g:AQxGbE1WIbHxueCF6J1FEx2NBuoBT0aorIDyFrd6SRm6Ww&age[0]=26&age[1]=35&country[0]=TR&interests[0]=6003547497642&interests[1]=6002970347721&interests[2]=6003423248519&gender=2&relationship[0]=0&relationship[2]=2&relationship[3]=4&relationship[4]=5&metrics[0]=2&admarket_id=23844093502180140&logger_session_id=ba53e88e6c56b3530792301c62cb696bbe33082c&__user=100044116672366&__a=1&__dyn=7xeXxaBz8fXpUS2q2mfyWDAUsBWqxiEqwCwTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwSz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0iS12Ki8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei0i61dw&__csr=&__req=2v&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=2&__rev=1001722648&__s=fu1ab4%3Avaybue%3A9f00qf&__hsi=6794739195959889700-0&__comet_req=0&jazoest=28193&__spin_r=1001722648&__spin_b=trunk&__spin_t=1582021532',
     'TR', 'MEN', '26-35'),
    ('ID_8', 'non-Single',
     'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQzyY4Ti3f5VO7odh1deurAdeD_Jbhei5dzTOLC0NQTA-g:AQxGbE1WIbHxueCF6J1FEx2NBuoBT0aorIDyFrd6SRm6Ww&age[0]=26&age[1]=35&country[0]=TR&interests[0]=6003547497642&interests[1]=6002970347721&interests[2]=6003423248519&gender=1&relationship[0]=0&relationship[2]=2&relationship[3]=4&relationship[4]=5&metrics[0]=2&admarket_id=23844093502180140&logger_session_id=ba53e88e6c56b3530792301c62cb696bbe33082c&__user=100044116672366&__a=1&__dyn=7xeXxaBz8fXpUS2q2mfyWDAUsBWqxiEqwCwTKq2i5Uf9E6C7UW3qi4FoGu7EiwzwmoWdwJx659ouwSz82iG4EG6Ehy82mwho1upE4WUbEqwLgC3mbx-9xmbwrEsxe0IV8O2W2y11xnzoO0iS12Ki8wl8G1uw_wsU9kbxR1-7Ua85W0AEbGwCxe12xq1izUuxei0i61dw&__csr=&__req=2v&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=2&__rev=1001722648&__s=fu1ab4%3Avaybue%3A9f00qf&__hsi=6794739195959889700-0&__comet_req=0&jazoest=28193&__spin_r=1001722648&__spin_b=trunk&__spin_t=1582021532',
     'TR', 'WOMEN', '26-35'),
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

    res_json = get_request(url)
    process_json(g_id, res_json, gender, country, age, status)


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
