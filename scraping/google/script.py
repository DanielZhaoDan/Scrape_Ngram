# -*- coding: utf-8 -*-
import re
import requests
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
from urlparse import urlparse
import time
import random

sheet1_data = [['Keywords', 'Country', 'No of Articles', 'Page No.', 'News Url', 'Date', 'Name of Publisher', 'Main url of newspaper/magazine', 'Headline', 'Content']]
sheet2_data = [['Topic', 'Topic URL', 'Reply Date', 'Reply Content']]

url_bases = 'https://www.google.com.sg/search?q="{key_word}"+location:{location}&newwindow=1&safe=strict&hl=en&tbm=nws&start='

key_words = ['HR Information System', 'HR metrics', 'HR Analytics', 'Workforce Analytics', 'Employee Productivity', 'Employee Retention']

locations = ['Singapore', 'USA', 'India']

cookie = 'OGPC=5062177-26:5062195-14:5062216-26:695701504-19:699960320-23:448059392-20:527891456-85:1037221888-4:82459648-15:; SID=ogQ-uhu0gtYW2LAUn1TEZ3zKjBSlywkz-w1KM6pu6lExJbg72Zriqs0Lsom3Nk2H-kuQrg.; HSID=ASgV7y4JPaYghkJON; SSID=ANqUkno9H1wPOniiO; APISID=r3GDWUyqOtE3tADc/ARA8hfHW0PcJPvnqd; SAPISID=qrhlBv5K6RVQtXJI/AknB9oTSHZTA5tRx-; NID=102=i26Qbnudi7iPfJYTeiPzZZD_OUmIJc_5EltaEd0i3A7xcPgBTMeCmO20juR45DzkCwgfB1YWaKrIgz49xT7vD68Dm14cpfHXskdK3BgpKQarEMd7zJ20U01viP4UehbP64-y5Et4tL3dFom_sn8LUCyrBJ06NNSXg-1Mw0Ahmi9TKqDblHKKBMufZPI7TZcmh0AY7Nlid31pfeb9JqeqDRTWGQrf58EDP76bRTeo5O2SB-L4dNAUGH_1mdMplw43h8J3jJsTeCpIXGabKnkG0CUXQyEctlsMzw; DV=E6kuk-h3zUdIwDI3GDguhO-R-cpmvVXY2sbrhwXZ-wIAAFB7bXfHy01PBAEAAIyhjZShX-shVgAAAA; UULE=a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTQ5Mzk1MTExOTAwNjAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6MTI5OTc3OTYgbG9uZ2l0dWRlX2U3OjEwMzc4ODA2MjF9IHJhZGl1czoyNzkwMA=='

agent_ip = [
    '124.206.22.120', '125.93.149.42', '121.232.146.89', '106.0.6.165', '183.31.144.180', '1.71.115.188', '121.232.148.70', '121.232.145.250', '183.196.201.30', '110.73.4.31',
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
    reg = 'id="resultStats">.*?(\d.*?) result'
    results = re.compile(reg).findall(html)
    if results:
        return int(results[0].replace(',', ''))
    return 10


def request_sheet1(key_word, location, url_base):
    global sheet1_data
    total_count = 0
    page_no = 1
    while True:
        url = url_base + str(page_no-1) + '0'
        print url
        if page_no > 10:
            break
        html = get_request(url)
        if total_count == 0:
            total_count = get_total_count(html)
        topic_detail_reg = 'class="l _HId".*?href="(.*?)".*?>(.*?)<.*?"_tQb _IId">(.*?)<.*?f nsa _uQb">(.*?)<'
        topic_detail = re.compile(topic_detail_reg).findall(html)
        if not topic_detail:
            break
        for detail in topic_detail:
            url = detail[0]
            o = urlparse(url)
            main_url = o.scheme + '://' + o.netloc
            headline = remove_html_tag(detail[1])
            publisher = detail[2]
            date = get_date(detail[3])
            content = get_raw_content(url)
            one_row = [key_word, location, total_count, page_no, url, date, publisher, main_url, headline, content]
            sheet1_data.append(one_row)
        page_no += 1
        time.sleep(10)


def get_raw_content(url):
    try:
        html = get_request(url)
        reg = '<body.*?>(.*?)</body>'
        contents = re.compile(reg).findall(html)
        if contents:
            content = contents[0]
            step_0 = remove_html_tag(content) # remove html tag
            step_1 = re.sub('[ \t\n\r]+', ' ', step_0) # remove multiple blank, newline and tab
            return step_1
        return html
    except:
        return ''


def request_sheet2(topic, url):
    global sheet2_data
    reg = 'post_message_container.*?post_message fonts_resizable os_14.*?>(.*?)<.*?subj_info os_14(.*?)</div'
    question = None
    if url:
        html = get_request(url)
        reply_lists = re.compile(reg).findall(html)
        for reply in reply_lists:
            content = remove_html_tag(reply[0])
            anw, com, date = get_date(reply[1])
            if not question:
                question = content
            else:
                one_row = [topic, url, content, date]
                sheet2_data.append(one_row)
    return question


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_date(ori):
    try:
        date = datetime.strptime(ori, '%d %b %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
        'x-client-data': 'CJG2yQEIprbJAQjBtskBCPKZygEI+5zKAQipncoB',
        'User-Agent': random.choice(agent_ip),
        # ':authority': 'www.google.com.sg',
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')
urls = []
for key_word in key_words:
    for location in locations:
        urls.append([key_word, location, url_bases.format(key_word=key_word.replace(' ', '+'), location=location)])

for url in urls:
    request_sheet1(url[0], url[1], url[2])
write_excel('data/sheet1.xls', sheet1_data)
