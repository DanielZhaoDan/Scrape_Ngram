# -*- coding: utf-8 -*-
import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd
import requests
import json
import time
import ssl

P_ID = 1
sheet0_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Title', 'Company']]
sheet1_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Personal Location', 'Followers', 'Self Desp.', 'Start', 'End', 'duration', 'Company URL', 'Company Name', 'Company Location', 'Current Title', 'Current Job Desp.']]
sheet2_data = [['Profile ID', 'Skill Name', 'Endorsements']]
pwd = 'babushona13'
cookie = 'JSESSIONID=ajax:8568514931401773276; bcookie="v=2&5e642870-bae7-4d7d-86f2-a88f4250c1c4"; bscookie="v=1&20180217075906d4de8175-476a-43d3-8a59-addca01437f2AQGQfAavP6iKl8lQZv-IXl-DC48s83M8"; _ga=GA1.2.282991545.1518854461; _gat=1; liap=true; sl=v=1&rjBnu; li_at=AQEDASYTMb4CJh5fAAABYaLGmvAAAAFhxtMe8FEABxu2YSdDYNem9Kzqsno0INDJvKpIATkdK6jFVCaCll6pb3-AUfVKCU-4xihWCpO7qR0Itk144Zq95gsCoad_R1OY4U576LRQfdl4h9-kB9gUitqy; RT=s=1518854493911&r=https%3A%2F%2Fwww.linkedin.com%2F; visit="v=1&M"; lang="v=2&lang=en-us"; _lipt=CwEAAAFhosfvERUXFq-oVDIW0-y6Vn6SbAFbSwzadan08wcYFjqvhpp42snOqhqkpzIzpsC6tKbB7NC7JpRjl1khbwzOYI5th30JIiXKy_qZ3_J2F0bhnrNF9dA; lidc="b=SGST01:g=3:u=1:i=1518854467:t=1518940780:s=AQF07H7sYt4pyYmC1skt6-G_7qN4aZXL"'

manual_data = [
    {'url': 'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B"my%3A0"%5D&keywords=Telecommunications&page=', 'keyword': 'Telecommunications', 'total_result': 61774, 'pid_prefix': 'TC_%d', 'location': 'MY'},
    {'url': 'https://www.linkedin.com/search/results/people/?keywords=Axiata%20Digital&page=', 'keyword': 'Axiata Digital', 'total_result': 445, 'pid_prefix': 'AD_%d', 'location': 'Global'},
]


unique_set = set()
company_data = {}

files = []


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


def get_profile_list(item, index):
    global P_ID, sheet0_data, unique_set
    url = item['url'] + str(index)
    print(url)

    raw_reg = '"firstName":"(.*?)","lastName":"(.*?)".*?"occupation":"(.*?)".*?"objectUrn":"(.*?)".*?"publicIdentifier":"(.*?)"'
    html = get_request(url)
    profiles = re.compile(raw_reg).findall(html)

    for profile in profiles:
        try:
            fir_name = profile[0]
            if 'firstName' in fir_name:
                fir_name = fir_name.split('firstName":"')[-1]
            las_name = profile[1]
            name = ' '.join([fir_name, las_name])
            if name == 'Ahana Mukherjee' or name == 'Zhao Dan':
                continue
            member_id = profile[3]
            occupation_company = profile[2].split(' at ')
            occupation = occupation_company[0]
            company = occupation_company[-1]
            personal_url = 'https://www.linkedin.com/in/' + profile[4]
            if personal_url in unique_set:
                continue
            unique_set.add(personal_url)
            profile_id = item['pid_prefix'] % P_ID
            one_row = [item['keyword'], item['location'], item['total_result'], profile_id, name, personal_url, occupation, company]
            sheet0_data.append(one_row)
            P_ID += 1
        except urllib2.HTTPError as e:
            if e.code == 302:
                return 0
        except Exception as e:
            print str(e)
            print 'ERR---level 1---' + url
    return len(profiles)


def request_profile(profile_id, personal_url):
    personal_html = get_request(personal_url)
    profile_details = request_profile_detail(personal_html)

    # get_endorse_details(profile_id, personal_url)
    return profile_details


def request_profile_detail(html):
    start_date = [1970, 1]
    current_job = ['N/A', 'N/A']
    company_url = 'N/A'
    follower_count = 0

    follower_reg = '"followersCount":(.*?),'
    follower_data = re.compile(follower_reg).findall(html)
    if follower_data:
        follower_count = int(follower_data[0])
    summary_reg = '"summary":"(.*?)".*?"locationName":"(.*?)"'
    summary_data = re.compile(summary_reg).findall(html)
    if summary_data:
        location = summary_data[0][1]
        summary_data = summary_data[0][0]
    else:
        summary_data = ''
        location = ''
    data_reg = '\{"data":\{"patentView"(.*?)\}\]\}'
    data_str = re.compile(data_reg).findall(html)
    if data_str:
        data_str = '{"data":{"patentView"' + data_str[0] + '}]}'
        data_obj = json.loads(data_str)
        type_lists = {}
        for item in data_obj.get('included', []):
            div_type = item.get('$type', '')
            value = type_lists.get(div_type, [])
            value.append(item)
            type_lists[div_type] = value
        date_list = type_lists['com.linkedin.voyager.common.DateRange']

        lastest_start_date = 'N/A'
        for date_item in date_list:
            if 'endDate' in date_item.get('$deletedFields', []) and 'urn:li:fs_position' in date_item.get('$id'):
                lastest_start_date = date_item.get('startDate', '')
                break

        if lastest_start_date != '':
            start_end_item = type_lists['com.linkedin.common.Date']
            for item in start_end_item:
                if lastest_start_date == item.get('$id', ''):
                    start_date = [item.get('year', 1970), item.get('month', 1)]
                    break

        jobs_list = type_lists['com.linkedin.voyager.identity.profile.Position']
        entry_id = lastest_start_date.split(',timePeriod')[0]
        for job in jobs_list:
            if entry_id == job.get('entityUrn'):
                current_job = [job.get('companyName', ''), job.get('locationName', ''), job.get('title', ''), job.get('description', '')]
                company_id = job.get('companyUrn', '').split(':')[-1]
                company_url = 'https://www.linkedin.com/company/%s/' % company_id
                break
        if start_date[0] == 1970:
            duration = 0
        else:
            duration = (2018 - start_date[0] - 1) * 12 + (12 - start_date[1]) + 2

    return [location, follower_count, summary_data, '%d/%d' % (start_date[1], start_date[0]), 'Present', duration, company_url] + current_job


def get_endorse_details(profile_id, url):
    global sheet2_data
    endorse_url = 'https://www.linkedin.com/voyager/api/identity/profiles/%s/featuredSkills?includeHiddenEndorsers=true&count=50' % url.split('/')[-1]
    html = get_request(endorse_url)
    data_obj = json.loads(html)

    for item in data_obj.get('elements', []):
        one_row = [profile_id, item['skill']['name'], item['endorsementCount']]
        sheet2_data.append(one_row)


def get_date(timestamp):
    try:
        ret = datetime.fromtimestamp(int(timestamp)/1000).strftime('%d/%m/%Y')
        return ret
    except:
        return 'N/A'


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def urllib_request(get_url):
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    # req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.linkedin.com/')
    req.add_header("Cookie", cookie)
    # req.add_header('csrf-token', 'ajax:8568514931401773276')
    req.add_header('upgrade-insecure-requests', '1')
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return HTMLParser.HTMLParser().unescape(res)


def get_request(url):
    header = {
        'cookie': cookie,
        'csrf-token': 'ajax:8568514931401773276',
    }
    res_data = requests.get(url, headers=header)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return HTMLParser.HTMLParser().unescape(res)


def request_company(url):
    company_reg = '"staffCount":(.*?),.*?"industries":(.*?),'
    html = get_request(url)
    staff_ind_list = re.compile(company_reg).findall(html)
    staff_count, industy = 0, []

    if staff_ind_list:
        staff_count = staff_ind_list[0][0]
        industy = json.loads(staff_ind_list[0][1])
    return staff_count, industy


def read_excel(filename, start=1):
    global company_data
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            stored_data = [row[j].value for j in range(6)]
            profile_url = stored_data[5]
            details = request_profile(stored_data[3], profile_url)
            one_row = stored_data + details
            print(one_row)
            sheet1_data.append(one_row)
        except Exception as e:
            print(str(e))
            print(i)


reload(sys)
sys.setdefaultencoding('utf-8')

# scrape profile data
read_excel('data/Employed_0_Axiata Digital.xls', start=293)
write_excel('data/res1.xls', sheet1_data)
write_excel('data/res2.xls', sheet2_data)
