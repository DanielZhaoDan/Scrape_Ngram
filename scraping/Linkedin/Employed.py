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
sheet1_data = [['Keyword+Name', 'Key', 'keyword', 'name', 'skill', 'endorsed', 'URL', 'Title', 'Company', 'Company URL', 'Followers', 'Start', 'End', 'Current Title', 'Current Job Desp.', 'Company-Size', 'Industry']]

cookie = 'bcookie="v=2&2f6c9444-0b2f-466a-8183-ef73e05efa35"; bscookie="v=1&2017041006541990b97a3b-1e52-4da3-8e47-33e0e8e1e3aeAQGgvnt_FYPCpH58BfQhdPydnY6jBTcZ"; visit="v=1&M"; _chartbeat2=DCi2d9ksmx1CfcAv5.1493951580217.1493951580225.1; __utma=226841088.610623672.1491807398.1497595445.1497595445.1; __utmz=226841088.1497595445.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __ssid=ade20105-3abb-46d5-9567-d3cd78c040fd; _ga=GA1.2.610623672.1491807398; lang="v=2&lang=en-us"; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; JSESSIONID="ajax:0010415414095958648"; sl="v=1&9fQlp"; liap=true; li_at=AQEDAQFnLMYEd1B_AAABX-caGSIAAAFgCyadIlEAZ5ohDb7tbXInfVWkMMOiw6fBXiujxlAHCtAGwk-H5A4qDF1aQK9D2RfibWLusH81uFFEtZz7kf_qLbRe4YrhuOc27TQ2d_1WWt_ONRxLMN1L50g1; _gat=1; lidc="b=TB86:g=856:u=53:i=1511421006:t=1511500062:s=AQESfYlixoH7uOMt8bQAd2xrE7XoFmKe"; _lipt=CwEAAAFf57owjFN1lEwq9FhY1k5KqNVLrrxQGUoVHoOoylf5y9feQEsdkpkmSU4DHStBnzQPSKusTWYFMX5IXqa7bx_eokUkV5HNbU4CooHudg8ig35k3VGcAKnNBFGm5vKADPiBXII1FBfzM1cRhuWU447fi3nS2bzTRMhdSpikFvAbsIGlqVtSzFAkvfMDto4hwiY7KMq0s1SVzzhppPcG5GSH48s2mshkB2D9e2wd5GuVg7Z8t__K2B0cEZl9iDENIRwv-P8mdU-FHeUygorX6-tgE82h26k5GUzi3LoNENI9kR-GhGwEeaEf804TvhHGFr_xpSqEdtJX_Z0FxGC83uRD57SvEJLYBiyg5bcX5fdn9_p8xMV7AoU9tRuOGJSZzQ'

urls = [
    # 'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22sg%3A0%22%5D&keywords=FX&page=',
    'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22sg%3A0%22%5D&keywords=Foreign%20Exchange&page=',
    'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22sg%3A0%22%5D&keywords=International%20payments&page=',
]
key_words = [
    # 'FX',
    'Foreign Exchange',
    'International payments',
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


def request_sheet1(url, key_word):
    print url
    global sheet1_data, P_ID, unique_set
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
            if name == 'Ahana Mukherjee':
                continue
            member_id = profile[3]
            occupation_company = profile[2].split(' at ')
            occupation = occupation_company[0]
            company = occupation_company[-1]
            personal_url = 'https://www.linkedin.com/in/' + profile[4]
            if personal_url in unique_set:
                continue
            unique_set.add(personal_url)
            personal_html = get_request(personal_url)
            profile_details, company_url = request_profile_detail(personal_url, personal_html)

            skill_list = get_endorse_details(personal_url, personal_html)

            if company_url == 'N/A':
                staff_count, industries = 0, []
            else:
                if company_data.get(company_url):
                    staff_count, industries = company_data.get(company_url)
                else:
                    staff_count, industries = request_company(company_url)
                    company_data[company_url] = [staff_count, industries]

            if not industries:
                industries = ['N/A']

            if not skill_list:
                skill_list = [['N/A', 0]]

            for industry in industries:
               for item in skill_list:
                    skill = item[0]
                    one_row = ['%s_%s' % (key_word, name), '%s_%s' % (name, skill), key_word, name, skill, item[1], personal_url, occupation, company, company_url] + profile_details + [staff_count, industry]
                    sheet1_data.append(one_row)

        except Exception as e:
            print str(e)
            print 'ERR---level 1---' + url


def request_profile_detail(url, html):
    start_date = [1970, 1]
    current_job = ['N/A', 'N/A']
    company_url = 'N/A'
    follower_count = 0

    follower_reg = '"followersCount":(.*?),'
    follower_data = re.compile(follower_reg).findall(html)
    if follower_data:
        follower_count = int(follower_data[0])
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
                current_job = [job.get('title', ''), job.get('description', '')]
                company_id = job.get('companyUrn', '').split(':')[-1]
                company_url = 'https://www.linkedin.com/company/%s/' % company_id
                break

    return [follower_count, '%d/%d' % (start_date[1], start_date[0]), 'Present'] + current_job, company_url


def get_endorse_details(url, html):
    endorse_url = 'https://www.linkedin.com/voyager/api/identity/profiles/%s/featuredSkills?includeHiddenEndorsers=true&count=50' % url.split('/')[-1]
    html = get_request(endorse_url)
    data_obj = json.loads(html)
    ret = []

    for item in data_obj.get('elements', []):
        one_row = [item['skill']['name'], item['endorsementCount']]
        ret.append(one_row)
    return ret


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
    req.add_header('csrf-token', 'ajax:0010415414095958648')
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
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

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            profile_url = row[3].value
            id = row[0].value
            # request_sheet2(profile_url+'/recent-activity/', id)
            # request_sheet2(profile_url+'/recent-activity/shares/', id)
            companys = request_company(profile_url)
            one_row = [row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value] + companys
            company_data.append(one_row)
            if i % 400 == 0:
                write_excel('data/res'+str(i)+'.xls', company_data)
        except:
            print(i)


reload(sys)
sys.setdefaultencoding('utf-8')

# scrape profile data

for i in range(len(key_words)):
    key_word = key_words[i]
    for j in range(1, 50):
        url = urls[i] + str(j)
        request_sheet1(url, key_word)
    write_excel('data/1Employed_%s.xls' % key_word, sheet1_data)
    del sheet1_data
    sheet1_data = [
        ['Keyword+Name', 'Key', 'keyword', 'name', 'skill', 'endorsed', 'URL', 'Title', 'Company', 'Company URL',
         'Followers', 'Start', 'End', 'Current Title', 'Current Job Desp.', 'Company-Size', 'Industry']]