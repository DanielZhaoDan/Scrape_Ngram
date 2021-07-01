# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
import json
from scraping.utils import post_request_json, get_request_html_with_status, get_request_html, write_html, write_excel

R_ID = 1
sheet1_data = [['ID', 'SKU des', 'Rank', 'Price', 'Brand', 'Product Url', 'Display Size', 'Seller', 'Shipping location', 'Condition']]

cookie = 'SPC_IA=-1; SPC_EC=-; SPC_F=beDMZUNDjW7q71gIeFphq8UUSxm4YMis; REC_T_ID=9205007e-e798-11ea-ad45-ccbbfe5df652; SPC_U=-; _gcl_au=1.1.1699378879.1615729175; SPC_SI=mall.asx1eJLhmFJruc0rU3GvNstOwh2LdE6j; csrftoken=HXi5GXLiWmTJzLrA7RC75bTWOBeuT9wu; SPC_CT_960ac9a3="1615729175.tT3RO8WmOtDpKhpuYGzE4POqh9EOF9LbKr0eJj3oGKM="; _ga_SW6D8G0HXK=GS1.1.1615729176.5.0.1615729176.60; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.3.1523176960.1598445307; _gid=GA1.3.273393079.1615729177; _dc_gtm_UA-61904553-8=1; SPC_R_T_ID="CKTwoKX1481tfNAxhenGSd81uyJYKg8bsatJkU2dkOQanDZjkckztRVAZfhOAlM4DmNnXp6+4car/qD9AGhMfAcXGxNtvdv+bpt3TTjwHsY="; SPC_T_IV="6/3JTWDl+J9q7r5hLCKdzg=="; SPC_R_T_IV="6/3JTWDl+J9q7r5hLCKdzg=="; SPC_T_ID="CKTwoKX1481tfNAxhenGSd81uyJYKg8bsatJkU2dkOQanDZjkckztRVAZfhOAlM4DmNnXp6+4car/qD9AGhMfAcXGxNtvdv+bpt3TTjwHsY="'

price_division = {
    'SG': 100000,
    'PH': 100000,
    'MY': 100000,
    'TH': 100000,
    'ID': 100000000,
}

urls = [
    ('https://shopee.sg/api/v2/search_items/?by=sales&categoryids=633&keyword=laptop&limit=50&match_id=9&order=desc&page_type=search&skip_autocorrect=1&version=2', 'SG', '50', 'ALL'),
    ('https://shopee.ph/api/v2/search_items/?by=sales&categoryids=18601&keyword=laptop&limit=50&match_id=18599&order=desc&page_type=search&skip_autocorrect=1&version=2', 'PH', '45', 'ALL'),
    ('https://shopee.com.my/api/v2/search_items/?by=sales&categoryids=741&keyword=laptop&limit=50&match_id=174&order=desc&page_type=search&skip_autocorrect=1&version=2', 'MY', '100', 'ALL'),
    ('https://shopee.co.th/api/v2/search_items/?by=sales&categoryids=13849&keyword=laptop&limit=50&match_id=264&newest=0&order=desc&page_type=search&skip_autocorrect=1&version=2', 'TH', '39', 'ALL'),
    ('https://shopee.co.id/api/v2/search_items/?by=sales&categoryids=1367&keyword=laptop&limit=50&match_id=134&order=desc&page_type=search&skip_autocorrect=1&version=2', 'ID', '100', 'ALL'),
    #
    (
    'https://shopee.sg/api/v2/search_items/?by=sales&categoryids=633&conditions=used&keyword=laptop&limit=50&match_id=9&order=desc&page_type=search&skip_autocorrect=1&version=2',
    'SG', '50', 'USED'),
    (
    'https://shopee.ph/api/v2/search_items/?by=sales&categoryids=18601&conditions=used&keyword=laptop&limit=50&match_id=18599&order=desc&page_type=search&skip_autocorrect=1&version=2',
    'PH', '45', 'USED'),
    (
    'https://shopee.com.my/api/v2/search_items/?by=sales&categoryids=741&conditions=used&keyword=laptop&limit=50&match_id=174&order=desc&page_type=search&skip_autocorrect=1&version=2',
    'MY', '100', 'USED'),
    (
    'https://shopee.co.th/api/v2/search_items/?by=sales&categoryids=13849&conditions=used&keyword=laptop&limit=50&match_id=264&newest=0&order=desc&page_type=search&skip_autocorrect=1&version=2', 'TH', '39', 'USED'),
]

shop_dict = {}

add_header = {
    'x-requested-with': 'XMLHttpRequest',
    'accept': '*/*',
    'x-shopee-language': 'en',
    'if-none-match': '62eb7454004014eaf45fb4da06bd0356',
    'if-none-match-': '55b03-837edf7cfe6ae5bb9f8c6e977eecd50d',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
    'referer': 'https://shopee.co.th/search?category=55&facet=13849&keyword=laptop&noCorrection=true&page=1&sortBy=sales&subcategory=264',
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-origin',
    'x-api-source': 'pc',
}


def get_item_url(name, shopid, itemid):
    item_url = re.sub('[\[\]"%/|+ #,]', '-', name) + '-i.%d.%d' % (shopid, itemid)

    return re.sub('-+', '-', item_url)


def request_sheet1(item):
    global sheet1_data
    url_base, country, page_no, condition = item
    url_prefix = url_base.split('api')[0]

    i = 0
    count = 0

    while i < int(page_no):
        print (country, i, int(page_no), condition)

        if 'newest=' in url_base:
            url = url_base.replace('&newest=0', '&newest=%d' % (i * 50))
        else:
            url = url_base + '&newest=%d' % (i * 50)
        # url = 'https://shopee.co.th/api/v2/search_items/?by=sales&categoryids=13849&conditions=used&keyword=laptop&limit=50&match_id=264&newest=50&order=desc&page_type=search&skip_autocorrect=1&version=2'
        print url
        try:

            html, status = get_request_html_with_status(url, cookie, add_header=add_header)
            json_obj = json.loads(html)

            items = json_obj.get('items', [])

            j = 0
            for item in items:
                name = item.get('name')
                shopid = item.get('shopid')
                itemid = item.get('itemid')

                if not name or not shopid or not itemid:
                    continue

                item_url = url_prefix + get_item_url(name, shopid, itemid)

                if not item.get('price'):
                    price_max = item.get('price_max') / price_division[country]
                    price_min = item.get('price_max') / price_division[country]

                    price = '%d - %d' % (price_min, price_max)
                else:
                    price = item.get('price') / price_division[country]

                brand, size = request_sheet2(url_prefix, shopid, itemid)

                seller, location = request_seller(shopid, url_prefix)

                one_row = ['%s_%d_%d' % (country, itemid, shopid), name, '%d.%d' % (i+1, j), price, brand, item_url, size, seller, location, condition]

                sheet1_data.append(one_row)
                # print one_row

                count += 1
                j += 1

            i += 1
            if count >= 100:
                break
        except Exception as e:
            i += 1
            print 'ERR---', url, i, e


def request_seller(shopid, url_prefix):

    if shopid in shop_dict:
        return shop_dict[shopid]

    url = url_prefix + '/api/v2/shop/get?is_brief=1&shopid=' + str(shopid)
    seller = 'N/A'
    location = 'N/A'

    try:
        res = get_request_html(url, cookie, add_header=add_header)
        json_obj = json.loads(res)

        seller = json_obj.get('data', {}).get('account', {}).get('username', 'N/A')
        location = json_obj.get('data', {}).get('place', 'N/A')

        shop_dict[shopid] = (seller, location)

    except Exception as e:
        print 'seller', url, e
    return seller, location


def request_sheet2(url_prefix, shopid, itemid):
    url = url_prefix + 'api/v2/item/get?itemid=%s&shopid=%s' % (str(itemid), str(shopid))

    brand = 'N/A'
    size = 'N/A'
    try:

        res = get_request_html(url, cookie, add_header=add_header)
        json_obj = json.loads(res)
        attributes = json_obj.get('item',{}).get('attributes', [])

        for cat in attributes:
            if cat['name'] == 'Brand' or cat['name'] == 'ยี่ห้อ' or cat['name'] == 'Merek':
                brand = cat['value']
            elif cat['name'] == 'Screen Size (Inches)' or cat['name'] == 'Ukuran Layar':
                size = cat['value']

    except Exception as e:
        print 'detail', url, e
    return brand, size


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def step_1():
    for item in urls:
        request_sheet1(item)
        write_excel(item[1] + item[-1] + '_shopee.xls', sheet1_data)
    # write_excel(item[1] + item[-1] + 'shopee.xls', sheet1_data)


reload(sys)
sys.setdefaultencoding('utf-8')
step_1()