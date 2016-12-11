# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd
import gc

sheet1_data = [['Keyword', 'Forum topic', 'Forum link', 'Sub-forum topic', 'Sub-forum link', 'Text']]
sheet2_data = [['Thread in forum', 'Thread', 'Url of Thread', 'Replies', 'Views']]
sheet3_data = [['Thread title', 'Date', 'Comment text']]

keywords = ['Singtel', 'PC show']

cookie = '__cfduid=d52b7a6f2feca97b1c48998c888c517981481214002; cX_S=iwgkprrgasx9gzq5; __utma=98462808.202309017.1481214242.1481214242.1481214242.1; __utmc=98462808; __utmz=98462808.1481214242.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); PHPSESSID=e9117d08d75f0612d6cbb11d4fa33866; bb_sessionhash=94fff2833ba8117bbe4571fe83b92a90; bb_lastvisit=1481214098; bb_lastactivity=0; bb_forum_view=57972b5cfc0102c7b6e58e0703c3868c1a61fd3ca-1-%7Bi-473_i-1481285483_%7D; _gat=1; _ga=GA1.2.202309017.1481214242; __asc=266b94af158e3777ff53912ac42; __auc=3d194a02158df3fab81ed66b668; cX_P=iwgkprrlcweqjrg7; __atuvc=69%7C49; __atuvs=584a9d91986fd2e6003'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_'+str(flag)+'.xls')
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col][:32766])
            except:
                print(one_row[col])
    w.save(filename)
    print filename+"===========over============"


def request_sheet1(keyword, url):
    global sheet1_data
    # link, name, replies, views
    start_index = [0, 20, 40, 60, 80]
    reg_1 = 'GsearchResultClass.*?"title":"(.*?)".*?"url":"(.*?)"'

    for start in start_index:
        real_url = url
        print '---'+keyword+'--'+str(start)+'---'
        req_url = real_url.replace('#start#', str(start))
        try:
            html = get_request(req_url)
            title_url_list = re.compile(reg_1).findall(html)
            for title_url in title_url_list:
                one_row = [keyword, remove_html_tag(title_url[0]), title_url[1]]
                if 'special-events' in title_url[1]:
                    sub_forum = get_special_event(title_url[1])
                    for item in sub_forum:
                        sheet1_data.append(one_row + item)
                        if item[1].endswith('.html'):
                            m = re.search(r'index\d{1,2}\.html$', url)
                            if m:
                                request_sheet2(item[0], item[1])
                            elif item[1].endswith('index.html'):
                                request_sheet2(item[0], item[1])
                            else:
                                request_sheet3(item[0], item[1])
                            request_sheet3(item[0], item[1])
                        else:
                            request_sheet2(item[0], item[1])
                else:
                    sheet1_data.append(one_row + ['N/A', 'N/A', 'N/A'])
                    if title_url[1].endswith('.html'):
                        request_sheet3(title_url[0], title_url[1])
                    else:
                        request_sheet2(title_url[0], title_url[1])
        except:
            print 'ERROR--sheet1---'+url


def get_special_event(url):
    html = get_request(url)
    ret = []
    reg = '<div><a href="(.*?)".*?<strong>(.*?)</strong>.*?smallfont.*?>(.*?)<.*?<strong>'
    temp_list = re.compile(reg).findall(html)
    for temp in temp_list:
        name = temp[1]
        link = temp[0]
        if 'http://forums.hardwarezone.com.sg' not in link:
            link = 'http://forums.hardwarezone.com.sg' + link
        text = temp[2]
        ret.append([name, link, text])
    return ret


def total_page(html):
    reg = 'pagination popupmenu nohovermenu.*?Page.*?of (.*?)<'
    temp = re.compile(reg).findall(html)
    if temp:
        return int(temp[0])
    return 1


def get_total_page(html):
    reg_number = 'pagination.*?of (.*?)<.'
    page_number = 0
    if 'pagination' in html:
        number_body = re.compile(reg_number).findall(html)
        if number_body:
            page_number = int(number_body[0])
    if page_number > 50:
        page_number = 50
    return page_number


def request_sheet2(name, url):
    m = re.search(r'index\d{1,2}\.html$', url)
    if m:
        url = url[:m.start()]+'.html'
    try:
        html = get_request(url)
    except:
        print 'ERROR---sheet2--'+url
        return
    page_number = get_total_page(html)
    get_sheet2_body(name, html)
    for i in range(2, page_number+1):
        next_url = url+'index'+str(i)+'.html'
        try:
            html = get_request(next_url)
            get_sheet2_body(name, html)
        except:
            print 'ERROR--sheet2---'+next_url


def get_sheet2_body(name, html):
    global sheet2_data
    reg = 'id="td_threadtitle_.*?href="(.*?)".*?>(.*?)<.*?Replies: (.*?), Views: (.*?)"'
    thread_list = re.compile(reg).findall(html)
    for thread in thread_list:
        link = thread[0]
        if 'http://forums.hardwarezone.com.sg' not in link:
            link = 'http://forums.hardwarezone.com.sg' + link
        t_name = remove_html_tag(thread[1].replace('**', ''))
        reply = thread[2].replace(',', '')
        view = thread[3].replace(',', '')
        one_row = [remove_html_tag(name), remove_html_tag(t_name), link, reply, view]
        sheet2_data.append(one_row)
        request_sheet3(t_name, link)


def request_sheet3(name, url):
    if 'record-breaking' in url:
        return
    m = re.search(r'-\d{1,2}\.html$', url)
    if m:
        url = url[:m.start()]+'.html'
    print 'sheet3--' + url
    try:
        html = get_request(url)
    except:
        print 'ERROR---sheet3--'+url
        return
    get_sheet3_body(name, html)
    page_number = get_total_page(html)
    for i in range(2, page_number+1):
        next_url = url.replace('.html', '-'+str(i)+'.html')
        try:
            html = get_request(next_url)
            get_sheet3_body(name, html)
        except:
            print 'ERROR--sheet3---'+next_url


def get_sheet3_body(name, html):
    global sheet3_data
    reg = '<a name="post\d*?">.*?</a>(.*?)<.*?id="post_message_.*?>(.*?)</div'
    text_list = re.compile(reg).findall(html)
    for text in text_list:
        date = get_date(text[0])
        text = remove_html_tag(text[1])
        one_row = [remove_html_tag(name), date, text.replace('=', '')]
        sheet3_data.append(one_row)


def get_date(ori):
    try:
        d = datetime.strptime(ori, '%d-%m-%Y, %I:%M %p')
        date = d.strftime('%-d/%-m/%Y')
        return date
    except:
        return datetime.now().strftime('%-d/%-m/%Y')


def remove_html_tag(ori):
    ori = unicode(ori, 'unicode-escape')
    s = ori.encode('utf-8')
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', s)
    return str(HTMLParser.HTMLParser().unescape(dd))


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

i = 0
for i in range(len(keywords)):
    site = 'site%3Aforums.hardwarezone.com.sg%2F%20' + keywords[i].replace(' ', '%20')
    url = 'https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=en&prettyPrint=false&source=gcsc&gss=.sg&sig=0c3990ce7a056ed50667fe0c3873c9b6&start=#start#&cx=011134908705750190689:daz50x-t54k&q=#site#&googlehost=www.google.com&callback=google.search.Search.apiary19428&nocache=1481290177512'.replace('#site#', site)
    request_sheet1(keywords[i], url)
    write_excel(keywords[i].replace(' ', '_')+'_1.xls', sheet1_data)
    write_excel(keywords[i].replace(' ', '_')+'_2.xls', sheet2_data)
    write_excel(keywords[i].replace(' ', '_')+'_3.xls', sheet3_data)
    del sheet1_data
    sheet1_data = [['Keyword', 'Forum topic', 'Forum link', 'Sub-forum topic', 'Sub-forum link', 'Text']]
    del sheet2_data
    sheet2_data = [['Thread in forum', 'Thread', 'Url of Thread', 'Replies', 'Views']]
    del sheet3_data
    sheet3_data = [['Thread title', 'Date', 'Comment text']]
    gc.collect()
