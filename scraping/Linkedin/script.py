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
import sets

P_ID = 1
sheet1_data = [['ID', 'Key Words', 'Name', 'Personal page', 'Occupition', 'Company', 'Location']]
sheet2_data = [['ID', 'url', 'content', 'date', 'Comments', 'Likes', 'Total Engagement']]

cookie = 'bcookie="v=2&94ede669-f96d-4d7f-88df-20bb8b9ed56c"; bscookie="v=1&201608050319286fb0d9d7-11eb-4c4f-853f-2819c04ac829AQHDI3jFjJtWbtizwwj8_RtdcWBWfmiO"; visit="v=1&M"; _chartbeat2=Va5crvXhgBBqAl5L.1476436594042.1476440427196.1; __utma=226841088.1514381064.1470817606.1483846988.1487305243.2; __utmz=226841088.1483846988.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); bspNotice=2%7CMozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_10%3B%20rv%3A33.0)%20Gecko%2F20100101%20Firefox%2F33.0; sl="v=1&OpLtf"; lang="v=2&lang=en-us"; liap=true; li_at=AQEDARo-DEsFFm8GAAABW80RLFMAAAFbzsigU04AP1qR1JoVYgGjG754eAqlMIp8WUO27gM7Lf6PpexqeQSShKp90HvDNqhOdDf9xTbHH__WQVlDpIxUZmsPjYRBQkYu3qaqPDHsOmiooqj3mPgYua-x; JSESSIONID="ajax:3940183104206872464"; _ga=GA1.2.1514381064.1470817606; lidc="b=TB95:g=558:u=41:i=1493794142:t=1493840426:s=AQFdf_38OCduusH1eRon4dV5M_Xbo3f9"; _lipt=CwEAAAFbzR7VZ_HyrFE0wYpC0KsSdZl42Klrip4sfjMollqcZ6hPdLle6HcafPV4x_WKUOMtOEl74b_TGYWCqi60kd429nHfqQjtTT8m3Es0akRw0J4mRnpBifpnx7iWpa_zHJWQTJtEjYxJsTuW7Ckzv3YcCxCSTwN0T0AYj2pQ1yxzY1GaCo03hFVrNEiiPugy1pWAb5-idoW0Sn-ejpUSAXSqdk3KdLwzja2RgakQUo8tvcYfKhr-Jt4o1ZFL8Omn8Ygt8dXGcysbEYZpfdBK5nBSZWAUgSPLthcahGnOm6pVlcocU8a8VrjkGjYF4Cs3yVImTBPNOALbNXnA9QIIfsR23OCHMNkYNwNWFgmw3dO0qA'

urls = [
    'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22cn%3A0%22%2C%22in%3A0%22%2C%22sg%3A0%22%2C%22id%3A0%22%2C%22th%3A0%22%5D&keywords=employee%20retention&page=',
    'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22in%3A0%22%2C%22sg%3A0%22%2C%22cn%3A0%22%2C%22id%3A0%22%2C%22th%3A0%22%5D&keywords=employee%20productivity&page=',
]
key_words = [
    'employee retention',
    'employee productivity',
]

unique_set = set()

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
    global sheet1_data, P_ID, unique_set
    raw_reg = '"firstName":"(.*?)","lastName":"(.*?)".*?"occupation":"(.*?)".*?"objectUrn":"(.*?)".*?"publicIdentifier":"(.*?)"'
    html = get_request(url)
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
            if personal_url in unique_set:
                continue
            unique_set.add(personal_url)
            one_row = [P_ID, key_word, name, personal_url, occupation, company, location]
            sheet1_data.append(one_row)
            P_ID += 1
            # request_sheet2(P_ID, personal_url)
        except:
            print 'ERR---level 1---' + url


def get_token(html):
    pagenation_reg= '\{"paginationToken":"(.*?)"'
    token = re.compile(pagenation_reg).findall(html)
    if len(token) > 0:
        return token[0]
    return ''


def get_sheet2_data_by_json(html, id):
    resp_obj = json.loads(html)
    token = resp_obj.get('metadata', {}).get('paginationToken', '')
    posts = resp_obj.get('elements', [])
    for post in posts:
        post_link = post.get('permalink', '')
        like_comment = post.get('socialDetail', {}).get('totalSocialActivityCounts', {})
        like = like_comment.get('numComments', 0)
        comment = like_comment.get('numLikes', 0)
        content_values = ''

        value = post.get('value', {})
        date = 'N/A'
        for k, v in value.items():
            if v.get('createdTime'):
                date = get_date(v['createdTime'])
            if v.get('content'):
                content_values = get_text_from_content(v.get('content'))
            if v.get('text'):
                values = v.get('text').get('values',[])
                for value in values:
                    content_values += value.get('value', '')
            if 'Reshare' in k:
                new_value = v.get('originalUpdate', {}).get('value', {})
                for new_k, new_v in new_value.items():
                    if new_v.get('content'):
                        content_values += get_text_from_content(new_v.get('content'))

        one_row = [id, post_link, content_values, date, like, comment, int(like)+int(comment)]
        sheet2_data.append(one_row)

    return token


def get_text_from_content(ori):
    content = ori
    for kk, vv in content.items():
        if vv.get('text'):
            content_values = vv['text'].get('values', [''])[0]
            if content_values != '':
                content_values = content_values.get('value', '')
            return content_values
    return ''


def get_sheet2_data(uid, html, base_url, flag):
    if flag == 0:
        return get_sheet2_data_by_json(html, uid)
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
            one_row = [uid, base_url, text, date, like_count, comment_count, int(like_count) + int(comment_count)]
            # sheet2_data.append(one_row)
    return token


def request_sheet2(base_url, uid):
    global sheet2_data
    url = base_url
    profile_id = ''
    starter = 5
    flag = 1
    while True:
        print url
        html = get_request(url)
        token = get_sheet2_data(uid, html, base_url, flag)
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
    req.add_header('csrf-token', 'ajax:3940183104206872464')
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
            id = row[0].value
            request_sheet2(profile_url+'/recent-activity/', id)
            request_sheet2(profile_url+'/recent-activity/shares/', id)
        except:
            print(i)


reload(sys)
sys.setdefaultencoding('utf-8')

# request_sheet2('https://www.linkedin.com/in/kanikaagarwaltech/recent-activity/shares/', 'id')

filename = 'data/employee_productivity.xls'
read_excel(filename)
write_excel('data/res1.xls', sheet2_data)

# for i in range(len(key_words)):
#     key_word = key_words[i]
#     filename = 'data/' + key_word.replace(' ', '_') + '.xls'
#     for j in range(1, 100):
#         url = urls[i] + str(j)
#         request_sheet1(url, key_word)
# write_excel(filename, sheet1_data)

