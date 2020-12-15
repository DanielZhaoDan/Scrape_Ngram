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

cookie = '_uab_collina=159832265769569523139964; t_fv=1598322657614; t_uid=G8MX02iNjHrV3hNjipyZb16Z3beSpsPR; lzd_cid=dca654b7-258f-4226-d098-b8aee04149be; cna=hrXCF0Ce0FMCASp4SZ6S0pYk; _bl_uid=bpk7IeXw9s7c4a1n6l5wk2ndtd7d; _ga=GA1.3.1102477189.1598322662; pdp_sfo=1; JSESSIONID=C708DB027A25EA5CC947E2B4E41BF650; lzd_sid=112be3f72deb7cf45d98de2693645d26; _tb_token_=767f61367ebf7; hng=PH|en-PH|PHP|608; userLanguageML=en; t_sid=h6E6ptdjqsjHdznImI2btiTsWqqcNE5E; utm_channel=NA; _gcl_au=1.1.74247309.1607222235; _uetsid=f61b8600376b11eba622553b9cacb1b0; _uetvid=f61bd570376b11ebbd2d333763f8a654; _gid=GA1.3.1050123479.1607222240; _gat_UA-30245404-1=1; cto_axid=Twkw7dnTzN2IrFvxqR8tAOL45mYHRbgP; xlly_s=1; tfstk=cJalB7VeBx96hAm0fag7sfVAtlSAZYYEIyzburM2ouQsjD4ViOt2bLGFiY2uJH1..; l=eBQM6iNeOYITEN3LBOfZourza77OSIRYnuPzaNbMiOCPOU5p5dz1WZRdtkT9C3GVh6yvR3uLF1-pBeYBcS0DdUoyqYmDJeHmn; isg=BHt7D24MoE469JxyKo054dyxClnl0I_SyI06TW04KXqRzJqu8KRCI9ye4GyCVufK'

urls = [
    ('https://www.lazada.co.th/shop-laptops/?spm=a2o4m.home.cate_1.3.1125719cxYbYGn', 'TH', '25490', '102'),
    ('https://www.lazada.com.my/shop-laptops/?spm=a2o4k.home.cate_1.2.75f82e7eb9d11q', 'MY', '26604', '102'),
    ('https://www.lazada.sg/shop-laptops/?page=102&spm=a2o42.home.cate_1.3.654346b5ZtkEpx', 'SG', '13550', '102'),
    ('https://www.lazada.co.id/beli-laptop/?spm=a2o4j.home.cate_1.2.57991559MMbWnz', 'ID', '11213', '102'),
    ('https://www.lazada.com.ph/shop-laptops/?spm=a2o4l.home.cate_1.3.239e359dJdUwRF', 'PH', '15549', '102'),
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