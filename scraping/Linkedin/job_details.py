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
sheet1_data = [['index', 'url', 'Title', 'Company', 'Date', 'Views', 'Job Desp', 'Requirements', 'Level', 'Industry', 'Employment Type', 'Job Functions', 'Manager Level', 'Senior Level', 'Director Level', 'Entry Level', 'Master', 'Bachelor', 'MBA', 'Other Education']]
sheet2_data = [['Company index', 'Top Skills']]

cookie = 'bcookie="v=2&2f6c9444-0b2f-466a-8183-ef73e05efa35"; bscookie="v=1&2017041006541990b97a3b-1e52-4da3-8e47-33e0e8e1e3aeAQGgvnt_FYPCpH58BfQhdPydnY6jBTcZ"; visit="v=1&M"; _chartbeat2=DCi2d9ksmx1CfcAv5.1493951580217.1493951580225.1; __utma=226841088.610623672.1491807398.1497595445.1497595445.1; __utmz=226841088.1497595445.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __ssid=ade20105-3abb-46d5-9567-d3cd78c040fd; li_at=AQEDARo-DEsDI_rjAAABXe7gULIAAAFeO5By1FEAn2D-WPBHxvixfa4hz5OidGNyDviGJW1nFBtR-hAqaymqXnF8vdZzIrziKesqwjehelsPjBbphx2AaKgR3UVYUVIoAkX2igN7Sm00M4SmSGWmLvQO; liap=true; sl="v=1&isB1Y"; JSESSIONID="ajax:6931840371620771414"; _gat=1; lang=v=2&lang=en-us; _lipt=CwEAAAFeF6WWl1JEcsuyrM-nVK2GLyqNXNTDtWHQnSFhCGd1uyZTfvH7vGZey8y-WHebF9cMq95Z9-KFkBTsq7zxIUL6hf9-_AB8B9DDKOZWw4CZQWErj2_OCp_KUrggP9cU2OEXE0lOVBCgCedmUQ5DX8-y3WVODkWZ75J-PVm8yBnJbbE0ValdfURJ6fvQxaNxf2ABWfcbWwFhC7CLmxs4cg4WiNxY5tcghdyy_2EeWLKS3RnNkK3gG-JnevDIxwcINWOb8iBcRDGnb6KTNFEbiz-Y5TgssvVh2oQ2AMiv5zakliW-xWDcwuZWAEHEC_XphED3aas9lxNGnyV0Aaw-aXz_iflddvb_x61zRAoTWHRvS1Tro2bkAPY; lidc="b=SB95:g=28:u=49:i=1503635307:t=1503719475:s=AQEYE0JTsDrdoZmJyOMEBA9W19ao9NUG"; _ga=GA1.2.610623672.1491807398'
csrf = 'ajax:6931840371620771414'

urls = [
    'https://www.linkedin.com/jobs/search/?keywords=customer%20protection&location=India&locationId=in%3A0&start=',
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


def request_sheet1(url, key):
    raw_reg = 'fs_jobSavingInfo:(.*?)"'
    html = get_request(url)
    job_ids = re.compile(raw_reg).findall(html)

    for i in range(len(job_ids)):
        index = str(key) + '.' + str(i+1)
        request_job_details(index, job_ids[i])
        time.sleep(1)


def request_job_details(index, job_id):
    job_url = 'https://www.linkedin.com/jobs/view/%s/' % job_id
    applicant_url = 'https://www.linkedin.com/voyager/api/jobs/applicantInsights/%s' % job_id
    company_url = 'https://www.linkedin.com/voyager/api/jobs/jobPostings/%s' % job_id
    job_html = get_request(job_url)

    company_reg = '"name":"(.*?)"'

    company_name = re.compile(company_reg).findall(job_html)
    if company_name:
        company_name = company_name[0]
    else:
        company_reg = '"companyName":"(.*?)"'
        company_name = re.compile(company_reg).findall(job_html)
        if company_name:
            company_name = company_name[0]
        else:
            company_name = ''

    company_html = get_json_resp(company_url)
    date = get_date(company_html.get('listedAt', 0) / 1000)
    level = company_html.get('formattedExperienceLevel', '')
    industry = ', '.join(company_html.get('formattedIndustries', []))
    employ_type = company_html.get('formattedEmploymentStatus', '')
    views = company_html.get('views', 0)
    job_functions = ', '.join(company_html.get('formattedJobFunctions', []))

    title = company_html.get('title', '')
    text = company_html.get('description', {}).get('text', '').replace('\n', '').split('Requirements')
    desp = text[0].strip() if text[0].strip() != '' else text[-1].strip()
    requirements = text[-1].strip() if len(text) == 2 else ''

    bachelor = mba = master = 0
    applicant_html = get_json_resp(applicant_url)
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
    for skill in skill_details:
        name = skill.get('formattedSkillName', '')
        if name != '':
            sheet2_data.append([index, name])

    sheet1_one_row = [index, job_url, title, company_name, date, views, desp, requirements, level, industry, employ_type, job_functions, manager, senior, director, entry, master, bachelor, mba, other]
    print index, company_name, date, views, level, manager, master, len(skill_details)
    sheet1_data.append(sheet1_one_row)


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
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.linkedin.com/')
    req.add_header("Cookie", cookie)
    req.add_header('csrf-token', csrf)
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return HTMLParser.HTMLParser().unescape(res)


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
            print one_row
            company_data.append(one_row)
            if i % 400 == 0:
                write_excel('data/res'+str(i)+'.xls', company_data)
        except:
            print(i)


reload(sys)
sys.setdefaultencoding('utf-8')

for url_prefix in urls:
    for i in range(10):
        url = url_prefix + str(25 * i)
        request_sheet1(url, i+1)

write_excel('data/sheet1.xls', sheet1_data)
write_excel('data/sheet2.xls', sheet2_data)

