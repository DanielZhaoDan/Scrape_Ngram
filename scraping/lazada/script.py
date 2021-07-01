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
sheet1_data = [['country', 'ID', 'SKU des', 'Rank', 'Price', 'Brand', 'Product Url', 'Display Size', 'Seller', 'Shipping location', 'Condition']]

cookie = '_uab_collina=159832240685631356886046; t_fv=1598322406649; t_uid=eHKsifNYMfMR3KrPZxny9MRbxfmMCq6M; cna=hrXCF0Ce0FMCASp4SZ6S0pYk; lzd_cid=8970c25d-9c24-4b0d-a8be-796c0d176b51; _ga=GA1.3.1746694825.1598322410; lzd_sid=120fb952baa490ebede471b5da6aeee4; _tb_token_=ebb3eb3b5357e; hng=TH|th|THB|764; userLanguageML=th; _gcl_au=1.1.191635468.1615728570; _bl_uid=URkIUmgp9F97Fs2bvn0aq080R6kI; _gid=GA1.3.901189380.1615728572; cto_axid=Cu7tWyBfLFWTzrGoDV67WHgvZ3FAD7qe; xlly_s=1; JSESSIONID=1F6936606083D430A81829F9D0803169; t_sid=eNZimK7ZhJowb09uAFJPXRakSaFZ0h74; utm_channel=NA; _uetsid=4f94fae084c911eb98ba57be45e5786f; _uetvid=4f954e0084c911eb9cdb9738542206e4; _gat_UA-30236174-1=1; l=eBjasUbHOYIOrn6CBOfZnurza77OSIRASuPzaNbMiOCPOy5p5-xcW6NUUiY9CnhVh6ly-3u7Dd3MBeYBcIX1j6G7KcSisfDmn; tfstk=cx3RB_4huIC-xkFx_0KcOraxt9OcZM-YLgwGJQhb_Yrfi8_diO0iWN6BN568kIC..; isg=BAwM2vlRgBF696tnYFQsc3kU3Ww-RbDv-rxzq2bNGLda8az7jFWAfwJDlPlJlOhH'

urls = [
    ('https://www.lazada.co.th/shop-laptops/?spm=a2o4m.searchlistcategory.cate_1.3.4eef11d6PcdJhc', 'TH', '27478', '102'),
    ('https://www.lazada.com.my/shop-laptops/?spm=a2o4k.home.cate_1.2.68d82e7emRipEw', 'MY', '29118', '102'),
    ('https://www.lazada.sg/shop-laptops/?spm=a2o42.home.cate_1.3.654346b5ZtkEpx', 'SG', '13550', '102'),
    ('https://www.lazada.co.id/beli-laptop/?spm=a2o4j.home.cate_1.2.57991559MMbWnz', 'ID', '11213', '102'),
    ('https://www.lazada.com.ph/shop-laptops/?spm=a2o4l.home.cate_1.3.47ee359dUkZxwD', 'PH', '15549', '102'),
]

uid_level_dict = {}


def get_page_no(html):
    if 'class="pageNumbers"' not in html:
        return 1
    page_reg = 'data-page-number="(.*?)"'

    data = re.compile(page_reg).findall(html)

    if data:
        return int(data[-1])


def request_sheet1(item):
    global sheet1_data
    url, country, total, page_no = item

    i = 1
    count = 0

    while i <= int(page_no):
        print country, i, int(page_no)
        try:
            html = get_request_html(url + '&page=%d' % i, cookie)

            reg = '"name":"(.*?)".*?productUrl":"(.*?)".*?"priceShow":"(.*?)".*?.*?"location":"(.*?)".*?"sku":"(.*?)"'
            ori = html.split('"listItems"')[-1].split('"sortItems"')[0]
            data = re.compile(reg).findall(ori)

            j = 1
            for item in data:
                name = item[0]
                item_url = 'https:' + item[1]
                price = item[2]
                location = item[3]
                id = item[4]

                detail = request_sheet2(item_url)

                one_row = [country, id, name, '%d.%d' % (i, j), price, detail[0], item_url, detail[1], detail[3], location, detail[2]]

                sheet1_data.append(one_row)

                j += 1
                count += 1

            i += 1
            if count >= 100:
                break
        except Exception as e:
            i += 1
            print 'ERR---', url, i, e


def request_sheet2(url):

    html = get_request_html(url, cookie)

    brand = 'N/A'
    size = 'N/A'
    condition = 'N/A'
    seller = 'N/A'

    if '"Brand"' in html:
        reg = '"Brand":"(.*?)"'
        brand = re.compile(reg).findall(html)[0]

    if '"Display Size"' in html:
        reg = '"Display Size":"(.*?)"'
        size = re.compile(reg).findall(html)[0]

    if '"Condition"' in html:
        reg = '"Condition":"(.*?)"'
        condition = re.compile(reg).findall(html)[0]

    if '"seller_name"' in html:
        reg = '"seller_name":"(.*?)"'
        seller = re.compile(reg).findall(html)[0]

    return [brand, size, condition, seller]


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def step_1():
    for item in urls:
        request_sheet1(item)
        write_excel(item[1] + '_lzd.xls', sheet1_data)


reload(sys)
sys.setdefaultencoding('utf-8')
step_1()