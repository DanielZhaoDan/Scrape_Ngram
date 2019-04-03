# -*- coding: utf-8 -*-

import re
import xlwt
from datetime import datetime
import os
import requests
import HTMLParser
import time
import uuid


sheet0_data = [['Id', 'Name', 'URL', 'Total Post No.', 'Title', 'Title URL', 'Reposted From', 'No. UpVotes', 'Sub', 'Sub URL', 'Date', 'No. comments']]
sheet1_data = [['Title Thread URL', 'Text']]

P_ID = 1

MAX_COUNT = 2000

cookie = 'kuid=ZwZ1AlwWIuKMohV0DQlhAg==; __asc=24bc9c43167b67849cac95403a9; __auc=24bc9c43167b67849cac95403a9; __utma=40758456.698408157.1544954596.1544954596.1544954596.1; __utmc=40758456; __utmz=40758456.1544954596.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); AMP_TOKEN=%24NOT_FOUND; _ga=GA1.3.698408157.1544954596; _gid=GA1.3.1390293499.1544954596; notices=%5B%5D; thread_lastview=a%3A1%3A%7Bs%3A24%3A%225492995596bde615218b456d%22%3Bi%3A1544758618%3B%7D; post_order=1; forkrtg={"generic":"29112019"}; _fbp=fb.2.1544954990430.1707517265; iUUID=dfa4db9d0a5ed79fd80ec7473bd0b700; innity.dmp.170.sess.id=250431571.170.1544954990507; innity.dmp.cks.appxs=1; innity.dmp.cks.innity=1; _a1_f=99c1269d-8702-4367-b9d1-2eb52f9199ee; _daxbypass=true; __gads=ID=745729c3adcef617:T=1544954991:S=ALNI_MZCdfTch3xvE2Qahhkqts6GwsJzeg; innity.dmp.170.sess=2.1544954990507.1544954990507.1544954994868; __utmt=1; __utmb=40758456.29.10.1544954596; _dc_gtm_UA-132312-41=1; _gat_UA-132312-41=1; _gat=1; _dc_gtm_UA-132312-60=1'

url_list = [
    # ('health', 'https://www.reddit.com/search?q=health&sort=relevance', 250),
    # ('wellness', 'https://www.reddit.com/search?q=wellness&sort=relevance', 205),
    # ('nutrition', 'https://www.reddit.com/search?q=nutrition&sort=relevance', 244),
    # ('fitness', 'https://www.reddit.com/search?q=fitness&sort=relevance', 248),
    # ('healthy food', 'https://www.reddit.com/search?q=healthy%20food&sort=relevance', 238),
    # ('vegan', 'https://www.reddit.com/search?q=vegan&sort=relevance', 245),
    # ('herbal', 'https://www.reddit.com/search?q=herbal&sort=relevance', 243),
    # ('chinese medicine', 'https://www.reddit.com/search?q=chinese%20medicine&sort=relevance', 240),
    ('ayurveda', 'https://www.reddit.com/search?q=ayurveda&sort=relevance', 243),
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


def request_sheet0(topic_name, url, total_number):
    global sheet0_data, sheet1_data, P_ID
    main_reg = 'class="scrollerItem.*?id="(.*?)".*?class="_1rZYMD_4xY3gRcSS3p8ODO".*?>(.*?)<.*?SQnoC3ObvgnGjWt90zD9Z.*?href="(.*?)".*?class="imors3-0 euspgB">(.*?)<div.*?data-click-id="timestamp".*?>(.*?)<.*?data-click-id.*?href="(.*?)">(.*?)<.*?FHCV02u6Cp2zYL0fhQPsO.*?>(.*?) '
    html = get_request(url)
    main_list = re.compile(main_reg).findall(html)
    last_id = None
    print url,
    for item in main_list:
        try:
            id = item[0]
            upvote = parse_number(item[1])
            thread_url = 'https://www.reddit.com' + item[2]
            title = remove_html_tag(item[3])
            reposted_from = get_reposted_from(item[3])
            date = get_date(item[4])
            sub_name, sub_url = get_sub(thread_url)
            no_comment = parse_number(item[7])
            one_row = [topic_name + '_%d' % P_ID, topic_name, url, total_number, title, thread_url, reposted_from, upvote, sub_name, sub_url, date, no_comment]

            sheet0_data.append(one_row)
            P_ID += 1
            last_id = id
            request_sheet1(thread_url)
            print '.',
            time.sleep(1)
        except Exception as e:
            print 'EXP_sheet1--', url, e
    if last_id:
        request_json(topic_name, url, last_id, len(main_list), total_number)


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


def request_json(topic_name, url, last_id, count, total_number):
    global P_ID, sheet0_data
    while count < MAX_COUNT and last_id:
        time.sleep(2)
        try:
            json_url = 'https://gateway.reddit.com/desktopapi/v1/search?q=' + topic_name + '&sort=relevance&t=all&type=link,sr,user&after=' + last_id + '&search_correlation_id=' + str(uuid.uuid4()) + '&allow_over18=&include=structuredStyles'
            json_resp = get_json_request(json_url)
            last_id = json_resp['tokens']['posts']
            print last_id

            sub_posts = json_resp['posts']

            for post_id, v in sub_posts.items():
                title = v.get('title', '')
                thread_url = v.get('permalink', '')
                if v.get('source'):
                    reposted_from = v.get('source').get('url', '')
                else:
                    reposted_from = 'N/A'
                no_comment = v.get('numComments', 0)
                sub_name, sub_url = get_sub(thread_url)
                upvote =v.get('score', 0)
                date = get_date_from_timestamp(v.get('created'))
                one_row = [topic_name + '_%d' % P_ID, topic_name, url, total_number, title, thread_url, reposted_from, upvote, sub_name, sub_url,
                           date, no_comment]
                sheet0_data.append(one_row)

                request_sheet1(thread_url)
                count += 1
                P_ID += 1
            print count, json_url
        except Exception as e:
            print 'EXP_sheet2==', url, e


def get_sub(url):
    sub_names = url.split('/')
    return '/'.join(sub_names[3:5]), '/'.join(sub_names[:5])


def get_date_from_timestamp(timestamp):
    try:
        return datetime.utcfromtimestamp(timestamp/1000).strftime('%d/%m/%Y')
    except:
        return 'N/A'


def get_reposted_from(ori):
    reg = 'href="(.*?)"'
    urls = re.compile(reg).findall(ori)

    return urls[0] if urls else 'N/A'


def request_share_and_commment_count(main_url, main_topic, sub_name, url_base, total_num):
    num = 1
    global sheet1_data
    create_date = None
    reg = 'id="post.*?datetime="(.*?)T.*?Fx\(flexZero\) D\(f\) jsTippy(.*?)Fx\(flexZero\).*?article.*?>(.*?)</article'
    for i in range(1, total_num + 1):
        url = url_base + str(i)
        try:
            html = get_request(url)
            start_index = 0 if i == 1 else 1
            data_list = re.compile(reg).findall(html)
            for data in data_list[start_index:]:
                try:
                    comment_date = get_date(data[0])
                    reputation = get_reputation(data[1])
                    content = remove_html_tag(data[2]).replace('Quote:Original Posted By ', '')
                    one_row = [main_topic, main_url, sub_name, url_base, num, comment_date, reputation, content]
                    sheet1_data.append(one_row)
                    num += 1
                    if not create_date:
                        create_date = comment_date
                except Exception as e:
                    continue
        except Exception as e:
            print 'EX-sheet2: ', url, e
    return create_date


def get_reputation(ori):
    if 'c-red' in ori:
        return -ori.count('c-red')
    elif 'c-green' in ori:
        return ori.count('c-green')
    return 0


def parse_number(ori):
    try:
        if 'k' in ori or 'K' in ori :
            new = ori.replace('.', '').replace('k', '').replace('K', '') + '00'
        elif 'm' in ori or 'M' in ori:
            new = ori.replace('.', '').replace('m', '').replace('M', '') + '00000'
        else:
            new = ori
        return int(new)
    except:
        return 0


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    try:
        return str(HTMLParser.HTMLParser().unescape(dd)).strip()
    except:
        return str(dd).strip()


def get_date(ori):
    try:
        d = datetime.strptime(ori, '%d-%m-%Y')
        date = d.strftime('%d/%m/%Y')
    except:
        return ori
    return date


def get_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
    }
    req = requests.get(get_url, headers=headers)
    res = req.content
    res = str(res).replace('\t', '').replace('\r', '').replace('\n', '').replace('&amp;', '&').replace('\\t', '').replace('\\r', '').replace('\\n', '')
    return res


def get_json_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
    }
    req = requests.get(get_url, headers=headers)
    return req.json()


for name_url in url_list:
    P_ID = 1
    name = name_url[0]
    url = name_url[1]
    request_sheet0(name, url, name_url[2])

    write_excel('data/%s_main.xls' % name, sheet0_data)
    write_excel('data/%s_text.xls' % name, sheet1_data)
    del sheet0_data
    del sheet1_data
    sheet0_data = [['Id', 'Name', 'URL', 'Total Post No.', 'Title', 'Title URL', 'Reposted From', 'No. UpVotes', 'Sub', 'Sub URL', 'Date',
                    'No. comments']]
    sheet1_data = [['Title Thread URL', 'Text']]



