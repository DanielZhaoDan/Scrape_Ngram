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

sheet1_data = [['Keywords', 'Country', 'No of Articles', 'Page No.', 'News Url', 'Date', 'Name of Publisher', 'Main url of newspaper/magazine', 'Headline', 'Content', 'Rank']]
sheet_dict = {}

url_bases = 'https://www.google.com.sg/search?q="{key_word}"+location:{location}&newwindow=1&safe=strict&hl=en&tbm=nws&tbm=nws&ei=iLEdWZebA8GKvQTWspmABA&sa=N&biw=1777&bih=404&&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2016%2Ccd_max%3A6%2F14%2F2017&start='

key_words = ['jj lin']

locations = ['Singapore', 'malaysia']

cookie = [
    'OGPC=230377472-30:; SID=twQ33SNTOsmjYAu2iIvfrlQ_srIl_SEG3q_YtxMvMpKMvv3vmjJnrslLENcwLQu7RxKq7g.; HSID=AUZDODrHWYoDnMCPF; SSID=A194xqAa-VcD2Y8uD; APISID=9qk2md2vzrw7a2bc/AN_jRZIIGA3GAH1LR; SAPISID=dAWmxXTCYpny2M6d/A8eI4DqSwYb4KP0F9; NID=104=lGgfZ_yN7HjYbtYKZOAa4pj_3TjD0fqWahOKuAPezritULb4CKabz7Hui--BcCxEBwZ_M5_hof2h7KpKjSx-ONntpZudFnHMrULW3wKvcBP3pWK0R_oQUZAXJVAOKgZ78pczPzj5_4pPTUF162MUNUFjU6ltwHy_0tSGWueLnpuIHsg7LxeMKHBxnsR_RFM0E1L00U9tTIcTdxv_VOPcHbKyQdQmUC9DkJf6ZH6CHGbuqkqgieQMSEd65dmL7NwQKhFmmJntH2DcUM8ICg; DV=471lmmdi7j5CMIY2UoZ-rYfYU_mKxRXL3GDguBC-BwEAABC2tvH6YUH2vgAAANRe293xctMTRQAAAA; UULE=a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTQ5NjEzNjYwNDQ5ODAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6MTI5OTc2NDcgbG9uZ2l0dWRlX2U3OjEwMzc4ODEwOTR9IHJhZGl1czoxOTIyMA==',
]

agent_ip = [
    '61.153.232.218', '117.90.0.80', '218.86.128.57', '218.95.246.53', '112.95.22.210', '61.139.104.216', '111.20.214.25', '211.142.141.210', '112.95.22.153', '111.202.121.57',
]

API_KEY = '051278798bc5c8d530a33186637244a9'

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


def get_total_count(html):
    reg = 'id="resultStats">.*?(\d.*?) result'
    results = re.compile(reg).findall(html)
    if results:
        return int(results[0].split('about')[-1].replace(',', ''))
    return 10


def request_sheet1(key_word, location, url_base):
    global sheet1_data
    total_count = 0
    page_no = 1
    while True:
        url = url_base + str(page_no-1) + '0'
        print url
        if page_no > 10:
            break
        html = get_request(url)
        if total_count == 0:
            total_count = get_total_count(html)
        topic_detail_reg = '<h3 .*?href="(.*?)".*?>(.*?)<.*?span.*?>(.*?)<.*?f nsa _.*?">(.*?)<'
        topic_detail = re.compile(topic_detail_reg).findall(html)
        if not topic_detail:
            break
        i = 1
        for detail in topic_detail:
            url = detail[0]
            o = urlparse(url)
            main_url = o.scheme + '://' + o.netloc
            headline = remove_html_tag(detail[1])
            publisher = detail[2]
            date = get_date(detail[3])
            # content = get_raw_content(url)
            content = ''
            rank = str(page_no) + '.' + ('0' if i < 10 else '') + str(i)
            one_row = [key_word, location, total_count, page_no, url, date, publisher, main_url, headline, content, rank]
            sheet1_data.append(one_row)
            i += 1
        page_no += 1
        time.sleep(3)


def get_raw_content(url):
    try:
        html = get_request(url)
        reg = '<body.*?>(.*?)</body>'
        contents = re.compile(reg).findall(html)
        if contents:
            content = contents[0]
            step_0 = remove_html_tag(content) # remove html tag
            step_1 = re.sub('[ \t\n\r]+', ' ', step_0) # remove multiple blank, newline and tab
            return step_1
        return html
    except:
        return ''


def request_sheet2(base_url):
    global sheet_dict
    if sheet_dict.get(base_url):
        return sheet_dict[base_url]

    if len(sheet_dict) and len(sheet_dict) % 5 == 0:
        print 'Sleeping 300 seconds'
        time.sleep(60)
    else:
        print 'Sleeping 10 seconds'
        time.sleep(10)
    rank_reg = 'rankingItem--global.*?rankingItem-value.*?>(.*?)<.*?rankingItem--country.*?rankingItem-value.*?>(.*?)<.*?rankingItem--category.*?rankingItem-value.*?>(.*?)<.*?Total Visits.*?countValue">(.*?)<'
    country_tag = 'accordion-toggle.*?countValue">(.*?)<.*?country-name.*?>(.*?)<'

    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[-1]
    print url + ' ' + str(len(sheet_dict))
    html = get_request(url)
    if 'NAME="ROBOTS"' in html:
        print 'ROBOT DETECTED!, sleeping 600 seconds'
        time.sleep(600)
        return None
    global_ranks = re.compile(rank_reg).findall(html)
    if global_ranks:
        ret = [global_ranks[0][0].replace('[#,]', ''), global_ranks[0][1].replace('[#,]', ''), global_ranks[0][2].replace('[#,]', ''), global_ranks[0][3]]
    else:
        ret = [0, 0, 0, 0]

    country_ranks = re.compile(country_tag).findall(html)
    for country in country_ranks:
        ret.append(country[1])
        ret.append(country[0])
    if len(ret) == 4:
        ret += [0 for i in range(10)]
    sheet_dict[base_url] = ret
    return ret


def read_excel(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            main_url = row[7].value
            publisher = row[6].value
            article_url = row[4].value
            country = row[1].value
            details = request_sheet2(main_url)
            if not details:
                i -= 1
                continue
            one_row = [publisher, main_url, article_url, country] + details
            print one_row
            sheet2_data.append(one_row)
        except:
            print(i)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_date(ori):
    try:
        date = datetime.strptime(ori, '%d %b %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': random.choice(cookie),
        'x-client-data': 'CJG2yQEIprbJAQjBtskBCPKZygEI+5zKAQipncoB',
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')
# scrape google search result
urls = []
for key_word in key_words:
    for location in locations:
        urls.append([key_word, location, url_bases.format(key_word=key_word.replace(' ', '+'), location=location)])
print len(urls)
for url in urls:
    request_sheet1(url[0], url[1], url[2])
write_excel('data/sheet1.xls', sheet1_data)

# scrape rank data
# filename = 'data/sheet1.xls'
# read_excel(filename, 1)
# write_excel('data/sheet2.xls', sheet2_data)
