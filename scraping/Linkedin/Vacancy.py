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

P_ID = 1
email = 'aavi.rawson@oou.us'
company_employee = {}
company_data = {}

keyword_urls = [
    # ['CFO', 'https://www.linkedin.com/jobs/search/?keywords=cfo&location=Singapore&locationId=sg&start='],
    # ['Treasury', 'https://www.linkedin.com/jobs/search/?keywords=Treasury&location=Singapore&locationId=sg&start='],
    # ['Risk Management',
    #  'https://www.linkedin.com/jobs/search/?keywords=Risk%20Management&location=Singapore&locationId=sg&start='],
    # ['Finance Manager',
    #  'https://www.linkedin.com/jobs/search/?keywords=Finance%20Manager&location=Singapore&locationId=sg&start='],
    # ['Forward', 'https://www.linkedin.com/jobs/search/?keywords=Forwards&location=Singapore&locationId=sg&start='],
    # ['Exchange Rate',
    #  'https://www.linkedin.com/jobs/search/?keywords=Exchange%20Rate&location=Singapore&locationId=sg&start='],
    # ['Forward Contract',
    #  'https://www.linkedin.com/jobs/search/?keywords=Forward%20Contract&location=Singapore&locationId=sg&start='],
    # ['Invoice', 'https://www.linkedin.com/jobs/search/?keywords=Invoice&location=Singapore&locationId=sg&start='],
    # ['Accounts Payable',
    #  'https://www.linkedin.com/jobs/search/?keywords=Accounts%20Payable&location=Singapore&locationId=sg&start='],
    # ['Accounts Payable Specialist',
    #  'https://www.linkedin.com/jobs/search/?keywords=Accounts%20Payable%20Specialist&location=Singapore&locationId=sg&start='],
    # ['Currency Transactions',
    #  'https://www.linkedin.com/jobs/search/?keywords=Currency%20Transactions&location=Singapore&locationId=sg&start='],
    # ['Remittance',
    #  'https://www.linkedin.com/jobs/search/?keywords=Remittances&location=Singapore&locationId=sg&start='],
    # ['Transaction Processing',
    #  'https://www.linkedin.com/jobs/search/?keywords=Transaction%20Processing&location=Singapore&locationId=sg&start='],
    # ['Cash flow management',
    #  'https://www.linkedin.com/jobs/search/?keywords=Cash%20Flow%20Management&location=Singapore&locationId=sg&start='],
    # ['Online Payments Solutions',
    #  'https://www.linkedin.com/jobs/search/?keywords=Online%20Payments%20Solutions&location=Singapore&locationId=sg&start='],
    # ['Payments Solutions',
    #  'https://www.linkedin.com/jobs/search/?keywords=Payments%20Solutions&location=Singapore&locationId=sg&start='],
    # ['International Payments',
    #  'https://www.linkedin.com/jobs/search/?keywords=International%20Payments&location=Singapore&locationId=sg&start='],
    # ['Foreign Exchange',
    #  'https://www.linkedin.com/jobs/search/?keywords=Foreign%20Exchange&location=Singapore&locationId=sg&start='],
    # ['FX', 'https://www.linkedin.com/jobs/search/?keywords=FX&location=Singapore&locationId=sg&start='],
    # ['B2B Payments',
    #  'https://www.linkedin.com/jobs/search/?keywords=B2B%20payments&location=Singapore&locationId=sg&start='],
    # ['Corporate Payments',
    #  'https://www.linkedin.com/jobs/search/?keywords=Corporate%20Payments&location=Singapore&locationId=sg&start='],
    ['Corporate Payment',
     'https://www.linkedin.com/jobs/search/?keywords=Corporate%20Payment&location=Singapore&locationId=sg&start='],
]

sheet_data = [['Keywords&Index', 'Keyword', 'Index', 'Top Skills', 'URL', 'Title', 'Company', 'Company URL', 'No. of Employee', 'Date', 'Views', 'Job Desp', 'Requirements', 'Level', 'Industry', 'Employment Type', 'Job Functions', 'Manager Level', 'Senior Level', 'Director Level', 'Entry Level', 'Master', 'Bachelor', 'MBA', 'Other Education', 'Total Applicants']]

cookie = 'bcookie="v=2&94ede669-f96d-4d7f-88df-20bb8b9ed56c"; bscookie="v=1&201608050319286fb0d9d7-11eb-4c4f-853f-2819c04ac829AQHDI3jFjJtWbtizwwj8_RtdcWBWfmiO"; visit="v=1&M"; _chartbeat2=Va5crvXhgBBqAl5L.1476436594042.1476440427196.1; __utma=226841088.1514381064.1470817606.1483846988.1487305243.2; PLAY_SESSION=0c0be92d0a9ebfd3caf822b8c03613c50ca5ba90-chsInfo=cb56f3a9-8428-4069-a922-46e9f79bd7ad+premium_job_details_upsell_applicant_insights; __ssid=7bc82af0-6ae7-48cb-b62c-add9420e840b; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; _lipt=CwEAAAFf7KU03rf4gkRjKi2JomCuEuiQRgQbPIO4cIWQi8Ctal5CsG2o2KmQD9tIp1CgLvGT8xxeYdxT8TWbT4L6PkQdtOFZilcKg9rdg6EoIII0-YzE5H1O29M_uwfpU9YJX9uqq6adGzwgTB3BySHgE2OCzRrh5JX6VTEBjaTHzLjgLIJehN2429AUawP3Gnb7kXO55V71zFzIAayJRvMssWIfklOSsPIMF_G6YeqoPSq74-ndcUb8yGspz-LHfjS6b6H4wTqroDdvl8iZdVmBVs0t_rb7cuuoR7AvTbgtlkuHZf7vsftQr3aE9Q; _ga=GA1.2.1514381064.1470817606; _gat=1; sl="v=1&LmctT"; lang="v=2&lang=en-us"; liap=true; li_at=AQEDASUWWJkE2_4NAAABX-0NDfkAAAFgERmR-VEAiuwqHwE081qjnT2or5Or83ZZudJ7mL41IQADbMke1roekvZZZpCX9HxeZ17w_VP73o-jpymyu_b4IWKD-4wR1fzRynVJ939vgLTz0EL267ltQavg; JSESSIONID="ajax:2282448947320097342"; lidc="b=SB65:g=48:u=2:i=1511510576:t=1511596976:s=AQFK9FVUs7fNCUQgO6T6vtUG3rGvTHsh"; RT=s=1511510731451&r=https%3A%2F%2Fwww.linkedin.com%2Fuas%2Fconsumer-captcha-v2%3FchallengeId%3DAQGZrUTsGCMBZgAAAV_tDOyqigR7t5Mr5hFoZMHPos8wpKejwDVQEDQAmK70LvbZEWzO0jDZS-SUkCHTz5Q-xlPLxC0cjFZt2Q'
csrf = 'ajax:2282448947320097342'

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
    req = urllib2.Request(get_url)
    req.add_header("user-agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.linkedin.com/')
    req.add_header("Cookie", cookie)
    req.add_header('csrf-token', csrf)
    res_data = urllib2.urlopen(req, timeout=10)
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

for keyword_url in keyword_urls:
    keyword = keyword_url[0]
    url_prefix = keyword_url[1]
    for i in range(10):
        url = url_prefix + str(25 * i)
        request_sheet1(url, i + 1, keyword)

    write_excel('data/Vacancy_%s.xls' % keyword, sheet_data)
    del sheet_data
    sheet_data = [['Keywords&Index', 'Keyword', 'Index', 'Top Skills', 'URL', 'Title', 'Company', 'Company URL',
                   'No. of Employee', 'Date', 'Views', 'Job Desp', 'Requirements', 'Level', 'Industry',
                   'Employment Type', 'Job Functions', 'Manager Level', 'Senior Level', 'Director Level', 'Entry Level',
                   'Master', 'Bachelor', 'MBA', 'Other Education', 'Total Applicants']]
