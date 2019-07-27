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

url_bases = 'https://www.google.com/search?q={key_word}&newwindow=1&safe=strict&rlz=1C5CHFA_enSG792SG793&source=lnms&tbm=nws&sa=X&ved=0ahUKEwi8jMn9zs7hAhUDbn0KHc6mABMQ_AUIDigB&biw=1440&bih=798&start='
# url_bases = 'https://www.google.com/search?q={key_word}&tbm=nws&start='

FIRST_START = 1
cookie = [
    'CGIC=InZ0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIz; ANID=AHWqTUmO8w1qOdrwQVFRYsuXMaiCZISEiYZnRxN56vS78KD4eZYIFyl_AATHefbx; SID=mQc33W3LSF99ekG9eLtEyv_nSUxEsZjSGg2JFQOhvoWczvtKxIKORi-dCj2NeV2U1BGEOA.; HSID=AZmgxefONPYiGv9Md; SSID=AH4jqU2_YcWuLZ0N8; APISID=NkmiXhUdobCd4UdY/A6S6SFnbflsnny0pv; SAPISID=4HJsgOO2YfyLW-1i/ANdfdcAxTCuUT3AGL; CONSENT=YES+SG.en+20180429-14-0; SEARCH_SAMESITE=CgQItI0B; NID=188=Qd0lVGEmyZMGhxHHk5t_vhJ4JuRMEKGK1iSeduQ_X4mwMUpd72BVRRT-271aTuX5OOSAB-3Mc55xAKVzan8bcoDd5KsRj6zoS1aJGKiUf6HdigSo7IxngIb7_7ySSvvq5ykI8yMHsxZKKRZP2GI1xAE_3RrDDuryw9BABtbgbP1nJxh7gWcHkO5NDNyjHR1YFhnCzQ1xGnxIEPTnP8Ulh0bzPqfowOnfhzPJZETLJajiLZe8pAhT4nJGUnbBqAM168AkC8_BFwcFgAUk10fqp4iYA-hX; DV=471lmmdi7j5CEC-3iDq2DVtigzAWwxYvSfGgakooKQAAAGCxdu1bVsRpBgAAALgeeSgvfOIYAAAAAA; 1P_JAR=2019-7-27-3; SIDCC=AN0-TYsNxFmuJXhIXzGCEAQL_nCQ7IGSF-SVCQ3qCuXgY_G-vKgGQ4a7d1TFLphQHItMo-L3iPj9'
]

key_words = [
    {'keyword': 'amd intext:benchmark', 'bucket': 'AMD', 'country': 'ALL'},
    {'keyword': 'intel intext:benchmark', 'bucket': 'AMD', 'country': 'ALL'},
]


x_client_data = 'CIi2yQEIo7bJAQjBtskBCKmdygEI153KAQjZncoBCKijygE='

API_KEY = '051278798bc5c8d530a33186637244a9'


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


def get_total_count(html):
    reg = 'id="resultStats">.*?(\d.*?) result'
    results = re.compile(reg).findall(html)
    if results:
        return int(results[0].split('about')[-1].replace(',', ''))
    return 10


def request_sheet1(key_word, url_base, page_no=1):
    global sheet1_data
    total_count = 0
    while True:
        url = url_base + str(page_no - 1) + '0'
        print(url)
        if page_no > 10:
            break
        html = get_request(url)
        if 'Our systems have detected unusual traffic from your computer network' in html:
            return True
        if total_count == 0:
            total_count = get_total_count(html)
        topic_detail_reg = '<h3 .*?href="(.*?)".*?>(.*?)</a>.*?span.*?>(.*?)<.*?f nsa .*?">(.*?)<'
        topic_detail = re.compile(topic_detail_reg).findall(html)
        if not topic_detail:
            break
        i = 1
        for detail in topic_detail:
            url = detail[0]
            o = urlparse(url)
            main_url = o.scheme + '://' + o.netloc
            headline = remove_html_tag(detail[1])
            publisher = detail[2]
            date = get_date(detail[3])
            bucket = key_word['keyword'].split(' intext:')[0]
            # content = get_raw_content(url)
            content = ''
            rank = str(page_no) + '.' + ('0' if i < 10 else '') + str(i)
            one_row = [key_word['keyword'], bucket, key_word['country'], total_count, page_no, url, date,
                       publisher, main_url, headline, content,
                       rank]
            sheet1_data.append(one_row)
            i += 1
        page_no += 1
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

    rank_reg = 'rankingItem--global.*?rankingItem-value.*?>(.*?)<.*?rankingItem--country.*?rankingItem-value.*?>(.*?)<.*?rankingItem--category.*?rankingItem-value.*?>(.*?)<.*?Total Visits.*?countValue">(.*?)<'
    country_tag = 'accordion-toggle.*?countValue">(.*?)<.*?country-name.*?>(.*?)<'

    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[
        -1]
    print(url + ' ' + str(len(sheet_dict)))
    html = get_request(url)
    if 'NAME="ROBOTS"' in html:
        print('ROBOT DETECTED!, sleeping 600 seconds')
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
        date = datetime.strptime(ori, '%d %b %Y')
        return date.strftime('%d/%m/%Y')
    except Exception as e:
        return ori


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': random.choice(cookie),
        'x-client-data': x_client_data,
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
print(len(urls))

ts = int(time.time())
for i in range(len(urls)):
    url = urls[i]
    page_no = 1 if i > 0 else FIRST_START
    stop = request_sheet1(url[0], url[1], page_no=page_no)
    if stop:
        break
te = int(time.time())
print('time: ', te - ts)
write_excel('data/sheet1.xls', sheet1_data)