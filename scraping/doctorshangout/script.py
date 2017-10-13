# -*- coding: utf-8 -*-
import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd
import time
import requests
import json

C_ID = 1
T_ID = 1
sheet1_data = [['Category ID', 'Category', 'Category URL', 'No. Discussions']]
sheet2_data = [['Category ID', 'Title ID', 'Title', 'Content', 'Create Date', 'Title URL', 'No. Replies', 'Latest Date']]
sheet3_data = [['Title ID', 'Comments', 'Date']]

cookie = 'bcookie="v=2&2f6c9444-0b2f-466a-8183-ef73e05efa35"; bscookie="v=1&2017041006541990b97a3b-1e52-4da3-8e47-33e0e8e1e3aeAQGgvnt_FYPCpH58BfQhdPydnY6jBTcZ"; visit="v=1&M"; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; join_wall=v=2&AQFhNUYNvP5n8AAAAVvSGU2GWS-2YElFKFQfNLC9Lu27yuc26LdeUp9IUsKvRn7BvDIJPGj6Zt09FXQUVCLbJE5T4W0KMdm9iux6K5mfVuB5Al9lYuJTWUBl0xM5cg4AMo4OmPiAUgPTTiMJIvsvxX3_7b8rimV18UwuwyE_ICE9FB5ZyYrBVwHPGg; _gid=GA1.2.990777859.1493878542; sl="v=1&sHIVY"; lang="v=2&lang=en-us"; li_at=AQEDARo-DEsAlf1eAAABW9IZzwoAAAFb09FDClYAzTg2ibTPV-O_Dqr3MSP-yhBB8KrNn4Sa9FY7OP-sBHXfvSDGKlzMJUbF12JOgmIxNmG6sXSF3r4_PKBUvZu-f2F3gCEr560b6Dh1BVf4llZka-Qo; JSESSIONID="ajax:1423185689819717669"; liap=true; lidc="b=TB95:g=558:u=43:i=1493878607:t=1493887866:s=AQFM0gn66ojmBqIFbNtwViz-OMqniwCu"; _ga=GA1.2.610623672.1491807398; _gat=1; _lipt=CwEAAAFb0mlL-HRaJDSReqC3hAtYV6Gup6SrDmh9grOcTvZEwbVaZrD-Js3CtvzL2XQ5DsbJ1aTSgvt48xo9T6UM8oP5utFRJ53syRDWfYqRUCQnjHn-AFyM7d-TySMlw7lVj3eigG4NQFSEpO1mmy1XA5S9_r2Ie4UjKVH90oKCl1PPzy_xQKRFP3ijNfrmn7dHnVfyWApPdWiWijUTNjra8ApDgf7DIiFGK7mZGx5CJ_aYGnD1XC8N-UWnv5LcTCzos3rB3VxRHzjjioox1ZtLKrVdKo_M55QfM85UL6RcwUbbGx0iPa_T_fRshq1RrwkgZKtPAnOlGeOoGnYQdv6p4D7mCgKUbdFYDiZrViiYjqzFAw'

files = []

category_name_id_dict = {
    'Internal Medicine': 1,
    'Pediatrics': 2,
    'General Surgery': 3,
    'Obstetrics & Gynecology': 4,
    'Orthopedics': 5,
    'Ophthalmology': 6,
    'Otolaryngology-ENT': 7,
    'Dermatology': 8,
    'Radiology': 9,
    'Anesthesiology': 10,
    'Psychiatry': 11,
    'Cardiology': 12,
    'Emergency Medicine': 13,
    'Infectious Diseases': 14,
    'USMLE': 15,
    'Medical Students': 16,
    'Medical Ebooks': 17,
    'Medical Software': 18,
    'Book Reviews': 19,
    'The Lounge': 20,
    'Pathology': 21,
    'Neurology': 22,
    'Nephrology': 23,
    'Gastroenterology': 24,
    'Technology': 25,
    'Endocrinology': 26,
    'Pulmonology': 27,
    'Hematology': 28,
    'Medical Oncology': 29,
    'Immunology': 30,
    'Rheumatology': 31,
    'Geriatrics': 32,
    'Critical Care Medicine': 33,
    'Toxicology': 34,
    'Pain Medicine': 35,
    'Sports Medicine': 36,
    'Military Medicine': 37,
    'Family Medicine': 38,
    'Community Medicine': 39,
    'Radiation Oncology': 40,
    'Pharmacology': 41,
    'Forensic Medicine': 42,
    'Microbiology': 43,
    'Dental Medicine': 44,
    'Anatomy': 45,
    'Physiology': 46,
    'Biochemistry': 47,
    'Gastrointestinal Surgery': 48,
    'Robotic Surgery': 49,
    'Cardiothoracic surgery': 50,
    'Neurosurgery': 51,
    'Pediatric surgery': 52,
    'Urology': 53,
    'Plastic surgery': 54,
    'Vascular surgery': 55,
    'Surgical Oncology': 56,
    'Podiatric surgery': 57,
    'Organ Transplantation': 58,
    'Medical Practice': 59,
    'Evidence Based Medicine': 60,
    'Medical Informatics': 61,
    'Medical Job Offers': 62,
    'Genetics': 63,
    'Suggestion box': 64,
    'Nutrition': 65,
    'Medical Ethics': 66,
    'Medical Events & Conferences': 67,
    'Finance & Investing': 68,
    'MedicoLegal': 69,
    'Social & Humor': 70,
    'EMR': 71,
    'For Sale': 72,
}

BASE_URL = 'http://www.doctorshangout.com/forum?page=%d'


def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path or 'txt' in path:
            if 'result' not in path:
                files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files


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
    global sheet1_data, C_ID
    raw_reg = 'class="xg_lightborder"><h3><a href="(.*?)">(.*?)<.*?bignum xg_lightborder">(.*?)<'
    html = get_request(url)
    categories = re.compile(raw_reg).findall(html)
    for category in categories:
        try:
            url = category[0]
            name = category[1]
            discussion_count = int(category[2])
            one_row = [C_ID, name, url, discussion_count]
            sheet1_data.append(one_row)
            if discussion_count > 0:
                request_sheet2(C_ID, url+'?page=%d', discussion_count // 10 + 1)
            C_ID += 1
        except Exception as e:
            print 'ERR---level 1---%s' % str(e)


def request_sheet2(C_ID, base_url, page_number):
    global sheet2_data, T_ID
    content_reg = 'xg_module_body.*?categories.*?>(.*?)</table>'
    reg = 'h3.*?href="(.*?)".*?>(.*?)<.*?xg_lightborder">(.*?)<.*?xg_lightborder">(.*?)<'
    for page in range(1, page_number+1):
        url = base_url % page
        print url
        html = get_request(url)
        content = re.compile(content_reg).findall(html)
        if not content:
            print 'ERROR--No content for %s' % url
            continue
        content = content[0]
        details = re.compile(reg).findall(content)
        for category in details:
            url = category[0]
            content, create_date = get_content_and_create_date(url)
            name = category[1]
            reply_count = int(category[2])
            date = get_latest_date(category[3].strip().split('on ')[-1])
            one_row = [T_ID, C_ID, name, content, create_date, url, reply_count, date]
            sheet2_data.append(one_row)

            # if reply_count > 0:
                # request_sheet3(T_ID, url + '?page=%d', reply_count // 10 + 1)
            T_ID += 1


def request_sheet3(T_ID, base_url, page_number):
    global sheet3_data
    reg = 'discussion clear i.*? xg_lightborder.*?timestamp">(.*?) at.*?xg_user_generated">(.*?)</div'
    for page in range(1, page_number + 1):
        url = base_url % page
        html = get_request(url)
        comments = re.compile(reg).findall(html)

        for category in comments:
            date = get_date(category[0])
            comment = remove_html_tag(category[1])
            one_row = [T_ID, comment, date]
            sheet3_data.append(one_row)


def get_latest_date(ori_time):
    if 'Friday' in ori_time:
        ori_time = 'Sep 29, 2017'
    elif 'Thursday' in ori_time:
        ori_time = 'Sep 28, 2017'
    elif 'Wednesday' in ori_time:
        ori_time = 'Sep 27, 2017'
    elif 'Tuesday' in ori_time:
        ori_time = 'Sep 26, 2017'
    elif 'Monday' in ori_time:
        ori_time = 'Sep 25, 2017'
    elif 'Saturday' in ori_time:
        ori_time = 'Sep 30, 2017'
    elif 'Sunday' in ori_time:
        ori_time = 'Oct 1, 2017'
    if ',' not in ori_time:
        ori_time += ', 2017'
    try:
        ret = datetime.strptime(ori_time, "%b %d, %Y").strftime('%d/%m/%Y')
        return ret
    except Exception as e:
        return ori_time


def get_date(ori_time):
    try:
        ret = datetime.strptime(ori_time, "%B %d, %Y").strftime('%d/%m/%Y')
        return ret
    except Exception as e:
        return ori_time


def get_content_and_create_date(url):
    html = get_request(url)
    reg = 'navigation byline.*?on(.*?)at.*?class="xg_user_generated">(.*?)</div>'
    data = re.compile(reg).findall(html)
    if data:
        data = data[0]
        return remove_html_tag(str(data[1].strip())), get_date(data[0].strip())
    return '', ''


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.linkedin.com/')
    req.add_header("Cookie", cookie)
    req.add_header('csrf-token', 'ajax:3940183104206872464')
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return HTMLParser.HTMLParser().unescape(res)


def read_excel(filename, start=1):
    global sheet2_data
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    reg = 'a class="nolink">.*?a class="nolink">.*?href=.*?>(.*?)<'

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            url = row[5].value
            html = get_request(url)
            category_name = re.compile(reg).findall(html)
            if category_name:
                category_name = category_name[0]
                category_id = category_name_id_dict.get(category_name, 0)
                print category_id, category_name
        except:
            print(i)
    write_excel('data/res.xls', sheet2_data)


reload(sys)
sys.setdefaultencoding('utf-8')
# for i in range(1, 5):
#     url = BASE_URL % i
#     request_sheet1(url)
# write_excel('data/sheet1.xls', sheet1_data)
# write_excel('data/sheet2.xls', sheet2_data)
# write_excel('data/sheet3.xls', sheet3_data)
read_excel('data/sheet2.xls')