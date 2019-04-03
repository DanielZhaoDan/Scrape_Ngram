# -*- coding: utf-8 -*-

import re
import xlwt
from datetime import datetime
import os
import requests
import HTMLParser


sheet0_data = [['Thread', 'Thread URL', 'Sub topic name', 'No. views', 'No. replies', 'Sub topic URL', 'Create Date', 'Last Date']]
sheet1_data = [['Thread', 'Thread URL', 'Sub topic name', 'Sub topic URL', 'Repli No.', 'Reply date', 'Replier reputation', 'Text']]

cookie = 'kuid=ZwZ1AlwWIuKMohV0DQlhAg==; __asc=24bc9c43167b67849cac95403a9; __auc=24bc9c43167b67849cac95403a9; __utma=40758456.698408157.1544954596.1544954596.1544954596.1; __utmc=40758456; __utmz=40758456.1544954596.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); AMP_TOKEN=%24NOT_FOUND; _ga=GA1.3.698408157.1544954596; _gid=GA1.3.1390293499.1544954596; notices=%5B%5D; thread_lastview=a%3A1%3A%7Bs%3A24%3A%225492995596bde615218b456d%22%3Bi%3A1544758618%3B%7D; post_order=1; forkrtg={"generic":"29112019"}; _fbp=fb.2.1544954990430.1707517265; iUUID=dfa4db9d0a5ed79fd80ec7473bd0b700; innity.dmp.170.sess.id=250431571.170.1544954990507; innity.dmp.cks.appxs=1; innity.dmp.cks.innity=1; _a1_f=99c1269d-8702-4367-b9d1-2eb52f9199ee; _daxbypass=true; __gads=ID=745729c3adcef617:T=1544954991:S=ALNI_MZCdfTch3xvE2Qahhkqts6GwsJzeg; innity.dmp.170.sess=2.1544954990507.1544954990507.1544954994868; __utmt=1; __utmb=40758456.29.10.1544954596; _dc_gtm_UA-132312-41=1; _gat_UA-132312-41=1; _gat=1; _dc_gtm_UA-132312-60=1'

url_list = [
    # ('Fitness & Healthy Body', 'https://www.kaskus.co.id/forum/558/fitness--healthy-body/%d'),
    # ('Fat-Loss,Gain-Mass,Nutrisi Diet & Suplementasi Fitness', 'https://www.kaskus.co.id/forum/274/fat-lossgain-massnutrisi-diet--suplementasi-fitness/%d'),
    ('Muscle Building', 'https://www.kaskus.co.id/forum/236/muscle-building/%d'),
    ('Health Consultation', 'https://www.kaskus.co.id/forum/724/health-consultation/%d'),
    ('Healthy Lifestyle', 'https://www.kaskus.co.id/forum/725/healthy-lifestyle/%d'),
    ('Quit Drugs, Alcohol & Smoking', 'https://www.kaskus.co.id/forum/559/quit-drugs-alcohol--smoking/%d'),
    ('Women’s Health', 'https://www.kaskus.co.id/forum/718/womens-health/%d'),
]


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


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


def request_sheet0(topic_name, url):
    global sheet0_data, sheet1_data
    html = get_request(url)
    reg = 'class="C\(#4a4a4a\) Td\(n\):h.*?href="(.*?)\?.*?>(.*?)<div.*?Mstart\(7.*?>(.*?)<.*?Mstart\(7.*?>(.*?)<'
    threads = re.compile(reg).findall(html)
    for thread in threads:
        try:
           sub_topic_url = thread[0]
           sub_topic_name = remove_html_tag(thread[1])
           no_view = parse_number(thread[2])
           no_reply = parse_number(thread[3])
           sheet2_num = no_reply // 20 + 1
           create_date = request_share_and_commment_count(url, topic_name, sub_topic_name, sub_topic_url, sheet2_num)
           one_row = [topic_name, url, sub_topic_name, no_view, no_reply, sub_topic_url, create_date, create_date]
           sheet0_data.append(one_row)
           print one_row
        except Exception as e:
            print 'EX-sheet1', e
    return len(threads)


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
    if 'k' in ori or 'K' in ori :
        new = ori.replace('.', '').replace('k', '').replace('K', '') + '00'
    elif 'm' in ori or 'M' in ori:
        new = ori.replace('.', '').replace('m', '').replace('M', '') + '00000'
    else:
        new = ori
    return int(new)


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


for name_url in url_list:
    name = name_url[0]
    url_base = name_url[1]
    for i in range(1, 28):
        url = url_base % i
        print name, i
        if 0 == request_sheet0(name, url):
            break
    write_excel('data/%s_main.xls' % name, sheet0_data)
    write_excel('data/%s_reply.xls' % name, sheet1_data)
    del sheet0_data
    del sheet1_data
    sheet0_data = [
        ['Thread', 'Thread URL', 'Sub topic name', 'No. views', 'No. replies', 'Sub topic URL', 'Create Date',
         'Last Date']]
    sheet1_data = [
        ['Thread', 'Thread URL', 'Sub topic name', 'Sub topic URL', 'Repli No.', 'Reply date', 'Replier reputation',
         'Text']]


