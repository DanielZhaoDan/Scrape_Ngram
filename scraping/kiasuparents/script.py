# -*- coding: utf-8 -*-

import re
import xlwt
from datetime import datetime
from scraping import utils
import os
import html
import requests

import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

sheet0_data = [['Topic ID', 'Forum Category',  'Forum Name', 'Forum url', 'No. Topics', 'No. Posts', 'Last post date', 'Last post date Converted']]
sheet1_data = [['Topic ID', 'Forum Category', 'Forum Name', 'Topic Name', 'Topics url', 'Replies', 'Views', 'First Post Date', 'First Post Date Converted', 'Last Post date', 'Last post date converted']]
sheet2_data = [['Sub Topic', 'Link to Sub Topic', 'Replies', 'Views', 'First Post Date', 'First Post Date Converted', 'Last Post date', 'Last post date converted', 'Comment URL', 'Comment Text', 'Comment Date', 'Comment Date Converted']]

url_base = 'https://www.kiasuparents.com/kiasu/forum/viewforum.php?f=32&start=%s'

cookie = 'phpbb3_e5hmi_wps_u=1; phpbb3_e5hmi_wps_k=; phpbb3_e5hmi_wps_sid=a59d4f87b753b7ce087ce43a1506921b; _ga=GA1.2.971203275.1575473549; _gid=GA1.2.1685841714.1575473550'


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


def get_category(i):
    if i < 12:
        return 'General parenting'
    if i < 19:
        return 'Schooling'
    return 'Educare'


def request_sheet0():
    global sheet1_data, sheet2_data
    url = 'https://www.kiasuparents.com/kiasu/forum/index.php'
    reg = 'class="row".*?href="(.*?)".*?>(.*?)</a>(.*?)</dt>.*?class="topics">(.*?)<.*?class="posts">(.*?)<.*?Last post.*?<br />(.*?)<'
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
        one_row = [id, get_category(id), title, link, topics, posts, last_date, last_date_converted]
        sheet0_data.append(one_row)
        print one_row
        request_sheet1(id, get_category(id), link, title, int(topics) // 20)
        id += 1


def request_sheet1(main_id, form_category, main_url, form_name, size):
    global sheet1_data
    # size = min(size, 40)
    topic_body_reg = 'class="forumbg".*?class="topiclist topics"(.*?)action-bar bar-bottom'
    topic_detail_reg = 'No unread posts.*?href="(.*?)".*?>(.*?)<.*?&raquo; (.*?)<.*?class="posts">(.*?) .*?class="views">(.*?) .*?sr-only.*?br />(.*?)<'
    last_main_date = None

    url_base = main_url + '&start=%s'

    for i in range(1, size):
        print('-----Level 1 Page ' + str(i) + '-----' + str(size))
        url = url_base % str(i*20)
        html = get_request(url)
        topic_body = re.compile(topic_body_reg).findall(html)
        if not topic_body:
            continue
        topic_detail = re.compile(topic_detail_reg).findall(topic_body[0])
        for detail in topic_detail:
            topic_url = 'https://www.kiasuparents.com/kiasu/forum/' + detail[0].replace('./', '').replace('&amp;', '&')
            topic = utils.remove_html_tag(detail[1])
            first_date = detail[2]
            first_date_converted = get_date(first_date)

            replies = int(detail[3])
            views = int(detail[4])
            last_date = detail[5]
            last_date_converted = get_date(last_date)

            one_row = [main_id, form_category, form_name, topic, topic_url, replies, views, first_date, first_date_converted, last_date, last_date_converted]
            sheet1_data.append(one_row)

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
            content = utils.remove_html_tag(reply[1])
            one_row = [sub_title, sub_link, sub_replied, sub_views, sub_first_date, sub_first_date_con, sub_last_date, sub_last_date_con, url, content, comment_date, date]
            sheet2_data.append(one_row)



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
write_excel('data/sheet1.xls', sheet1_data)
