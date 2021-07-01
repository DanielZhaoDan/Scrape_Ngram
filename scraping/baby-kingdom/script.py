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
sheet1_data = []

cookie = '_ga=GA1.2.294996316.1599391441; _hjid=23aa1c70-eb99-4598-a923-ddda11e613e6; _qg_fts=1599391442; QGUserId=3445983362825749; mlbu=1599391442.384E87BB5B-6819-4C20-9BDD-9F49FBC5A123; __cfduid=d2ad354c866eafd92f2b998f4ea5f4d8c1610548295; rAvd_2132_lastvisit=1610544728; _gcl_au=1.1.1436246555.1610548330; googcdn=0x18; _hjTLDTest=1; _qg_cm=1; from_site=https%3A%2F%2Fwww.baby-kingdom.com%2Fsearch.php%3Fmod%3Dforum%26searchid%3D705%26orderby%3Dlastpost%26ascdesc%3Ddesc%26searchsubmit%3Dyes%26page%3D1%26range_time%3Dyear%26srchfrom%3D31536000%26__cf_chl_captcha_tk__%3D65354c730cd48e3a5621f4684ed39b7fd5af0454-1610548295-0-AcPhmmdOzw9FgCOP8E1Zb9JNAj64ElWGp054O6KkFQZ3sHVDOKbZSsFGdniKl_MEKSfdliVBwRuNCQhTH9BdxZ99_c_RRM2LfSi--dRDNyxSqkpWG6RJNM30fug3vQrHqu9A4-JLM6ZW-DvoiTShapoRwpV_zO8IFUR8JyzIVOkQ-4-sniVyHzINcGqUV5ExpBcuBRraMsO57m5v3Lyvem9VATyCeAyWIDaSzfMFycBiVcdyDGxisLfk97M_uSZV16e5RrfPSdpIeTESI7hYwg85KK1LceNOYEuw5NH7yuGuC25JnXN9pTYn2YHBk3fh59B4TqI8x_LfMy6sbvf7gMTvod4_y3TgDjTkiHRoFXri9lsAsfwWuBMcPbnssditpjXTEHCk7EoHQb8oMUjW3Bs3QDZw1hV26UVw9x_Ja9ajwUrScwpsLrG5PILbRkayr3OpC_av3T-tczKLd-gRVSUMs23-dH4eFmYG6IpJtY-9sD3-mLxm6foDWVqiwBt3HvYkhOP24WqFawOhf5f5eMRTdwQg2O5pfGygtkw6A4_YSAwq2tPHQlMwCTQv1LRD5jkULPnSe_koYbqeEpEEhT6Bh8MjInB9uMhR1aU3SRzVsdtNwTkF8hlqv9Nk81k55cvvNiTlNhR4m4ad2_jaLYda6_fIsrb6Ta319AM6aJzA; rAvd_2132_visitedfid=717D728D9D162D19D1111; googtrans=/zh-CN/en; googtrans=/zh-CN/en; cf_chl_prog=a19; cf_clearance=7bb84be767788462e11d27487aa30ed0257f6e7d-1610785883-0-250; rAvd_2132_sid=0nP2Bj; rAvd_2132_lastact=1610785883%09search.php%09forum; rtdSEG=658318,658320,659257; _gid=GA1.2.2023962357.1610785887; _gat_UA-197201-3=1; _hjAbsoluteSessionInProgress=0; _qg_pushrequest=true'

urls = [
    # ('emigration Property', '移民 物業', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=570&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E7%89%A9%E6%A5%AD'),
    # ('emigration funds', '移民 資金', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=791&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E8%B3%87%E9%87%91'),
    # ('emigrate UK', '移民 英國', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=792&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E8%8B%B1%E5%9C%8B'),
    # ('emigrate New Zealand', '移民 紐西蘭', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=793&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E7%B4%90%E8%A5%BF%E8%98%AD'),
    # ('emigrate Australia', '移民 澳洲', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=794&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E6%BE%B3%E6%B4%B2'),
    # ('emigrate Canada', '移民 加拿大', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=795&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E5%8A%A0%E6%8B%BF%E5%A4%A7'),
    # ('emigrate Taiwan', '移民 台灣', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=796&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E5%8F%B0%E7%81%A3'),
    # ('emigrate Singapore', '移民 新加坡', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=797&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E6%96%B0%E5%8A%A0%E5%9D%A1'),
    # ('emigrate US', '移民 美國', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=798&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E7%BE%8E%E5%9C%8B'),
    # ('emigrate start up business', '移民 創業', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=799&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E5%89%B5%E6%A5%AD'),
    # ('emigrate Schooling', '移民 升學', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=802&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E5%8D%87%E5%AD%B8'),
    # ('emigrate Education', '移民 教育', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=803&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E6%95%99%E8%82%B2'),
    # ('emigrate Universities', '移民 大學', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=804&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E5%A4%A7%E5%AD%B8'),
    # ('Investment in Oversea funds', '海外基金 投資', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=807&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E6%B5%B7%E5%A4%96%E5%9F%BA%E9%87%91+%E6%8A%95%E8%B3%87'),
    # ('Investment in Oversea properties', '海外物業 投資', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=808&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E6%B5%B7%E5%A4%96%E7%89%A9%E6%A5%AD+%E6%8A%95%E8%B3%87'),
    # ('Oversea house buying', '海外買樓', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=809&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E6%B5%B7%E5%A4%96%E8%B2%B7%E6%A8%93'),
    # ('Oversea job hunting', '海外搵工', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=811&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E6%B5%B7%E5%A4%96%E6%90%B5%E5%B7%A5'),
    # ('Emigrate Change Jobs', '移民 轉工', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=812&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E8%BD%89%E5%B7%A5'),
    # ('emigration Invest', '移民 投資', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=789&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E6%8A%95%E8%B3%87'),
    # ('Skill-based immigration', '技術移民', 'Baby kingdom', 'https://www.baby-kingdom.com/search.php?mod=forum&searchid=805&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E6%8A%80%E8%A1%93%E7%A7%BB%E6%B0%91'),
    ('Emigrate Pay Tax', '移民 交稅', 'Baby kingdom',
     'https://www.baby-kingdom.com/search.php?mod=forum&searchid=2085&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E4%BA%A4%E7%A8%85'),
    ('Emigrate Tax Types', '移民 稅項', 'Baby kingdom',
     'https://www.baby-kingdom.com/search.php?mod=forum&searchid=2087&orderby=lastpost&ascdesc=desc&searchsubmit=yes&keyword=%E7%A7%BB%E6%B0%91+%E7%A8%85%E9%A0%85'),

]

uid_level_dict = {}


def request_sheet0(item):
    en_key, cn_key, forum_name, main_url = item

    page_no = 5
    i = 1
    while i <= page_no:
        try:
            html = get_request_html(main_url + '&page=%d' % i, cookie)

            # if not page_no:
            #     try:
            #         page_reg = '找到相關主題 (.*?) '
            #         page_no = re.compile(page_reg).findall(html)[0] / 30
            #     except:
            #         page_no = 10
            reg = 'class="xs3".*?href="(.*?)"'
            url_list = re.compile(reg).findall(html)

            for url in url_list:
                if 'mod=viewthread' in url:
                    request_sheet1(i, page_no, url, [en_key, cn_key, forum_name, main_url])
            i += 1
        except Exception as e:
            i += 1
            print 'ERR0---', main_url, i, e


def request_sheet1(parent_index, parent_no, url, list_prefix):
    global sheet1_data

    base_reg = 'class="xs2".*?href.*?>(.*?)<.*?pagination-lastpage.*?page=(.*?)".*?查看: (.*?)<.*?回覆: (.*?)<.*?id="postmessage_.*?>(.*?)</span'
    comment_reg = 'id="postmessage_.*?>(.*?)</span'

    i = 1

    html = get_request_html(url + '&page=%d' % i, cookie)

    if 'postmessage_' not in html:
        return
    data = re.compile(base_reg).findall(html)

    if not data:
        print 'ERR_BASIC', url
        return
    item = data[0]
    topic = item[0]
    try:
        page_no = int(item[1])
    except:
        page_no = 1
    no_view = item[2]
    no_reply = item[3]
    post = item[4].replace('&amp;', '&')

    while i <= min(page_no, 9):
        print list_prefix[1], parent_index, i, page_no, url
        try:
            if i > 1:
                html = get_request_html(url + '&page=%d' % i, cookie)
            data = re.compile(comment_reg).findall(html)

            if i == 1:
                one_row = list_prefix + [url, no_view, no_reply, remove_html_tag(post), 'Main Post']
                sheet1_data.append(one_row)
                start_index = 1
            else:
                start_index = 0

            for item in data[start_index:]:
                comments = get_comments(item)

                one_row = list_prefix + [url, no_view, no_reply, comments.strip(), 'Reply']
                sheet1_data.append(one_row)
            i += 1
        except Exception as e:
            i += 1
            print 'ERR1---', url, i, e


def get_comments(ori):
    escape_words = ['的帖子', '</blockquote>', '編輯']

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
