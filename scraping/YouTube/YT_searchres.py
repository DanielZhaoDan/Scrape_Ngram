#', '*- coding: utf-8', '*-

import re
import xlwt, xlrd
from datetime import datetime
import os
import requests
import json
import time
from scraping.utils import write_excel, get_request_html, remove_html_tag, write_html, post_request_html, post_request_json, write_excel

cookie = 'VISITOR_INFO1_LIVE=FmzkzUMsdYU; __Secure-3PSID=7Qc33eBlv498vI1fh1MU6OIhaIXJjQk0Eme90jZeTQndf54GlVcgWn_CeQcd5uhz_OPU4A.; __Secure-3PAPISID=gqi5SeWjS8I0Iooq/AFnNEQdmw1aS7OV04; YSC=S96byrYyy8k; LOGIN_INFO=AFmmF2swRgIhAKLPMWzCVo45tAaHM9HYilXC8-WSfvUNYWukvzdlf6jbAiEAyoVYUVaC8IKdEXKGP2qzSnApv0GacH5ETM_scSTjWHk:QUQ3MjNmekZtd3VheUlGaGluaEpzbXFGMlhBTEhMYWozM24xWEhfaDVucVNZYktYR0I3ZWVHRlloWkQ1VkxIcTAxOTJfMEZwMlFzcTF3UmQ4OUlfenV1UkVtSzRKdGo3TDZ3a25sV0F4OTJPbnRHM193Vi12aXFaWHN5SkdqZUtPSnRmbWlDR0lVN1R1dFNFTlZKX2ZHM21qMEJOSVlTYUNR; wide=1; PREF=tz=Asia.Singapore&f4=4000000; __Secure-3PSIDCC=AJi4QfFdwVOgowKG6ITHgVlcH6-RKvkf_pJLE52drlahUD7ES5A9fxMHcri95OVM4UycEHjrYma1; ST-fe0y63=itct=CDAQ8JMBGAEiEwj79vm3hdHwAhVNvGMGHU3ZBOE%3D&csn=MC41NzU4MjE1Mjg1Mjc4MTU.&endpoint=%7B%22clickTrackingParams%22%3A%22CDAQ8JMBGAEiEwj79vm3hdHwAhVNvGMGHU3ZBOE%3D%22%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fuser%2FCLEARIndonesia%2Fvideos%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_CHANNEL%22%2C%22rootVe%22%3A3611%2C%22apiUrl%22%3A%22%2Fyoutubei%2Fv1%2Fbrowse%22%7D%7D%2C%22browseEndpoint%22%3A%7B%22browseId%22%3A%22UC_KpTo38SI2SwQgm1aqaQmw%22%2C%22params%22%3A%22EgZ2aWRlb3M%253D%22%2C%22canonicalBaseUrl%22%3A%22%2Fuser%2FCLEARIndonesia%22%7D%7D'
prefix = 'https://www.youtube.com'
sheet1_data = []
sub_count_dict = {}

urls = [
    ('Thailand', 'https://www.youtube.com/user/clearthailand'),
    ('Vietnam', 'https://www.youtube.com/user/ClearVietnam'),
    ('Philippines', 'https://www.youtube.com/user/clearstadium'),
    ('Russia', 'https://www.youtube.com/channel/UCdnwZRdLICD1Gbxz2dg0YOw'),
    ('Turkey', 'https://www.youtube.com/user/ClearTurkiye'),
    ('Indonesia', 'https://www.youtube.com/user/CLEARIndonesia'),
]

def request_channel(country, url):
    header = {
        'referer': 'https://www.youtube.com/results?search_query=clear+russia&sp=CAISAhAB',
        'x-goog-visitor-id': 'CgtGbXprelVNc2RZVSiymoqFBg%3D%3D',
    }
    html = get_request_html(url, cookie, add_header=header)
    write_html(html, 'c1.html')


def request_search_result(country, url):
    header = {
        'referer': 'https://www.youtube.com/results?search_query=clear+russia&sp=CAISAhAB',
        'x-goog-visitor-id': 'CgtGbXprelVNc2RZVSiymoqFBg%3D%3D',
    }


    next_token = None
    api_key = None
    stop = False

    while not stop and (url or next_token):
        if not next_token:
            html = get_request_html(url, cookie, pure=True, add_header=header)
            reg = 'innertubeApiKey":"(.*?)".*?itemSectionRenderer(.*?)continuationItemRenderer.*?continuationCommand.*?token":"(.*?)"'
            detail_reg = 'title.*?text":"(.*?)".*?webCommandMetadata.*?url":"(.*?)".*?publishedTimeText.*?simpleText":"(.*?)".*?viewCountText.*?simpleText":"(.*?) .*?navigationEndpoint.*?url":"(.*?)"'
        else:
            reg = 'itemSectionRenderer(.*?)continuationItemRenderer.*?continuationCommand.*?token": "(.*?)"'
            detail_reg = 'title.*?text": "(.*?)".*?webCommandMetadata.*?url": "(.*?)".*?publishedTimeText.*?simpleText": "(.*?)".*?viewCountText.*?simpleText": "(.*?) .*?navigationEndpoint.*?url": "(.*?)"'
            data = '{"context":{"client":{"hl":"en","gl":"SG","remoteHost":"47.89.100.1","deviceMake":"Apple","deviceModel":"","visitorData":"CgtGbXprelVNc2RZVSjNpP-EBg%3D%3D","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20210513.07.00","osName":"Macintosh","osVersion":"10_15_7","originalUrl":"https://www.youtube.com/results?search_query=clear+russia&sp=CAISAhAB","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","timeZone":"Asia/Singapore","browserName":"Chrome","browserVersion":"90.0.4430.93","screenWidthPoints":1382,"screenHeightPoints":273,"screenPixelDensity":1,"screenDensityFloat":1,"utcOffsetMinutes":480,"userInterfaceTheme":"USER_INTERFACE_THEME_DARK","connectionType":"CONN_CELLULAR_4G","mainAppWebInfo":{"graftUrl":"https://www.youtube.com/results?search_query=clear+russia&sp=CAISAhAB","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":false}},"user":{"lockedSafetyMode":false},"request":{"useSsl":true,"internalExperimentFlags":[],"consistencyTokenJars":[]},"clientScreenNonce":"MC42ODQ1OTAxNjQ4MzY1Ng..","clickTracking":{"clickTrackingParams":"CAAQvGkiEwjE9v7r7cvwAhXMWSoKHem1Cfc="},"adSignalsInfo":{"params":[{"key":"dt","value":"1621086797714"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"480"},{"key":"u_his","value":"6"},{"key":"u_java","value":"false"},{"key":"u_h","value":"1080"},{"key":"u_w","value":"1920"},{"key":"u_ah","value":"1055"},{"key":"u_aw","value":"1862"},{"key":"u_cd","value":"24"},{"key":"u_nplug","value":"2"},{"key":"u_nmime","value":"2"},{"key":"bc","value":"31"},{"key":"bih","value":"273"},{"key":"biw","value":"1366"},{"key":"brdim","value":"151,124,151,124,1862,25,1382,875,1382,273"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]}},"continuation":"' + next_token + '"}'
            html_obj = post_request_json('https://www.youtube.com/youtubei/v1/search?key=' + api_key, cookie, data=data)
            html = json.dumps(html_obj)

        raw_data = re.compile(reg).findall(html)
        if not raw_data:
            break
        raw_data = raw_data[0]

        detail = re.compile(detail_reg).findall(raw_data[-2])
        for item in detail:
            title = item[0]
            channel_url = prefix + item[1]
            raw_time = item[2]
            no_view = item[3]
            video_url = prefix + item[4]
            try:

                detail, year = get_video_detail(video_url)

                if year <= 2019:
                    stop = True
                    break
                one_row = [country, 0, channel_url, title, video_url, no_view, detail[0], detail[2], detail[1]]
                print(one_row)
                sheet1_data.append(one_row)
            except Exception as e:
                print('item error: ', video_url, e)

        if not api_key:
            api_key = raw_data[0]
        next_token = raw_data[-1]


def get_video_detail(url):
    header = {
        'referer': 'https://www.youtube.com/results?search_query=clear+russia&sp=CAISAhAB',
        'x-goog-visitor-id': 'CgtGbXprelVNc2RZVSjNpP-EBg%3D%3D',
    }
    html = get_request_html(url, cookie, add_header=header)

    if 'Comments are turned off' in html:
        reg = '"iconType":"LIKE".*?simpleText":"(.*?)".*?dateText".*?simpleText":"(.*?)"'
    else:
        reg = '"iconType":"LIKE".*?simpleText":"(.*?)".*?dateText".*?simpleText":"(.*?)".*?continuation":"(.*?)".*?clickTrackingParams":"(.*?)"'
    data_list = re.compile(reg).findall(html)
    for data in data_list:
        like_count = parse_number(data[0])
        date, year = parse_date(data[1])
        if (len(data) > 2):
            comment_track = data[2]
            itct = data[3]
            return [like_count, date, comment_track + '-----' + itct], year
        return [like_count, date, 'N/A'], year


def parse_date(ori):
    date_list = ori.split(' ')
    date_str = '-'.join(date_list[-3:])
    return get_date(date_str)


def get_date(ori):
    try:
        d = datetime.strptime(ori, '%b-%d,-%Y')
        date = d.strftime('%d/%m/%Y')
    except:
        return ori, 2021
    return date, int(d.year)


def get_comments(ctoken, continuation, itct):
    global sheet1_data
    comment_base_url = 'https://www.youtube.com/comment_service_ajax?action_get_comments=1&pbj=1&ctoken=%s&continuation=%s&itct=%s'
    try:
        url = comment_base_url % (ctoken, continuation, itct)
        json_obj = post_json_request(url)
        comments_count = json_obj['response']['continuationContents']['itemSectionContinuation']['header']['commentsHeaderRenderer']['commentsCount']['runs']
        return parse_number(comments_count[0]['text'])
    except Exception as e:
        return 0


def post_json_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
        'x-client-data': 'CIe2yQEIo7bJAQjBtskBCKmdygEIlqzKAQiOucoBCPjHygEIufvKAQjknMsBCKmdywEIoKDLARjM8ssB',
        'x-spf-previous': 'https://www.youtube.com/channel/UCscRTJnqjvJhuHJBPiB2WIQ/videos',
        'x-spf-referer': 'https://www.youtube.com/channel/UCscRTJnqjvJhuHJBPiB2WIQ/videos',
        'content-type': 'application/x-www-form-urlencoded',
        'x-youtube-client-name': '1',
        'x-youtube-client-version': '2.20190130',
        'x-youtube-identity-token': 'QUFFLUhqbFZBUnVVUEt5OHpPZlRxbWlZZ2JhZzNKMm94UXw=',
        'x-youtube-page-cl': '230970375',
        'x-youtube-page-label': 'youtube.ytfe.desktop_20181219_4_RC2',
        'x-youtube-utc-offset': '480',
        'x-youtube-variants-checksum': '3bb6b151a0266521f80bacee55e26119',
        'referer': 'https://www.youtube.com/channel/UCscRTJnqjvJhuHJBPiB2WIQ/videos',
    }
    data = {
        'session_token': 'QUFFLUhqblR0MmVXczVHNktNRkZRQzB4NUV4Q1NxNkYyUXxBQ3Jtc0tuY1pKNm1vWmtnYkJtblBoNThtYjJLUmFocW0tU3gzN2dGalRkVnZhQWdUUzJXRUFSdHdCWl9hQndlX3pCVW1sUjVLZ1QtbmNzSmt6MkxMRENERkJZLVhFOWUyUGZfVW5tN0ZWNWs2bEkybkx6bzlWYw==',
    }
    req = requests.post(get_url, headers=headers, data=data)
    return req.json()


def parse_number(ori):
    try:
        if 'k' in ori or 'K' in ori :
            new = float(ori.replace('k', '').replace('K', '').replace(",", "")) * 1000
        elif 'm' in ori or 'M' in ori:
            new = float(ori.replace(',', '').replace('m', '').replace('M', '')) * 1000000
        else:
            new = float(ori.replace(',', ''))
        return int(new)
    except:
        if 'LIKE' in ori or 'DISLIKE' in ori:
            return 'N/A'
        return ori


def get_subs_count(url):
    if url in sub_count_dict:
        return sub_count_dict[url]
    name = 'N/A'
    try:
        html = get_request_html(url, cookie)
        name = get_channel_name(html)
        reg = 'subscriberCountText":.*?simpleText":"(.*?) '
        res = parse_number(re.compile(reg).findall(html)[0])
    except Exception as e:
        res = 'N/A', name
    sub_count_dict[url] = [res, name]
    return res, name


def get_channel_name(html):
    reg = 'channelMetadataRenderer.*?title":"(.*?)"'
    data = re.compile(reg).findall(html)

    if data:
        return data[0]
    return 'N/A'


def read_excel(filename, start=1):
    global sheet1_data
    data = xlrd.open_workbook(filename, encoding_override="utf8")
    table = data.sheets()[0]
    print('process', '> '+filename,str(table.nrows))

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            stored_data = [row[j].value for j in range(9)]
            channel_url = stored_data[2]
            channel_detail = get_subs_count(channel_url)
            stored_data[1] = channel_detail[0]
            stored_data.append(channel_detail[1])

            raw_comment = stored_data[7]
            if raw_comment != 'N/A':
                raw_list = raw_comment.split('-----')
                stored_data[7] = get_comments(raw_list[0], raw_list[1], raw_list[1])

            if stored_data[6] == 'Like':
                stored_data[6] = 0
            if stored_data[5] == 'No':
                stored_data[5] = 0

            print(stored_data)
            sheet1_data.append(stored_data)
        except Exception as e:
            print(str(e))
            if 'Expecting value' in str(e):
                break


# for item in urls:
#     if 'search_query' in item[1]:
#         request_search_result(item[0], item[1] + '&sp=CAISAhAB')
#     else:
#         request_search_result(item[0], item[1] + '/videos?view=0&sort=dd&flow=grid')
#
# write_excel('rawdata.xls', sheet1_data)
#
#
read_excel('data/rawdata.xls', start=0)
write_excel('data.xls', sheet1_data)
