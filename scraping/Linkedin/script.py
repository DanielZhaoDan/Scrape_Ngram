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

P_ID = 1
sheet1_data = [['ID', 'Key Words', 'Name', 'Personal page', 'Occupition', 'Company', 'Location']]
sheet2_data = [['url', 'content', 'date', 'Likes', 'Comments']]

cookie = 'bcookie="v=2&74219b48-1ccd-4aeb-8466-f59864535f9c"; bscookie="v=1&201608091552185c8d9623-6d9e-4a35-8691-d110a1d88056AQGZm-7AEvD7o3e2bz1bNcK_8yK41Y9o"; visit="v=1&M"; join_wall=v=2&AQHGNl4BBq9GOAAAAVt3jR2WyM_EPzUNytO02L3Zstuq5G80RQUH17hnPqEIbwQYd-9a0cs8n0gMsX0tyD2GR1sM0B-sNCOk-06Q9ldyi_caz_t-7Cee-pEESd0zgpGPKVKyIh-EajCNLbF4FthwPZrs; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; _ga=GA1.2.1479882839.1470758235; _gat=1; sl="v=1&hODEf"; JSESSIONID="ajax:7848834846581413184"; liap=true; li_at=AQEDARo-DEsE3XvPAAABW3vD-C0AAAFbfXtsLVEAPtoRvZmDJUIa1iMYJGZiBumX8SZVjZPElVfSjxudmHICi7G3VYr2NYIi02sRki55u8_mt8LkYxdGgNneQLsf77GgTyX_VBxEg2Ue8EzLnzeAk5w0; lang=v=2&lang=en-us; lidc="b=SB95:g=22:u=40:i=1492430093:t=1492516458:s=AQFD7rSJmPOH03KSBFiSLyAQkaUm0Mwe"; RT=s=1492430093582&r=https%3A%2F%2Fwww.linkedin.com%2Fuas%2Fconsumer-captcha-v2%3FchallengeId%3DAQHVIZrU9p3TEAAAAVt7w8vIke3EBrB4m4aCk4IxGflCaaeQBLsL69pPSLZ6WoZyNFAreZ9IONFufFPl_GSuJh7yhmO-llA03g; _lipt=CwEAAAFbe8QTYdaDPrz5rTLdTTB9M7aVfyzaT342_4usMo35BdehjFc2qOGw-srqlePdfS_2jg_VpiqHPdvnKi2gKZXh7qtxO9olZGZ6Kqb5LSIiJHjm0GObQny-_3B4OFb6sYZeQACrxWELqLXg5-miLqWbjb-qfokgWr0fzvQa4KDCawpG5ewb6ONRiqhq-BxS60MnvgKx-Iel-3WedIjCFcHdb0ogRso4yfrCLtNsE2KGVmXXxj5PejRa0VQGHHTN8FrvQEYwUUHXiXpP5tYnNCo4a8IJrja4XuxR3elLM_VBVxlVSy7nqEUZjxYlfn6TQpMWwN-bGcraV6s8w4-ySFczyDNT8fBBvMikQVBlvNgW5w'

urls = [
    'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22cn%3A0%22%2C%22in%3A0%22%2C%22sg%3A0%22%2C%22id%3A0%22%2C%22th%3A0%22%5D&keywords=workforce%20analytics&page=',
    'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22in%3A0%22%2C%22sg%3A0%22%2C%22cn%3A0%22%2C%22id%3A0%22%2C%22th%3A0%22%5D&keywords=hr%20analytics&page=',
    'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22in%3A0%22%2C%22sg%3A0%22%2C%22cn%3A0%22%2C%22id%3A0%22%2C%22th%3A0%22%5D&keywords=hr%20metrics&page=',
    'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22in%3A0%22%2C%22sg%3A0%22%2C%22cn%3A0%22%2C%22id%3A0%22%2C%22th%3A0%22%5D&keywords=hr%20information%20systems&page=',
]
key_words = [
    'workforce analytics',
    'hr nalytics',
    'hr metrics',
    'hr information systems',
]

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


def request_sheet1(url, key_word):
    global sheet1_data, P_ID
    raw_reg = '"firstName":"(.*?)","lastName":"(.*?)".*?"occupation":"(.*?)".*?"objectUrn":"(.*?)".*?"publicIdentifier":"(.*?)"'
    html = HTMLParser.HTMLParser().unescape(get_request(url))
    profiles = re.compile(raw_reg).findall(html)
    location_reg = '"backendUrn":"(.*?)".*?location":"(.*?)"'
    member_location = re.compile(location_reg).findall(html)
    member_loca_dict = {}
    for item in member_location:
        member_loca_dict[item[0]] = item[1]
    if not profiles:
        return
    for profile in profiles:
        try:
            fir_name = profile[0]
            las_name = profile[1]
            name = ' '.join([fir_name, las_name])
            if name == 'Zhao Dan':
                continue
            member_id = profile[3]
            occupation_company = profile[2].split(' at ')
            occupation = occupation_company[0]
            company = occupation_company[-1]
            location = member_loca_dict.get(member_id, '')
            personal_url = 'https://www.linkedin.com/in/' + profile[4]
            one_row = [P_ID, key_word, name, personal_url, occupation, company, location]
            sheet1_data.append(one_row)
            P_ID += 1
            request_sheet2(P_ID, personal_url)
        except:
            print 'ERR---level 1---' + url


def get_token(html):
    pagenation_reg= '\{"paginationToken":"(.*?)"'
    token = re.compile(pagenation_reg).findall(html)
    if len(token) > 0:
        return token[0]
    return ''


def get_sheet2_data(html, id, flag):
    global sheet2_data
    token = get_token(html)
    if token == '':
        return ''
    comment_reg = '"numComments":(.*?),.*?activity:(.*?)".*?"numLikes":(.*?),'
    if flag == 1:
        content_reg = 'deletedFields":\["entity"\],"value":"(.*?)".*?activity:(.*?)\)'
        date_reg = 'createdTime":(.*?),.*?activity:(.*?)\)'
    else:
        content_reg = '\[\{"value":"(.*?)".*?activity:(.*?)"'
        date_reg = 'createdTime":(.*?),.*?activity:(.*?)"'
    comments = re.compile(comment_reg).findall(html)
    contents = re.compile(content_reg).findall(html)
    dates = re.compile(date_reg).findall(html)
    contents_dict = {}
    for content in contents:
        activity_id = content[1]
        text = content[0]
        contents_dict[activity_id] = text
    dates_dict = {}
    for date in dates:
        activity_id = date[1]
        date = get_date(date[0])
        dates_dict[activity_id] = date
    for comment in comments:
        comment_count = comment[0]
        activity_id = comment[1]
        like_count = comment[2]
        text = contents_dict.get(activity_id, '')
        date = dates_dict.get(activity_id, 'N/A')
        if text != '':
            one_row = [id, text, date, like_count, comment_count]
            sheet2_data.append(one_row)
    return token

def request_sheet2(base_url):
    global sheet2_data
    print base_url
    url = base_url
    profile_id = ''
    starter = 5
    flag = 1
    while True:
        html = get_request(url)
        token = get_sheet2_data(html, base_url, flag)
        if token == '':
            break
        if profile_id == '':
            profile_id = get_profile_id(html)
            flag = 0
        url = 'https://www.linkedin.com/voyager/api/feed/updates?count=5&moduleKey=member-shares%3Aphone&paginationToken='+token+'&profileId='+profile_id+'&q=memberShareFeed&start='+str(starter)
        starter += 5
        if starter > 49:
            break
        if profile_id == 'end':
            break


def get_profile_id(html):
    reg = '"profileId":"(.*?)"'
    profiles = re.compile(reg).findall(html)
    if len(profiles) > 0:
        return profiles[0]
    return 'end'

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


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.linkedin.com/')
    req.add_header("Cookie", cookie)
    req.add_header('csrf-token', 'ajax:7848834846581413184')
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return HTMLParser.HTMLParser().unescape(res)


def read_excel(filename, start=1):
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            profile_url = row[3].value
            request_sheet2(profile_url+'/recent-activity/')
            request_sheet2(profile_url+'/recent-activity/shares/')
        except:
            print(i)


reload(sys)
sys.setdefaultencoding('utf-8')

filenames = walk('data')

for filename in filenames:
    read_excel(filename)
    write_excel(filename.replace('sheet1', 'sheet2'), sheet2_data)
    sheet2_data = [['url', 'content', 'date', 'Likes', 'Comments']]




