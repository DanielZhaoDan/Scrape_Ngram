# -*- coding: utf-8 -*-
import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd
import time
import requests
import json
import sets

C_ID = 1
T_ID = 1
sheet0_data = [['Category ID', 'Category', 'Category URL', 'No. Topics', 'No. Posts']]
sheet1_data = [['Category ID', 'Topic ID', 'Topic Name', 'Topic URL', 'No. Replies', 'No. Views', 'Latest Date']]
sheet2_data = [['Category ID', 'Topic ID', 'Reply Content', 'Responder Name', 'Responder URL', 'Responder Profession', 'Responder Posts', 'Responder Join Date']]
sheet3_data = [['Responder Name', 'Group', 'Profession', 'URL', 'No. Posts', 'Most active Forum', 'Post By Most Active Forum', 'Current Topic', 'Current Topic Posts']]

scraped_profile_name = set()

cookie = 'bcookie="v=2&2f6c9444-0b2f-466a-8183-ef73e05efa35"; bscookie="v=1&2017041006541990b97a3b-1e52-4da3-8e47-33e0e8e1e3aeAQGgvnt_FYPCpH58BfQhdPydnY6jBTcZ"; visit="v=1&M"; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; join_wall=v=2&AQFhNUYNvP5n8AAAAVvSGU2GWS-2YElFKFQfNLC9Lu27yuc26LdeUp9IUsKvRn7BvDIJPGj6Zt09FXQUVCLbJE5T4W0KMdm9iux6K5mfVuB5Al9lYuJTWUBl0xM5cg4AMo4OmPiAUgPTTiMJIvsvxX3_7b8rimV18UwuwyE_ICE9FB5ZyYrBVwHPGg; _gid=GA1.2.990777859.1493878542; sl="v=1&sHIVY"; lang="v=2&lang=en-us"; li_at=AQEDARo-DEsAlf1eAAABW9IZzwoAAAFb09FDClYAzTg2ibTPV-O_Dqr3MSP-yhBB8KrNn4Sa9FY7OP-sBHXfvSDGKlzMJUbF12JOgmIxNmG6sXSF3r4_PKBUvZu-f2F3gCEr560b6Dh1BVf4llZka-Qo; JSESSIONID="ajax:1423185689819717669"; liap=true; lidc="b=TB95:g=558:u=43:i=1493878607:t=1493887866:s=AQFM0gn66ojmBqIFbNtwViz-OMqniwCu"; _ga=GA1.2.610623672.1491807398; _gat=1; _lipt=CwEAAAFb0mlL-HRaJDSReqC3hAtYV6Gup6SrDmh9grOcTvZEwbVaZrD-Js3CtvzL2XQ5DsbJ1aTSgvt48xo9T6UM8oP5utFRJ53syRDWfYqRUCQnjHn-AFyM7d-TySMlw7lVj3eigG4NQFSEpO1mmy1XA5S9_r2Ie4UjKVH90oKCl1PPzy_xQKRFP3ijNfrmn7dHnVfyWApPdWiWijUTNjra8ApDgf7DIiFGK7mZGx5CJ_aYGnD1XC8N-UWnv5LcTCzos3rB3VxRHzjjioox1ZtLKrVdKo_M55QfM85UL6RcwUbbGx0iPa_T_fRshq1RrwkgZKtPAnOlGeOoGnYQdv6p4D7mCgKUbdFYDiZrViiYjqzFAw'

files = []

BASE_URL = 'http://www.doctorshangout.com/forum?page=%d'


def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path or 'txt' in path:
            if 'result' not in path:
                files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files


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


def request_sheet0():
    global sheet0_data
    url = 'https://www.doctorslounge.com/forums/'
    html = get_request(url)
    reg = 'icon forum_read.*?href="(.*?)".*?>(.*?)<.*?class="topics">(.*?)<.*?class="posts">(.*?)<'
    sheet0_raw_data = re.compile(reg).findall(html)
    for row in sheet0_raw_data:
        url = 'https://www.doctorslounge.com/forums' + row[0][1:]
        category = row[1]
        topic = int(row[2].strip())
        posts = int(row[3].strip())
        c_id = int(url.split('f=')[1].split('&')[0])
        one_row = [c_id, category, url, topic, posts]
        print one_row
        sheet0_data.append(one_row)


def request_sheet1(c_id, url_base, total_post):
    global sheet1_data
    reg = 'icon topic_read.*?href="(.*?)".*?>(.*?)<.*?class="posts">(.*?)<.*?class="views">(.*?)<.*?View the latest post<.*?<br />(.*?)<'
    start = 0
    while start <= total_post - 100:
        url = url_base % start
        print 'SHEET_1 ' + url
        try:
            html = get_request(url)
            sheet1_raw_data = re.compile(reg).findall(html)
            for row in sheet1_raw_data:
                url = 'https://www.doctorslounge.com/forums' + row[0][1:]
                name = row[1]
                posts = int(row[2].strip())
                views = int(row[3].strip())
                t_id = int(url.split('t=')[1].split('&')[0])
                date = get_date(row[4])
                one_row = [c_id, t_id, name, url, posts, views, date]
                sheet1_data.append(one_row)
                request_sheet2(c_id, t_id, url)
        except Exception as e:
            print 'SHEET1_ERROR: %s, %s' % (url, e)
        start += 100


def request_sheet2(c_id, t_id, url):
    global sheet2_data, T_ID
    reg = 'avatar-container.*?href="(.*?)".*?username.*?>(.*?)<.*?class="profile-rank">(.*?)<.*?href.*?>(.*?)<.*?Joined.*?>(.*?)<.*?class="content">(.*?)<'
    html = get_request(url)
    replies = re.compile(reg).findall(html)
    for row in replies:
        profile_url = 'https://www.doctorslounge.com/forums' + row[0][1:]
        profile_name = row[1]
        profession = row[2]
        posts = int(row[3].strip())
        join_date = get_date(row[4].strip())
        content = remove_html_tag(row[5])
        one_row = [c_id, t_id, content, profile_name, profile_url, profession, posts, join_date]

        if profile_name not in scraped_profile_name:
            request_sheet3(profile_url, profile_name)
        sheet2_data.append(one_row)


def request_sheet3(url, profile_name):
    global sheet3_data
    sheet3_data.append([url, profile_name])
    # reg = 'discussion clear i.*? xg_lightborder.*?timestamp">(.*?) at.*?xg_user_generated">(.*?)</div'
    # for page in range(1, page_number + 1):
    #     url = base_url % page
    #     html = get_request(url)
    #     comments = re.compile(reg).findall(html)
    #
    #     for category in comments:
    #         date = get_date(category[0])
    #         comment = remove_html_tag(category[1])
    #         one_row = [T_ID, comment, date]
    #         sheet3_data.append(one_row)


def get_latest_date(ori_time):
    if 'Friday' in ori_time:
        ori_time = 'Sep 29, 2017'
    elif 'Thursday' in ori_time:
        ori_time = 'Sep 28, 2017'
    elif 'Wednesday' in ori_time:
        ori_time = 'Sep 27, 2017'
    elif 'Tuesday' in ori_time:
        ori_time = 'Sep 26, 2017'
    elif 'Monday' in ori_time:
        ori_time = 'Sep 25, 2017'
    elif 'Saturday' in ori_time:
        ori_time = 'Sep 30, 2017'
    elif 'Sunday' in ori_time:
        ori_time = 'Oct 1, 2017'
    if ',' not in ori_time:
        ori_time += ', 2017'
    try:
        ret = datetime.strptime(ori_time, "%b %d, %Y").strftime('%d/%m/%Y')
        return ret
    except Exception as e:
        return ori_time


def get_date(ori_time):
    try:
        ret = datetime.strptime(ori_time, "%a %b %d, %Y %I:%M %p").strftime('%d/%m/%Y')
        return ret
    except Exception as e:
        return ori_time


def get_content_and_create_date(url):
    html = get_request(url)
    reg = 'navigation byline.*?on(.*?)at.*?class="xg_user_generated">(.*?)</div>'
    data = re.compile(reg).findall(html)
    if data:
        data = data[0]
        return remove_html_tag(str(data[1].strip())), get_date(data[0].strip())
    return '', ''


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.linkedin.com/')
    req.add_header("Cookie", cookie)
    req.add_header('csrf-token', 'ajax:3940183104206872464')
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return HTMLParser.HTMLParser().unescape(res)


def read_excel(filename, start=1):
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            c_id = int(row[0].value)
            url = row[2].value + '&start=%d'
            total_post = int(row[3].value)
            request_sheet1(c_id, url, total_post)
        except Exception as e:
            print(i)
            print e


reload(sys)
sys.setdefaultencoding('utf-8')
request_sheet2(1,1,'https://www.doctorslounge.com/forums/viewtopic.php?f=84&t=12046&sid=0a42950f6bd084bc6b1393d0c0074bda')
read_excel('data/sheet0.xls')
write_excel('data/sheet1.xls', sheet1_data)
write_excel('data/sheet2.xls', sheet2_data)
write_excel('data/sheet3.xls', sheet3_data)