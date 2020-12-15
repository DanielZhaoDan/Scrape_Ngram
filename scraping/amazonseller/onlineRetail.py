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

cookie = 'session-id=357-6516861-3431162; ubid-acbsg=356-2157839-3441606; x-acbsg="7ZVCncggBjBvVVSRgNvBSYxeAAPsi9op@6s8CJCsR8VdEKQ2PvnTlD2WyPQDb3pF"; at-acbsg=Atza|IwEBIMEHmuErrnEYwVUFkpNctkhroo73cnXrMojTYCzU_pEKoBanDU0oiLjaLojQt6tJRmI4_5dC8BkfFGBPd3Zmj6UgMcMj2t5DD4tEmEpwRJClqKqhWedJRc7GjSi_FKoEiE4OhE4rvqvnyZh9mqJnRwV7Y2-myAkkY52BP1bmbMsWEXfIs6NGFUhV1FVcOGcEPsXjkBPCRZRfq9mPx3-i1hqR5yol4sZTYYk9wyeVeXLEHsITpMrVTfZFbx9cm2-3ZVY; sess-at-acbsg="KQJJ+QDxxFW1H+6X1h2zTFT0yKSXiwky/pncHTyFbt8="; sst-acbsg=Sst1|PQFqOaQnYrMbARCXsCAnwWVQCaJZGnaIw3Jz6lK9xGmACYQPQibU-ETqdGYcCXDVFHvQZoobz9Z09YzcRb9_jIb7V2IM59dDhLyFsqLgolKYVEvV9YmV4061D2KLKEnStBOsOYJF4Kjyq2u0t9GQTGxwL3NbxZeggdo_4Oxq79CLl4Dc8M7S-wGiEo03PzPRfvW4MtrdKc5mJE739r8JEkev8xhhIjcwA6uttJU772lmoQs7_bDKvAmK1tEluuUyiaYHJhN5GdXC_35HUqN9NxVOeUtz4GP1YJlVB74m-69hH_o; i18n-prefs=SGD; session-token="erljp7i6pm9BlHJmU+Gmq6ie5EeYy7APifBn4+ez6oEAKfJCpVMuGJgoqjHCKXo5uVJjEw0VOv1s+9bOhZM7kNicds92160Zk+3+7GNa34v9iNeiYQ5gWdfERWah3y8H/1rrIFejBDGgyaNm9tXrv0HhKawKI3Kr+BWhrNJorXWMybE5u3EYlRqh2mqfJt/503hVJO9urSLqzwRDPBOg6g=="; csm-hit=tb:s-AKA49CBVQNWWS6Q9T3M5|1607243913254&t:1607243914625&adb:adblk_no; session-id-time=2082787201l'

header = {
    'downlink': '10',
    'ect': '4g',
    'referer': 'https://www.amazon.sg/Laptops/b/?ie=UTF8&node=6436117051&ref_=sv_pc_1',
    'rtt': '0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
}


def request_sheet1(url, page_no):
    global sheet1_data

    i = 1
    count = 0

    while i <= int(page_no):
        print i, int(page_no)
        try:
            html = get_request_html(url + '&page=%d' % i, cookie)

            reg = 'div class="s-item-container".*?title="(.*?)href="(.*?)".*?price.*?\$(.*?)<'
            data = re.compile(reg).findall(html)

            j = 1
            for item in data:
                name = item[0]
                item_url = item[1].split('?')[0]
                # price = get_price(item[2])
                price = item[2]
                one_row = request_sheet2(item_url, '%d.%d' % (i, j), price, name)

                # print one_row
                sheet1_data.append(one_row)

                j += 1
                count+=1

            i += 1
        except Exception as e:
            i += 1
            print 'ERR---', url, i, e
        if count >= 100:
            break


def get_price(ori):
    if '<span class="a-offscreen">' in ori:
        reg = '<span class="a-offscreen">S(.*?)<'
        return re.compile(reg).findall(ori)[0]
    return 'N/A'


def request_sheet2(url, item_rank, price='', name=''):

    html = get_request_html(url, cookie, add_header=header)

    brand = 'N/A'
    size = 'N/A'
    condition = 'NEW'
    seller = 'N/A'
    location = 'N/A'
    rank = 'N/A'

    # seller & location
    if 'these sellers' in html and 'Available from' in html:
        reg = 'Available from .*?href=\'(.*?)\''
        sub_url = 'https://www.amazon.sg' + re.compile(reg).findall(html)[0]
        seller, price, condition, location = get_sub_detail(sub_url, price)
    else:
        if 'Ships from and sold by' in html:
            reg = 'Ships from and sold by(.*?)<span'
            data = re.compile(reg).findall(html)[0]
            if 'from' in data:
                seller = remove_html_tag(data.split('from ')[0]).replace('.','').replace(',','').strip()
                location = data.split('from ')[-1].split('.')[0]
            else:
                seller = remove_html_tag(data).replace('.','').replace(',','').strip()
        if 'International product' in html:
            reg = 'International product.*?from (.*?)<'
            location = re.compile(reg).findall(html)[0].strip()

    detail_table_reg = 'productDetails_techSpec_section_1(.*?)</table'
    detail_table_reg2 = 'productDetails_detailBullets_sections1(.*?)</table'

    reg = 'th.*?>(.*?)<.*?td.*?>(.*?)<'

    detail_list = []

    if 'productDetails_techSpec_section_1' in html:
        detail_table = re.compile(detail_table_reg).findall(html)[0]
        detail_list += re.compile(reg).findall(detail_table)
    if 'productDetails_detailBullets_sections1' in html:
        detail_table = re.compile(detail_table_reg2).findall(html)[0]
        detail_list += re.compile(reg).findall(detail_table)

    for item in detail_list:
        if item[0] == 'Brand':
            brand = item[1]
        elif item[0] == 'Standing screen display size':
            size = item[1]
        elif item[0] == 'Screen Size':
            size = item[1]
        elif item[0] == 'Amazon Best Sellers Rank':
            rank = item[1]

    return [item_rank, name, price, brand, url, location, seller, rank, size, condition]


def get_sub_detail(url, price):
    html = get_request_html(url, cookie)
    reg = 'olpOfferPrice.*?S(.*?) .*?olpCondition .*?>(.*?)<.*?olpSellerName.*?<a.*?>(.*?)<.*?'

    data = re.compile(reg).findall(html)
    if data:
        return data[0][2], price if price != 'N/A' else data[0][0], data[0][1].strip(), 'Singapore' if 'Singapore' in data[0][2] or 'SG' in data[0][2] else 'outside Singapore'
    return 'N/A', price, 'N/A', 'N/A'


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


reload(sys)
sys.setdefaultencoding('utf-8')
url = 'https://www.amazon.sg/Laptops/b/?ie=UTF8&node=6436117051&ref_=sv_pc_1'
request_sheet1(url, 229)
write_excel('laptop_amz.xls', sheet1_data)
# print request_sheet2('https://www.amazon.sg/All-New-Amazon-Fire-Tablet-display/dp/B07KD8R6HD/ref=lp_6436117051_1_11?s=electronics&ie=UTF8&qid=1607239720&sr=1-11', '')
