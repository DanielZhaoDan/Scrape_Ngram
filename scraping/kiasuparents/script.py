# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd

sheet1_data = [['Topic', 'No. Replies', 'No. Views', 'Date of First Post', 'Day of the Week', 'Date of Last Post', 'Day of the Week']]
sheet2_data = [['Topic', 'Replies', 'Date', 'Day of the Week']]

url_base = 'https://www.kiasuparents.com/kiasu/forum/viewforum.php?f=30&start=%s'

cookie = 'phpbb3_e5hmi_wps_u=1; phpbb3_e5hmi_wps_k=; phpbb3_e5hmi_wps_sid=64778e7d97e12f8dfde10c5c88c75062; _gat_UA-2531648-1=1; style_cookie=printonly; _ga=GA1.2.2127770656.1486522026; __atuvc=16%7C6; __atuvs=589a86aa96ff4ad700f'


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


def request_sheet1(url):
    global sheet1_data
    # link, name, replies, views
    topic_body_reg = 'class="forumbg".*?class="topiclist topics"(.*?)/ul'
    html = get_request(url)
    topic_body = re.compile(topic_body_reg).findall(html)
    if not topic_body:
        return
    topic_detail_reg = '<dt .*?title.*?>(.*?)</dt>.*?class="posts">(.*?)<.*?class="views">(.*?)<.*?title="View the latest post".*?<br />(.*?)<'
    topic_detail = re.compile(topic_detail_reg).findall(topic_body[0])
    for detail in topic_detail:
        raw_topic = detail[0]
        topic, link, first_date, first_day_week = extract_raw_topic(raw_topic)
        replies = int(detail[1])
        views = int(detail[2])
        last_date, last_day_week = get_date(detail[3])
        one_row = [topic, str(replies), str(views), first_date, str(first_day_week), last_date, str(last_day_week)]
        sheet1_data.append(one_row)
        page_number = replies / 10 + 1
        request_sheet2(topic, page_number, link)


def extract_raw_topic(raw_topic):
    reg = 'href="(.*?)".*?>(.*?)<.*?&raquo; (.*?)<'
    entry = re.compile(reg).findall(raw_topic)[0]
    url = 'https://www.kiasuparents.com/kiasu/forum/' + entry[0].replace('./', '').replace('&amp;', '&')
    first_date = get_date(entry[2])
    return entry[1].replace('&amp;', '&'), url, first_date[0], first_date[1]


def request_sheet2(topic, number, url2_base):
    global sheet2_data
    reg = 'class="postbody".*?class="author".*?&raquo; (.*?) <.*?class="content">(.*?)</div>'
    for i in range(number):
        url = url2_base + '&start=' + str(i*10)
        print url
        html = get_request(url)
        reply_lists = re.compile(reg).findall(html)
        for reply in reply_lists:
            date, day = get_date(reply[0])
            content = remove_html_tag(reply[1])
            one_row = [topic, content, date, str(day)]
            sheet2_data.append(one_row)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_date(ori):
    d = datetime.strptime(ori, '%a %b %d, %Y %I:%M %p')
    date = d.strftime('%d/%m/%Y')
    return date, d.weekday() + 1


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", get_url)
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')

size = 9
for i in range(size):
    print '-----Level 1 Page ' + str(i) + '-----'
    url = url_base % str(i*50)
    request_sheet1(url)
write_excel('data/sheet1.xls', sheet1_data)
write_excel('data/sheet2.xls', sheet2_data)