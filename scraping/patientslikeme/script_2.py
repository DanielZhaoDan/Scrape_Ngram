# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd
from scraping.utils import get_request_html

sheet1_data = [['Topic ID', 'Topic URL', 'Topic Name', 'No. Likes']]
sheet2_data = [['Topic ID', 'Topic URL', 'UserName', 'Reply Date', 'Reply Content', 'No. likes']]

url_base = 'https://www.patientslikeme.com/forum/plm/topics/search?forum_id=plm&search%5Btext%5D='

key_words = [
    ('Probiotics', 2),
    ('Prebiotics', 12),
    ('Microbiome', 1),
]

UID = 1

cookie = '__uzma=5528134681358703737; __uzmb=1600871698; _csrf_token=vMus%2FoZDl%2FsxHRh5yeQLxHpddAVpuaOWJMkfQasVvG0%3D; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=ea1fe93e-f7a3-41e9-8eae-fccc97ca46f6; __uzmbj2=1600871700; metric_guid=97f3ceea-19d3-40a6-8e8c-7dce9f111aa5; _session_id=7c56c7fe3c1ccf88987d147c19d8fa68; amplitude_idpatientslikeme.com=eyJkZXZpY2VJZCI6IjI2YWU2ZWY2LTI4YWQtNGQ1OS04MjAyLTI2MjdhMjk3ZmViYVIiLCJ1c2VySWQiOiI5N2YzY2VlYS0xOWQzLTQwYTYtOGU4Yy03ZGNlOWYxMTFhYTUiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE2MDA4NzE3MDA0NjgsImxhc3RFdmVudFRpbWUiOjE2MDA4NzI1NjA5MjYsImV2ZW50SWQiOjQyLCJpZGVudGlmeUlkIjoyMiwic2VxdWVuY2VOdW1iZXIiOjY0fQ==; __uzmcj2=975277323973; __uzmdj2=1600872560; __uzmd=1600872561; __uzmc=6899523585082'


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


def request_sheet1(item):
    global sheet1_data, UID

    key_word, page_no = item

    reg = 'header-3" href="(.*?)">(.*?)<.*?Number of helpful marks received.*?Number of helpful marks received">(.*?)<'

    for i in range(1, page_no+1):
        url = url_base + key_word + '&page=' + str(i)
        print url

        try:
            html = get_request_html(url, cookie)
            data = re.compile(reg).findall(html)

            for it in data:
                topic_url = 'https://www.patientslikeme.com' + it[0]
                name = it[1]
                no_like = it[2]

                one_row = [key_word + '_' + str(UID), topic_url, name, no_like]
                # print one_row
                sheet1_data.append(one_row)
                UID += 1

        except Exception as e:
            print 'ERR--', url, e


def request_sheet2(topic_id, url2_base):
    global sheet2_data
    reg = 'avatarText":"(.*?)".*?datetime="(.*?)".*?data-react-props.*?body(.*?)"}.*?post_helpful_marker(.*?)Mark this post as helpful'

    page_no = None
    i = 1
    while not page_no or i <= page_no:

        try:
            html = get_request_html(url2_base + '&page=' + str(i), cookie)

            if not page_no:
                page_no = get_page_no(html)
            comments = re.compile(reg).findall(html)

            for com in comments:
                username = com[0]
                text_time = get_date(com[1])
                text = remove_html_tag(str(com[2]))
                no_like = get_no_like(com[3])

                one_row = [topic_id, url2_base, username, text_time, text, no_like]
                sheet2_data.append(one_row)
            print url2_base, i, page_no, len(comments)

            i += 1

        except Exception as e:
            print 'ERR--', url2_base, i, e


def get_no_like(ori):
    if '"Number of helpful marks received">' in ori:
        return ori.split('"Number of helpful marks received">')[-1].split('<')[0]
    return 0


def get_page_no(ori):
    if 'previous_page' not in ori:
        return 1
    reg = 'aria-label="Page (.*?)"'

    return int(re.compile(reg).findall(ori)[-1])


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_date(ori):
    d = datetime.strptime(ori.split('T')[0], '%Y-%m-%d')
    date = d.strftime('%d/%m/%Y')
    return date


def read_excel(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            profile_id = row[0].value
            profile_url = row[1].value
            request_sheet2(profile_id, profile_url)
        except Exception as e:
            print(i, e)


def remove_tag(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            text = row[4].value
            pure = remove_html_tag(text).replace('":"', '')
            sheet2_data.append([pure])
        except Exception as e:
            print(i, e)

reload(sys)
sys.setdefaultencoding('utf-8')

# for key_word in key_words:
#     request_sheet1(key_word)

# read_excel('data/sheet1.xls')
remove_tag('data/sheet2.xls')
write_excel('data/sheet3.xls', sheet2_data)