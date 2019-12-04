# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import sys
from datetime import datetime
import HTMLParser
import os
from urlparse import urlparse
import time
import random
import xlsxwriter
import csv

sheet1_data = [['ID', 'Title', 'title url', 'Category', 'Date', 'No. Replies', 'No. Views', 'Content', 'Main Comment', 'Sub Comment']]

url_bases = 'https://cafe.naver.com/ArticleSearchList.nhn?search.clubid=10094499&search.media=0&search.searchdate=all&userDisplay=50&search.option=0&search.sortBy=date&search.searchBy=0&search.query=%B9%E8%BA%AF+%C8%C6%B7%C3&search.viewtype=title&search.page='

cookie = 'ncvid=#vid#_85.203.47.8xsv6; NNB=N543UILXD6IF2; nci4=efd13b15014d2190c92760777a91f398237f986a2079db40a64a7989160520ef5eb21ec01d382a0e971a2ab5d57d1c94451bdac7beda9bbe69c56d977170df1d7d73797a742a5a557c5b6858515c644775354649684f7c5a7c735676440a767e597d521c6e614067541b6569486f5c051e11311a2b6467636b7c787d7f080722053a7473187074482255482559472c; nid_inf=1347302832; NID_AUT=oHFE7H2emgjT7QaGafj5SKjRZi0gwMH8RRO9rfYSfk6dfLYJzQM3XUVnCrvK9GEp; NID_SES=AAABhU2X27nEoqGla9vP3Xnsa1btLyfS8MP8gWzGxejb+QgQANIPBHe2oNAL46x5OnATYcVq25NMH2yp9CNjQ8ylGtbRL8Fb7VbItkW5tkBtgiEyCVoAKLh2gM0+Ot8qQwHlYU4uYHe8IefXrTArrtTipKfWepgUi5eCp+aNWmkHXHYwnJA1DnUrNeYqqP0olUavxr2g6o3s12w9Gsv5/KYgZJg8RgJ/nh5tWcTtRci1kyrnMmtN58lltF1V8PbXWOSKJ7hnBX+uZ5Ut0f9brUqOsIZhGjQ+rwRzGc6VoCjjTWdgy8JoBdrRfITSlpaXldZHWW0zPkDW5PFXXvc+2oicSRoEmXtCvBk9nVUfKBiJjF9XpCuNfU8NgzJerIK7Uh5ChNYHgrhCmJ7uzUAIDrUK9k0rJgRF68/+aWqc/YHJq0KnVvPuB0QkYvNm5Z2Lu7rnI7FWOdWXhOa5c6DgqQ4FAQuEYyIqY+D8ryzZRhtVgDpZU4PezKqiGotRQMyaIMrraq3YhG7emA559AGGYNBpZRI=; NID_JKL=vUSOJSi1Oh9vkZSiSTLjwIKoCRu2bMrMyrlXGg2jIeE=; ncu=88b14c7378721caf8a1d72657ea81665cec01cfa70; ncmc4=87b9537d692549f8a14f081f12eb9dfe4802bc5f0b51c714ce2c21c7705d9877884f8c45a7bd1c7f78ea9f67ef49f402fbfbe0d625125b5456deeb; ncvc2=9aa35e616a600ebd98631c2616f78af55607e718501aff25de1e28f148a1; JSESSIONID=AD87C0DC868AEA840061F40522E8D9EB'

G_ID = 548
#29434212

def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='cp950')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col][:32766])
            except Exception as e:
                try:
                    ws.write(row, col, one_row[col])
                except Exception as er:
                    ws.write(row, col, 'N/A')
                    print('===Write excel ERROR===' + str(one_row[col]), e, er)
    w.save(filename)
    print(filename + "===========over============")


def request_sheet1(index, url, starter=0):
    global sheet1_data, G_ID

    print url
    html = get_request(url)

    topic_detail_reg = 'class="article" href="(.*?)".*?>(.*?)</a.*?p-nick.*?href.*?>(.*?)<.*?td_date">(.*?)<'
    topic_detail = re.compile(topic_detail_reg).findall(html)

    for detail in topic_detail:
        try:
            id = 'ID_%d' % G_ID
            url = 'https://cafe.naver.com' + detail[0]
            article = remove_html_tag(detail[1])
            category = remove_html_tag(detail[2])

            if '201' in detail[3]:
                date = detail[3].replace('.', '/')
            else:
                date = '2019/09/29'

            comment_list = request_sheet2(url)

            if not comment_list:
                one_row = [id, article, url, category, date, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
                sheet1_data.append(one_row)
            else:
                for comment in comment_list:
                    one_row = [id, article, url, category, date] + comment
                    sheet1_data.append(one_row)
            print [index, id, len(comment_list), url, article]
            G_ID += 1
        except Exception as e:
            print 'ERROR-- ' + url
            print e


def request_sheet2(topic_url):

    html = get_request(topic_url)

    article_id = get_article_id_from_url(topic_url)

    detail_reg = 'id="tbody".*?>(.*?)<table.*?role="presentation".*?class="reply".*?id="comment">.*? (.*?)<.*?b m-tcol-c reply.*?b m-tcol-c reply">(.*?)<'

    detail = re.compile(detail_reg).findall(html)

    content = remove_html_tag(detail[0][0])
    no_reply = int(detail[0][1].replace(',',''))
    no_view = int(detail[0][2].replace(',',''))

    if no_reply == 0:
        return [[no_reply, no_view, content, 'N/A', 'N/A']]

    comment_url = 'https://cafe.naver.com/CommentView.nhn?search.clubid=29434212&search.articleid=%s&search.lastpageview=true&lcs=Y' % article_id

    comment_json = get_json(comment_url)

    id_content = {}
    refid_content = {}

    main_id = set()

    comment_list = comment_json['result'].get('list', [])
    for comment in comment_list:
        commentid = comment['commentid']
        ref_commentid = comment['refcommentid']
        comment_text = remove_html_tag(comment['content'])
        id_content[commentid] = comment_text
        if commentid == ref_commentid:
            main_id.add(commentid)
        else:
            if not refid_content.get(ref_commentid):
                refid_content[ref_commentid] = []
            refid_content[ref_commentid].append(commentid)

    res = []
    for k in main_id:
        main_comment = id_content[k]
        sub_ids = refid_content.get(k)
        if not sub_ids:
            one_row = [no_reply, no_view, content, main_comment, 'N/A']
            res.append(one_row)
        else:
            for sub_id in sub_ids:
                sub_comment = id_content[sub_id]
                one_row = [no_reply, no_view, content, main_comment, sub_comment]
                res.append(one_row)
    return res


def get_article_id_from_url(url):
    return url.split('articleid=')[-1].split('&')[0]


def remove_html_tag(ori):
    try:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', ori)
        return str(HTMLParser.HTMLParser().unescape(dd)).strip().replace('&nbsp;', '').decode('cp949')
    except Exception as e:
        try:
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', ori)
            return str(dd).strip().replace('&nbsp;', '').decode('cp949')
        except Exception as er:
            return ori


def get_last_date(ori):
    if 'Today' in ori:
        return '25/07/2017'
    elif 'Yesterday' in ori:
        ori = '24/07/2017'
    try:
        date = datetime.strptime(ori.split('-')[0].replace('th ', ' ').replace('rd ', ' ').replace('st ', ' ').replace('nd ', ' '), '%d %B %Y ')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_date(ori):
    try:
        date = datetime.strptime(ori, '%b %d %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
        'Host': 'cafe.naver.com',
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    time.sleep(1)
    return res


def get_json(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
        'Host': 'cafe.naver.com',
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.json()
    return res


def write_old_excel(filename, alldata):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    i = 0
    while len(alldata) > 65500:
        for row in range(0, 65500):
            one_row = alldata[row]
            for col in range(0, len(one_row)):
                try:
                    ws.write(row, col, one_row[col][:32766])
                except:
                    try:
                        ws.write(row, col, one_row[col])
                    except:
                        print '===Write excel ERROR==='+str(one_row[col])
        alldata = alldata[65500:]
        print len(alldata)
        new_filename = filename.replace('.xls', '_%d.xls'%i)
        w.save(new_filename)
        print new_filename + "===========over============"
        i += 1
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col][:32766])
            except:
                try:
                    ws.write(row, col, one_row[col])
                except:
                    print '===Write excel ERROR==='+str(one_row[col])
    w.save(filename)
    print filename+"===========over============"


reload(sys)
sys.setdefaultencoding('utf-8')


# for i in range(11, 31):
#     url = url_bases + str(i)
#
#     try:
#
#         request_sheet1(i, url, starter=0)
#
#         if i % 10 == 0:
#             write_excel('data/sheet1_%d.xls' % i, sheet1_data)
#             del sheet1_data
#             sheet1_data = [['ID', 'Title', 'Category', 'Date', 'No. Replies', 'No. Views', 'Content', 'Main Comment', 'Replies']]
#     except Exception as e:
#         print e
#
# write_excel('data/sheet1.xls', sheet1_data)

url_bases = 'https://cafe.naver.com/ArticleSearchList.nhn?search.clubid=29434212&search.media=0&search.searchdate=all&userDisplay=50&search.option=0&search.sortBy=date&search.searchBy=0&search.query=%B9%E8%BA%AF+%C8%C6%B7%C3&search.viewtype=title&search.page='
del sheet1_data
sheet1_data = [['ID', 'Title', 'title url', 'Category', 'Date', 'No. Replies', 'No. Views', 'Content', 'Main Comment', 'Sub Comment']]
G_ID = 1

for i in range(1, 31):
    url = url_bases + str(i)

    try:
        request_sheet1(i, url, starter=0)

        if i % 10 == 0:
            write_excel('data/sheet2_%d.xls' % i, sheet1_data)
            del sheet1_data
            sheet1_data = [
                ['ID', 'Title', 'Category', 'Date', 'No. Replies', 'No. Views', 'Content', 'Main Comment', 'Replies']]
    except Exception as e:
        print e

write_excel('data/sheet2.xls', sheet1_data)