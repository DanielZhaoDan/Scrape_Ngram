# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import sys
from datetime import datetime, timedelta
import HTMLParser
import os
from urlparse import urlparse
import time
import random

sheet1_data = [
    ['Keywords String', 'Bucket', 'Country', 'No of Articles', 'Page No.', 'News Url', 'Date', 'Name of Publisher',
     'Main url of newspaper/magazine', 'Headline', 'Content', 'Rank']]
sheet_dict = {}

url_bases = 'https://www.google.com/search?q={key_word}&newwindow=1&safe=strict&rlz=1C5CHFA_enSG792SG793&source=lnms&tbm=nws&sa=X&ved=0ahUKEwi8jMn9zs7hAhUDbn0KHc6mABMQ_AUIDigB&biw=1440&bih=798&tbs=qdr:y&start='
# url_bases = 'https://www.google.com/search?q={key_word}&tbm=nws&start='

FIRST_START = 1 # latest + 1
cookie = [
    'CGIC=EhQxQzVDSEZBX2VuQ045MTdTRzkxOCKHAXRleHQvaHRtbCxhcHBsaWNhdGlvbi94aHRtbCt4bWwsYXBwbGljYXRpb24veG1sO3E9MC45LGltYWdlL2F2aWYsaW1hZ2Uvd2VicCxpbWFnZS9hcG5nLCovKjtxPTAuOCxhcHBsaWNhdGlvbi9zaWduZWQtZXhjaGFuZ2U7dj1iMztxPTAuOQ; HSID=A5Ih5jNB8oyGjIXTx; SSID=AH1M1EVJJxaiJThB8; APISID=OcqjtgzVNahCxh0x/AR86aXJZJkw2ha6NI; SAPISID=3IgpFeZLrJfJb9gO/ADFzzMTgR95YSrf3e; __Secure-3PAPISID=3IgpFeZLrJfJb9gO/ADFzzMTgR95YSrf3e; OGPC=19019112-1:; SEARCH_SAMESITE=CgQI0JAB; SID=1gc33ZTLp7-0jcS053ZQGdcPKicSY3SrC1gRanBVukzSa2Lplpq9_PkOjfhjSJxpa6WbbA.; __Secure-3PSID=1gc33ZTLp7-0jcS053ZQGdcPKicSY3SrC1gRanBVukzSa2LpgbMh5BfrHzAurmhtLQaQmA.; NID=204=VL5UZP1q1evxgqCe80Fcpu9Hzhvs1dohAow05wkXKzc8xlZsnNwM54rKdmrd-kstJaPiR7vjvjC6pLIHrmzc_jJ0yu6kRZzMFtDRp1pX02A__YMHkJ5r8ZjU8s-RxwSrmF0HO6UUmYpNWEQXwlO1SIkyko8THhdPdusQhkYYxsSfAZGnaXWv4DoMOxXK-ndq2TQDgAlatcfU0NWDZjM7CHhraZFx43-mudpwds9D; 1P_JAR=2020-10-16-17; DV=471lmmdi7j5CEL5WPJip-J_GpJcmU5d7gAFAyE5GFAQAAFBxZ8UCkzF_DwEAAASIm0L1K13faQAAAA; SIDCC=AJi4QfEdCwpZwwJ4xZdckwIljPA9KO9FT8j__PQWXwYYWXC8jACFIjEaSaRk-PxG6pJx1-0CAsM; __Secure-3PSIDCC=AJi4QfHYY2D1hB31yhsRoe6DwSmHbJmHqTyHfuWpEfI75It2q_91B0QIjyHQkyzgLijPXOUgeCU'
]

key_words = [
    {'keyword': 'edtech intext:teachers intext:training location:india'},

]


x_client_data = 'CLG1yQEIh7bJAQimtskBCMG2yQEIqZ3KAQjQoMoBCJesygEIrMfKAQj1x8oBCOfIygEI6cjKAQjC18oBCPyXywEYi8HKAQ==Decoded:message ClientVariations {  // Active client experiment variation IDs.  repeated int32 variation_id = [3300017, 3300103, 3300134, 3300161, 3313321, 3313744, 3315223, 3318700, 3318773, 3318887, 3318889, 3320770, 3329020];  // Active client experiment variation IDs that trigger server-side behavior.  repeated int32 trigger_variation_id = [3317899];}'

API_KEY = '051278798bc5c8d530a33186637244a9'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
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
                    print('===Write excel ERROR===' + str(one_row[col]))
    w.save(filename)
    print(filename + "===========over============")


def get_total_count(html):
    reg = 'id="resultStats">.*?(\d.*?) result'
    results = re.compile(reg).findall(html)
    if results:
        return int(results[0].split('about')[-1].replace(',', ''))
    return 10


def request_sheet1(key_word, url_base, page_no=1):
    global sheet1_data
    total_count = 0
    while True:
        url = url_base + str(page_no - 1) + '0'
        print(url)
        if page_no > 5:
            break
        html = get_request(url)
        if 'Our systems have detected unusual traffic from your computer network' in html:
            return True
        if total_count == 0:
            total_count = get_total_count(html)
        topic_detail_reg = 'class="dbsr" .*?href="(.*?)".*?>.*?class="QyR1Ze".*?>.*?img>(.*?)<.*?JheGif nDgy9d.*?>(.*?)</div.*?class="WG9SHc".*?span>(.*?)<'
        topic_detail = re.compile(topic_detail_reg).findall(html)
        if not topic_detail:
            break
        i = 1
        for detail in topic_detail:
            url = detail[0]
            o = urlparse(url)
            main_url = o.scheme + '://' + o.netloc
            headline = remove_html_tag(detail[2])
            publisher = detail[1]
            date = get_date(detail[3])
            bucket = key_word['keyword'].split(' intext:')[0]
            # content = get_raw_content(url)
            content = ''
            rank = str(page_no) + '.' + ('0' if i < 10 else '') + str(i)
            one_row = [key_word['keyword'], '-', '-', total_count, page_no, url, date,
                       publisher, main_url, headline, content,
                       rank]
            print one_row
            sheet1_data.append(one_row)
            i += 1
        page_no += 1
    return False


def get_raw_content(url):
    try:
        html = get_request(url)
        reg = '<body.*?>(.*?)</body>'
        contents = re.compile(reg).findall(html)
        if contents:
            content = contents[0]
            step_0 = remove_html_tag(content)  # remove html tag
            step_1 = re.sub('[ \t\n\r]+', ' ', step_0)  # remove multiple blank, newline and tab
            return step_1
        return html
    except:
        return ''


def request_sheet2(base_url):
    global sheet_dict
    if sheet_dict.get(base_url):
        return sheet_dict[base_url]

    rank_reg = 'rankingItem--global.*?rankingItem-value.*?>(.*?)<.*?rankingItem--country.*?rankingItem-value.*?>(.*?)<.*?rankingItem--category.*?rankingItem-value.*?>(.*?)<.*?Total Visits.*?countValue">(.*?)<'
    country_tag = 'accordion-toggle.*?countValue">(.*?)<.*?country-name.*?>(.*?)<'

    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[
        -1]
    print(url + ' ' + str(len(sheet_dict)))
    html = get_request(url)
    if 'NAME="ROBOTS"' in html:
        print('ROBOT DETECTED!, sleeping 600 seconds')
        return None
    global_ranks = re.compile(rank_reg).findall(html)
    if global_ranks:
        ret = [global_ranks[0][0].replace('[#,]', ''), global_ranks[0][1].replace('[#,]', ''),
               global_ranks[0][2].replace('[#,]', ''), global_ranks[0][3]]
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

    for i in range(start, table.nrows - 1):
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
            print(one_row)
            sheet2_data.append(one_row)
        except:
            print(i)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_date(datetime_ago):
    matches = re.search(r"(\d+ weeks?,? )?(\d+ days?,? )?(\d+ hours?,? )?(\d+ mins?,? )?(\d+ secs? )?ago", datetime_ago)

    if not matches:
        date = datetime.strptime(datetime_ago, "%b %d, %Y")
        return date.strftime("%d/%m/%Y")

    date_pieces = {'week': 0, 'day': 0, 'hour': 0, 'min': 0, 'sec': 0}

    for i in range(1, len(date_pieces) + 1):
        if matches.group(i):
            value_unit = matches.group(i).rstrip(', ')
            if len(value_unit.split()) == 2:
                value, unit = value_unit.split()
                date_pieces[unit.rstrip('s')] = int(value)

    d = datetime.today() - timedelta(
        weeks=date_pieces['week'],
        days=date_pieces['day'],
        hours=date_pieces['hour'],
        minutes=date_pieces['min'],
        seconds=date_pieces['sec']
    )

    return d.strftime("%d/%m/%Y")


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': random.choice(cookie),
        'x-client-data': x_client_data,
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
    urls.append([key_word, url_bases.format(key_word=key_word['keyword'].replace(' ', '+'))])
print(len(urls))

ts = int(time.time())
for i in range(len(urls)):
    url = urls[i]
    page_no = 1 if i > 0 else FIRST_START
    stop = request_sheet1(url[0], url[1], page_no=page_no)
    if stop:
        break
te = int(time.time())
print('time: ', te - ts)
write_excel('data/sheet1.xls', sheet1_data)