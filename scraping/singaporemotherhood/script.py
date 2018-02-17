# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd
import requests

import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

sheet0_data = [['Topic ID', 'Main Topic', 'Main Topic URL', 'Discussions', 'Messages']]
sheet1_data = [['Topic ID', 'Main Topic URL', 'Main Topic', 'Topics Level 1 Threads', 'Topics Level 1 URL', 'Topic Open Date', 'Topic Open Date (converted)', 'Last message date', 'Last message date (converted)', 'Replies', 'Views']]
sheet2_data = [['Topic ID', 'Main Topic URL', 'Main Topic', 'Topics Level 1 Threads', 'Topics Level 2 URL', 'Comment text', 'Comment Date', 'Comment Date (converted)']]

cookie = '__smVID=0176230909296cac73f4a763407f49b78bc3b77a5234760af6e8b757256d18fa; xf_session=a120e9680446edf05a80bc804f514396; _ga=GA1.2.680697549.1512142873; _gid=GA1.2.1432284110.1512142873; __smToken=5rjcF16nvaW6ZMXiZlkBcXA3'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xlsx', '_'+str(flag)+'.xls')
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


def request_sheet0():
    global sheet1_data, sheet2_data
    url = 'https://singaporemotherhood.com/forum/'
    html = get_request(url)
    reg = 'class="nodeText".*?href="(.*?)".*?>(.*?)<.*?<dd>(.*?)<.*?<dd>(.*?)<.*?'
    lists = re.compile(reg).findall(html)
    id = 1
    urls = []
    for list in lists:
        if id <= 2:
            id += 1
            continue
        url = 'https://singaporemotherhood.com/forum/' + list[0]
        title = remove_html_tag(list[1])
        dis_count = list[2].replace(',', '')
        msg_count = list[3].replace(',', '')
        urls.append([title, url])
        one_row = [id, title, url, dis_count, msg_count]
        sheet0_data.append(one_row)
        request_sheet1(id, url, title, int(dis_count) / 40 + 1)
        write_excel('data/sheet1_%d.xls' % id, sheet1_data)
        write_excel('data/sheet2_%d.xls' % id, sheet2_data)
        del sheet1_data
        del sheet2_data
        sheet1_data = [['Topic ID', 'Main Topic URL', 'Main Topic', 'Topics Level 1 Threads', 'Topics Level 1 URL', 'Topic Open Date', 'Topic Open Date (converted)', 'Last message date', 'Last message date (converted)', 'Replies', 'Views']]
        sheet2_data = [['Topic ID', 'Main Topic URL', 'Main Topic', 'Topics Level 1 Threads', 'Topics Level 2 URL', 'Comment text', 'Comment Date', 'Comment Date (converted)']]
        id += 1


def request_sheet1(main_id, url_base, main_title, page_count):
    global sheet1_data
    reg = 'class="discussionListItem .*?class="title".*?href="(.*?)".*?>(.*?)<.*?class="DateTime".*?>(.*?)<.*?Replies.*?dd>(.*?)<.*?<dd>(.*?)<.*?class="dateTime">.*?>(.*?)<'
    if page_count > 30:
        page_count = 30
    for i in range(1, page_count+1):
        url = (url_base + 'page-%s') % i
        print main_id, url, page_count, i
        html = get_request(url)
        topics = re.compile(reg).findall(html)
        for topic in topics:
            try:
                level1_title = remove_html_tag(topic[1])
                level1_title = remove_html_tag(level1_title)
                level1_url = 'https://singaporemotherhood.com/forum/' + topic[0]
                first_date = topic[2].split(' at')[0]
                first_date_converted = get_date(first_date)
                replies = topic[3].replace(',', '')
                views = topic[4].replace(',', '')
                last_date = topic[5].split(' at')[0]
                last_date_converted = get_date(last_date)
                one_row = [main_id, url_base, main_title, level1_title, level1_url, first_date, first_date_converted, last_date, last_date_converted, replies, views]
                sheet1_data.append(one_row)
                request_sheet2(main_id, url_base, main_title, level1_title, int(replies) / 50 + 1, level1_url)
            except Exception as e:
                print 'Exception - level1 - %s - %s' % (url, str(e))


def request_sheet2(main_id, main_url, main_title, level1_title, page_number, level1_url):
    global sheet2_data
    reg = 'blockquote.*?>(.*?)</blockquote>.*?class="DateTime".*?>(.*?)<'
    if page_number > 50:
        page_number = 50
    for i in range(1, page_number+1):
        url = level1_url + 'page-' + str(i)
        try:
            html = get_request(url)
            comments = re.compile(reg).findall(html)
            for comment in comments:
                text = remove_html_tag(comment[0])
                text = remove_html_tag(text)
                date = comment[1].split(' at')[0]
                date_converted = get_date(date)
                one_row = [main_id, main_url, main_title, level1_title, level1_url, text, date, date_converted]
                sheet2_data.append(one_row)
        except Exception as e:
            print 'Exception - level2 - %s - %s' % (url, str(e))


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_date(ori):
    d = datetime.strptime(ori, '%b %d, %Y')
    date = d.strftime('%d/%m/%Y')
    return date


def get_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
        'Host': 'www.singaporemotherhood.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2',
        'Cache-Control': 'no-cache',
    }
    req = requests.get(get_url, headers=headers)
    res = req.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')
request_sheet0()