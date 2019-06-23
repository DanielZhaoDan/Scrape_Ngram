# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import os, sys

age_list = [
    ('18', '65'),
]

location_list = [
    ('SG', 2525, 'SG'), #R
]

gender_list = ['1']
interest_list = [
    ('6003224711745', 'Mobile Payment'),
    ('6003466585319', 'Online Banking'),
]
cookie = 'datr=RKzWW_1NuhIxB9RG7RUemqv0; sb=ovjqW-tww_Qe7OR39cZQ91wp; c_user=100006957738125; xs=204%3AxJOImzLFdPhW1A%3A2%3A1546597455%3A20772%3A8703; pl=n; ; spin=r.4830042_b.trunk_t.1551963620_s.1_v.2_; fr=0mVSQPNFOoV7LvCYc.AWV5yq_803Lmkjam_V3JgZUwKkE.Bb0aQ1.Cv.Fx7.0.0.BcgRXl.AWXc6OIb; act=1551963747451%2F0; dpr=2; wd=1385x306; presence=EDvF3EtimeF1551964137EuserFA21B06957738125A2EstateFDt3F_5b_5dElm3FA2user_3a175814135854019A2Eutc3F1551963747010G551964137684CEchFDp_5f1B06957738125F2CC; pnl_data2=eyJhIjoib25hZnRlcmxvYWQiLCJjIjoiWEFkc0tlcGxlckNvbnRyb2xsZXIiLCJiIjpmYWxzZSwiZCI6Ii9hZHMvYXVkaWVuY2UtaW5zaWdodHMvaW50ZXJlc3RzIiwiZSI6W119'
base_url = 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQyRhuALEuDh4pN97RIT5obt4w9obn6E_Nz2Pb2yagG5uQ:AQy2yDHqx4_dMGr4kWXqF-nC8zX7vDFwLiS8jKZHeVfv_Q&age[0]=18&age[1]=65&country[0]=SG&interests[0]=%s&metrics[0]=2&admarket_id=6017625189745&logger_session_id=2d8838e2a9692973cb46c957d8143d0375e5b522&__user=100006957738125&__a=1&__dyn=7xeUmFoO3yqSudwCwBzUKFVe79uCEkG2q6e3uVE98nwYCwqovzEdF8iByFUuwSwmoWdwJx659o4258O1hwgaxaaxG4oy0w8lwho3ewaGq1eK2V1CdwxgC3mbx-9xmbwrEsxe4U23xKicwKwBG11xnyGz81sbAy85iawnEfU7e2l2Utgvwi85W&__req=2o&__be=1&__pc=PHASED:ufi_home_page_pkg&dpr=2&__rev=4830042&jazoest=27985&__spin_r=4830042&__spin_b=trunk&__spin_t=1551963620'

url_tail = '&admarket_id=6017625189745&logger_session_id=84ec3335e34085c39cb8563f1ff0fb7755ea16e6&__user=100006957738125&__a=1&__dyn=7xeUmFoO3yqSudwCwBzUKFVe79uCEkG2q6e3uVE98nwgU6C7UW3qi4FoixW3q1pzES2S4okBwg8kz85610G4EG6Ehw8C5o4m0PE2GCwjHwKgpzo8k9wRyUvyolyU6W78jxe0wUrAz8bE9qwgolUGEO0n2V8y1kyE5W3-1PwBgK7k7U4y1uw&__req=i&__be=1&__pc=PHASED%3Aufi_home_page_pkg&dpr=2&__rev=4830042&jazoest=27985&__spin_r=4830042&__spin_b=trunk&__spin_t=1551963620'

sheet1_data = [['interests', 'location', 'Age group', 'category', 'Relevance', 'page name', 'url', 'audience', 'Facebook', 'Affinity']]

url_list = [
    # ('18-65', 'SG', 'https://www.facebook.com/ads/audience-insights/query/?fb_dtsg_ag=AQyRhuALEuDh4pN97RIT5obt4w9obn6E_Nz2Pb2yagG5uQ:AQy2yDHqx4_dMGr4kWXqF-nC8zX7vDFwLiS8jKZHeVfv_Q&age[0]=18&age[1]=65&country[0]=SG&interests[0]=%s&metrics[0]=2&admarket_id=6017625189745&logger_session_id=2d8838e2a9692973cb46c957d8143d0375e5b522&__user=100006957738125&__a=1&__dyn=7xeUmFoO3yqSudwCwBzUKFVe79uCEkG2q6e3uVE98nwYCwqovzEdF8iByFUuwSwmoWdwJx659o4258O1hwgaxaaxG4oy0w8lwho3ewaGq1eK2V1CdwxgC3mbx-9xmbwrEsxe4U23xKicwKwBG11xnyGz81sbAy85iawnEfU7e2l2Utgvwi85W&__req=2o&__be=1&__pc=PHASED:ufi_home_page_pkg&dpr=2&__rev=4830042&jazoest=27985&__spin_r=4830042&__spin_b=trunk&__spin_t=1551963620'),
    # ('25-35M', 'ID', 'https://www.facebook.com/ads/audience-insights/query/?dpr=2&age[0]=25&age[1]=35&country[0]=ID&gender=2&metrics[0]=2&admarket_id=6017625189745&logger_session_id=e26d0c2b09149f49b70bd155fa98b3642e2ec774&__user=100006957738125&__a=1&__dyn=5V8WUmFoO3yqSudg9odoKFVe8UhBWqxiF88ooUdXCwAy8WqErxSawmWx-ex2axuF8iBAzouxa2e6FQ3mcUS2S4og-m10xicx21hwEyoC8yEqx6cw9a15UnDxm5EK10wOwRxeaCwjHGbwLghKbm7Qpy9US252odoKUryolyU6W78hDzo23xKicDwCx-mE465uaG4Hx63e0z8S15w_Ki8xWbwFyFE-17xS&__req=n&__be=1&__rev=4365232&__spin_r=4365232&__spin_b=trunk&__spin_t=1538186191&__pc=PHASED:DEFAULT&fb_dtsg_ag=AdyjS0F6SS__bcy29MRcsADIzmHoTDJhp0763NHcc0oWcQ:Adz907OWkmK8rW-QnFJGU0SnqdHR37xIZWZ6w0N7MB0TYQ&interests[0]=6003174867249&interests[1]=6003174913249&interests[2]=6003573036687&interests[3]=6003594632887&interests[4]=6004160395895'),
    # ('18-24W', 'ID', 'https://www.facebook.com/ads/audience-insights/query/?dpr=2&age[0]=18&age[1]=24&country[0]=ID&gender=2&metrics[0]=2&admarket_id=6017625189745&logger_session_id=e26d0c2b09149f49b70bd155fa98b3642e2ec774&__user=100006957738125&__a=1&__dyn=5V8WUmFoO3yqSudg9odoKFVe8UhBWqxiF88ooUdXCwAy8WqErxSawmWx-ex2axuF8iBAzouxa2e6FQ3mcUS2S4og-m10xicx21hwEyoC8yEqx6cw9a15UnDxm5EK10wOwRxeaCwjHGbwLghKbm7Qpy9US252odoKUryolyU6W78hDzo23xKicDwCx-mE465uaG4Hx63e0z8S15w_Ki8xWbwFyFE-17xS&__req=n&__be=1&__rev=4365232&__spin_r=4365232&__spin_b=trunk&__spin_t=1538186191&__pc=PHASED:DEFAULT&fb_dtsg_ag=AdyjS0F6SS__bcy29MRcsADIzmHoTDJhp0763NHcc0oWcQ:Adz907OWkmK8rW-QnFJGU0SnqdHR37xIZWZ6w0N7MB0TYQ&interests[0]=6002839660079&interests[1]=6003174867249&interests[2]=6003270811593&interests[3]=6003327060545&interests[4]=6003745655504&interests[5]=6003896280066&interests[6]=6004160395895'),
    # ('25-35W', 'ID', 'https://www.facebook.com/ads/audience-insights/query/?dpr=2&age[0]=25&age[1]=35&country[0]=ID&gender=2&metrics[0]=2&admarket_id=6017625189745&logger_session_id=e26d0c2b09149f49b70bd155fa98b3642e2ec774&__user=100006957738125&__a=1&__dyn=5V8WUmFoO3yqSudg9odoKFVe8UhBWqxiF88ooUdXCwAy8WqErxSawmWx-ex2axuF8iBAzouxa2e6FQ3mcUS2S4og-m10xicx21hwEyoC8yEqx6cw9a15UnDxm5EK10wOwRxeaCwjHGbwLghKbm7Qpy9US252odoKUryolyU6W78hDzo23xKicDwCx-mE465uaG4Hx63e0z8S15w_Ki8xWbwFyFE-17xS&__req=n&__be=1&__rev=4365232&__spin_r=4365232&__spin_b=trunk&__spin_t=1538186191&__pc=PHASED:DEFAULT&fb_dtsg_ag=AdyjS0F6SS__bcy29MRcsADIzmHoTDJhp0763NHcc0oWcQ:Adz907OWkmK8rW-QnFJGU0SnqdHR37xIZWZ6w0N7MB0TYQ&interests[0]=6003174867249&interests[1]=6003232228485&interests[2]=6003270811593&interests[3]=6003327060545&interests[4]=6003445225483&interests[5]=6003745655504&interests[6]=6003896280066&interests[7]=6004160395895'),
]


def compose_urls():
    for interest in interest_list:
        key = interest[1]
        url_list.append((key, 'Singapore', base_url % interest[0]))


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


def parse_data(url_key):
    global sheet1_data
    key, location, url = url_key
    res_json = get_request(url)
    data_list = res_json['payload']['2']['data']
    for name, values in dict(data_list).items():
        for value in values.get('pages'):
            try:
                one_row = [key, location, name, value.get('rank'), value.get('title'), value.get('url'), value.get('audience'), value.get('benchmark'), int(value.get('affinity'))]
                print one_row
                sheet1_data.append(one_row)
            except:
                print('ERR-row: ',value)


def parse_data_from_file(filename_key):
    global sheet1_data
    key, location, age, filename = filename_key
    res_json = get_request_from_file(filename)
    data_list = res_json['payload']['2']['data']
    for name, values in dict(data_list).items():
        for value in values.get('pages'):
            try:
                one_row = [key, location, age, name, value.get('rank'), value.get('title'), value.get('url'), value.get('audience'), value.get('benchmark'), int(value.get('affinity'))]
                sheet1_data.append(one_row)
            except:
                print('ERR-row: ',value)


def get_followers(url):
    try:
        html = get_request_of_url(url)
        reg = 'class="_4bl9">(.*?)people like this.*?class="_4bl9".*?><div>(.*?)people'
        data = re.compile(reg).findall(html)
        if data:
            return data[0][1]
        return 'N/A'
    except:
        print('ERR- get follower', url)


def get_request_of_url(url):
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
    req.add_header("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    res = HTMLParser.HTMLParser().unescape(res).decode('unicode-escape').replace('\\', '')
    return res


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


def get_request_from_file(filename):
    with open(filename, 'r') as content_file:
        content = content_file.read()
        return json.loads(content)


def scrape_from_urls():
    compose_urls()
    for url in url_list:
        print(url)
        try:
            parse_data(url)
        except:
            print('ERR-parse: ', url)


def scrape_from_files():
    filename_list = [
        ('Mazda', 'MY', 'MEN', 'MZ_M.html'),
        ('Mazda', 'MY', 'WOMEN', 'MZ_W.html'),
        ('Honda', 'MY', 'MEN', 'HD_M.html'),
        ('Honda', 'MY', 'WOMEN', 'HD_W.html'),
        ('Toyota', 'MY', 'MEN', 'TO_M.html'),
        ('Toyota', 'MY', 'WOMEN', 'TO_W.html'),
        ('Ford Motor Company', 'MY', 'MEN', 'FD_M.html'),
        ('Ford Motor Company', 'MY', 'WOMEN', 'FD_W.html'),
        ('Nissan', 'MY', 'MEN', 'NI_M.html'),
        ('Nissan', 'MY', 'WOMEN', 'NI_W.html'),
        ('Isuzu Motors', 'MY', 'MEN', 'IM_M.html'),
        ('Isuzu Motors', 'MY', 'WOMEN', 'IM_W.html'),
        ('Mitsubishi Motors', 'MY', 'MEN', 'MM_M.html'),
        ('Mitsubishi Motors', 'MY', 'WOMEN', 'MM_W.html'),
        ('Chevrolet', 'MY', 'MEN', 'CH_M.html'),
        ('Chevrolet', 'MY', 'WOMEN', 'CH_W.html'),
    ]
    for filename in filename_list:
        try:
            parse_data_from_file(filename)
        except Exception as e:
            print('ERR-parse: ', filename, e)

reload(sys)
# scrape_from_urls()
sys.setdefaultencoding('utf8')
scrape_from_files()
write_excel('data/sheet1.xls', sheet1_data)