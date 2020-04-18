# -*- coding: utf-8 -*-
import re
import xlwt
import sys
from datetime import datetime
import html
import os
import xlrd
import requests
import json
import time
import ssl
from scraping.utils import write_excel

P_ID = 1
sheet0_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Title', 'Company']]
sheet1_data = [['Keyword', 'Location', 'Total Result', 'Profile ID', 'Name', 'Profile URL', 'Personal Location', 'Followers', 'Self Desp.', 'Start', 'End', 'duration', 'Company URL', 'Company Size', 'Company Name', 'Company Location', 'Current Title', 'Current Job Desp.']]
sheet2_data = [['Profile ID', 'Skill Name', 'Endorsements']]
company_data = []
pwd = 'babushona13'
email = 'tegan.jarin@0hboy.com'
# cookie = 'bcookie="v=2&3e470d6e-fee8-426c-8726-d79eef672dc9"; bscookie="v=1&201701021358090f97fb6d-775b-4655-801b-d9eba782defdAQE25DicscU3FoKVlh4xa_LoXsyFYCNS"; JSESSIONID="ajax:6858942346055442004"; lang="v=2&lang=en-us"; leo_auth_token="GST:ZTjiPE0iIFyoArInCFIb2EA-5rPoRO6pQ9IV7G0rta-lFJs51AyKz0:1523289977:0d498476057ca91d6a34d79d51b0630a1fab085d"; sl="v=1&shQfZ"; liap=true; li_at=AQEDARzXAV8CZ6JJAAABYqsodUsAAAFizzT5S1EAG_srlFPhpaBAS-nJQJ-7o6iu06KarobUduLd8cl9VnEhhVYZN1Q3P8GDiSfvqJYnoURPSu7s3stJc1PZNcPUnmJJuDzdO_xa5iML93pStzfvbf3B; RT=s=1523289978560&r=https%3A%2F%2Fwww.linkedin.com%2Fuas%2Flogin; _guid=739ca3da-4b66-4cda-8799-805ebac3b3b0; _ga=GA1.2.428934987.1523289981; _gat=1; visit="v=1&M"; _lipt=CwEAAAFiqyojDHIdjeKy3crFpztvoTSKrtRJcymIujN_l7memSDT0uh0Yc8sdx2r-7tEP2gi9hY9B1ZdUqARLUEbuTGm932ekbQaYP2Vbq-tYz-jBur1AbiDzDQv-E--at_kZLd30mE-kgrsst5CCtxmnk9-xaEh56ed5S1CUzYAWu_OeTwWjbt3-LIpObK7GEAs3zC7U3GBbaiG4tTkxaJ95tb_gao0MAzMrYKe2lkcmOkH3YMreXnYprRL94npEJUz8aBFIvB7F39EjLIAj-PhTtkO9Ey_Onhumi63I8t1w7Kdqzodir2kP9LMRYRE30tdGHrzq7N9OIjJEsT7Y4332rsbAwpoSfwiVi9zY0OgHjW5i8thDaT8olo; lidc="b=SB39:g=48:u=56:i=1523290340:t=1523335206:s=AQGKuX_g5h5KXALwUCYhkMCsLjTahj4m"'
# csrf = 'ajax:6858942346055442004'
cookie = 'li_sugr=a8ce6728-71d6-4b67-abf1-fd22471a652a; _ga=GA1.2.1103327498.1578739635; aam_uuid=67510623380186900253362623901423547553; _guid=0bc3ad95-9840-4d57-8e4e-c629e8a6d46e; lissc1=1; lissc2=1; cap_session_id=3029172246:1; u_tz=GMT+08:00; li_oatml=AQFWt9jC8rbmPQAAAW_Q2xxXmYrvpp5wzqyqnrEWOBNNNAIGuSdvJHf9L32SEmkH413u6hiX42T3oI-_NFc1YgdFE9aNsLPn; bcookie=v=2&aadbda16-1705-4ed3-8b4e-6cb06e3868a3; bscookie=v=1&2019112809180736397064-7c03-48ee-8c1c-0224dd7be59cAQFN8z_rzSFPrnVCTGKoPzx1PRK8emTl; lissc=1; fid=AQFErU8xR2XxzwAAAW_SwnKZeoIZbJlK97f6Camhnr-pt2W3gbKzwoQdDiXv5NYi0mnG5_P9y2kqeA; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; spectroscopyId=5416f06f-7b8f-48be-9805-47ef843ddbbb; visit=v=1&M; _lipt=CwEAAAFv1gP0vCPnISYiXCxezdux-MoYXMLXjjv5NrKPQ0INr60; JSESSIONID="ajax:8800147073815231271"; sl=v=1&d17Jg; li_at=AQEDARo-DEsBfFNBAAABb9cJhLgAAAFv-xYIuE0AF1HbU3Nsf5iluls_XOmJm-LKNLNf1E9SBujaJxNHUGQCT1HQtLg4TpTQcA3qWejih32ggtwHYF-DxsxN7VzIXWi_qdGfYTbU4r30QZeH8fMfCjcZ; liap=true; lang=v=2&lang=en-us; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-1303530583%7CMCIDTS%7C18285%7CMCMID%7C67373062266571776343343183455992432490%7CMCAAMLH-1580465535%7C3%7CMCAAMB-1580465535%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1579864353s%7CNONE%7CvVersion%7C3.3.0%7CMCCIDH%7C-89769995; _gat=1; UserMatchHistory=AQItM-iFnZyOIAAAAW_XfgT6Ft3eE6WoPjlTp2pmFqhnefDQJNMiofjvrjjC6LgYPeukiIlc7wHcegqON0S8WkSeaRT1CEeJvmrboSOrudID-S2Ca_71sF0W3UO2rr5QZSHQdLyAa0CbbLTneifEyEu3xmmPGbNd-GcXKFemkrDU-3RLTI_b8j15t_-CpzWYyw4UcifxgZIJVH4hL5oQBA2NOu8LcY5f; lidc="b=SB95:g=134:u=174:i=1579868359:t=1579926639:s=AQGD3VixFBjbLugLbZyPMct41hDRwW2I"'
csrf = 'ajax:8800147073815231271'

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
    if profile_id in ['C_25', 'C_34', 'C_123', 'C_132', 'C_145', 'C_156', 'C_163', 'C_164', 'C_170', 'C_186', 'C_189',
                'C_206', 'C_208', 'C_220', 'C_221', 'C_225', 'C_226', 'C_228', 'C_231', 'C_232', 'C_233', 'C_234',
                'C_235', 'C_238', 'C_239', 'C_240', 'C_241', 'C_253', 'C_262', 'C_263', 'C_270', 'C_271', 'C_279',
                'C_291', 'C_293', 'C_360', 'C_370', 'C_387', 'C_388', 'C_390', 'C_391', 'C_394', 'C_395', 'C_396',
                'C_400', 'C_405', 'C_417', 'C_462', 'C_476', 'C_557', 'C_559', 'C_562', 'C_565', 'C_567', 'C_573',
                'C_582', 'C_583', 'C_584', 'C_592', 'C_595', 'C_611', 'C_620', 'C_633', 'C_656', 'C_722', 'C_727',
                'C_728', 'C_731', 'C_736', 'C_737', 'C_741', 'C_742', 'C_744', 'C_746', 'C_747', 'C_748', 'C_752',
                'C_754', 'C_755', 'C_759', 'C_760', 'C_762', 'C_767', 'C_768', 'C_769', 'C_770', 'C_771', 'C_775',
                'C_778', 'C_786', 'C_792', 'C_795', 'C_804', 'C_810', 'C_813', 'C_838', 'C_839', 'C_844', 'C_872',
                'C_898', 'C_909', 'C_910', 'C_925', 'C_929', 'C_930', 'C_931', 'C_932', 'C_934', 'C_936', 'C_942',
                'C_946', 'C_947', 'C_948', 'C_949', 'C_950', 'C_952', 'C_953', 'C_956', 'C_966', 'C_968', 'C_969',
                'C_971', 'C_973', 'C_978', 'C_982', 'C_990', 'C_993', 'C_996', 'C_999', 'C_1000', 'C_1002', 'C_1003',
                'C_1020', 'C_1023']:
        one_row = [profile_id, url, 'N/A', 'N/A', 'N/A']
        sheet2_data.append(one_row)
    return 1
    endorse_url = 'https://www.linkedin.com/voyager/api/identity/profiles/%s/skillCategory?includeHiddenEndorsers=true&count=50' % url.split('/')[-1]
    html = get_request(endorse_url)
    data_obj = json.loads(html)

    name_dic = {}
    category_dic = {}
    res = []

    if data_obj.get('status'):
        print url, data_obj.get('status')
    for item in data_obj.get('included', []):

        if item.get('$type') == 'com.linkedin.voyager.identity.profile.EndorsedSkill':
            res.append([item.get('originalCategoryType'), item.get('endorsementCount'), item.get('*skill')])
        elif item.get('$type') == 'com.linkedin.voyager.identity.profile.Skill':
            name_dic[item['entityUrn']] = item['name']
        elif item.get('$type') == 'com.linkedin.voyager.identity.profile.ProfileSkillCategory':
            category_dic[item.get('type')] = item['categoryName']

    for item in res:
        one_row = [profile_id, url, category_dic.get(item[0], item[0]), name_dic.get(item[2], item[2]), item[1]]
        print one_row
        sheet2_data.append(one_row)
    return len(item)


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
        'accept': 'application/vnd.linkedin.normalized+json+2.1',
        'csrf-token': csrf,
        'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;S/sxjWBcSZaqeRO3Ln/XXw==',
        'referer': url,
    }
    res_data = requests.get(url, headers=header, timeout=8)
    res = res_data.content.decode("utf-8")
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


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


def get_data2(filename):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]

    for i in range(1, 383):
        row = table.row(i)
        c_id = row[0].value
        url = row[2].value
        try:
            length = get_endorse_details(c_id, url)
            print '----', c_id, url, length, '---'
            # time.sleep(3)
        except Exception as e:
            print c_id, e
    write_excel('sheet2.xls', sheet2_data)



# scrape profile data
# step 1: profile data
# request_sheet0()
# step 2: profile details
# read_excel('predata/sheet0_digital ID.xls', start=P_ID)
# write_excel('data/res1.xls', sheet1_data)
# write_excel('data/res2.xls', sheet2_data)
# step 3: company size
# preload_company_size()
# request_company_size()
get_data2('data/sheet0.xls')