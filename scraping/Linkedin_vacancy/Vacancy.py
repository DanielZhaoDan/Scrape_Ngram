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
import time
import ssl

P_ID = 1
email = 'jaysie.dreyah@oou.us'
company_employee = {}
company_data = {}

keyword_urls = [
    ['Certification SG', 'https://www.linkedin.com/jobs/search/?keywords=Certification&location=Singapore&locationId=sg%3A0&start='],
]

sheet_data = [['Keywords&Index', 'Keyword', 'Index', 'Top Skills', 'URL', 'Title', 'Company', 'Company URL', 'No. of Employee', 'Date', 'Views', 'Job Desp', 'Requirements', 'Level', 'Industry', 'Employment Type', 'Job Functions', 'Manager Level', 'Senior Level', 'Director Level', 'Entry Level', 'Master', 'Bachelor', 'MBA', 'Other Education', 'Total Applicants']]

cookie = 'JSESSIONID=ajax:8568514931401773276; bcookie="v=2&5e642870-bae7-4d7d-86f2-a88f4250c1c4"; bscookie="v=1&20180217075906d4de8175-476a-43d3-8a59-addca01437f2AQGQfAavP6iKl8lQZv-IXl-DC48s83M8"; _ga=GA1.2.282991545.1518854461; _gat=1; liap=true; sl=v=1&rjBnu; li_at=AQEDASYTMb4CJh5fAAABYaLGmvAAAAFhxtMe8FEABxu2YSdDYNem9Kzqsno0INDJvKpIATkdK6jFVCaCll6pb3-AUfVKCU-4xihWCpO7qR0Itk144Zq95gsCoad_R1OY4U576LRQfdl4h9-kB9gUitqy; RT=s=1518854493911&r=https%3A%2F%2Fwww.linkedin.com%2F; visit="v=1&M"; lang="v=2&lang=en-us"; _lipt=CwEAAAFhosfvERUXFq-oVDIW0-y6Vn6SbAFbSwzadan08wcYFjqvhpp42snOqhqkpzIzpsC6tKbB7NC7JpRjl1khbwzOYI5th30JIiXKy_qZ3_J2F0bhnrNF9dA; lidc="b=SGST01:g=3:u=1:i=1518854467:t=1518940780:s=AQF07H7sYt4pyYmC1skt6-G_7qN4aZXL"'
csrf = 'ajax:8568514931401773276'

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
                    print '===Write excel ERROR===' + str(one_row[col])
    w.save(filename)
    print filename + "===========over============"


def request_sheet1(url, key, keyword):
    raw_reg = 'fs_jobSavingInfo:(.*?)"'
    html = get_request(url)
    job_ids = re.compile(raw_reg).findall(html)

    for i in range(len(job_ids)):
        index = str(key) + '.' + str(i + 1)
        request_job_details(index, job_ids[i], keyword)
        time.sleep(1)



def request_company(url):
    company_reg = '"staffCount":(.*?),.*?"industries":(.*?),'
    html = get_request(url)
    staff_ind_list = re.compile(company_reg).findall(html)
    staff_count, industy = 0, []

    if staff_ind_list:
        staff_count = staff_ind_list[0][0]
    return staff_count, industy


def request_job_details(index, job_id, keyword):
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

    industries = industry.split(',')

    for skill in top_skills:
        for industry in industries:
            one_row = ['%s_%s' % (keyword, str(index)), keyword, index, skill, job_url, title, company_name, company_page_url, staff_count, date, views, desp, requirements, level, industry.strip(),
                              employ_type, job_functions, manager, senior, director, entry, master, bachelor, mba, other, total_app]
            sheet_data.append(one_row)
    print keyword, index, job_url, company_name, company_page_url, staff_count, date, views, len(skill_details)


def get_date(timestamp):
    try:
        ret = datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
        return ret
    except:
        return 'N/A'


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_json_resp(url):
    resp = requests.get(url, headers={
        'Cookie': cookie,
        'csrf-token': csrf,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    })
    if resp.status_code == 200:
        return resp.json()
    return {}


def get_request(get_url):
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.linkedin.com/')
    req.add_header("Cookie", cookie)
    req.add_header('csrf-token', 'ajax:1666134097818962763')
    res_data = urllib2.urlopen(req, timeout=10, context=ctx)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return HTMLParser.HTMLParser().unescape(res)


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
            print one_row
            company_data.append(one_row)
        except Exception as e:
            print str(i) + ' -> ' + str(e)
            company_data.append(['na', '0'])
    write_excel('data/res.xls', company_data)


reload(sys)
sys.setdefaultencoding('utf-8')
stop = False

for keyword_url in keyword_urls:
    if stop:
        break
    keyword = keyword_url[0]
    url_prefix = keyword_url[1]
    for i in range(10):
        if stop:
            break
        try:
            url = url_prefix + str(25 * i)
            request_sheet1(url, i + 1, keyword)
        except urllib2.HTTPError as e:
            if e.code == 302:
                stop = True

    write_excel('data/Vacancy_%s.xls' % keyword, sheet_data)
    del sheet_data
    sheet_data = [['Keywords&Index', 'Keyword', 'Index', 'Top Skills', 'URL', 'Title', 'Company', 'Company URL',
                   'No. of Employee', 'Date', 'Views', 'Job Desp', 'Requirements', 'Level', 'Industry',
                   'Employment Type', 'Job Functions', 'Manager Level', 'Senior Level', 'Director Level', 'Entry Level',
                   'Master', 'Bachelor', 'MBA', 'Other Education', 'Total Applicants']]
