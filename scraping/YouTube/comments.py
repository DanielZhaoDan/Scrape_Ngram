# -*- coding: utf-8 -*-

import re
import xlwt, xlrd
from datetime import datetime
import os
import requests
import HTMLParser

files = []
cookie = 'SID=oQY33Rlhx85J4af4B2n72NOPr2pNAbvfPICmny5miXNDXRVxNM4DTHHjxNBkJfTVjohQGg.; HSID=Ao3DV1zpAU0S0edwr; SSID=ANLBPWBojaVvVWNCa; APISID=RVOf0003eCk60c8A/Aguwcd_oSWKjIfYVh; SAPISID=MUoaHPbzZY5IAWLF/AnunP-RaP6Oa2A_wm; YSC=TIHKEa72H8w; VISITOR_INFO1_LIVE=_mc71dTLYXI; LOGIN_INFO=AFmmF2swRAIgd1yNnqGVzV6P7XCNcy7z0E1dxg-QS8z3JwSxn1toLwECIEzJGcG8C0lODRl3LS7vyv9MAbjn9DeAjtaA697DCFAq:QUQ3MjNmd2tfb0V2Z2RtX2ZybnVnSHU3NU1pcXBoWWNVR2l6WF9ERHlLa0h3Y2J1enJma0RBcFl3UXVqRUc2S1VWTm9YTkxISEo5MHlCaEdJMWFvQzV6Mk9zTFFJdkF5UE1OV1NzZV9zY1kyMEVTMXZQT0dFLWYtcXM1bmp3eEFwWkVlbUtMZXFfLWxCV0V3N2FYNU9vdnV2WDNzMjlzc29ZMUduNUFoQkIwWC1LbGw5ZnRDWmI4; PREF=f1=50000000&al=en-SG&f4=4000000'
base_url = 'https://www.youtube.com/comment_service_ajax?action_get_comments=1&pbj=1&ctoken=%s&continuation=%s&itct=%s'
sheet1_data = [['Id', 'Video URL', 'No. comments', 'Comment Date', 'Comment Text', 'No likes', 'No dislikes', 'No. replies']]
MAX_COUNT = 250


def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path or 'txt' in path:
            if 'result' not in path:
                files.append(path.split('/')[-1].split('_')[0])
        if os.path.isdir(path):
            walk(path)
    return files


def write_excel(filename, alldata, flag=None):
    filename = 'data/' + filename
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)

    i = 0
    while len(alldata) > 65500:
        _filename = filename.replace('.xls', '_%s.xls' % i)
        start_index = 0
        end_index = 65500
        data = alldata[start_index:end_index]
        alldata = alldata[end_index:]
        w = xlwt.Workbook(encoding='utf-8')
        ws = w.add_sheet('old', cell_overwrite_ok=True)
        for row in range(0, len(data)):
            one_row = data[row]
            for col in range(0, len(one_row)):
                try:
                    ws.write(row, col, one_row[col][:32766])
                except:
                    try:
                        ws.write(row, col, one_row[col])
                    except:
                        print('===Write excel ERROR===' + str(one_row[col]))
        w.save(_filename)
        print("%s===========over============%d" % (_filename, len(data)))
        i += 1
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
                    print('===Write excel ERROR===' + str(one_row[col]))
    w.save(filename)
    print("%s===========over============%d" % (filename, len(alldata)))


def read_excel(filename, start=1):
    global sheet1_data
    print('process -> '+filename)
    try:
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]

        for i in range(start, table.nrows):
            if i <= 46000:
                continue
            row = table.row(i)
            try:
                id = row[0].value
                video_url = row[5].value
                total_count = request_comments(id, video_url)
                print id, video_url, total_count
            except:
                print(i)
            if i % 500 == 0:
                write_excel('ID_comment%d.xls' % i, sheet1_data)
                sheet1_data = []
    except Exception as e:
        print 'EXP--'+filename, e


def post_json_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
        'x-client-data': 'CIi2yQEIo7bJAQjBtskBCKmdygEIu53KAQioo8oBCL+nygEIz6fKAQjiqMoBGPmlygE=',
        'x-spf-previous': 'https://www.youtube.com/channel/UCscRTJnqjvJhuHJBPiB2WIQ/videos',
        'x-spf-referer': 'https://www.youtube.com/channel/UCscRTJnqjvJhuHJBPiB2WIQ/videos',
        'content-type': 'application/x-www-form-urlencoded',
        'x-youtube-client-name': '1',
        'x-youtube-client-version': '2.20181220',
        'x-youtube-identity-token': 'QUFFLUhqbFZBUnVVUEt5OHpPZlRxbWlZZ2JhZzNKMm94UXw=',
        'x-youtube-page-cl': '226370883',
        'x-youtube-page-label': 'youtube.ytfe.desktop_20181219_4_RC2',
        'x-youtube-utc-offset': '480',
        'x-youtube-variants-checksum': '19458f0ba28c6857cc7c11f992c8a25c',
        'referer': 'https://www.youtube.com/channel/UCscRTJnqjvJhuHJBPiB2WIQ/videos',
    }
    data = {
        'session_token': 'QUFFLUhqbjg2VzVrMjZtcHNSeEhKMWFTLUV2d1NqeG9mZ3xBQ3Jtc0ttdWYyOXl3MTRUcXQxemV4WjlLM3R6amN4Tm4tYllnSkpORDhhdUVwZ2wtWFpzX1RFSWJiWnBWWndOOEN0OXBlcF92ZlhBalJrMmdyNFpiaUxJX3EtamZMUG9odkVFVVFiMXNRaGdQaTBKcVFZcXYyb0gxajBXUkluNFRoR2MwUDhTYXBNbG9YYWtmVWVjSjZSdWl2SHNjcWlsLVE=',
    }
    req = requests.post(get_url, headers=headers, data=data)
    return req.json()


def get_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
    }
    req = requests.get(get_url, headers=headers)
    res = req.content
    res = str(res).replace('\t', '').replace('\r', '').replace('\n', '').replace('&amp;', '&').replace('\\t', '').replace('\\r', '').replace('\\n', '')
    return res


def get_video_detail(url):
    html = get_request(url)
    reg = 'itemSectionRenderer.*?nextContinuationData":.*?continuation":"(.*?)".*?clickTrackingParams":"(.*?)"'
    data_list = re.compile(reg).findall(html)
    if not data_list:
        return None, None
    data = data_list[0]
    comment_track = data[0]
    itct = data[1]
    return comment_track, itct


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


def request_comments(video_id, video_url):
    global sheet1_data
    total_count = 0
    comment_tract, itct = get_video_detail(video_url)
    comment_count = None

    while comment_tract and itct and total_count < MAX_COUNT:
        url = base_url % (comment_tract, comment_tract, itct)
        try:
            json_resp = post_json_request(url)
            if not json_resp['response'].get('continuationContents'):
                break
            itemSectionContinuation = json_resp['response']['continuationContents']['itemSectionContinuation']
            comment_tract, itct = get_comment_tract(itemSectionContinuation)

            if not comment_count:
                comment_count = get_comment_count(itemSectionContinuation)

            if comment_count == 0:
                break

            comment_content = itemSectionContinuation['contents']

            for comment_item in comment_content:
                try:
                    # 'Comment Date', 'Comment Text', 'No likes', 'No dislikes', 'No. replies'
                    comment_obj = comment_item['commentThreadRenderer']['comment']
                    comment_text = get_comment_text(comment_obj)
                    comment_date = comment_obj['commentRenderer']['publishedTimeText']['runs'][0]['text']
                    no_like = comment_obj['commentRenderer']['likeCount']
                    no_dislike = 'N/A'
                    no_replies = get_reply_count(comment_item['commentThreadRenderer'])
                    one_row = [video_id, video_url, comment_count, comment_date, comment_text, no_like, no_dislike, no_replies]
                    sheet1_data.append(one_row)
                    # print one_row
                except Exception as e:
                    print 'EXP_C--', e
            total_count += len(comment_content)
        except Exception as e:
            print 'EXP_V--', video_url, e
    return total_count


def get_comment_tract(itemSectionContinuation):
    try:
        nextContinuationData = itemSectionContinuation['continuations'][0]['nextContinuationData']
        comment_tract = nextContinuationData['continuation']
        itct = nextContinuationData['clickTrackingParams']
        return comment_tract, itct
    except:
        return None, None


def get_comment_text(obj):
    try:
        return obj['commentRenderer']['contentText']['simpleText'].replace('\n', '')
    except Exception:
        try:
            runs = obj['commentRenderer']['contentText']['runs']
            text = ''.join([run['text'] for run in runs])
            return text
        except:
            return ''


def get_comment_count(obj):
    try:
        return int(obj['header']['commentsHeaderRenderer']['countText']['simpleText'].split(' ')[0].replace(',', ''))
    except:
        try:
            return obj['header']['commentsHeaderRenderer']['countText']['simpleText']
        except:
            return 0


def get_reply_count(obj):
    try:
        res = obj['replies']['commentRepliesRenderer']['moreText']['simpleText']
        if res == 'View reply':
            return 1
        return int(res.split(' ')[1].replace(',', ''))
    except:
        try:
            return obj['replies']['commentRepliesRenderer']['moreText']['simpleText']
        except:
            return 0


read_excel('data/ID_Main.xlsx')
# request_comments('1', 'https://www.youtube.com/watch?v=IHNzOHi8sJs')
write_excel('ID_comment_last.xls', sheet1_data)



