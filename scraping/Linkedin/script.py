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

cookie = 'bcookie="v=2&74219b48-1ccd-4aeb-8466-f59864535f9c"; bscookie="v=1&201608091552185c8d9623-6d9e-4a35-8691-d110a1d88056AQGZm-7AEvD7o3e2bz1bNcK_8yK41Y9o"; visit="v=1&M"; lang="v=2&lang=en-us"; sl="v=1&F_2qT"; liap=true; li_at=AQEDARo-DEsCI0uZAAABW8m1X-gAAAFby2zT6FEAAAXdq8FT4mNWPYo_OfB8y_joJ3DNMPRjcbFafPSbGDkCB5BMqlH4upEj-J8Oe6uZ6ZiOTh0isc-LoTshKYcSPsBGZB_ILDlomzM5CaQZ9ao3TVT6; JSESSIONID="ajax:7848834846581413184"; _ga=GA1.2.1479882839.1470758235; lidc="b=SB95:g=22:u=40:i=1493738537:t=1493824142:s=AQE38-7rNvuBDh_yIv1ef5Waha1TO2Dm"; _lipt=CwEAAAFbycf7giVcJ6qCOkjgSY34TmRhFdWAjp4luw1A73wZEg5tGqgEDj76OOcXi26O-heZroSYLUsh4Fpmjv0irDlqnFJgxEB61XfKXC5AmWu0F2iuePH4gMm75hRqL0rZEgs6X7G_-8yTa9JLPovYkqW2ZM5qf7gML13asjDml4ujrNNkqWrTcQeijAT8BW0Hn4iJ8eeB4phpozrT9wUu8LgQn7yR5ZHAlzTd2Bss8JRMaKgQGk5POUwjfJDnLZFGyOQ69t0n5nxQI4ucOeoNw98avS4uBrPayZzMpIZ6dnjLMNeTG5VnaGzil36FP_K9_dCvcmdPsBTSCliswVVl143CHfgu6v1j5GG9QZlqI43D9I3CtNr4Ag7zJHeC0FQR3Ye7sWMFH5Na9wEedrMmv-5NvXCW_4TdwtOKbiexkztqfoY28vHAWA3kOvcbUHsBKjUm1H636ZQ0WOJrUDhEtBaCUL7w17QAYZLhr8568A2hA4jOdfz1wYAy2CQv2RWNvKh7lYPCoTDbTMf13TlhuvuusFANipT6eQ1QG2DTRS-bG9Ubz_KiduUawiSKtjRVReIod72sh08tb38m7ifR5GJAQKZHcEHVC1cKc-ek3EIH8pQA2E7iCwc8XRFoi_A2XT9oCF4f8E6TlB2j5fDdf35Kezk5dkBSW0AvbvUevOFftkyo5r8wtZvMyRKKIwI4efVyJtSsji9PJZqfUbf_HyYrnLG5PiPBN1UK33pcEORBnfJe9BQ2m3WJ_yNJrdd7RdE28OHYXL74XYOm54fpAiCLoneL8nUqMzlH2P2kNwxZ2xnLJft_2_rnXRx6aI0G1ieWUgfWm8mbMTIU1-Ya2LBpfJ4P5CDAlgccgTHs95eoUTV83BIQjwp3_KmVlpU6Zzlx3MOnRFicHPAs20cr0dnLFFHnhbfc3vcFMHjRF-j3ylJQHto43q87gvUxOJeu_a9tXfiJpNeaSDZ3D-gLYa2RQELvEHOwnyjTGWV7DJlecPnNMyOaEsb199b9Rnm6zhTAGMUfun0mNlNc3qWCqOlG0JywjCSV9RqHoF4qTeIL7oBhmmnXHf7eIU5YuzqXo-pW139bsgPzxgS5hmn5Kwm1igIxVOG2e4Z_bx7L_WpVwaKLV8_0T8tULYCv-dUrP-2Lvub7lNUQBI-hT2te4Uu0lTVHOxHVcXg'

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
        write(html, str(starter)+'.html')
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
request_sheet2('https://www.linkedin.com/in/kanikaagarwaltech/recent-activity/shares/')

# filenames = walk('data')
#
# for filename in filenames:
#     read_excel(filename)
#     write_excel(filename.replace('sheet1', 'sheet2'), sheet2_data)
#     sheet2_data = [['url', 'content', 'date', 'Likes', 'Comments']]
