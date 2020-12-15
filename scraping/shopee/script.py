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

cookie = 'SPC_IA=-1; SPC_EC=-; SPC_F=kK5l5w0eACl1hLqOB1W4CE6auqn0Isvz; REC_T_ID=36230cf2-e689-11ea-9582-9c7da3191b54; SPC_U=-; language=en; _gcl_au=1.1.917022037.1607226315; csrftoken=lYNt8WWkEL3r2S17RkycjRTpwq9wOStN; SPC_SI=mall.6lkD1MBtdMm8J7pzeIfnR8ZbpRKS2cQR; SPC_R_T_ID="M3qWDCCJYXc2nUKGxRqaTiSBYrhLxyU5eESNE0fuNDOyLlleE720IeVLxYoK5H1p4uZ8BWaI0JbXyCalDQOIZd3kkVR0Z0d0Djt3HHNmKWc="; SPC_CT_bc7ebfaa=1607654714.5gvXXENoafLJfpmfvN918OOiCREU4Zs6Mn7YdfByekLsrw3n6hWK5uf3Y5I8E1ob; SPC_T_ID="M3qWDCCJYXc2nUKGxRqaTiSBYrhLxyU5eESNE0fuNDOyLlleE720IeVLxYoK5H1p4uZ8BWaI0JbXyCalDQOIZd3kkVR0Z0d0Djt3HHNmKWc="; SPC_R_T_IV="8jqokRylzv5cJsgou4QbJg=="; SPC_T_IV="8jqokRylzv5cJsgou4QbJg=="; _ga_L4QXS6R7YG=GS1.1.1607654715.3.0.1607654715.0; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.3.456797804.1598328762; _gid=GA1.3.1502265687.1607654716; _dc_gtm_UA-61914165-6=1'

price_division = {
    'SG': 10000,
    'PH': 10000,
    'MY': 10000,
    'TH': 10000,
    'ID': 100000000,
}

urls = [
    # ('https://shopee.sg/api/v2/search_items/?by=sales&categoryids=633&keyword=laptop&limit=50&match_id=9&order=desc&page_type=search&skip_autocorrect=1&version=2', 'SG', '50', 'ALL'),
    ('https://shopee.ph/api/v2/search_items/?by=sales&categoryids=18601&keyword=laptop&limit=50&match_id=18599&order=desc&page_type=search&skip_autocorrect=1&version=2', 'PH', '45', 'ALL'),
    ('https://shopee.com.my/api/v2/search_items/?by=sales&categoryids=741&keyword=laptop&limit=50&match_id=174&order=desc&page_type=search&skip_autocorrect=1&version=2', 'MY', '100', 'ALL'),
    # ('https://shopee.co.th/api/v2/search_items/?by=sales&categoryids=13849&keyword=laptop&limit=50&match_id=264&newest=0&order=desc&page_type=search&skip_autocorrect=1&version=2', 'TH', '39', 'ALL'),
    # ('https://shopee.co.id/api/v2/search_items/?by=sales&categoryids=1367&keyword=laptop&limit=50&match_id=134&order=desc&page_type=search&skip_autocorrect=1&version=2', 'ID', '100', 'ALL'),
    #
    # (
    # 'https://shopee.sg/api/v2/search_items/?by=sales&categoryids=633&conditions=used&keyword=laptop&limit=50&match_id=9&order=desc&page_type=search&skip_autocorrect=1&version=2',
    # 'SG', '50', 'USED'),
    (
    'https://shopee.ph/api/v2/search_items/?by=sales&categoryids=18601&conditions=used&keyword=laptop&limit=50&match_id=18599&order=desc&page_type=search&skip_autocorrect=1&version=2',
    'PH', '45', 'USED'),
    (
    'https://shopee.com.my/api/v2/search_items/?by=sales&categoryids=741&conditions=used&keyword=laptop&limit=50&match_id=174&order=desc&page_type=search&skip_autocorrect=1&version=2',
    'MY', '100', 'USED'),
    # (
    # 'https://shopee.co.th/api/v2/search_items/?by=sales&categoryids=13849&conditions=used&keyword=laptop&limit=50&match_id=264&newest=0&order=desc&page_type=search&skip_autocorrect=1&version=2', 'TH', '39', 'USED'),
]

shop_dict = {}

add_header = {
    'x-requested-with': 'XMLHttpRequest',
    'accept': '*/*',
    'x-shopee-language': 'en',
    'if-none-match-': '55b03-e8919217d41032c10be5f1f314b5642d',
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
                price_max = item.get('price_max') / price_division[country]
                price_min = item.get('price_max') / price_division[country]

                price = '%d - %d' % (price_min, price_max)

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