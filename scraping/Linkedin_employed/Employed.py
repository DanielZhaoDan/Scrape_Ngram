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
sheet1_data = [['Keyword+Name', 'Key', 'keyword', 'name', 'skill', 'endorsed', 'URL', 'Title', 'Company', 'Company URL', 'Followers', 'Start', 'End', 'Current Title', 'Current Job Desp.', 'Company-Size', 'Industry']]
pwd = 'babushona13'
cookie = 'bcookie="v=2&a2c264bf-22f6-4e04-8e45-ea33a1a215c3"; bscookie="v=1&201801170600573d40b408-6b30-455f-872a-d3dfab037411AQEeUoBXCefKKDrESZX4DdNmjYJciPRv"; _ga=GA1.2.1722318312.1516173771; visit="v=1&M"; lang="v=2&lang=en-us"; sdsc=22%3A1%2C1518836114040%7ECONN%2C0Cu%2BJACrk78B3WoQ%2BWzgyhvq3g7k%3D; JSESSIONID="ajax:1666134097818962763"; join_wall=v=3&AQFZwa7E8U7ZsAAAAWGiA4NtzsuUCEn_rbkXPvaSP-5Od1uD78moVQD9NXQNjQLYQzkpKnCfduQRqbh-XKUn4ZzHK7jSzGsGR061HZjUmDEBgzY9Up5r2YAkKKfNoQ-_KAmzaC5ydRM9dLlOGuv_Xe-Dr9CzfRkemuAE1o1ZQL5yro_NqtwPUAxTvWNw6DnZnD-AbLAiX1LYk41-Vyo; _gat=1; leo_auth_token="GST:9NtV1IVXj3VhO-xnFBpi5cD5A0wuSY2h5xHrUp-X7ZGp9yNhkdgxFX:1518844903:e395a9ace150a975367c363898564859a3123f90"; sl="v=1&KDRH8"; li_at=AQEDARo-DEsE5BvdAAABYaI2AQAAAAFhxkKFAFEAbbPO41Tyc4j3gnbOOU0kPeWznNzaSme0Z65a_Tnsa01MWU4nDQsP8ssZjf8uFTtRLDQrV5TE0jBanK-RDnSPOs-XGiaiuL_qSDsolYVt1zyqk3lM; liap=true; RT=s=1518845017730&r=https%3A%2F%2Fwww.linkedin.com%2F; _lipt=CwEAAAFhojaBuqwnE1HKAGEiXjfM96e9m5fBgMVSJVDCQHFh_LanAYXJe3xFkVn2GbBkIMvRAbQsV0ELvcDoJdwX5w8Wp8lzH0y_NW8L6qx88ucwdKKGRRpRxxkTDQVFmKggt_d_KpE7OJ1ODOgJgPlYjqoBwSM6kBOGjq0NAgVqWevSyZFJ7RWH03gSBz8cPIZoYdy0s3XLcvrwBdwNsJaMezctI3C6okngqd7MCLKPPlmX3x4UZNuu2E6OqnbJ8dMzuKWst0K2_OKdpJ-5LQWWG9UU26XuIXHfVK8nsrOPTW_SaxGuWW1cp28eSzR56fsGjHS591Bri0Xd_PXSkOAakMnU2ho9CjcPqXSBZGsM; lidc="b=SB95:g=44:u=75:i=1518844959:t=1518922482:s=AQE4Noczc5HiH0TSYIMGcHiaXTg6qRs1"'

urls = [
    # 'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22my%3A0%22%5D&keywords=adax&page=',
    'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B"my%3A0"%5D&keywords=Telecommunications&page=',
    # 'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22sg%3A0%22%5D&keywords=Digitalization&page=',
]
key_words = [
    'khazanah nasional',
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
        except urllib2.HTTPError as e:
            if e.code == 302:
                return 0
        except Exception as e:
            print str(e)
            print 'ERR---level 1---' + url
        time.sleep(5)
    return len(profiles)


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
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.linkedin.com/')
    req.add_header("Cookie", cookie)
    # req.add_header('csrf-token', 'ajax:1666134097818962763')
    res_data = urllib2.urlopen(req, timeout=10, context=ctx)
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
stop = False
for i in range(len(key_words)):
    key_word = key_words[i]
    if stop:
        break
    for j in range(1, 30):
        try:
            url = urls[i] + str(j)
            count = request_sheet1(url, key_word)
            if count == 0:
                break
        except urllib2.HTTPError as e:
            if e.code == 302:
                stop = True
    write_excel('data/Employed_%s.xls' % key_word, sheet1_data)
    del sheet1_data
    sheet1_data = [
        ['Keyword+Name', 'Key', 'keyword', 'name', 'skill', 'endorsed', 'URL', 'Title', 'Company', 'Company URL',
         'Followers', 'Start', 'End', 'Current Title', 'Current Job Desp.', 'Company-Size', 'Industry']]