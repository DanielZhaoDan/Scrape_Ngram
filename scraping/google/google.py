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

sheet1_data = [
    ['Keywords String', 'Bucket', 'Country', 'No of Articles', 'Page No.', 'News Url', 'Date', 'Name of Publisher',
     'Main url of newspaper/magazine', 'Headline', 'Content', 'Rank']]
sheet_dict = {}

url_bases = 'https://www.google.com.sg/search?q={key_word}&newwindow=1&safe=strict&tbs=cdr:1,cd_min:1/1/2016,cd_max:6/30/2017&ei=fwqLWeO_PMXmvgTO977gCw&sa=N&biw=1220&bih=703&start='

key_words = [
    # {'keyword': 'kaligtasan sa credit credit card inurl:ph', 'bucket': 'Credit Card', 'country': 'Philippines'},
    # {'keyword': 'panloloko sa credit credit card inurl:ph', 'bucket': 'Credit Card', 'country': 'Philippines'},
    # {'keyword': 'panloloko sa internet inurl:ph', 'bucket': 'Online', 'country': 'Philippines'},
    {'keyword': 'proteksyon sa password inurl:ph', 'bucket': 'Online', 'country': 'Philippines'},
    # {'keyword': 'phishing sa pilipinas inurl:ph', 'bucket': 'Online', 'country': 'Philippines'},
    # {'keyword': 'scam online sa pinas inurl:ph', 'bucket': 'Online', 'country': 'Philippines'},
    # {'keyword': 'credit card sa internet inurl:ph', 'bucket': 'Credit Card', 'country': 'Philippines'},
    # {'keyword': 'panloloko sa bangko online inurl:ph', 'bucket': 'Online', 'country': 'Philippines'},
    # {'keyword': 'ligtas na paglalakbay inurl:ph', 'bucket': 'Travel', 'country': 'Philippines'},
    # {'keyword': 'raket sa paglalakbay inurl:ph', 'bucket': 'Travel', 'country': 'Philippines'},
    # {'keyword': 'tips sa paglalakbay inurl:ph', 'bucket': 'Travel', 'country': 'Philippines'},
    # {'keyword': 'kabayaran sa kinabukasan online inurl:ph', 'bucket': 'Future payment/online',
    #  'country': 'Philippines'},
]

http_proxies = [
    'http://183.88.29.181:8080',
]

cookie = [
    'OGPC=845686784-30:5062177-3:5062227-6:; SID=xQQ33Svb38r7qmapGxt4UVPyp9NavhVmfx1EBDGUtDzBdkC3FoPleuGWRx54BqpzkAkGhQ.; HSID=Azl-v0_BCpCYNZwMX; SSID=AUWY-HQGFpGmFQi2o; APISID=LfvnGfiTI2WZUQC-/AQrf72uCq7KTRkhoH; SAPISID=_6td03PWM2tP_0ej/ALEul5vhqbyIa_axX; GOOGLE_ABUSE_EXEMPTION=ID=abcc502aa7cea33a:TM=1502287996:C=r:IP=119.74.13.134-:S=APGng0u-Zbqu0qGFQZF1euPKm_dG-0amWw; NID=109=uQ57QFa8ZDLUWWFTOhWB6DGhYl0REVk-ml-wLSMsz1PrJJgROQqhp2HnVrfoDFDvpA6zTxgwxT2_oE8UR3yB1fXJP8MthNfqSjqz7EOqj2w5yFfUg7MKREAwYoz0LL8IeiaeUm1t6r_U7OgZ7OtnKGOtYZI4bUzLa0nxAj3-WlBJ-WafjNEYiryBL6H91h2UU0xbySIsZtbTEbvHX1BqL_u7hbKCQ_EZ2JNtFTP3wQ0vp4cCCOgx9wRJkHcZDLd9NFPBr0g--dXsVlHyxKDxfwRq12Po7iV6MuKp7GwNFPbeDAVKODhj57Bm7sW36LLRaDMqfYr9_F7PSDeSXk3CWV_bFmr9dKs; DV=471lmmdi7j5CMIY2UoZ-rYeIYX113FXttd0dLzc90QEAAMAyNxg4LoTvEQEAAIStbbx-WJC9WwAAAA; UULE=a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTUwMjI4ODAxMzM5MDAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6MTM1ODk2NzYgbG9uZ2l0dWRlX2U3OjEwMzg0MzY3NTF9IHJhZGl1czoyNDgwMA==',
]

API_KEY = '051278798bc5c8d530a33186637244a9'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


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
                    print '===Write excel ERROR===' + str(one_row[col])
    w.save(filename)
    print filename + "===========over============"


def get_total_count(html):
    reg = 'id="resultStats">.*?(\d.*?) result'
    results = re.compile(reg).findall(html)
    if results:
        return int(results[0].split('about')[-1].replace(',', ''))
    return 10


def request_sheet1(key_word, url_base):
    global sheet1_data
    total_count = 0
    page_no = 1
    while True:
        url = url_base + str(page_no - 1) + '0'
        print url
        if page_no > 4:
            break
        html = get_request(url)
        if 'Our systems have detected unusual traffic' in html or '我们的系统检测到您的计算机网络' in html:
            return True
        if total_count == 0:
            total_count = get_total_count(html)

        topic_detail_reg = '<h3 .*?href="(.*?)".*?>(.*?)</a>.*?span class="f">(.*?)<.*?>(.*?)</span'
        topic_detail = re.compile(topic_detail_reg).findall(html)
        if not topic_detail:
            break
        i = 1
        for detail in topic_detail:
            url = detail[0]
            o = urlparse(url)
            main_url = o.scheme + '://' + o.netloc
            headline = remove_html_tag(detail[1])
            publisher = o.netloc
            date = get_date(detail[2].split(' - ')[0])
            content = remove_html_tag(detail[3])
            rank = str(page_no) + '.' + ('0' if i < 10 else '') + str(i)
            one_row = [key_word['keyword'], key_word['bucket'], key_word['country'], total_count, page_no, url, date,
                       publisher, main_url, headline, content,
                       rank]
            sheet1_data.append(one_row)
            print(one_row)
            i += 1
        page_no += 1
        time.sleep(3)
    return False


def get_raw_content(url):
    try:
        html = get_request(url)
        reg = '<body.*?>(.*?)</body>'
        contents = re.compile(reg).findall(html)
        if contents:
            content = contents[0]
            step_0 = remove_html_tag(content)  # remove html tag
            step_1 = re.sub('[ \t\n\r]+', ' ', step_0)  # remove multiple blank, newline and tab
            return step_1
        return html
    except:
        return ''


def request_sheet2(base_url):
    global sheet_dict
    if sheet_dict.get(base_url):
        return sheet_dict[base_url]

    if len(sheet_dict) and len(sheet_dict) % 5 == 0:
        print 'Sleeping 300 seconds'
        time.sleep(60)
    else:
        print 'Sleeping 10 seconds'
        time.sleep(10)
    rank_reg = 'rankingItem--global.*?rankingItem-value.*?>(.*?)<.*?rankingItem--country.*?rankingItem-value.*?>(.*?)<.*?rankingItem--category.*?rankingItem-value.*?>(.*?)<.*?Total Visits.*?countValue">(.*?)<'
    country_tag = 'accordion-toggle.*?countValue">(.*?)<.*?country-name.*?>(.*?)<'

    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[
        -1]
    print url + ' ' + str(len(sheet_dict))
    html = get_request(url)
    if 'NAME="ROBOTS"' in html:
        print 'ROBOT DETECTED!, sleeping 600 seconds'
        time.sleep(600)
        return None
    global_ranks = re.compile(rank_reg).findall(html)
    if global_ranks:
        ret = [global_ranks[0][0].replace('[#,]', ''), global_ranks[0][1].replace('[#,]', ''),
               global_ranks[0][2].replace('[#,]', ''), global_ranks[0][3]]
    else:
        ret = [0, 0, 0, 0]

    country_ranks = re.compile(country_tag).findall(html)
    for country in country_ranks:
        ret.append(country[1])
        ret.append(country[0])
    if len(ret) == 4:
        ret += [0 for i in range(10)]
    sheet_dict[base_url] = ret
    return ret


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
            print one_row
            sheet2_data.append(one_row)
        except:
            print(i)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_date(ori):
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
        'x-client-data': 'CJS2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQ==',
    }
    proxy = {
        'http': random.choice(http_proxies),
        'https': random.choice(http_proxies),
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')
# scrape google search result
urls = []
for key_word in key_words:
    urls.append([key_word, url_bases.format(key_word=key_word['keyword'].replace(' ', '+'))])
print len(urls)
for url in urls:
    stop = request_sheet1(url[0], url[1])
    if stop:
        break
write_excel('data/sheet2.xls', sheet1_data)
