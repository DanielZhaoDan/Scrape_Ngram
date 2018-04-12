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
import time
import ssl
import json
stop = False

P_ID = 1
TOTAL_REQUEST_COUNT = 0
email = 'luke.dagoberto@0hboy.com spenser.mekael@0hboy.com'
company_employee = {}
company_data = {}

keyword_urls = [
    ['digital technology MY', 'https://www.linkedin.com/jobs/search/?keywords=digital%20technology&location=Malaysia&locationId=my%3A0&start=', 830, 'MY'],
]

sheet0_data = [['Keyword', 'Location', 'Total Result', 'Vacancy ID', 'Vacancy URL']]
sheet_data = [['Keyword', 'Location', 'Total Result', 'Vacancy ID', 'Vacancy URL', 'Company Name', 'Company Size', 'Company URL', 'Position', 'Level', 'Industry', 'Job Functions', 'Job Desp', 'Requirements', 'Manager Level', 'Senior Level', 'Director Level', 'Entry Level', 'Total Applicants Count']]
sheet2_data = [['Vacancy  ID', 'Top Skill']]

cookie = 'bcookie="v=2&75157af0-547f-4e4e-8069-c5d3f29ce794"; bscookie="v=1&20180411111250fdd22d95-0efe-4a39-8af0-25e197014689AQFjc0Ca6O4v8TdGFiICs-qFuNepNKSi"; _guid=5802464e-188c-40a2-b7bd-46ce89cee494; visit="v=1&M"; PLAY_SESSION=1123899b115259b12c159179928f9c44afcf8c32-chsInfo=5babdc86-00b0-45d4-8168-ca1d0e1e6f89+premium_nav_upsell_text; __ssid=49a5c84d-4f71-41c1-8c48-6350f7078723; _ga=GA1.2.537612569.1523455485; _lipt=CwEAAAFiuLEDC1PIC2IBp5N1VjUI5HOu3zb5P1bDN1CYd4SfSzrvN-NTA_nPuWNTwCqPzQPghu4xrcwxBUxD3H3r_UsiHI5gBHrLLVRF21Bk74ZdVwxBnOMHgBY; rtc=AQE3HsAoSicJFwAAAWK4_JIYAygABGHY3pd5tKh7S-PS0o6sWgRK_rSojDRSZiB6n0-TFA4KpQs8BlnyT9801QJ8XQZ7m-8YWfsmUDgAcBf9D5CVOSsD3igx4EPlKqLzQ_LN6JpDazcCq-g-rFtTK_KbwCoiJHCvo_jw10V4wd1lRKFhnQlUkPx7MTAGXeJyTiCuOBlwtda76LwNpA7zX8jEwXNA-zwYL9JgZ3IGCrn_QTfLBj7Myiq119jKZVI6JuqjmwSWJXakjKUNqZf3qUVTn4q6dmJRvB5hIRZexLy-DA==; leo_auth_token="GST:ZCvyPeLXzXVEW2gPrAYrpokPDFyKPqEh4nYVsuROXn-lPxdhpda_yf:1523522011:22593049d0dd0403b390c3844bf039668fa35d04"; sl="v=1&-ICKc"; lang="v=2&lang=en-us"; li_at=AQEDASbKqgEBhB2tAAABYrj9AIUAAAFi3QmEhVEAQ4RHCHbPwkg-xSga3gAygE-LiqrOL63oPuPj68r0AEFC2QEB8rd-rlcjf9ke8Zs7k1Ge-yw49xpBWj2sMzc5I-B9bUWq2Ztnx4U3fkfjJvtfKNXs; liap=true; JSESSIONID="ajax:3675240927329675624"; RT=s=1523522012000&r=https%3A%2F%2Fwww.linkedin.com%2Fuas%2Fconsumer-captcha-v2%3FchallengeId%3DAQEaaaBAEzgxSAAAAWK4_NwRkTGnfvBRlvO_jtGiifYsLpJywL85HOS2P_bMve5ZwGlSl3ZmNN-kj5k-ESgIFGPVjW5Wlp5rQQ; lidc="b=SB01:g=67:u=2:i=1523522045:t=1523603622:s=AQESzEf062daInobKRFJCo0PQOxVxRI1"'
csrf = 'ajax:3675240927329675624'


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
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
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
                    print('===Write excel ERROR===' + str(one_row[col]))
    w.save(filename)
    print(filename + "===========over============")


def save_job_ids(url, keyword):
    global P_ID, stop, sheet0_data
    raw_reg = 'fs_jobSavingInfo:(.*?)"'
    html = get_request(url)
    job_ids = re.compile(raw_reg).findall(html)

    if len(job_ids) < 1:
        return -1
    for i in range(len(job_ids)):
        job_id = job_ids[i]
        job_url = 'https://www.linkedin.com/jobs/view/%s/' % job_id
        one_row = [keyword[0], keyword[3], keyword[2], 'VAC_%d' % P_ID, job_url]
        sheet0_data.append(one_row)
        P_ID += 1
    return len(job_ids)


def request_sheet1(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]
    print('process -> %s: %d' % (filename, table.nrows))

    for i in range(start, table.nrows):
        row = table.row(i)
        job_id = row[3].value
        try:
            job_url = row[4].value
            if i <= 34:
                continue
            # if job_id not in ['VAC_80', 'VAC_148', 'VAC_192', 'VAC_194', 'VAC_202', 'VAC_214', 'VAC_220', 'VAC_244 VAC_248', 'VAC_272', 'VAC_288', 'VAC_307', 'VAC_316', 'VAC_322', 'VAC_323', 'VAC_341', 'VAC_343', 'VAC_346', 'VAC_347', 'VAC_350', 'VAC_352', 'VAC_358', 'VAC_359', 'VAC_361', 'VAC_362', 'VAC_363', 'VAC_368', 'VAC_369', 'VAC_375', 'VAC_382', 'VAC_386', 'VAC_395', 'VAC_396', 'VAC_402', 'VAC_403', 'VAC_416', 'VAC_418', 'VAC_422', 'VAC_424', 'VAC_426', 'VAC_433', 'VAC_437', 'VAC_447', 'VAC_448', 'VAC_459', 'VAC_462', 'VAC_469', 'VAC_470', 'VAC_475', 'VAC_478', 'VAC_479', 'VAC_481', 'VAC_483', 'VAC_484', 'VAC_487', 'VAC_489', 'VAC_493', 'VAC_497', 'VAC_499', 'VAC_503', 'VAC_509', 'VAC_511', 'VAC_512', 'VAC_514', 'VAC_515', 'VAC_529', 'VAC_534', 'VAC_540', 'VAC_544', 'VAC_546', 'VAC_549', 'VAC_550', 'VAC_562', 'VAC_568', 'VAC_569', 'VAC_574', 'VAC_579', 'VAC_580', 'VAC_582', 'VAC_587', 'VAC_589', 'VAC_596', 'VAC_601', 'VAC_602', 'VAC_604', 'VAC_608', 'VAC_613', 'VAC_619', 'VAC_624', 'VAC_627', 'VAC_628', ]:
            #     continue
            name = row[0].value
            total_result = int(row[2].value)
            location = row[1].value
            status = request_job_details(job_id, location, total_result, name, job_url)
            if not status:
                return status
        except Exception as e:
            print('ERROR===%s' % job_id, e)
            continue
        time.sleep(2)
    return True


def request_company(url):
    company_reg = '"staffCount":(.*?),.*?"industries":(.*?),'
    html = get_request(url)
    staff_ind_list = re.compile(company_reg).findall(html)
    staff_count, industy = 0, []

    if staff_ind_list:
        staff_count = staff_ind_list[0][0]
    return staff_count, industy


def request_job_details(vac_id, location, total_result, keyword, job_url):
    global sheet_data
    job_id = job_url.split('/')[-2]
    applicant_url = 'https://www.linkedin.com/voyager/api/jobs/applicantInsights/%s' % job_id
    company_url = 'https://www.linkedin.com/voyager/api/jobs/jobPostings/%s' % job_id
    job_html = get_request(job_url)
    applicant_html = get_json_resp(applicant_url)
    company_html = get_json_resp(company_url)
    if not applicant_html and not company_html:
        return False
    company_reg = '"companyName":"(.*?)"'
    company_id_reg = '"company":"(.*?)"'

    company_name = re.compile(company_reg).findall(job_html)
    if company_name:
        company_name = company_name[0]
    else:
        company_reg = '"name":"(.*?)"'
        company_name = re.compile(company_reg).findall(job_html)
        if company_name:
            company_name = company_name[-1]
        else:
            company_name = ''

    company_page_url = 'N/A'
    company_id = re.compile(company_id_reg).findall(job_html)
    staff_count = 0
    if company_id:
        company_id = company_id[0].split(':')[-1]
        company_page_url = 'https://www.linkedin.com/company/%s/' % company_id
        if company_data.get(company_page_url):
            staff_count, industries = company_data.get(company_page_url)
        else:
            staff_count, industries = request_company(company_page_url)
            company_data[company_page_url] = [staff_count, industries]
    else:
        company_id = 'M/A'

    date = get_date(company_html.get('listedAt', 0) / 1000)
    level = company_html.get('formattedExperienceLevel', '')
    industry = ', '.join(company_html.get('formattedIndustries', []))
    employ_type = company_html.get('formattedEmploymentStatus', '')
    views = company_html.get('views', 0)
    job_functions = ', '.join(company_html.get('formattedJobFunctions', []))

    title = company_html.get('title', '')
    all_desp = company_html.get('description', {}).get('text', '').replace('\n', '')
    desp = requirements = ''
    for word in ['Requirements', 'Qualifications', 'Responsibilities']:
        text = all_desp.split(word)
        desp = text[0].strip() if text[0].strip() != '' else text[-1].strip()
        requirements = text[-1].strip() if len(text) == 2 else ''
        if requirements != '':
            break

    bachelor = mba = master = 0
    degree_details = applicant_html.get('degreeDetails', [])
    for degree in degree_details:
        degree_name = degree.get('formattedDegreeName', '')
        if 'Bachelor' in degree_name:
            bachelor = degree.get('percentage', 0)
        elif 'Business Administration' in degree_name:
            mba = degree.get('percentage', 0)
        elif 'Master' in degree_name and 'Business Administration' not in degree_name:
            master = degree.get('percentage', 0)
    other = 100 - bachelor - mba - master
    if other == 100:
        other = 0

    manager = senior = entry = director = 0
    seniority_details = applicant_html.get('seniorityDetails', [])
    total_app = applicant_html.get('applicantCount', 0)
    for seniority in seniority_details:
        name = seniority.get('formattedSeniorityCategoryName', '')
        if 'Manager' == name:
            manager = seniority.get('count', 0)
        elif 'Senior' == name:
            senior = seniority.get('count', 0)
        elif 'Entry' == name:
            entry = seniority.get('count', 0)
        elif 'Director' == name:
            director = seniority.get('count', 0)

    skill_details = applicant_html.get('skillDetails', [])
    top_skills = []
    for skill in skill_details:
        name = skill.get('formattedSkillName', '')
        if name != '':
            top_skills.append(name)
    if not top_skills:
        top_skills = ['N/A']

    one_row = [keyword, location, total_result, vac_id, job_url, company_name, staff_count, company_page_url, title, level, industry, job_functions, desp, requirements, manager, senior, director, entry, total_app]
    sheet_data.append(one_row)
    for skill in top_skills:
        sheet2_data.append([vac_id, skill])
    print(vac_id, job_url, company_name, staff_count, title, manager, total_app, desp)
    return True


def get_date(timestamp):
    try:
        ret = datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
        return ret
    except:
        return 'N/A'


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(html.unescape(dd))


def get_json_resp(url):
    global TOTAL_REQUEST_COUNT
    TOTAL_REQUEST_COUNT += 1
    resp = requests.get(url, headers={
        'Cookie': cookie,
        'csrf-token': csrf,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    }, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    return {}


def get_request(url):
    global TOTAL_REQUEST_COUNT
    TOTAL_REQUEST_COUNT += 1
    header = {
        'cookie': cookie,
        'csrf-token': csrf,
    }
    res_data = requests.get(url, headers=header, timeout=10)
    res = res_data.content.decode("utf-8")
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return html.unescape(res)


def read_excel(filename, start=1):
    company_data = []
    print('process -> ' + filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            url = row[2].value
            job_id = url.split('/')[-2]
            number_of_employee = int(row[5].value)
            if number_of_employee == 0:
                number_of_employee = request_company(job_id)
            one_row = [job_id, number_of_employee]
            print(one_row)
            company_data.append(one_row)
        except Exception as e:
            print(str(i) + ' -> ' + str(e))
            company_data.append(['na', '0'])
    write_excel('data/res.xls', company_data)


def get__job_ids():
    global stop, P_ID, sheet2_data, sheet_data, sheet0_data
    for keyword_url in keyword_urls:
        if stop:
            break
        if P_ID > keyword_url[2]:
            break
        keyword = keyword_url[0]
        url_prefix = keyword_url[1]
        for i in range(0, 50):
            if stop:
                break
            try:
                url = url_prefix + str(25 * i)
                print(url)
                status = save_job_ids(url, keyword_url)
                if status == -1:
                    break
            except Exception as e:
                print(str(e))
                if 'Read timed out' not in str(e) and ' Max retries exceeded' not in str(e):
                    stop = True
        write_excel('predata/sheet0_%s.xls' % keyword, sheet0_data)
        print('====%s done=== %d' % (keyword, len(sheet0_data)))
        del sheet0_data
        sheet0_data = [['Keyword', 'Location', 'Total Result', 'Vacancy ID', 'Vacancy URL']]
        P_ID = 1


def request_details_data():
    global sheet0_data, sheet2_data, sheet_data
    files = walk('predata/')
    for filename in files:
        status = request_sheet1(filename)
        keyword = filename.split('_')[1].split('.')[0]
        write_excel('data/sheet1_%s.xls' % keyword, sheet_data)
        write_excel('data/sheet2_%s.xls' % keyword, sheet2_data)
        if not status:
            print('=====COOKIE ERROR=====')
            break
        del sheet_data
        del sheet2_data
        sheet_data = [['Keyword', 'Location', 'Total Result', 'Vacancy ID', 'Vacancy URL', 'Company Name', 'Company Size',
                       'Company URL', 'Position', 'Level', 'Industry', 'Job Functions', 'Job Desp', 'Requirements',
                       'Manager Level', 'Senior Level', 'Director Level', 'Entry Level', 'Total Applicants Count']]
        sheet2_data = [['Vacancy  ID', 'Top Skill']]


# step1: scraping job ids
# get__job_ids()
# step2: scraping job details according to job ids
request_details_data()
print('=====TOTAL_REQUEST_COUNT: %d=====' % TOTAL_REQUEST_COUNT)
