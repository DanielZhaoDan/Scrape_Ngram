# -*- coding: utf-8 -*-

import time
import re
import urllib2
import xlwt
import sys
import HTMLParser
import gc

alldata = [['link','title','No. of review','Hardware List']]
cookie = 'npic=86Ziis71UF5OoAByOqjBsZnu9xDawFDZ/k2PkFDPDYFCq+y6xPV1xNwas7GZTQD9CA==; NNB=3MDNY6SQWSSFO; page_uid=SIgs3spl8T0ssu/F5cVssssssul-428974'

def write(html,filename):
    fp = open(filename,"w")
    fp.write(html)
    fp.close()
    print "write over"

def write_excel(filename):
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    ##column name.*?<td>(.*?)<
    for row in range(0,len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            ws.write(row,col,one_row[col])
    w.save(filename)
    print filename+"===========over============"

def request_html(url):
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    req.add_header('Referer', 'http://steamcommunity.com/discussions/forum/1/?fp=2')
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t','').replace('\r','').replace('\n','')
    return res

def get_url_list(url):
    html = request_html(url)
    reg = r'yt-uix-scroller-scroll-unit.*?a href="(.*?)".*?yt-ui-ellipsis yt-ui-ellipsis-2.*?>(.*?)<'
    return re.compile(reg).findall(html)

def parse_html(urls):
    global alldata

    for url_name in urls:
        link = 'https://www.youtube.com' + url_name[0].strip()
        title = url_name[1].strip()
        html = request_html(link)
        reg = r'watch-view-count">(.*?)view.*?eow-description(.*?)</p'
        view_hardware = re.compile(reg).findall(html)[0]
        view_count = view_hardware[0].strip().replace(',', '')
        hardware = remove_html_tag(view_hardware[1])

        one_row = [link, title, view_count, hardware]
        alldata.append(one_row)

def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))

reload(sys)
sys.setdefaultencoding('utf-8')

url_template = 'https://www.youtube.com/watch?v=36WE_78qB7A&index=68&list=PLTW2MN17j-L12h8Jq5fGGt8VV1ISZT-De'
url_list = get_url_list(url_template)
parse_html(url_list)
write_excel('setup.xls')

