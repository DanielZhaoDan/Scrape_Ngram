# coding: utf-8
import sys, urllib
import urllib2
import re
import HTMLParser
import xlwt, xlrd
import os
import time

out_f = open("out.txt", 'w+')

stop = False

FB_ACCOUNT = ['mymicro@live.com'][0]
all_data = [['Also Like Url', 'No. likes', 'No. followers']]
driver = None
cookie = 'sb=4vPuWu4_DWNmHEBouS4jeeAI; datr=6vPuWmi5IYVhJZtr0yzaQ4Jl; js_ver=3130; dpr=2; locale=en_GB; ; c_user=100006957738125; xs=15%3AV4OG6OHVXc5A5Q%3A2%3A1533303142%3A20772%3A8703; fr=0NT9QsWhwBGUSDrtW.AWXZU8hiJ11Cq2_lr3GgWjlc5PM.BazwYT.Bv.AAA.0.0.BbZFlm.AWXK_LSG; pl=n; spin=r.4172604_b.trunk_t.1533303143_s.1_v.2_; wd=1233x386; act=1533303332078%2F0; presence=EDvF3EtimeF1533305363EuserFA21B06957738125A2EstateFDutF1533305363147CC'

url_data_dict = set()
ERROR_COUNT = 0


def get_ori_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    page.close()
    return html


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_request_of_url(url):
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
    req.add_header("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    res = HTMLParser.HTMLParser().unescape(res).decode('unicode-escape').replace('\\', '')
    return res


def get_request(url):
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res


def scrape_like_follow_of_url(idx, url):
    global url_data_dict
    if '/pages/' in url:
        return
    if url not in url_data_dict:
        html = get_request_of_url(url)
        reg = 'class="_4bl9">(.*?)people like this.*?class="_4bl9".*?>(.*?)people'
        data = re.compile(reg).findall(html)
        one_row = [url, remove_html_tag(data[0][0].split('Page')[1]), remove_html_tag(data[0][1])]
        url_data_dict.add(url)
        all_data.append(one_row)
        print idx, one_row[:50]
        print >> out_f, one_row[:50]


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
    global all_data, cookie, ERROR_COUNT
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    print 'total size: ', table.nrows

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            profile_url = row[0].value
            scrape_like_follow_of_url(i, profile_url)
            # if (i+1) % 5000 == 0:
            #     write_excel('like_follower_%d.xls' % i, all_data)
            #     del all_data
            #     all_data = []
            ERROR_COUNT = 0
        except Exception as e:
            print(i, e[:20])
            if 'list index out of range' in e:
                ERROR_COUNT += 1
                if ERROR_COUNT >= 3:
                    ERROR_COUNT = 0
                    cookie = get_new_cookie()


def get_new_cookie():
    cookie = raw_input('Please input new cookie:')
    return cookie


def pre_load(filename):
    global all_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(1, table.nrows):
        row = table.row(i)
        url = row[0].value
        url_data_dict.add(url)

    print 'pre load size: ', len(url_data_dict)

#
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    pre_load('data/like_follower_pre.xlsx')
    # init_browser()
    read_excel('data/also_likes.xlsx', start=0)
    write_excel('like_follower.xls', all_data)
