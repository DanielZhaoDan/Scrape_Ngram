# -*- coding: utf-8 -*-

import re
import xlwt
from datetime import datetime
from html.parser import HTMLParser
import os
import xlrd
import html
import requests

import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

sheet0_data = [['Topic ID', 'Main Topic Name', 'Link to inside', 'Topics within', 'Posts within', 'First Post Date', 'First Post Date Converted', 'Last Post date', 'Last post date converted']]
sheet1_data = [['Topic ID', 'Main Topic Name', 'Link to inside', 'Topics within', 'Posts within', 'Sub Topic', 'Link to Sub Topic', 'Replies', 'Views', 'First Post Date', 'First Post Date Converted', 'Last Post date', 'Last post date converted']]
sheet2_data = [['Sub Topic', 'Link to Sub Topic', 'Replies', 'Views', 'First Post Date', 'First Post Date Converted', 'Last Post date', 'Last post date converted', 'Comment URL', 'Comment Text', 'Comment Date', 'Comment Date Converted']]

url_base = 'https://www.kiasuparents.com/kiasu/forum/viewforum.php?f=32&start=%s'

cookie = 'phpbb3_e5hmi_wps_u=1; phpbb3_e5hmi_wps_k=; phpbb3_e5hmi_wps_sid=c8f9fc66fa215bfa9be9a386cf054dde; integral-mailchimp-cookie=e644a99940ed66361bb5ed52187d089a; PHPSESSID=8441ec3e356be16243e3d9632246ed8d; ksp_visited=1; style_cookie=null; _ga=GA1.2.1977853298.1512140249; _gid=GA1.2.828697368.1512140249'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


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
                    print('===Write excel ERROR==='+str(one_row[col]))
    w.save(filename)
    print(filename+"===========over============")


def request_sheet0():
    global sheet1_data, sheet2_data
    url = 'https://www.kiasuparents.com/kiasu/forum/index.php'
    reg = 'class="row".*?href="(.*?)".*?>(.*?)</a>(.*?)</dt>.*?class="topics">(.*?)<.*?class="posts">(.*?)<.*?View the latest post.*?</a> <br />(.*?)</span'
    html = get_request(url)
    lists_0 = re.compile(reg).findall(html)
    id = 1
    for list_0 in lists_0:
        link = 'https://www.kiasuparents.com/kiasu/forum/' + list_0[0].split('/')[-1]
        title = list_0[1]
        topics = list_0[3].strip()
        posts = list_0[4].strip()
        last_date = list_0[5]
        last_date_converted = get_date(last_date)
        first_date = request_sheet1(id, title, link, topics, posts, int(topics) // 50 + 1)
        one_row = [id, link, title, topics, posts, first_date, get_date(first_date), last_date, last_date_converted]
        sheet0_data.append(one_row)
        id += 1
        write_excel('data/sheet1_%d.xls' % id, sheet1_data)
        write_excel('data/sheet2_%d.xls' % id, sheet2_data)
        del sheet1_data
        del sheet2_data
        sheet1_data = [['Topic ID', 'Main Topic Name', 'Link to inside', 'Topics within', 'Posts within', 'Sub Topic', 'Link to Sub Topic', 'Replies', 'Views', 'First Post Date', 'First Post Date Converted', 'Last Post date', 'Last post date converted']]
        sheet2_data = [['Sub Topic', 'Link to Sub Topic', 'Replies', 'Views', 'First Post Date', 'First Post Date Converted', 'Last Post date', 'Last post date converted', 'Comment URL', 'Comment Text', 'Comment Date', 'Comment Date Converted']]


def request_sheet1(main_id, main_title, main_url, main_topics, main_posts, size):
    global sheet1_data
    size = min(size, 40)
    topic_body_reg = 'class="forumbg".*?class="topiclist topics"(.*?)/ul'
    topic_detail_reg = '<dt .*?title.*?>(.*?)</dt>.*?class="posts">(.*?)<.*?class="views">(.*?)<.*?title="View the latest post".*?<br />(.*?)<'
    last_main_date = None
    for i in range(1, size+1):
        url_base = main_url + '&start=%s'
        print('-----Level 1 Page ' + str(i) + '-----' + str(size))
        url = url_base % str(i*50)
        html = get_request(url)
        topic_body = re.compile(topic_body_reg).findall(html)
        if not topic_body:
            continue
        topic_detail = re.compile(topic_detail_reg).findall(topic_body[0])
        for detail in topic_detail:
            raw_topic = detail[0]
            topic, link, first_date = extract_raw_topic(raw_topic)
            first_date_converted = get_date(first_date)
            replies = int(detail[1])
            views = int(detail[2])
            last_date = detail[3]
            last_date_converted = get_date(last_date)
            one_row = [main_id, main_title, main_url, main_topics, main_posts, topic, link, replies, views, first_date, first_date_converted, last_date, last_date_converted]
            sheet1_data.append(one_row)
            page_number = replies // 10
            request_sheet2(topic, link, replies, views, first_date, first_date_converted, last_date_converted, last_date_converted, page_number)
            last_main_date = last_date
    return last_main_date


def extract_raw_topic(raw_topic):
    reg = 'href="(.*?)".*?>(.*?)<.*?&raquo; (.*?)<'
    entry = re.compile(reg).findall(raw_topic)[0]
    url = 'https://www.kiasuparents.com/kiasu/forum/' + entry[0].replace('./', '').replace('&amp;', '&')
    first_date = entry[2]
    return entry[1].replace('&amp;', '&'), url, first_date


def request_sheet2(sub_title, sub_link, sub_replied, sub_views, sub_first_date, sub_first_date_con, sub_last_date, sub_last_date_con, number):
    global sheet2_data
    number = min(number, 40)
    reg = 'class="postbody".*?class="author".*?&raquo; (.*?) <.*?class="content">(.*?)</div>'
    for i in range(1, number+1):
        url = sub_link + '&start=' + str(i*10)
        try:
            html = get_request(url)
        except:
            print('ERR---'+url)
            continue
        reply_lists = re.compile(reg).findall(html)
        for reply in reply_lists:
            comment_date = reply[0]
            date = get_date(comment_date)
            content = remove_html_tag(reply[1])
            one_row = [sub_title, sub_link, sub_replied, sub_views, sub_first_date, sub_first_date_con, sub_last_date, sub_last_date_con, url, content, comment_date, date]
            sheet2_data.append(one_row)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(html.unescape(dd)).strip()


def get_date(ori):
    d = datetime.strptime(ori, '%a %b %d, %Y %I:%M %p')
    date = d.strftime('%d/%m/%Y')
    return date


def get_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
        'Host': 'www.kiasuparents.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2',
        'Cache-Control': 'no-cache',
        'Referer': 'https://www.kiasuparents.com/kiasu/forum/viewforum.php?f=28',
        'Pragma': 'no-cache',
    }
    req = requests.get(get_url, headers=headers)
    res = req.content
    res = str(res).replace('\t', '').replace('\r', '').replace('\n', '').replace('&amp;', '&').replace('\\t', '').replace('\\r', '').replace('\\n', '')
    return res

print(request_sheet0())
write_excel('data/sheet0.xls', sheet0_data)
