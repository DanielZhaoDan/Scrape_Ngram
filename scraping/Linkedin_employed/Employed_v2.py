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

P_ID = 1
sheet0_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Title', 'Company']]
sheet1_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Personal Location', 'Followers', 'Self Desp.', 'Start', 'End', 'duration', 'Company URL', 'Company Size', 'Company Name', 'Company Location', 'Current Title', 'Current Job Desp.']]
sheet2_data = [['Profile ID', 'Skill Name', 'Endorsements']]
company_data = []
pwd = 'babushona13'
email = 'tegan.jarin@0hboy.com'
# cookie = 'bcookie="v=2&3e470d6e-fee8-426c-8726-d79eef672dc9"; bscookie="v=1&201701021358090f97fb6d-775b-4655-801b-d9eba782defdAQE25DicscU3FoKVlh4xa_LoXsyFYCNS"; JSESSIONID="ajax:6858942346055442004"; lang="v=2&lang=en-us"; leo_auth_token="GST:ZTjiPE0iIFyoArInCFIb2EA-5rPoRO6pQ9IV7G0rta-lFJs51AyKz0:1523289977:0d498476057ca91d6a34d79d51b0630a1fab085d"; sl="v=1&shQfZ"; liap=true; li_at=AQEDARzXAV8CZ6JJAAABYqsodUsAAAFizzT5S1EAG_srlFPhpaBAS-nJQJ-7o6iu06KarobUduLd8cl9VnEhhVYZN1Q3P8GDiSfvqJYnoURPSu7s3stJc1PZNcPUnmJJuDzdO_xa5iML93pStzfvbf3B; RT=s=1523289978560&r=https%3A%2F%2Fwww.linkedin.com%2Fuas%2Flogin; _guid=739ca3da-4b66-4cda-8799-805ebac3b3b0; _ga=GA1.2.428934987.1523289981; _gat=1; visit="v=1&M"; _lipt=CwEAAAFiqyojDHIdjeKy3crFpztvoTSKrtRJcymIujN_l7memSDT0uh0Yc8sdx2r-7tEP2gi9hY9B1ZdUqARLUEbuTGm932ekbQaYP2Vbq-tYz-jBur1AbiDzDQv-E--at_kZLd30mE-kgrsst5CCtxmnk9-xaEh56ed5S1CUzYAWu_OeTwWjbt3-LIpObK7GEAs3zC7U3GBbaiG4tTkxaJ95tb_gao0MAzMrYKe2lkcmOkH3YMreXnYprRL94npEJUz8aBFIvB7F39EjLIAj-PhTtkO9Ey_Onhumi63I8t1w7Kdqzodir2kP9LMRYRE30tdGHrzq7N9OIjJEsT7Y4332rsbAwpoSfwiVi9zY0OgHjW5i8thDaT8olo; lidc="b=SB39:g=48:u=56:i=1523290340:t=1523335206:s=AQGKuX_g5h5KXALwUCYhkMCsLjTahj4m"'
# csrf = 'ajax:6858942346055442004'
cookie = 'bcookie="v=2&74219b48-1ccd-4aeb-8466-f59864535f9c"; bscookie="v=1&201608091552185c8d9623-6d9e-4a35-8691-d110a1d88056AQGZm-7AEvD7o3e2bz1bNcK_8yK41Y9o"; visit="v=1&M"; _chartbeat2=BJt6ifO0CcmBe3LOe.1500744286051.1500744286064.1; __ssid=33c01209-3fc9-4b43-8b5f-46a7229d7a41; _lipt=CwEAAAFiqGlLFm4uXKMO45-wun8YIHnQzuKik-ykpoN9VoS4BoH53n9QfaeBWZLZx_38T1V4fiQq6NBgh722ZbOFQl4Ed0kGek06SqtVzikJUXzPNGKoTJZH23c; PLAY_SESSION=0d6aaf00389ac14afec669ee410ea4f3789c7fe7-chsInfo=fe832c30-003f-4c21-953e-83f3bc513985+premium_nav_upsell_text; li_at=AQEDASbBeMkFTk3rAAABYqrJXBwAAAFiztXgHFEAxzb_kbtPoO4fO_zW72uLXLLH0gJTkASLoqzV4XDyg9Wp87g6Koj_YuZ5sjX6Drh94_tPQbvwlniAYknFUGWgDOj4JgeqX_xYo5jPFjnBc3TsM7L4; JSESSIONID="ajax:0527940450066958550"; liap=true; _gat=1; lidc="b=SB77:g=48:u=2:i=1523283846:t=1523369541:s=AQGYSooA62ELWoz84g-NVR0pr5uwLXWm"; lang="v=2&lang=en-us"; RT=s=1523283849548&r=https%3A%2F%2Fwww.linkedin.com%2Fpremium%2Fcancel%2Fcomplete; _ga=GA1.2.1479882839.1470758235'
csrf = 'ajax:0527940450066958550'

manual_data = [
    {'url': 'https://www.linkedin.com/search/results/people/?company=&facetGeoRegion=%5B%22id%3A0%22%5D&facetIndustry=%5B%228%22%5D&keywords=digital&page=', 'keyword': 'digital ID', 'total_result': 3896, 'pid_prefix': 'DI_ID_%d', 'location': 'ID'},
]

company_size = {}
unique_set = set()
files = []


def walk(rootDir):
    files = []
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
    print(filename+"===========over============"+str(len(alldata)))


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
    duration = 0
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
    res_data = requests.get(url, headers=header, timeout=8)
    res = res_data.content.decode("utf-8")
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return html.unescape(res)


def request_company(url):
    company_reg = '"staffCount":(.*?),'
    html = get_request(url)
    if len(html) < 1500:
        return -1
    staff_ind_list = re.compile(company_reg).findall(html)
    staff_count = 0

    if staff_ind_list:
        staff_count = staff_ind_list[0]
    try:
        return int(staff_count)
    except:
        return 0


def read_excel(filename, start=1):
    global company_data
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]
    print('process -> '+filename+str(table.nrows))

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
            if 'Expecting value' in str(e):
                break


def read_company_url(filename, start=1):
    global company_size, company_data
    print('process -> ' + filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        company_url = row[12].value
        try:
            staff_count = int(row[13].value)
            if company_url == 'N/A' or company_url == 'https://www.linkedin.com/company//':
                staff_count = 0
            elif staff_count <= 0:
                staff_count = company_size.get(company_url, -1)
                if staff_count <= 0:
                    staff_count = request_company(company_url)
                    time.sleep(2)
                    if staff_count == -1:
                        return -1
                    company_size[company_url] = staff_count
            print([company_url, staff_count])
            company_data.append([company_url, staff_count])
        except Exception as e:
            company_data.append([company_url, 0])
            print(str(e))
            print(i)
    return 1


def request_sheet0():
    global sheet0_data, P_ID
    for item in manual_data:
        for i in range(1, 40):
            try:
                get_profile_list(item, i)
            except Exception as e:
                print(e)
        write_excel('predata/sheet0_%s.xls' % item['keyword'], sheet0_data)
        del sheet0_data
        sheet0_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Title', 'Company']]
        P_ID = 1


def load_pre_company_data(filename):
    global company_size
    print('process -> ' + filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(1, table.nrows):
        row = table.row(i)
        company_url = row[12].value
        size = int(row[13].value)
        if size > 0:
            company_size[company_url] = size


def request_company_size():
    global company_data
    files = walk('data/')
    for filename in files:
        status = read_company_url(filename)
        write_excel(filename.replace('.xls', '_com.xls'), company_data)
        del company_data
        company_data = []
        if status == -1:
            print('=====COOKIE ERROR=====')
            break


def preload_company_size():
    files = walk('finished/')
    for filename in files:
        load_pre_company_data(filename)
    print('preload size: ', len(company_size))



# scrape profile data
# step 1: profile data
# request_sheet0()
# step 2: profile details
# read_excel('predata/sheet0_digital ID.xls', start=P_ID)
# write_excel('data/res1.xls', sheet1_data)
# write_excel('data/res2.xls', sheet2_data)
# step 3: company size
preload_company_size()
request_company_size()

