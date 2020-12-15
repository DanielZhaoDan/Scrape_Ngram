# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
import json
from scraping.utils import post_request_json, get_request_html, write_html, write_excel

saved_hotel = set()
R_ID = 1
sheet1_data = [['ID', 'SKU des', 'Rank', 'Price', 'Brand', 'Product Url', 'Display Size', 'Seller', 'Shipping location', 'Condition']]

cookie = '_uab_collina=159832265769569523139964; t_fv=1598322657614; t_uid=G8MX02iNjHrV3hNjipyZb16Z3beSpsPR; t_sid=r8fnMIwHlftKVDbXIS9HjuPPbcw2rc5M; utm_channel=NA; lzd_cid=dca654b7-258f-4226-d098-b8aee04149be; cna=hrXCF0Ce0FMCASp4SZ6S0pYk; lzd_sid=174afad1062218c0b62df830039fe2b5; _tb_token_=ee3543596ed0e; hng=PH|en-PH|PHP|608; userLanguageML=en; _bl_uid=bpk7IeXw9s7c4a1n6l5wk2ndtd7d; _ga=GA1.3.1102477189.1598322662; _gid=GA1.3.914441529.1598322662; JSESSIONID=4EEEC139D3C325F10BB704AEB4602CC5; _uetsid=00a83f0f3bca6c8d6553e74e9a491feb; _uetvid=972ec552ba80866be6a767318e8e123d; _gat_UA-30245404-1=1; tfstk=cIMNBQiAw-0B7y2XwRwVhAbX0BwOZ4HoHwrbsjctgathqyPGijQYAzlLT7aJK5f..; l=eBQM6iNeOYITEKJDBOfwourza77OSIRAguPzaNbMiOCPOA1p59CcWZP-Rl89C3GVh6y9R3lNl-6eBeYBcWNInxv9qYmDJeHmn; isg=BPPzpT-oqN5IC2SK4iVBiWSZgvEdKIfqNgf1Y6WRDJNupBJGLfwxO32sWNRKBN_i'

urls = [
    ('https://www.chiphell.com/thread-2218560-%d-1.html', 'Jewery'),
    ('https://www.chiphell.com/thread-2253311-%d-1.html', 'Collection'),
    ('https://www.chiphell.com/thread-2186648-%d-1.html', 'Wine'),
]

uid_level_dict = {}


def request_sheet1(item, uid):
    global sheet1_data

    url, topic = item

    base_reg = 'class="hm ptn".*?xi1">(.*?)<.*?xi1">(.*?)<.*?id="postmessage_.*?>(.*?)</td'
    comment_reg = 'id="postmessage_.*?>(.*?)</td'

    i = 1

    html = get_request_html(url % i, cookie)
    data = re.compile(base_reg).findall(html)

    if not data:
        print 'ERR_BASIC', url
        return
    item = data[0]
    try:
        no_post = int(item[1])
        page_no = no_post / 15 + 1
    except:
        page_no = 1
    no_view = item[0]
    no_reply = item[1]
    post = get_comments(item[2]).replace('&amp;', '&')

    print topic, page_no, url

    while i <= page_no:
        try:
            if i > 1:
                html = get_request_html(url % i, cookie)
            data = re.compile(comment_reg).findall(html)

            if i == 1:
                start_index = 1
            else:
                start_index = 0

            for item in data[start_index:]:
                comments = get_comments(item)

                one_row = [uid, topic, url % 1, no_view, no_reply, post, comments.strip()]
                print one_row
                sheet1_data.append(one_row)
            i += 1
        except Exception as e:
            i += 1
            print 'ERR---', url, i, e


def get_comments(ori):

    escape_words = ['的帖子', '</blockquote>', '編輯', '编辑']

    for word in escape_words:
        if word in ori:
            ori = remove_html_tag(ori.split(word)[-1])
    return remove_html_tag(ori)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def step_1():
    uid = 1
    for item in urls:
        request_sheet1(item, 'CN_CH_%d' % uid)
        uid += 1
    write_excel('CN_chiphell.xls', sheet1_data)


reload(sys)
sys.setdefaultencoding('utf-8')
step_1()