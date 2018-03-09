# -*- coding: utf-8 -*-
import re
import xlwt
import sys
from datetime import datetime
from html.parser import HTMLParser
import html
import os
import xlrd
import requests
import json
import time
import ssl

P_ID = 378
sheet0_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Title', 'Company']]
sheet1_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Personal Location', 'Followers', 'Self Desp.', 'Start', 'End', 'duration', 'Company URL', 'Company Size', 'Company Name', 'Company Location', 'Current Title', 'Current Job Desp.']]
sheet2_data = [['Profile ID', 'Skill Name', 'Endorsements']]
company_data = []
pwd = 'babushona13'
cookie = 'bcookie="v=2&a2c264bf-22f6-4e04-8e45-ea33a1a215c3"; bscookie="v=1&201801170600573d40b408-6b30-455f-872a-d3dfab037411AQEeUoBXCefKKDrESZX4DdNmjYJciPRv"; _ga=GA1.2.1722318312.1516173771; visit="v=1&M"; lang="v=2&lang=en-us"; mobilesplash=1519783881259; JSESSIONID="ajax:2154262542411227916"; chp_token=AQFI7SwqHyvvcAAAAWHaOepgMSPBtrBWhyftJijhm1DTwVkjVmZWYfZR-FkLoooixmRgLAXWU0F1ZxTjfutZOVUFZA; liap=true; li_at=AQEDARo-DEsBU6Z9AAABYeDD0W0AAAFiLYJ86lEAEdPhQDwtOA-of5jo0VnZ4cSZcpp6lsFVzBrWhRCtOacI5DbuTJvnmYnNlXmH321u7K46v04R8T51BtIk72UwZ4VcdqC9e7xwtnVCdjch0Q8ahKj6; sl="v=1&BxB09"; _gat=1; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; _lipt=CwEAAAFiCXYFW-YG12u9bYl8DvntUl3K0-lqxhbhJFk1qiJIIXXCh2hO1ujVuNiLZkPNBwNftRab4-GGjtnNCEQ0nCK7tOHTP_YwivEue4eBvC2tSjN2me7oWBPcdK0wDW2wOk-WuwgRY1r6km92-LFmasH6QmlN3_y6mPW7s2VoS_3jHYpBoP5M4x520Jl9XH9egrop--2fuN4k2_tbUkqZGARrmhFXqU6x-DFcpGxfrSlqgqiLdRlhVm_akAXXUYfSCEff3nYhnXIlS20M8Viu5BCU7NGWcfZ_PjHjS52KNNi5BI-fDixXA5KAwxlB_62fLsHw_meRugDZDbq-qV8EPB7khp5yqP1SyaJhygxkEYrHpQj0KZWv; lidc="b=VGST01:g=737:u=1:i=1520577152:t=1520663552:s=AQGgmg-qRjCCZekEdu1xgFFyVIjDSpdy"'
csrf = 'ajax:2154262542411227916'

manual_data = [
    {'url': 'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B"id%3A0"%5D&keywords=Digital%20Financial%20Services&page=', 'keyword': 'Digital Financial services', 'total_result': 6971, 'pid_prefix': 'DFS_%d', 'location': 'ID'},
    {'url': 'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B"id%3A0"%5D&keywords=Digital%20advertising&page=', 'keyword': 'Digital advertising', 'total_result': 32248, 'pid_prefix': 'DA_%d', 'location': 'ID'},
    {'url': 'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B"id%3A0"%5D&keywords=Telecommunications&page=', 'keyword': 'Telecommunications', 'total_result': 98765, 'pid_prefix': 'TC_%d', 'location': 'ID'},
]

company_size = {}


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
        except Exception as e:
            print(str(e))
            print('ERR---level 1---' + url)
    return len(profiles)


def request_profile(profile_id, personal_url):
    personal_html = get_request(personal_url)
    profile_details = request_profile_detail(personal_html)

    get_endorse_details(profile_id, personal_url)
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
    employee_count = 0

    return [location, follower_count, summary_data, '%d/%d' % (start_date[1], start_date[0]), 'Present', duration, company_url, employee_count] + current_job


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


def get_request(url):
    header = {
        'cookie': cookie,
        'csrf-token': csrf,
    }
    res_data = requests.get(url, headers=header)
    res = res_data.content.decode("utf-8")
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return html.unescape(res)


def request_company(url):
    company_reg = '"staffCount":(.*?),'
    html = get_request(url)
    staff_ind_list = re.compile(company_reg).findall(html)
    staff_count = 0

    if staff_ind_list:
        staff_count = staff_ind_list[0]
    return staff_count


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


def read_company_url(filename, start=1):
    global company_size, company_data
    print('process -> ' + filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            company_url = row[12].value
            staff_count = int(row[13].value)
            if company_url == 'N/A' or company_url == 'https://www.linkedin.com/company//':
                staff_count = 0
            elif staff_count <= 0:
                staff_count = company_size.get(company_url, -1)
                if staff_count == -1:
                    staff_count = request_company(company_url)
                    company_size[company_url] = staff_count
            print([company_url, staff_count])
            company_data.append([company_url, staff_count])
        except Exception as e:
            print(str(e))
            print(i)


def request_sheet0():
    global sheet0_data, P_ID
    for item in manual_data:
        for i in range(1, 50):
            get_profile_list(item, i)
        write_excel('data/sheet0_%s.xls' % item['keyword'], sheet0_data)
        del sheet0_data
        sheet0_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Title', 'Company']]
        P_ID = 1


def request_company_size():
    global company_data
    files = walk('data/Employed')
    for filename in files:
        read_company_url(filename)
        write_excel(filename.replace('.xls', '_com.xls'), company_data)
        del company_data
        company_data = []


# scrape profile data
# step 1: profile data
# request_sheet0()
# step 2: profile details
read_excel('data/sheet0_Digital Financial services.xls', start=P_ID)
write_excel('data/res1.xls', sheet1_data)
write_excel('data/res2.xls', sheet2_data)

# step 3: company size
# request_company_size()

