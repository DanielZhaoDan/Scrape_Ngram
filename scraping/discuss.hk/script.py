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

cookie = '__cfduid=d9684b5b0d077450cecbb4f3cdfcdf7301610621202; cf_chl_prog=a21; nwtc=6000212f39c150.29487145; curr_hostname=news.discuss.com.hk; lotame_domain_check=discuss.com.hk; AB_18=B; AB_28=A; AB_29=A; AB_34=B; AB_full=18-B_28-A_29-A_34-B; cdb_nc_open_datetime=2021-01-14%2018%3A47%3A11; _cc_id=61cb1465ec5bb00fdaa46dfaf2bf2110; __asc=62a0b7891770081a2cc838b4841; __auc=62a0b7891770081a2cc838b4841; up_c=1610621232; _ga=GA1.4.1509731538.1610621232; _gid=GA1.4.282494883.1610621232; _dc_gtm_UA-4077994-2=1; nvg56367=be991a3cc03caecbd4fb855ef09|2_15; def_crw=eyJpdiI6IlVINGJhOTFOS1JcL0xuZkRTVjlIM05RPT0iLCJ2YWx1ZSI6IjdCYVAxa0xSdVBoSkgxVUVpb25GM3NtdndKWlZGZmsrUFUxTnBhS29JcUg0YmFyR094VHBkNzBCdTlJSDNDXC9Td2VlTkY2dUJyU3pnMFdhNFpSTHM0aXU4ZmV5RGVuVDNjVTVZOVFvMFFOVkJlaWpSUEo0TmdETDg4OTBPSUduY3o2T2FNbldkOUZjNkNGeGhONGZtNVU3RUJiM2xiYWdHUmhMUDZpWm1IOEVQaXFrVDQxck1mWTk1UndqektFUkdRN1l1cFhWUG4raHh1cEtYVFE1dCsybzdUUTJ5T2YwSmRWeExxNzlCZlhaczNJYm5EWXgwcDg2cUF0bTUyams2OEtpZXFWbE9vTEhMTFdvMVUxSUE0QT09IiwibWFjIjoiODk4NTAwNzk1ZTNkZGIxMGU4M2MwMjdmODI0OGZkMjQ0NzJmZWQyMTNlNDcwZTIyZmFkOGEzZWMzZTk1MzZkZSJ9; cf_clearance=8e5a517bc35d064f226dbd2d09eef8e450daba1b-1610621234-0-250; cdb_lastrequest=WqcBN4Df%2BvjnlQBbp%2B49fM1I; cdb_sid=aoizAG; viewthread_history=29033384; dfp_seg_ids=%5B%5D; cdb_oldtopics=D29033384D; cdb_visitedfid=54; cdb_urihistory=29033384-1%3B; cdb_urihistorycount=1; ttd-web=1610621234; davincii-web=1610621234; nmc-web=1610621234; innity-web=1610621234; ats_referrer_history=%5B%22news.discuss.com.hk%22%5D; lotame-audience-web=1610621234; cookieconsent_status=dismiss'

urls = [
    # ('emigration Property', '移民 物業', 'Discuss', 'https://www.discuss.com.hk/search.php?searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E7%89%A9%E6%A5%AD&srchtime=1y&orderby=most_relevant'),
    # ('emigration Invest', '移民 投資', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E6%8A%95%E8%B3%87&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigration funds', '移民 資金', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E8%B3%87%E9%87%91&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate UK', '移民 英國', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E8%8B%B1%E5%9C%8B&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate New Zealand', '移民 紐西蘭', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E7%B4%90%E8%A5%BF%E8%98%AD&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate Australia', '移民 澳洲', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E6%BE%B3%E6%B4%B2&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate Canada', '移民 加拿大', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E5%8A%A0%E6%8B%BF%E5%A4%A7&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate Taiwan', '移民 台灣', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E5%8F%B0%E7%81%A3&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate Singapore', '移民 新加坡', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E6%96%B0%E5%8A%A0%E5%9D%A1&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate US', '移民 美國', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91%E7%BE%8E%E5%9C%8B&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate start up business', '移民 創業', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E5%89%B5%E6%A5%AD&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate Schooling', '移民 升學', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E5%8D%87%E5%AD%B8&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate Education', '移民 教育', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E6%95%99%E8%82%B2&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('emigrate Universities', '移民 大學', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E5%A4%A7%E5%AD%B8&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('Skill-based immigration', '技術移民', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E6%8A%80%E8%A1%93%E7%A7%BB%E6%B0%91&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('Investment in Oversea funds', '海外基金 投資', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E6%B5%B7%E5%A4%96%E5%9F%BA%E9%87%91+%E6%8A%95%E8%B3%87&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('Investment in Oversea properties', '海外物業 投資', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E6%B5%B7%E5%A4%96%E7%89%A9%E6%A5%AD+%E6%8A%95%E8%B3%87&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('Oversea house buying', '海外買樓', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E6%B5%B7%E5%A4%96%E8%B2%B7%E6%A8%93&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('Oversea job hunting', '海外搵工', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E6%B5%B7%E5%A4%96%E6%90%B5%E5%B7%A5&srchuname=&srchtime=1y&orderby=most_relevant'),
    # ('Emigrate Change Jobs', '移民 轉工', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&orderby=most_relevant&searchsubmit=yes&srcheng=1&srchtxt=%E7%A7%BB%E6%B0%91+%E8%BD%89%E5%B7%A5&srchtime=1y'),
    ('Emigrate Pay Tax', '移民 交稅', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&orderby=most_relevant&searchsubmit=yes&srcheng=1&srchtxt=%E7%A7%BB%E6%B0%91+%E4%BA%A4%E7%A8%85&srchtime=1y'),
    ('Emigrate Tax Types', '移民 稅項', 'Discuss', 'https://www.discuss.com.hk/search.php?formhash=8b6f926e&searchsubmit=true&srchtxt=%E7%A7%BB%E6%B0%91+%E7%A8%85%E9%A0%85&srchuname=&srchtime=1y&orderby=most_relevant'),
]

uid_level_dict = {}


def request_sheet0(item):
    en_key, cn_key, forum_name, main_url = item

    page_no = 10
    i = 1
    while i <= page_no:
        try:
            html = get_request_html(main_url + '&page=%d' % i, cookie)

            reg = 'search-result-subject.*?.*?ptid=(.*?)&'
            ptid_list = re.compile(reg).findall(html)

            for ptid in ptid_list:
                url = 'https://news.discuss.com.hk/viewthread.php?tid=' + ptid
                request_sheet1(i, page_no, url, [en_key, cn_key, forum_name, main_url])
            i += 1
        except Exception as e:
            i += 1
            print 'ERR0---', url, i, e


def request_sheet1(parent_index, parent_no, url, list_prefix):
    global sheet1_data

    base_reg = 'topbar_fid1a.*?href.*?>(.*?)<.*?pagination-buttons.*?;(.*?)&.*?瀏覽: (.*?)<.*?回覆: (.*?)<.*?id="postmessage.*?>(.*?)</span'
    comment_reg = 'id="postmessage_.*?>(.*?)</span'

    i = 1

    html = get_request_html(url + '&page=%d' % i, cookie)
    if 'postmessage' not in html:
        pass

    if 'pagination-buttons' not in html:
        base_reg = 'topbar_fid1a.*?href.*?>(.*?)<.*?瀏覽: (.*?)<.*?回覆: (.*?)<.*?id="postmessage.*?>(.*?)</span'
    data = re.compile(base_reg).findall(html)

    if not data:
        print 'ERR_BASIC', url
        return
    item = data[0]
    topic = item[0]
    if 'pagination-buttons' not in html:
        page_no = 1
    else:
        try:
            no_post = int(item[1])
            page_no = no_post / 15 + 1
        except:
            page_no = 1
    page_no = min(page_no, 10)
    no_view = item[-3]
    no_reply = item[-2]
    post = remove_html_tag(item[-1]).replace('&amp;', '&').strip()

    while i <= page_no:
        print parent_index, parent_no, i, page_no, url
        try:
            if i > 1:
                html = get_request_html(url + '&page=%d' % i, cookie)
            data = re.compile(comment_reg).findall(html)

            if i == 1:
                start_index = 1
                one_row = list_prefix + [url, no_view, no_reply, post, 'Main Post']
                # print one_row
                sheet1_data.append(one_row)
            else:
                start_index = 0

            for item in data[start_index:]:
                comments = get_comments(item)

                one_row = list_prefix + [url, no_view, no_reply, comments.strip(), 'Reply']
                # print one_row
                sheet1_data.append(one_row)
            i += 1
        except Exception as e:
            i += 1
            print 'ERR---', url, i, e


def get_comments(ori):

    escape_words = ['的帖子', '</blockquote>', '發表']

    for word in escape_words:
        if word in ori:
            ori = remove_html_tag(ori.split(word)[-1])
    return remove_html_tag(ori)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def step_0(items):
    global sheet1_data
    for item in items:
        sheet1_data = []
        request_sheet0(item)
        write_excel(item[0]+'.xls', sheet1_data)


reload(sys)
sys.setdefaultencoding('utf-8')
step_0(urls)