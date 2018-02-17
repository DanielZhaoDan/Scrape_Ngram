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
import xlsxwriter

sheet1_data = [
    ['ID', 'Headline', 'URL', 'Replies', 'Views', 'Topic Starter', 'Last Update Date', 'Post Date']]
sheet2_data = [['ID', 'Comments Text']]
url_bases = 'https://forum.lowyat.net/TelcoTalk/+%d'

cookie = 'lyn_mobile=0; __qca=P0-1345311929-1500711678191; lyn_modtids=%2C; _gat=1; lyn_forum_read=a%3A1%3A%7Bi%3A235%3Bi%3A1500947066%3B%7D; _ga=GA1.2.1862363292.1500711678; _gid=GA1.2.1299710544.1500947127; __asc=491f27b715d776b9b7bb0a13a0e; __auc=7f59fe9715d6962ee771362d915'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlsxwriter.Workbook(filename)
    ws = w.add_worksheet()
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write_string(row, col, (one_row[col]))
            except:
                ws.write(row, col, (one_row[col]))
    w.close()
    print filename+"===========over============"


def request_sheet1(url, starter=0):
    global sheet1_data

    print url
    html = get_request(url)
    topic_detail_reg = 'Begin Topic Entry (\d*).*?This topic was started: (.*?)">(.*?)<.*?<td.*?href.*?>(.*?)<.*?class="desc".*?>(.*?)<.*?<td.*?<td.*?= "(.*?)".*?class="lastaction">(.*?)<'
    topic_detail = re.compile(topic_detail_reg).findall(html)

    i = 0

    for detail in topic_detail:
        try:
            if i < starter:
                i += 1
                continue
            id = int(detail[0])
            topic_url = 'https://forum.lowyat.net/topic/%d/' % id
            start_date = get_date(detail[1].split(',')[0])
            headline = detail[2] + ' ' + detail[3]
            replies = detail[4]
            if '--' in replies:
                replies = 0
            else:
                replies = int(replies.replace(',', ''))
            views = detail[5]
            if '--' in views:
                views = 0
            else:
                views = int(views.replace(',', ''))
            end_date = get_last_date(detail[6])
            one_row = [id, headline, topic_url, replies, views, end_date, start_date]
            sheet1_data.append(one_row)
            # request_sheet2(id, topic_url+'+%d')
        except Exception as e:
            print 'ERROR-- ' + url
            print e
        i += 1


def request_sheet2(topic_id, topic_url):
    global sheet2_data
    html = get_request(topic_url % 0)
    detail_reg = 'class="postcolor post_text".*?>(.*?)<div class="signature"'

    if 'title="Jump to page..."' in html:
        total_page = get_total_page(html)
    else:
        total_page = 1
    print topic_url, total_page
    for i in range(total_page):
        single_url = topic_url % i*20
        if i > 0:
            html = get_request(single_url)
        comment_details = re.compile(detail_reg).findall(html)
        for comment in comment_details:
            if '<!--QuoteEEnd-->' in comment:
                comment = comment.split('<!--QuoteEEnd-->')[-1]
            comment = remove_html_tag(comment)
            one_row = [topic_id, comment]
            sheet2_data.append(one_row)


def get_total_page(html):
    reg = 'title="Jump to page...".*?>(.*?) Page'
    number = re.compile(reg).findall(html)
    if number:
        return int(number[0])
    return 1


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_last_date(ori):
    if 'Today' in ori:
        return '25/07/2017'
    elif 'Yesterday' in ori:
        ori = '24/07/2017'
    try:
        date = datetime.strptime(ori.split('-')[0].replace('th ', ' ').replace('rd ', ' ').replace('st ', ' ').replace('nd ', ' '), '%d %B %Y ')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_date(ori):
    try:
        date = datetime.strptime(ori, '%b %d %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
        'Host': 'forum.lowyat.net',
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    time.sleep(1)
    return res


def write_old_excel(filename, alldata):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    i = 0
    while len(alldata) > 65500:
        for row in range(0, 65500):
            one_row = alldata[row]
            for col in range(0, len(one_row)):
                try:
                    ws.write(row, col, one_row[col][:32766])
                except:
                    try:
                        ws.write(row, col, one_row[col])
                    except:
                        print '===Write excel ERROR==='+str(one_row[col])
        alldata = alldata[65500:]
        print len(alldata)
        new_filename = filename.replace('.xls', '_%d.xls'%i)
        w.save(new_filename)
        print new_filename + "===========over============"
        i += 1
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


reload(sys)
sys.setdefaultencoding('utf-8')

for i in range(0, 1):
    url = url_bases % (30 * i)
    request_sheet1(url, starter=0)

write_old_excel('data/sheet1.xlsx', sheet1_data)
write_old_excel('data/sheet2.xlsx', sheet2_data)

