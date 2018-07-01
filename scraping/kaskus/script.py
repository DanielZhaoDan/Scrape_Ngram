# -*- coding: utf-8 -*-

import re
import xlwt
from datetime import datetime
import os
import html
import requests


sheet0_data = [['Thread ID', 'Title', 'Title URL', 'Create Date', 'Last Date', 'No. views', 'No. shares', 'No. Replies', 'Category', 'Rating']]

url_base = 'https://www.kaskus.co.id/search/forum?q=air+mineral&sort=popular&order=desc&page=%d'
cookie = 'display=grid; kuid=ZwZ1A1ru1INQSTBIDgFvAg==; forkrtg={"generic":"29112019"}; __asc=0656012716334ee38013146c4c7; __auc=0656012716334ee38013146c4c7; __utma=40758456.522550202.1525601417.1525601417.1525601417.1; __utmc=40758456; __utmz=40758456.1525601417.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _ga=GA1.3.522550202.1525601417; _gid=GA1.3.1397254987.1525601417; notices=%5B%5D; AMP_TOKEN=%24NOT_FOUND; __utmb=40758456.5.10.1525601417'
P_ID = 1


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


def request_sheet0(url):
    global sheet0_data, P_ID
    html = get_request(url)
    reg = 'class="post-title".*?href="(.*?)".*?>(.*?)<.*?Created (.*?) .*?fa-tags.*?href.*?>(.*?)<.*?fa-eye.*?</i> (.*?)<.*?</i> (.*?) '
    threads = re.compile(reg).findall(html)
    for thread in threads:
        try:
            thread_url = thread[0]
            thread_name = thread[1]
            create_date = get_date(thread[2])
            category = thread[3]
            view_count = thread[4]
            last_date = get_date(thread[5])
            share_count, comment_count, rating = request_share_and_commment_count(thread_url)
            one_row = ['Kaskus_AM_%d' % P_ID, thread_name, thread_url, create_date, last_date, view_count, share_count, comment_count, category, rating]
            print(one_row)
            sheet0_data.append(one_row)
            P_ID += 1
        except Exception as e:
            print (e)


def request_share_and_commment_count(url):
    html = get_request(url)
    if 'pagination' in html:
        reg = 'votes, (.*?) average.*?class="total-share">.*?>(.*?)<.*?page-count.*?of (.*?)<.*?href="(.*?)"'
        share_page = re.compile(reg).findall(html)
        if not share_page:
            return 0, 0
        share_page = share_page[0]
        rating = share_page[0]
        share_count = share_page[1]
        next_url = 'https://www.kaskus.co.id/' + share_page[3] + '999'
        next_html = get_request(next_url)
    else:
        next_html = html
        reg = 'votes, (.*?) average.*?class="total-share">.*?>(.*?)<'
        share_count = re.compile(reg).findall(html)
        if share_count:
            share_count = share_count[0]
            rating = share_count[0]
            share_count = share_count[1]
        else:
            rating = 0
            share_count = 0
    comment_reg = 'class="permalink".*?name="(.*?)"'
    comment_list = re.compile(comment_reg).findall(next_html)
    if not comment_list:
        return parse_number(share_count), 0, rating
    return parse_number(share_count), comment_list[-1], rating


def extract_raw_topic(raw_topic):
    reg = 'href="(.*?)".*?>(.*?)<.*?&raquo; (.*?)<'
    entry = re.compile(reg).findall(raw_topic)[0]
    url = 'https://www.kiasuparents.com/kiasu/forum/' + entry[0].replace('./', '').replace('&amp;', '&')
    first_date = entry[2]
    return entry[1].replace('&amp;', '&'), url, first_date


def parse_number(ori):
    if 'k' in ori or 'K' in ori :
        new = ori.replace('.', ',').replace('k', '').replace('K', '') + '00'
    elif 'm' in ori or 'M' in ori:
        new = ori.replace('.', ',').replace('m', '').replace('M', '') + '00,000'
    else:
        new = ori
    return new


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(html.unescape(dd)).strip()


def get_date(ori):
    d = datetime.strptime(ori, '%d-%m-%Y')
    date = d.strftime('%d/%m/%Y')
    return date


def get_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
    }
    req = requests.get(get_url, headers=headers)
    res = req.content
    res = str(res).replace('\t', '').replace('\r', '').replace('\n', '').replace('&amp;', '&').replace('\\t', '').replace('\\r', '').replace('\\n', '')
    return res

for i in range(1, 12):
    url = url_base % i
    request_sheet0(url)

write_excel('data/sheet.xls', sheet0_data)

