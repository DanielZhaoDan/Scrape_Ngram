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

P_ID = 276
email = 'jaysie.dreyah@oou.us'
company_employee = {}
company_data = {}

keyword_urls = [
    ['Telecommunication', 'https://www.linkedin.com/jobs/search/?keywords=Telecommunication&location=Malaysia&locationId=my%3A0&start=', 386, 'MY'],
]

sheet_data = [['Keyword', 'Location', 'Total Result', 'Vacancy ID', 'Vacancy URL', 'Company Name', 'Company URL', 'Position', 'Level', 'Industry', 'Job Functions', 'Job Desp', 'Requirements', 'Manager Level', 'Senior Level', 'Director Level', 'Entry Level', 'Total Applicants Count']]
sheet2_data = [['Vacancy  ID', 'Top Skill']]

cookie = 'bcookie="v=2&74219b48-1ccd-4aeb-8466-f59864535f9c"; bscookie="v=1&201608091552185c8d9623-6d9e-4a35-8691-d110a1d88056AQGZm-7AEvD7o3e2bz1bNcK_8yK41Y9o"; visit="v=1&M"; _chartbeat2=BJt6ifO0CcmBe3LOe.1500744286051.1500744286064.1; _lipt=CwEAAAFhpG3jUAKzayEjc2vd3-EboVz_5K6Gc-vv_DP7bs8h2aqkbTNUoHodNnUc-ePPOpbGpujjzlQSs5JPMALSLeXKE4pN6k9hUwsB4JS0B7EYTMONLnkSUQogJpZV0EqaV8feJUEQxfqZzziB-4kySOZAz-SPKqxp_Tf-NMKvxo25VjxA-KQDMnZgePOHU2R_yQembhvPISZC0XCKgLfL-N-1UhQyfOqs5Rgxs1KGOaBSQnBT5Tc3WWSiWk9dZG3ojbAncDVFWDolj9IeYq07fa6gShk61eJoKqWZNaGIlzuEPL93yFtvuJncPSYVUXod9buxxQ6KZ9AWkVwwhWXaZ-rB2X6yoEBpdR9heGNoWAtaLqPlsRKzx_4jvuagkUBy0-nANAVAwNdCyPpDpuqxeSY8zypLXqCAiszte6mTPzyHe9oynrCm5DEhXdwMez4; sl="v=1&9bgWy"; liap=true; JSESSIONID="ajax:0527940450066958550"; li_at=AQEDAQFnLMYCUFQJAAABYaSvGeMAAAFhyLud41EAQJ1flnsyH4r5cSTJDZizt-60zZN2udcZwkX9Av99ECaSpY_cHUZXEzGQoF00rV_ewPfE4vHZPZxPt7GQ6irMDHP3l_xCflVsHVBfiiik1bN1zPGB; _gat=1; lang="v=2&lang=en-us"; _ga=GA1.2.1479882839.1470758235; lidc="b=SB86:g=31:u=70:i=1518912529:t=1518922393:s=AQFheT7XO0WkLnSgV_6HKx8lCT2ECaR8"'
csrf = 'ajax:0527940450066958550'

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


def request_sheet1(url, keyword):
    global P_ID, stop
    raw_reg = 'fs_jobSavingInfo:(.*?)"'
    html = get_request(url)
    job_ids = re.compile(raw_reg).findall(html)

    for i in range(len(job_ids)):
        request_job_details(job_ids[i], keyword, 'VAC_%d' % P_ID)
        P_ID += 1
        if P_ID > keyword[2]:
            stop = True
        if stop:
            break
        time.sleep(1)


def request_company(url):
    company_reg = '"staffCount":(.*?),.*?"industries":(.*?),'
    html = get_request(url)
    staff_ind_list = re.compile(company_reg).findall(html)
    staff_count, industy = 0, []

    if staff_ind_list:
        staff_count = staff_ind_list[0][0]
    return staff_count, industy


def request_job_details(job_id, keyword, vac_id):
    global sheet_data
    job_url = 'https://www.linkedin.com/jobs/view/%s/' % job_id
    applicant_url = 'https://www.linkedin.com/voyager/api/jobs/applicantInsights/%s' % job_id
    company_url = 'https://www.linkedin.com/voyager/api/jobs/jobPostings/%s' % job_id
    job_html = get_request(job_url)
    applicant_html = get_json_resp(applicant_url)
    company_html = get_json_resp(company_url)
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

    one_row = [keyword[0], keyword[3], keyword[2], vac_id, job_url, company_name, company_page_url, title, level, industry, job_functions, desp, requirements, manager, senior, director, entry, total_app]
    sheet_data.append(one_row)
    for skill in top_skills:
        sheet2_data.append([vac_id, skill])
    print(one_row)


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
    resp = requests.get(url, headers={
        'Cookie': cookie,
        'csrf-token': csrf,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    })
    if resp.status_code == 200:
        return resp.json()
    return {}


def get_request(url):
    header = {
        'cookie': cookie,
        'csrf-token': csrf,
    }
    res_data = requests.get(url, headers=header)
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


for keyword_url in keyword_urls:
    if stop:
        break
    if P_ID > keyword_url[2]:
        break
    keyword = keyword_url[0]
    url_prefix = keyword_url[1]
    for i in range(6, 50):
        if stop:
            break
        try:
            url = url_prefix + str(25 * i)
            request_sheet1(url, keyword_url)
        except Exception as e:
            print(str(e))
            stop = True

    write_excel('data/sheet11_%s.xls' % keyword, sheet_data)
    write_excel('data/sheet22_%s.xls' % keyword, sheet2_data)
    del sheet_data
    del sheet2_data
    sheet_data = [['Keyword', 'Location', 'Total Result', 'Vacancy ID', 'Vacancy URL', 'Company Name', 'Company URL', 'Position', 'Level', 'Industry', 'Job Functions', 'Job Desp', 'Requirements', 'Manager Level', 'Senior Level', 'Director Level', 'Entry Level', 'Total Applicants count']]
    sheet2_data = [['Vacancy  ID', 'Top Skill']]
    P_ID = 0
