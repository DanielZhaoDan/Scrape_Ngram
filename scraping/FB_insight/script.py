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
    ('18', '24'),
    ('24', '35'),
]

location_list = [
    ('Puebla', 2525, 'PB'), #R
]

gender_list = ['1']
interest_list = ['none']
cookie = 'datr=RKzWW_1NuhIxB9RG7RUemqv0; sb=ovjqW-tww_Qe7OR39cZQ91wp; c_user=100006957738125; xs=145%3Ay4f_mOf19tmvnQ%3A2%3A1542430919%3A20772%3A8703; pl=n; dpr=2; spin=r.4560902_b.trunk_t.1543236080_s.1_v.2_; fr=0mVSQPNFOoV7LvCYc.AWVjHNVKa0_8wKpfO8V4MnPhNWU.Bb0aQ1.Cv.Fv5.0.0.Bb_BWq.AWUaqBBs; act=1543247914543%2F4; presence=EDvF3EtimeF1543248134EuserFA21B06957738125A2EstateFDt3F_5b_5dEutc3F1542805611360G543248134727CEchFDp_5f1B06957738125F6CC; wd=1385x329; pnl_data2=eyJhIjoib25hZnRlcmxvYWQiLCJjIjoiWEFkc0tlcGxlckNvbnRyb2xsZXIiLCJiIjpmYWxzZSwiZCI6Ii9hZHMvYXVkaWVuY2UtaW5zaWdodHMvaW50ZXJlc3RzIiwiZSI6W119'
base_url = 'https://www.facebook.com/ads/audience-insights/query/?dpr=2&education[0]=2&age[0]=%s&age[1]=%s&region[0]=%s&gender=%s&metrics[0]=2'

url_tail = '&fb_dtsg_ag=AdyI1UDUPhaTf5LcrMZlfCBgT5MwGzaMJnKQMco1wvRfuQ:AdwXaKoRyzmR0lAQzwkCaPeAQRL5pyRipF_CAwIDZSOA1w&admarket_id=6017625189745&logger_session_id=46f5759fa1985733068e244d6fb16b276c40601f&__user=100006957738125&__a=1&__dyn=7xeUmFoO3yqSudwCwBzUKFVe8UhBWqxiF88ooUdXCwAy8KFGxK5FEG1rG7UW48G5WAxamimu7EiwzxGu3qcUS2S4og-mdwOxicx21hwEyoC8yEqx68w825o4nxuu5omyU423a3m4UGq1eKEK2Z16UJovhC8Dzo8k9wRyXxK9xmbwrEsx6udwo88ErAz9U9EpBBF0g8lUFoOmUhwPw8OdwhofXAy8uyUaoGqbK17xS267o5m2l2Utgvw&__req=5g&__be=1&__pc=PHASED:DEFAULT&__rev=4560902&__spin_r=4560902&__spin_b=trunk&__spin_t=1543236080'

sheet1_data = [['id', 'location', 'category', 'rank', 'page name', 'url', 'followers']]

url_list = [
    # ('18-14M', 'ID', 'https://www.facebook.com/ads/audience-insights/query/?dpr=2&age[0]=18&age[1]=24&country[0]=ID&gender=2&metrics[0]=2&admarket_id=6017625189745&logger_session_id=e26d0c2b09149f49b70bd155fa98b3642e2ec774&__user=100006957738125&__a=1&__dyn=5V8WUmFoO3yqSudg9odoKFVe8UhBWqxiF88ooUdXCwAy8WqErxSawmWx-ex2axuF8iBAzouxa2e6FQ3mcUS2S4og-m10xicx21hwEyoC8yEqx6cw9a15UnDxm5EK10wOwRxeaCwjHGbwLghKbm7Qpy9US252odoKUryolyU6W78hDzo23xKicDwCx-mE465uaG4Hx63e0z8S15w_Ki8xWbwFyFE-17xS&__req=n&__be=1&__rev=4365232&__spin_r=4365232&__spin_b=trunk&__spin_t=1538186191&__pc=PHASED:DEFAULT&fb_dtsg_ag=AdyjS0F6SS__bcy29MRcsADIzmHoTDJhp0763NHcc0oWcQ:Adz907OWkmK8rW-QnFJGU0SnqdHR37xIZWZ6w0N7MB0TYQ&interests[0]=6003142845761&interests[1]=6003174867249&interests[2]=6003174913249&interests[3]=6003176678152&interests[4]=6003290348256&interests[5]=6003573036687'),
    # ('25-35M', 'ID', 'https://www.facebook.com/ads/audience-insights/query/?dpr=2&age[0]=25&age[1]=35&country[0]=ID&gender=2&metrics[0]=2&admarket_id=6017625189745&logger_session_id=e26d0c2b09149f49b70bd155fa98b3642e2ec774&__user=100006957738125&__a=1&__dyn=5V8WUmFoO3yqSudg9odoKFVe8UhBWqxiF88ooUdXCwAy8WqErxSawmWx-ex2axuF8iBAzouxa2e6FQ3mcUS2S4og-m10xicx21hwEyoC8yEqx6cw9a15UnDxm5EK10wOwRxeaCwjHGbwLghKbm7Qpy9US252odoKUryolyU6W78hDzo23xKicDwCx-mE465uaG4Hx63e0z8S15w_Ki8xWbwFyFE-17xS&__req=n&__be=1&__rev=4365232&__spin_r=4365232&__spin_b=trunk&__spin_t=1538186191&__pc=PHASED:DEFAULT&fb_dtsg_ag=AdyjS0F6SS__bcy29MRcsADIzmHoTDJhp0763NHcc0oWcQ:Adz907OWkmK8rW-QnFJGU0SnqdHR37xIZWZ6w0N7MB0TYQ&interests[0]=6003174867249&interests[1]=6003174913249&interests[2]=6003573036687&interests[3]=6003594632887&interests[4]=6004160395895'),
    # ('18-24W', 'ID', 'https://www.facebook.com/ads/audience-insights/query/?dpr=2&age[0]=18&age[1]=24&country[0]=ID&gender=2&metrics[0]=2&admarket_id=6017625189745&logger_session_id=e26d0c2b09149f49b70bd155fa98b3642e2ec774&__user=100006957738125&__a=1&__dyn=5V8WUmFoO3yqSudg9odoKFVe8UhBWqxiF88ooUdXCwAy8WqErxSawmWx-ex2axuF8iBAzouxa2e6FQ3mcUS2S4og-m10xicx21hwEyoC8yEqx6cw9a15UnDxm5EK10wOwRxeaCwjHGbwLghKbm7Qpy9US252odoKUryolyU6W78hDzo23xKicDwCx-mE465uaG4Hx63e0z8S15w_Ki8xWbwFyFE-17xS&__req=n&__be=1&__rev=4365232&__spin_r=4365232&__spin_b=trunk&__spin_t=1538186191&__pc=PHASED:DEFAULT&fb_dtsg_ag=AdyjS0F6SS__bcy29MRcsADIzmHoTDJhp0763NHcc0oWcQ:Adz907OWkmK8rW-QnFJGU0SnqdHR37xIZWZ6w0N7MB0TYQ&interests[0]=6002839660079&interests[1]=6003174867249&interests[2]=6003270811593&interests[3]=6003327060545&interests[4]=6003745655504&interests[5]=6003896280066&interests[6]=6004160395895'),
    # ('25-35W', 'ID', 'https://www.facebook.com/ads/audience-insights/query/?dpr=2&age[0]=25&age[1]=35&country[0]=ID&gender=2&metrics[0]=2&admarket_id=6017625189745&logger_session_id=e26d0c2b09149f49b70bd155fa98b3642e2ec774&__user=100006957738125&__a=1&__dyn=5V8WUmFoO3yqSudg9odoKFVe8UhBWqxiF88ooUdXCwAy8WqErxSawmWx-ex2axuF8iBAzouxa2e6FQ3mcUS2S4og-m10xicx21hwEyoC8yEqx6cw9a15UnDxm5EK10wOwRxeaCwjHGbwLghKbm7Qpy9US252odoKUryolyU6W78hDzo23xKicDwCx-mE465uaG4Hx63e0z8S15w_Ki8xWbwFyFE-17xS&__req=n&__be=1&__rev=4365232&__spin_r=4365232&__spin_b=trunk&__spin_t=1538186191&__pc=PHASED:DEFAULT&fb_dtsg_ag=AdyjS0F6SS__bcy29MRcsADIzmHoTDJhp0763NHcc0oWcQ:Adz907OWkmK8rW-QnFJGU0SnqdHR37xIZWZ6w0N7MB0TYQ&interests[0]=6003174867249&interests[1]=6003232228485&interests[2]=6003270811593&interests[3]=6003327060545&interests[4]=6003445225483&interests[5]=6003745655504&interests[6]=6003896280066&interests[7]=6004160395895'),
]


def compose_urls():
    for age in age_list:
        for location in location_list:
            for gender in gender_list:
                for interest in interest_list:
                    url = base_url % (age[0], age[1], location[1], gender)
                    if interest != 'none':
                        interests = interest.split('-')
                        for i in range(0, len(interests)):
                            url  = url + '&interests[%d]=' % i + interests[i]
                    url += url_tail
                    key = age[0] + '-' + age[1] + ('F' if gender == '1' else 'M') + '-' + location[2]
                    url_list.append((key, location[0], url))


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
                one_row = [key, location, name, value.get('rank'), value.get('title'), value.get('url'), get_followers(value.get('url'))]
                print one_row
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

reload(sys)
sys.setdefaultencoding('utf8')
compose_urls()
for url in url_list:
    print(url)
    try:
        parse_data(url)
    except:
        print('ERR-parse: ', url)
write_excel('data/sheet1.xls', sheet1_data)