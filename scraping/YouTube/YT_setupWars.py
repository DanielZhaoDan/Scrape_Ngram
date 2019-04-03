# -*- coding: utf-8 -*-

import re
import xlwt, xlrd
from datetime import datetime
import os
import requests
import HTMLParser
import time


sheet0_data = [['Id', 'Name', 'URL', 'No. Subscriber', 'Video Title', 'Verified Channel Name', 'Video URL', 'No. Views', 'No. Likes', 'No. DisLikes', 'Main Text', 'Date', 'Category', 'No. of Comments', 'PlayList N/Y']]
sheet1_data = [['Id', 'Video URL', 'No. comments', 'Comment Date', 'Comment Text', 'No likes', 'No dislikes', 'No. replies']]

# P_ID = 30
P_ID = 1
COUNT = 0

MAX_COUNT = 500

comment_base_url = 'https://www.youtube.com/comment_service_ajax?action_get_comments=1&pbj=1&ctoken=%s&continuation=%s&itct=%s'

cookie = 'SID=oQY33Rlhx85J4af4B2n72NOPr2pNAbvfPICmny5miXNDXRVxNM4DTHHjxNBkJfTVjohQGg.; HSID=Ao3DV1zpAU0S0edwr; SSID=ANLBPWBojaVvVWNCa; APISID=RVOf0003eCk60c8A/Aguwcd_oSWKjIfYVh; SAPISID=MUoaHPbzZY5IAWLF/AnunP-RaP6Oa2A_wm; VISITOR_INFO1_LIVE=_mc71dTLYXI; LOGIN_INFO=AFmmF2swRAIgd1yNnqGVzV6P7XCNcy7z0E1dxg-QS8z3JwSxn1toLwECIEzJGcG8C0lODRl3LS7vyv9MAbjn9DeAjtaA697DCFAq:QUQ3MjNmd2tfb0V2Z2RtX2ZybnVnSHU3NU1pcXBoWWNVR2l6WF9ERHlLa0h3Y2J1enJma0RBcFl3UXVqRUc2S1VWTm9YTkxISEo5MHlCaEdJMWFvQzV6Mk9zTFFJdkF5UE1OV1NzZV9zY1kyMEVTMXZQT0dFLWYtcXM1bmp3eEFwWkVlbUtMZXFfLWxCV0V3N2FYNU9vdnV2WDNzMjlzc29ZMUduNUFoQkIwWC1LbGw5ZnRDWmI4; YSC=sxFcJmHwTOM; PREF=al=en-SG&cvdm=grid&f1=50000000&f4=4000000'

url_list = [
    ['Priya Malik', 'https://www.youtube.com/playlist?list=PLJsYaS5DbkuJv5v8gWlK2htFo4UCSW4iN', 'IND_%d'],
    ['Priya Malik', 'https://www.youtube.com/playlist?list=PLJsYaS5DbkuKVCuy5jdxs7TBx3JB5e16P&pbjreload=10', 'IND_%d'],
    ['Indian Girl Channel Trisha', 'https://www.youtube.com/playlist?list=PL6nP02mJL70YQXMFNiSuKNxq6lNLrPuDg',
     'IND_%d'],
    ['Super Style Tips', 'https://www.youtube.com/playlist?list=PLYcdnf-0W2J9FmMMsAk1CK259hpupkq_l', 'IND_%d'],
    ['Super Style Tips', 'https://www.youtube.com/playlist?list=PLYcdnf-0W2J8exhO8XVar2l3eJPaOwSRc', 'IND_%d'],
    ['Beauty Mantra', 'https://www.youtube.com/playlist?list=PLHG4DIQ2XVLEc3figCArDF6YbiFN0Jmpj', 'IND_%d'],
    ['Beauty Mantra', 'https://www.youtube.com/playlist?list=PLHG4DIQ2XVLEx3WZuKX_rBSda0wqYvoGp', 'IND_%d'],
    ['Beauty Mantra', 'https://www.youtube.com/playlist?list=PLHG4DIQ2XVLHGOiCs4y2aTlQdXMGhu8nd', 'IND_%d'],
    ['SimpleTips Anwesha', 'https://www.youtube.com/playlist?list=PLDL1ZQUOfhmnjuibvOh0vpC0LyruZHfso', 'IND_%d'],
    ['Asian Beauty Sarmistha', 'https://www.youtube.com/playlist?list=PLk2nCpMRwjywRuUwXTPGfBQkkq42XaeJq', 'IND_%d'],
    ['Asian Beauty Sarmistha', 'https://www.youtube.com/playlist?list=PLk2nCpMRwjywe2VB3weJLjR_3F6QYBV9A', 'IND_%d'],
    ['Asian Beauty Sarmistha', 'https://www.youtube.com/playlist?list=PLk2nCpMRwjyzwKmdFcc0oKiv779l9cL5K', 'IND_%d'],
    ['Aafreen beauty', 'https://www.youtube.com/playlist?list=PLqCGFIiShOpSsEvvVzH6wWTdoLJzK3IT2', 'IND_%d'],
    ['Royal Style', 'https://www.youtube.com/playlist?list=PLK5LuGYvN--xMWN2aVdD2N4LOVQKDf9tx', 'IND_%d'],
    ['Aarushi Jain', 'https://www.youtube.com/playlist?list=PLR-PjFPEz0FtHEHyjo-SUChZiLoMRapUV', 'IND_%d'],
    ['Aarushi Jain', 'https://www.youtube.com/playlist?list=PLR-PjFPEz0FudjoUkMb6kDIsBVup-gBpH', 'IND_%d'],
    ['Aarushi Jain', 'https://www.youtube.com/playlist?list=PLR-PjFPEz0FtlqarIYf_P3io4TjccF-_c', 'IND_%d'],
    ['Aarushi Jain', 'https://www.youtube.com/playlist?list=PLR-PjFPEz0FsaEdSefLcrejUj5DuZwyZd', 'IND_%d'],
    ['Indian Beauty Solutions', 'https://www.youtube.com/channel/UCgmp2st6zPBDfDKXfOIaZZQ/videos', 'IND_%d'],
    ['Shweta Makeup & Beauty', 'https://www.youtube.com/playlist?list=PLuLUiwTLareI-s5eJZOZEkD2xq7Dnr83y', 'IND_%d'],
    ['Shweta Makeup & Beauty', 'https://www.youtube.com/playlist?list=PLuLUiwTLareJIeEpnTUAUVi9WSTC3Fhlj', 'IND_%d'],
    ['Shweta Makeup & Beauty', 'https://www.youtube.com/playlist?list=PLuLUiwTLareJ2tjs5HJmxKHIbLwgkIQYK', 'IND_%d'],
    ['Shweta Makeup & Beauty', 'https://www.youtube.com/playlist?list=PLuLUiwTLareIp7lzZcuHxRn3TlY9FvFMT', 'IND_%d'],
    ['Shweta Makeup & Beauty', 'https://www.youtube.com/playlist?list=PLuLUiwTLareIyI90XBCZwJ1QKHqUlQE3P', 'IND_%d'],
    ['Look Gorgeous', 'https://www.youtube.com/playlist?list=PLR5b2Z8QH0a8RX7koufZ-0Xvfd1hN6zX_', 'IND_%d'],
    ['Mehar Beauty', 'https://www.youtube.com/playlist?list=PLBkrPx8fagw73VsInEZJvTO6weSOOJUiP', 'IND_%d'],
    ['AFSHA AARZU', 'https://www.youtube.com/playlist?list=PLciqP_taz13mXKaJp9QBOrDKaHUHCr6vG', 'IND_%d'],
    ['AFSHA AARZU', 'https://www.youtube.com/playlist?list=PLciqP_taz13niqMW8jqlOPX5TfXVNMxZ3', 'IND_%d'],
    ['AFSHA AARZU', 'https://www.youtube.com/playlist?list=PLciqP_taz13mORym6u6qa6G4SE0z-pYwQ', 'IND_%d'],
    ['AFSHA AARZU', 'https://www.youtube.com/playlist?list=PLciqP_taz13lLQ_BMulq3kTqB_iNp1Fce', 'IND_%d'],
    ['Beauty Infinite [Payel Deshmukh]', 'https://www.youtube.com/playlist?list=PLxXKanMTHfoPgjY-lDIHjdNZZdmGFzm3r',
     'IND_%d'],
    ['Beauty Infinite [Payel Deshmukh]', 'https://www.youtube.com/playlist?list=PLxXKanMTHfoPpUflCvS55AHl0WYZlPfjs',
     'IND_%d'],
    ['Beauty Infinite [Payel Deshmukh]', 'https://www.youtube.com/playlist?list=PLxXKanMTHfoORfHlb9GmVwoVicdpnIBFI',
     'IND_%d'],
    ['Beauty Infinite [Payel Deshmukh]', 'https://www.youtube.com/playlist?list=PLxXKanMTHfoNgqxUB0AQ6fFHFvmOPOmx1',
     'IND_%d'],
    ['Beauty Infinite [Payel Deshmukh]', 'https://www.youtube.com/playlist?list=PLxXKanMTHfoM3RWOjG_9IiFmNJmvcRNUQ',
     'IND_%d'],
    ['Beauty Infinite [Payel Deshmukh]', 'https://www.youtube.com/playlist?list=PLxXKanMTHfoPoAQcSwjaHDKTOGZ8uiSFP',
     'IND_%d'],
    ['Beauty Infinite [Payel Deshmukh]', 'https://www.youtube.com/playlist?list=PLxXKanMTHfoNqC6hgeTtE0xQcRSKUhWMV',
     'IND_%d'],
    ['Beauty Infinite [Payel Deshmukh]', 'https://www.youtube.com/playlist?list=PLxXKanMTHfoOvIvd1E7yp96mGx_icEyB-',
     'IND_%d'],
    ['Anubha Makeup and Beauty', 'https://www.youtube.com/playlist?list=PLbWNslN24tVCeOLp6tuq_CfO0v1Zakilf', 'IND_%d'],
    ['Anubha Makeup and Beauty', 'https://www.youtube.com/playlist?list=PLbWNslN24tVBmFgrzG-pbBnxG4Bc46-WP', 'IND_%d'],
    ['Anubha Makeup and Beauty', 'https://www.youtube.com/playlist?list=PLbWNslN24tVCx8OWpgrxHMF1VfhSZPjV9', 'IND_%d'],
    ['Anubha Makeup and Beauty', 'https://www.youtube.com/playlist?list=PLbWNslN24tVBgxgKMm8cas5uC9au1lsWx', 'IND_%d'],
    ['Anubha Makeup and Beauty', 'https://www.youtube.com/playlist?list=PLbWNslN24tVBRY6c1OUpnB7qaTUq-i9Rr', 'IND_%d'],
    ['Anubha Makeup and Beauty', 'https://www.youtube.com/playlist?list=PLbWNslN24tVDeFCz1zjH4UOaA1LHO0E1d', 'IND_%d'],
    ['Blossom Yourself', 'https://www.youtube.com/playlist?list=PL6YVYc-ECXOJvwSbiINOIkyFJx0xqom4-', 'IND_%d'],
    ['Blossom Yourself', 'https://www.youtube.com/playlist?list=PL6YVYc-ECXOLpqMv1yL7BtOB1Rst6mBJO', 'IND_%d'],
    ['Blossom Yourself', 'https://www.youtube.com/playlist?list=PL6YVYc-ECXOIQNuHjHUL7iDKgX9O58H5s', 'IND_%d'],
    ['Fashionista Eshani', 'https://www.youtube.com/playlist?list=PLgkrUPR1Gdd8t_-sjF602uf4Qwhg1bjsP', 'IND_%d'],
]


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_'+str(flag)+'.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col][:32766])
            except:
                try:
                    ws.write(row, col, one_row[col])
                except:
                    print('===Write excel ERROR==='+str(one_row[col]))
    w.save(filename)
    print(filename+"===========over============")


def get_scriber(html):
    reg = 'nextContinuationData.*?continuation":"(.*?)".*?clickTrackingParams":"(.*?)".*?subscriberCountText".*?simpleText":"(.*?)"'
    data = re.compile(reg).findall(html)
    if data:
        return data[0][2].replace(' subscribers', ''), data[0][1], data[0][0]
    reg = 'subscriberCountText".*?simpleText":"(.*?)"'
    data = re.compile(reg).findall(html)
    if data:
        return data[0].replace(' subscribers', ''), None, None
    return 'N/A', None, None


def request_sheet0_playlist(topic_name, url, prefix):
    global sheet0_data, sheet1_data, P_ID, COUNT
    html = get_request(url)
    no_scriber, track_cid, ctoken = get_scriber(html)

    print url
    main_reg = '"title":.*?label":"(.*?)".*?simpleText":"(.*?)".*?videoId":"(.*?)"'
    main_list = re.compile(main_reg).findall(html)
    for data in main_list:
        v_id = prefix % P_ID
        video_url = 'https://www.youtube.com/watch?v=' + data[2]
        try:
            video_title = data[1]
            no_view = parse_no_view(data[0])
            detail = get_video_detail(v_id, video_url)

            if detail:
                one_row = [v_id, topic_name.lower(), url, no_scriber, video_title, topic_name.lower(), video_url, no_view, detail[0],
                           detail[1], detail[3], detail[2], detail[4], detail[6], 'Y' if 'playlist' in url else 'N']
                sheet0_data.append(one_row)
                print [v_id, url, no_scriber, video_url, no_view]
                P_ID += 1
                COUNT += 1
        except:
            print 'EXPT--', video_url


def parse_no_view(ori):
    return ori.replace('views', '').replace('view', '').strip().split(' ')[-1]


def request_sheet0(topic_name, url, prefix):
    global sheet0_data, sheet1_data, P_ID, COUNT
    html = get_request(url)
    no_scriber, track_cid, ctoken = get_scriber(html)

    print url
    main_reg = 'gridVideoRenderer.*?videoId":"(.*?)".*?simpleText":"(.*?)"}.*?simpleText":"(.*?)".*?simpleText":"(.*?) '
    main_list = re.compile(main_reg).findall(html)
    for data in main_list:
        v_id = prefix % P_ID
        video_url = 'https://www.youtube.com/watch?v=' + data[0]
        video_title = data[1]
        no_view = parse_number(data[3])
        detail = get_video_detail(v_id, video_url)

        if detail:
            one_row = [v_id, topic_name.lower(), url, no_scriber, video_title, topic_name.lower(), video_url, no_view,
                       detail[0], detail[1], detail[3], detail[2], detail[4], detail[6], 'Y' if 'playlist' in url else 'N']
            sheet0_data.append(one_row)
            print [v_id, url, no_scriber, video_url, no_view]
            P_ID += 1
            COUNT += 1

    scroll_sheet0(topic_name, url, prefix, track_cid, ctoken, no_scriber)


def scroll_sheet0(topic_name, url, prefix, track_cid, ctoken, no_scriber):
    global sheet0_data, sheet1_data, P_ID, COUNT

    if track_cid and ctoken and COUNT < MAX_COUNT:
        scroll_url = 'https://www.youtube.com/browse_ajax?ctoken=%s&continuation=%s&itct=%s' % (ctoken, ctoken, track_cid)
        print scroll_url
        try:
            json_obj = get_json_request(scroll_url)

            items = json_obj[1]['response']['continuationContents']['gridContinuation']['items']

            try:
                track_cid = json_obj[1]['response']['continuationContents']['gridContinuation']['continuations'][0]['nextContinuationData']['clickTrackingParams']
                ctoken = json_obj[1]['response']['continuationContents']['gridContinuation']['continuations'][0]['nextContinuationData']['continuation']
            except:
                track_cid, ctoken = None, None

            for item in items:
                v_id = prefix % P_ID
                video_title = item['gridVideoRenderer']['title']['simpleText']
                video_url = 'https://www.youtube.com/watch?v=' + item['gridVideoRenderer']['videoId']
                no_view = parse_number(item['gridVideoRenderer']['viewCountText']['simpleText'].split(' ')[0])
                detail = get_video_detail(v_id, video_url)

                if detail:
                    one_row = [v_id, topic_name.lower(), url, no_scriber, video_title, detail[5].lower(), video_url, no_view, detail[0],
                               detail[1], detail[3], detail[2], detail[4], detail[6], 'Y' if 'playlist' in url else 'N']
                    sheet0_data.append(one_row)
                    # print one_row
                    P_ID += 1
                    COUNT += 1
        except Exception as e:
            print 'EXP--sheet1', scroll_url, e


def get_video_detail(v_id, url):
    html = get_request(url)
    reg = 'author":"(.*?)".*?"iconType":"LIKE".*?simpleText":"(.*?)".*?"iconType":"DISLIKE".*?simpleText":"(.*?)".*?dateText".*?simpleText":"(.*?)"(.*?)subscribeButton.*?ategory.*?"text":"(.*?)",.*?nextContinuationData":.*?continuation":"(.*?)".*?clickTrackingParams":"(.*?)"'
    data_list = re.compile(reg).findall(html)
    for data in data_list:
        author = data[0]
        like_count = parse_number(data[1])
        dislike_count = parse_number(data[2])
        date = parse_date(data[3])
        main_text = get_main_text(data[4])
        category = remove_html_tag(data[5])
        comment_track = data[6]
        itct = data[7]

        if comment_track:
             comment_count = get_comments(v_id, url, comment_track, comment_track, itct)
        else:
            comment_count = 'N/A'

        return [like_count, dislike_count, date, main_text, category, author, parse_number(comment_count)]
    return None


def get_comments(v_id, v_url, ctoken, continuation, itct):
    global sheet1_data
    try:
        url = comment_base_url % (ctoken, continuation, itct)
        json_obj = post_json_request(url)
        return json_obj['response']['continuationContents']['itemSectionContinuation']['header']['commentsHeaderRenderer']['commentsCount']['simpleText']

    except Exception as e:
        print e
        return 'N/A'

def post_json_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
        'x-client-data': 'CIi2yQEIo7bJAQjBtskBCKmdygEIqKPKAQi/p8oBCOynygEI4qjKARj5pcoB',
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
        'session_token': 'QUFFLUhqbUJYNWVscWJaczNIX1g5dWlMNkxwb0dwVGpBUXxBQ3Jtc0ttQTNoVFVwNjZtSVVmOGRkM2lJTW5KTy1BS0Z3MUVUdVE4S1o0UWxfTjRkZ3BEcUpqYl93QWN2TmZoeTJIdlRaemhBOXZDbS1HYUVZazZJMVhvNkZIRGFTUDY0UHR2NlJYWEFSN2ttUFdlU1JBNEhzR05PYlhoRkgtT21iY1RTYWZhZHd3WjZweU1iTmZwTG9fV3FUY3BXUk85S2c=',
    }
    req = requests.post(get_url, headers=headers, data=data)
    return req.json()


def parse_date(ori):
    date_list = ori.split(' ')
    date_str = '-'.join(date_list[-3:])
    return get_date(date_str)


def get_main_text(ori):
    reg = '"text":"(.*?)"'
    text = re.compile(reg).findall(ori)
    text_1 = ' '.join(text)
    reg = '"simpleText":"(.*?)"'
    text = re.compile(reg).findall(ori)
    text_2 = ' '.join(text)
    return text_1 + ' ' + text_2


def request_sheet1(thread_url):
    global sheet1_data
    html = get_request(thread_url)
    reg = 'class="y8HYJ-y_lTUHkQIc1mdCq">(.*?)</span.*?(.*?)t4Hq30BDzTeJ85vREX7_M">.*?>(.*?) '

    data_list = re.compile(reg).findall(html)

    if data_list:
        content = remove_html_tag(data_list[0][0])
        if 's90z9tc-10 fHRkcP' in data_list[0][1]:
            reg = 's90z9tc-10 fHRkcP">(.*?)</div'
            text = re.compile(reg).findall(data_list[0][1])
            content += remove_html_tag(text[0])
        one_row = [thread_url, content, data_list[0][2]]
        sheet1_data.append(one_row)


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


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    try:
        return str(HTMLParser.HTMLParser().unescape(dd)).strip()
    except:
        return str(dd).strip()


def get_date(ori):
    try:
        d = datetime.strptime(ori, '%b-%d,-%Y')
        date = d.strftime('%d/%m/%Y')
    except:
        return ori
    return date


def get_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
    }
    req = requests.get(get_url, headers=headers, timeout=5)
    res = req.content
    res = str(res).replace('\t', '').replace('\r', '').replace('\n', '').replace('&amp;', '&').replace('\\t', '').replace('\\r', '').replace('\\n', '')
    return res


def get_json_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
        'x-client-data': 'CIi2yQEIo7bJAQjBtskBCKmdygEIqKPKAQi/p8oBCOynygEI4qjKARj5pcoB',
        'x-spf-previous': 'https://www.youtube.com/channel/UCscRTJnqjvJhuHJBPiB2WIQ/videos',
        'x-spf-referer': 'https://www.youtube.com/channel/UCscRTJnqjvJhuHJBPiB2WIQ/videos',
        'x-youtube-client-name': '1',
        'x-youtube-client-version': '2.20181215',
        'x-youtube-identity-token': 'QUFFLUhqbFZBUnVVUEt5OHpPZlRxbWlZZ2JhZzNKMm94UXw=',
        'x-youtube-page-cl': '231012098',
        'x-youtube-page-label': 'youtube.ytfe.desktop_20181214_4_RC2',
        'x-youtube-utc-offset': '480',
        'x-youtube-variants-checksum': 'c2d5573fe68dc8fe9b8a37e11ee57de9',
        'referer': 'https://www.youtube.com/channel/UCscRTJnqjvJhuHJBPiB2WIQ/videos',
    }
    req = requests.get(get_url, headers=headers, timeout=5)
    return req.json()


def get_view_count(url):
    html = get_request(url)
    reg = '{"viewCount":\{"simpleText":"(.*?) views"}'
    try:
        data = re.compile(reg).findall(html)
        return parse_number(data[0])
    except:
        return 0


def read_excel(filename, start=1):
    global sheet1_data
    print('process -> '+filename)
    try:
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]

        for i in range(start, table.nrows):
            row = table.row(i)
            try:
                one_row = [row[j].value for j in range(0, table.ncols)]
                if row[9].value == '':
                    video_url = row[5].value
                    video_title = get_video_detail(row[0].value, video_url)[3]
                    one_row[9] = video_title
                    print one_row
                sheet0_data.append(one_row)

            except:
                print(i)
    except Exception as e:
        print 'EXP--'+filename, e


# request_sheet0_playlist('', 'https://www.youtube.com/playlist?list=PLtJeRYWXJivlPKl4uJljBqP7PK2CFZfnj', '')


for i in range(len(url_list)):
    name_url = url_list[i]
    try:
        name = name_url[0]
        url = name_url[1]
        COUNT = 0

        if 'playlist' not in url:
            if not url.endswith('videos'):
                url = url + '/videos'
            request_sheet0(name, url, name_url[2])
        else:
            request_sheet0_playlist(name, url, name_url[2])

        write_excel('data/%s_%d_main.xls' % (name, int(time.time())), sheet0_data)
        del sheet0_data
        del sheet1_data
        sheet0_data = [
            ['Id', 'Name', 'URL', 'No. Subscriber', 'Video Title', 'Verified Channel Name', 'Video URL', 'No. Views',
             'No. Likes', 'No. DisLikes', 'Main Text', 'Date', 'Category', 'No. of Comments']]
        sheet1_data = [
            ['Id', 'Video URL', 'No. comments', 'Comment Date', 'Comment Text', 'No likes', 'No dislikes', 'No. replies']]
    except Exception as e:
        print 'ERR-', name_url[1], e


