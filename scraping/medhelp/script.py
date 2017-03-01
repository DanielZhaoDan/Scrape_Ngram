# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd

sheet1_data = [['Topic', 'Topic URL', 'Question', 'No. Answers', 'No. Comments', 'Post Date']]
sheet2_data = [['Topic', 'Topic URL', 'Reply Date', 'Reply Content']]

url_base = 'http://www.medhelp.org/forums/Asthma/show/176?page=%d'

cookie = '_csrf_token=A3fyiG2omFMirX%2B6CjmexPEfnUd99%2Bz5MSaKw85QTYo%3D; is_member=92268e42f29c883d94f9f58a804e5a24b03918d1; _session_id=2b6981afa1b16490c15d73b9b9f2266d; __utmt=1; __utma=152361144.315543736.1487820506.1487820506.1487820506.1; __utmb=152361144.19.10.1487820506; __utmc=152361144; __utmz=152361144.1487820506.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=152361144.|5=metric_guid=fcd7937b-d430-444c-8c02-8587a819e1f7=1'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


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
                    print '===Write excel ERROR==='+str(one_row[col])
    w.save(filename)
    print filename+"===========over============"


def request_sheet1(url):
    global sheet1_data
    html = get_request(url)
    topic_detail_reg = 'subject_summary.*?href="(.*?)">(.*?)<.*?subj_info os_14(.*?)</div'
    topic_detail = re.compile(topic_detail_reg).findall(html)
    for detail in topic_detail:
        topic_url = 'http://www.medhelp.org/' + detail[0]
        topic = remove_html_tag(detail[1])
        answers, comments, date = get_date(detail[2])

        questions = request_sheet2(topic, topic_url)

        one_row = [topic, topic_url, questions, answers, comments, date]
        sheet1_data.append(one_row)


def request_sheet2(topic, url):
    global sheet2_data
    reg = 'post_message_container.*?post_message fonts_resizable os_14.*?>(.*?)<.*?subj_info os_14(.*?)</div'
    question = None
    if url:
        html = get_request(url)
        reply_lists = re.compile(reg).findall(html)
        for reply in reply_lists:
            content = remove_html_tag(reply[0])
            anw, com, date = get_date(reply[1])
            if not question:
                question = content
            else:
                one_row = [topic, url, content, date]
                sheet2_data.append(one_row)
    return question


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_date(ori):
    if 'answers</span' in ori or 'answer</span' in ori:
        reg = r'<span>(.*?) answer.*?'
        answer = re.compile(reg).findall(ori)[0]
    else:
        answer = 0
    if 'comment</span' in ori or 'comment</span' in ori:
        if 'answers</span' in ori or 'answer</span' in ori:
            reg = 'answer.*?<span>(.*?) comment.*?'
        else:
            reg = '<span>(.*?) comment.*?'
        comment = re.compile(reg).findall(ori)[0]
    else:
        comment = 0
    reg = 'data-timestamp=\'(.*?)\'>'
    data = re.compile(reg).findall(ori)[0]
    d = datetime.fromtimestamp(int(data))
    date = d.strftime('%d/%m/%Y')
    return int(answer), int(comment), date


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", get_url)
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')
size = 135
for i in range(1, size):
    print '-----Level 1 Page ' + str(i) + '-----'
    url = url_base % i
    request_sheet1(url)
write_excel('data/sheet1.xls', sheet1_data)
write_excel('data/sheet2.xls', sheet2_data)