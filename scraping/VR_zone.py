# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd

sheet1_data = [['Keyword', 'Forum title', 'Forum link', 'Replies', 'Views']]
sheet2_data = [['Forum title', 'Forum text', 'Date']]

urls = ['http://forums.vr-zone.com/search.php?searchid=1107112', 'http://forums.vr-zone.com/search.php?searchid=1107122', 'http://forums.vr-zone.com/search.php?searchid=1107123', 'http://forums.vr-zone.com/search.php?searchid=1107124', 'http://forums.vr-zone.com/search.php?searchid=1107128']
keywords = ['IT show', 'PC show', 'Comex', 'SITEX', 'Singtel']

cookie = '__cfduid=d52b7a6f2feca97b1c48998c888c517981481214002; cX_S=iwgkprrgasx9gzq5; __utma=98462808.202309017.1481214242.1481214242.1481214242.1; __utmc=98462808; __utmz=98462808.1481214242.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); PHPSESSID=e9117d08d75f0612d6cbb11d4fa33866; _gat=1; bb_lastvisit=1481214098; bb_lastactivity=0; bb_sessionhash=94fff2833ba8117bbe4571fe83b92a90; _ga=GA1.2.202309017.1481214242; __asc=408c01bd158e0ec280c8d4f1c01; __auc=3d194a02158df3fab81ed66b668; cX_P=iwgkprrlcweqjrg7; __atuvc=64%7C49; __atuvs=5849f6d2dbbe2d90002'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)
    print filename+"===========over============"


def request_sheet1(keyword, url, size):
    global sheet1_data
    # link, name, replies, views
    reg = 'class="searchtitle">.*?<a.*?href="(.*?)".*?>(.*?)<.*?"understate">(.*?)<.*?Views: (.*?)<'
    html = get_request(url)
    total_page = size
    data_list = re.compile(reg).findall(html)
    for data in data_list:
        sheet2_url = data[0]
        if 'http://forums.vr-zone.com/' not in sheet2_url:
            sheet2_url = 'http://forums.vr-zone.com/' + sheet2_url
        one_row = [keyword, data[1], sheet2_url, int(data[2].replace(',', '')), int(data[3].replace(',', ''))]
        sheet1_data.append(one_row)

        # request_sheet2(data[1], sheet2_url)
    for i in range(2, total_page):
        next_url = url + '&pp=&page=' + str(i)
        html = get_request(next_url)
        data_list = re.compile(reg).findall(html)
        for data in data_list:
            sheet2_url = data[0]
            if 'http://forums.vr-zone.com/' not in sheet2_url:
                sheet2_url = 'http://forums.vr-zone.com/' + sheet2_url
            one_row = [keyword, data[1], sheet2_url, int(data[2].replace(',', '')), int(data[3].replace(',', ''))]
            sheet1_data.append(one_row)

            # request_sheet2(data[1], sheet2_url)


def total_page(html):
    reg = 'pagination popupmenu nohovermenu.*?Page.*?of (.*?)<'
    temp = re.compile(reg).findall(html)
    if temp:
        return int(temp[0])
    return 1


def request_sheet2(name, url):
    global sheet2_data
    url = url.split('?')[0]
    print url
    html = get_request(url)
    page_number = total_page(html)
    if page_number > 100:
        page_number = 100
    reg = 'class="date">(.*?)&.*?class="content".*?<blockquote.*?>(.*?)</block'

    for i in range(1, page_number+1):
        if i != 1:
            next_url = url.replace('.html', '-'+str(i)+'.html')
            html = get_request(next_url)
            data_list = re.compile(reg).findall(html)
            for data in data_list:
                date = get_date(data[0])
                content = remove_html_tag(data[1])
                if not content.startswith(' Originally Posted by'):
                    one_row = [name, content, date]
                    sheet2_data.append(one_row)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_date(ori):
    temp = ori.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
    d = datetime.strptime(temp, '%b %d, %y,')
    date = d.strftime('%-d/%-m/%Y')
    return date


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

# i = 0
# size = [16, 18, 17, 15, 17]
# for i in range(len(urls)):
#     request_sheet1(keywords[i], urls[i], size[i])
#     write_excel(keywords[i].replace(' ', '_')+'.xls', sheet1_data)
#     sheet1_data = [['Keyword', 'Forum title', 'Forum link', 'Replies', 'Views']]
#     sheet2_data = [['Forum title', 'Forum text', 'Date']]
files = []


def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path or 'txt' in path:
            files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files


def load_data_from_excel(filename):
    ret = []
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(1, table.nrows):
        ret.append([table.row(i)[1].value, table.row(i)[2].value])
    return ret


def each_file(filename):
    rows = load_data_from_excel(filename)
    for row in rows:
        request_sheet2(row[0], row[1])


filenames = walk('sheet1')
for i in range(0, len(filenames)):
    print(filenames[i])
    each_file(filenames[i])
    write_excel(filenames[i].replace('sheet1', 'sheet2'), sheet2_data)
    sheet2_data = [['Forum title', 'Forum text', 'Date']]