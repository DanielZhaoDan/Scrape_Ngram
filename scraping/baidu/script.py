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

sheet1_data = [['Keywords', 'Country', 'No of Articles', 'Page No.', 'News Url', 'Date', 'Name of Publisher', 'Main url of newspaper/magazine', 'Headline', 'Content', 'Rank']]
sheet_dict = {}

url_base = 'http://news.baidu.com/ns?word={key_word}&pn={page_index}&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0'

key_words = [u'维生素', u'益生菌', u'维生素和矿物质', u'维生素D', u'补充剂', u'有机食品']

cookie = [
    'BIDUPSID=BFBD3CF9CBE26E37027528AF0EEF846C; PSTM=1470187991; __cfduid=debd361fc5ff9b250676babc59c94a3611476931139; BAIDUID=BFBD3CF9CBE26E37027528AF0EEF846C:FG=1; MCITY=-340%3A; BDUSS=doRmxUd2RTUGhmTlNaWkhpRjNtS29-TWd5WTRzZ3VvQ3dBVzFQWVQ5RGV0VWRZSVFBQUFBJCQAAAAAAAAAAAEAAADgZqAp1dS1pDI1MjcyOQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN4oIFjeKCBYZk; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[C0p6oIjvx-c]=mbxnW11j9Dfmh7GuZR8mvqV; BD_CK_SAM=1; PSINO=2; BDSVRTM=184; H_PS_PSSID=',
]


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_'+str(flag)+'.xls')
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
                    print '===Write excel ERROR==='+str(one_row[col])
    w.save(filename)
    print filename+"===========over============"


def get_total_count(html):
    reg = '<span class="nums">找到相关新闻约(.*?)篇</span>'
    results = re.compile(reg).findall(html)
    if results:
        return int(results[0].replace(',', ''))
    return 20


def request_sheet1(key_word):
    global sheet1_data
    total_count = 0
    page_no = 1
    while True:
        url = url_base.format(key_word=key_word, page_index=(page_no-1)*20)
        print url
        if page_no > 10:
            break
        html = get_request(url)
        if total_count == 0:
            total_count = get_total_count(html)
        topic_detail_reg = '<h3 class="c-title".*?href="(.*?)".*?>(.*?)</h3>.*?c-author">(.*?)<'
        topic_detail = re.compile(topic_detail_reg).findall(html)
        if not topic_detail:
            break
        i = 1
        for detail in topic_detail:
            url = detail[0]
            o = urlparse(url)
            main_url = o.scheme + '://' + o.netloc
            headline = remove_html_tag(detail[1])
            publisher, date = detail[2].split('&nbsp;&nbsp;')

            date = get_date(date)

            if not date:
                continue

            rank = str(page_no) + '.' + ('0' if i < 10 else '') + str(i)
            one_row = [key_word, total_count, page_no, url, date, publisher, main_url, headline, rank]
            sheet1_data.append(one_row)
            i += 1
        page_no += 1
        time.sleep(3)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_date(ori):
    try:
        date = datetime.strptime(ori.split(' ')[0], '%Y年%m月%d日')
        ts = int(time.mktime(date.timetuple()))
        if ts < 1451577600:
            return None
        return date.strftime('%d/%m/%Y')
    except:
        return None


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': random.choice(cookie),
        'x-client-data': 'CJG2yQEIprbJAQjBtskBCPKZygEI+5zKAQipncoB',
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
    request_sheet1(key_word)
write_excel('data/sheet1.xls', sheet1_data)