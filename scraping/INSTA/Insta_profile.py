# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
import requests
import gc
import json
from scraping.utils import get_request_html, write_html, write_excel, get_request_json
from datetime import datetime

alldata = [['id', 'url', 'Username', 'Post type', 'Content', 'Comments', 'Likes', 'Number of Views', 'date of posts']]
url = 'https://www.instagram.com/query/'
total_count = -1
url_prefix = 'https://www.instagram.com/p/'

cookie = 'ig_did=32EF62E6-2E0D-40FA-A387-0EA65DCEC289; mid=Ximr7wAEAAFv5zXx1KkXsLvG_z54; csrftoken=jhmwjduVDHhuwLoGd6gN3FKUqywwcBQL; ds_user_id=4871140174; sessionid=4871140174%3A4HUtLCwpDFGTiW%3A18; rur=ASH; urlgen="{\"42.60.37.32\": 9506}:1jG12T:D5kasQp_C1aip2_hwu-hfX1JXVI"'
crsf = 'jhmwjduVDHhuwLoGd6gN3FKUqywwcBQL'
U_ID = 1


def get_head():
    global U_ID, alldata
    html = get_request_html('https://www.instagram.com/explore/tags/keepaclearhead/', cookie)

    reg = '"shortcode":"(.*?)"'

    tag_list = re.compile(reg).findall(html)
    print len(tag_list)
    for tag in tag_list:
        url = url_prefix + tag
        try:
            id = 'P_%d' % U_ID
            one_row = get_detail(id, url)
            if one_row:
                alldata.append(one_row)
                print one_row
                U_ID += 1
        except Exception as e:
            print 'exc--', url, e


def get_next():
    global U_ID
    cursor = 'QVFDZEt0Sk5MQ1FYVGZPQ1dlc2hGOVN0Ujk4TWtnTU9pdTMxS1F5MnBNOEFqUEhCUEp3dk03MEViRUNyVUZKUnhwSER4T0l3WC14clVWTzBibkp2eUpsLQ=='

    while cursor and U_ID < 1180:
        try:
            url = 'https://www.instagram.com/graphql/query/?query_hash=bd33792e9f52a56ae8fa0985521d141d&variables=%7B%22tag_name%22%3A%22nothingtohide%22%2C%22first%22%3A4%2C%22after%22%3A%22' + cursor + '%22%7D'
            print url

            json_obj = get_request_json(url, cookie)
            html = json.dumps(json_obj)
            has_next_page = json_obj['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
            cursor = json_obj['data']['hashtag']['edge_hashtag_to_media']['page_info'].get('end_cursor')

            short_codes = re.compile(r'shortcode": "(.*?)"').findall(html)

            for short_code in short_codes:
                url = url_prefix + short_code
                try:
                    id = 'P_%d' % U_ID
                    one_row = get_detail(id, url)
                    if one_row:
                        alldata.append(one_row)
                        print one_row
                        U_ID += 1
                except Exception as e:
                    print 'exc--', url, e

            if not has_next_page:
                break
        except Exception as e:
            print e
            break


def get_detail(p_id, url):
    html = get_request_html(url, cookie)

    if 'is_video":true' not in html:
        return get_img(p_id, html, url)
    return get_video(p_id, html, url)


def get_video(p_id, html, url):
    if 'edge_media_preview_comment' not in html:
        reg = '"video_view_count":(.*?),.*?"edges":\[\{"node":\{"text":"(.*?)".*?"edge_media_to_comment":\{"count":(.*?),.*?taken_at_timestamp":(.*?),"edge_media_preview_like":\{"count":(.*?),.*?owner.*?name":"(.*?)"'
    else:
        reg = '"video_view_count":(.*?),.*?"edges":\[\{"node":\{"text":"(.*?)".*?"edge_media_preview_comment":\{"count":(.*?),.*?taken_at_timestamp":(.*?),"edge_media_preview_like":\{"count":(.*?),.*?owner.*?name":"(.*?)"'

    data = re.compile(reg).findall(html)

    if data:
        view_c = data[0][0]
        content = data[0][1]
        comment = data[0][2]
        date = get_date(data[0][3])
        like_c = data[0][4]
        u_name = data[0][5]
        one_row = [p_id, url, u_name, 'Video', content, comment, like_c, view_c, date]

        return one_row
    return None


def get_img(p_id, html, url):
    if 'edge_media_preview_comment' not in html:
        reg = '"edges":\[\{"node":\{"text":"(.*?)".*?"edge_media_to_comment":\{"count":(.*?),.*?taken_at_timestamp":(.*?),"edge_media_preview_like":\{"count":(.*?),.*?owner.*?name":"(.*?)"'
    else:
        reg = '"edges":\[\{"node":\{"text":"(.*?)".*?"edge_media_preview_comment":\{"count":(.*?),.*?taken_at_timestamp":(.*?),"edge_media_preview_like":\{"count":(.*?),.*?owner.*?name":"(.*?)"'

    data = re.compile(reg).findall(html)

    if data:
        content = data[0][0]
        comment = data[0][1]
        date = get_date(data[0][2])
        like_c = data[0][3]
        u_name = data[0][4]
        one_row = [p_id, url, u_name, 'Photo', content, comment, like_c, '-', date]
        return one_row
    return None


def get_date(timestamp):
    now = datetime.utcfromtimestamp(float(timestamp))

    return now.strftime("%d/%m/%Y")


get_head()
get_next()
write_excel('keepaclearhead.xls', alldata)
