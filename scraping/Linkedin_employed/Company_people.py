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
from scraping.utils import *


base_url = 'https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%2214318%22%5D&page='

cookie = 'li_sugr=a8ce6728-71d6-4b67-abf1-fd22471a652a; _ga=GA1.2.1103327498.1578739635; aam_uuid=67510623380186900253362623901423547553; _guid=0bc3ad95-9840-4d57-8e4e-c629e8a6d46e; lissc1=1; lissc2=1; cap_session_id=3029172246:1; u_tz=GMT+08:00; li_oatml=AQFWt9jC8rbmPQAAAW_Q2xxXmYrvpp5wzqyqnrEWOBNNNAIGuSdvJHf9L32SEmkH413u6hiX42T3oI-_NFc1YgdFE9aNsLPn; bcookie=v=2&aadbda16-1705-4ed3-8b4e-6cb06e3868a3; bscookie=v=1&2019112809180736397064-7c03-48ee-8c1c-0224dd7be59cAQFN8z_rzSFPrnVCTGKoPzx1PRK8emTl; lissc=1; fid=AQFErU8xR2XxzwAAAW_SwnKZeoIZbJlK97f6Camhnr-pt2W3gbKzwoQdDiXv5NYi0mnG5_P9y2kqeA; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; spectroscopyId=5416f06f-7b8f-48be-9805-47ef843ddbbb; visit=v=1&M; _lipt=CwEAAAFv1gP0vCPnISYiXCxezdux-MoYXMLXjjv5NrKPQ0INr60; JSESSIONID="ajax:8800147073815231271"; _gat=1; sl=v=1&d17Jg; li_at=AQEDARo-DEsBfFNBAAABb9cJhLgAAAFv-xYIuE0AF1HbU3Nsf5iluls_XOmJm-LKNLNf1E9SBujaJxNHUGQCT1HQtLg4TpTQcA3qWejih32ggtwHYF-DxsxN7VzIXWi_qdGfYTbU4r30QZeH8fMfCjcZ; liap=true; lang=v=2&lang=en-us; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-1303530583%7CMCIDTS%7C18285%7CMCMID%7C67373062266571776343343183455992432490%7CMCAAMLH-1580465535%7C3%7CMCAAMB-1580465535%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1579864353s%7CNONE%7CvVersion%7C3.3.0%7CMCCIDH%7C-89769995; UserMatchHistory=AQJhvlHP4lecBgAAAW_XCzOFysvLNMGFZ708d8buIFsyT8SyEanDI0nT4MBpX-zZqPXhvGv3cpOO_XB8fNdKaWXpXIau3p44jeMBHPU3dhxCLnkSLjPoeW3JqFkazK2FJ_7VRdLCJdZaqQYtObwJbbP1Ai5sSf1jIBkL41VfZKNTd4-xSh5fq0SGI8kfG8McgmdT76c-zyMGQoFuYal79eC4AOGiPqbj; lidc="b=SB95:g=134:u=174:i=1579860834:t=1579926639:s=AQFfnHqKZVjbQKH0JXWdKGS91XLtsEGG"'
unique_set = set()

sheet1_data = [['Unique ID', 'Name', 'Profile URL ', 'Latest Job Title', 'Company', 'Start Date', 'End Date ', 'Location', 'Previous Job Title', 'Company', 'Start Date', 'End Date', 'Location', 'University', 'Qualification']]
sheet2_data = [['Profile ID', 'Profile Url', 'Category', 'Skill Name', 'Endorsements']]
U_ID = 94


def get_sheet1(url):
    global U_ID, sheet1_data
    html = get_request_html(url, cookie)
    raw_reg = '"firstName":"(.*?)","lastName":"(.*?)".*?"occupation":"(.*?)".*?"objectUrn":"(.*?)".*?"publicIdentifier":"(.*?)"'

    profiles = re.compile(raw_reg).findall(html)

    for profile in profiles:
        personal_url = 'https://www.linkedin.com/in/' + profile[4]
        try:
            fir_name = profile[0]
            if 'firstName' in fir_name:
                fir_name = fir_name.split('firstName":"')[-1]
            las_name = profile[1]
            name = ' '.join([fir_name, las_name])
            if name == 'Ahana Mukherjee' or name == 'Zhao Dan' or profile[4] == 'zhao-dan-237544103':
                continue
            member_id = 'C_%d' % U_ID
            if personal_url in unique_set:
                continue
            # one_row = [member_id, name, personal_url] + request_profile(member_id, personal_url)
            one_row = [member_id, name, personal_url]
            print one_row
            sheet1_data.append(one_row)

            U_ID += 1
        except Exception as e:
            print 'exc--', personal_url, e


def request_profile(profile_id, personal_url):
    personal_html = get_request_html(personal_url, cookie)

    profile_details = request_profile_detail(personal_html)

    return profile_details


def request_profile_detail(html):
    reg = '<code.*?>(.*?)</'

    res = []
    includeds = re.compile(reg).findall(html)

    jobs = []
    education = []

    for included in includeds:
        try:
            if 'com.linkedin.voyager.dash.identity.profile.Position' not in included:
                continue
            data_obj = json.loads(included).get('included', [])
            for item in data_obj:
                div_type = item.get('$type', '')
                if div_type == 'com.linkedin.voyager.dash.identity.profile.Position':
                    jobs.append(item)
                if div_type == 'com.linkedin.voyager.dash.identity.profile.Education':
                    education.append(item)
        except Exception as e:
            print 'json load fail', e
            continue
    if jobs:
        res += sort_job(jobs)
    else:
        res += ['N/A' for i in range(10)]

    if education:
        res += sort_edu(education)
    else:
        res += ['N/A', 'N/A']
    return res


def sort_edu(ori_list):
    last = None
    big_y = None
    for ori in ori_list:
        if not ori.get('dateRange') or not ori['dateRange'].get('end') or not ori['dateRange'].get('start'):
            continue
        end_y = get_date_value(ori, 'end', 'year')
        if not last:
            big_y = end_y
            last = ori
            continue
        elif end_y > big_y:
            big_y = end_y
            last = ori

    if last:
        return [last.get('schoolName', 'N/A'), last.get('degreeName', 'N/A')]
    return ['N/A', 'N/A']


def sort_job(ori_list):
    res = []

    if len(ori_list) == 1:
        ori = ori_list[0]
        res += [ori.get('title', 'N/A'), ori.get('companyName', 'N/A'),
                get_date(get_date_value(ori, 'start', 'year'), get_date_value(ori, 'start', 'month')),
                'Present', ori.get('locationName', 'N/A')]
        res += [ori.get('title', 'N/A'), ori.get('companyName', 'N/A'),
                get_date(get_date_value(ori, 'start', 'year'), get_date_value(ori, 'start', 'month')),
                'Present', ori.get('locationName', 'N/A')]
        return res

    big_y = None
    big_m = None
    last = None
    present = None

    for ori in ori_list:
        if not ori.get('dateRange'):
            continue
        start_y = get_date_value(ori, 'start', 'year')
        start_m = get_date_value(ori, 'start', 'month')
        if not ori['dateRange'].get('end'):
            if not present:
                res += [ori.get('title', 'N/A'), ori.get('companyName', 'N/A'),
                        get_date(start_y, start_m), 'Present', ori.get('locationName', 'N/A')]
                present = ori
        else:
            end_y = get_date_value(ori, 'end', 'year')
            end_m = get_date_value(ori, 'end', 'month')
            if not last:
                big_y = end_y
                big_m = end_m
                last = ori
                continue
            if end_y > big_y:
                big_y = end_y
                big_m = end_m
                last = ori
            elif end_y == big_y and end_m > big_m:
                big_y = end_y
                big_m = end_m
                last = ori
    if last:
        ori = last
        res += [ori.get('title', 'N/A'), ori.get('companyName', 'N/A'),
                get_date(get_date_value(ori, 'start', 'year'), get_date_value(ori, 'start', 'month')),
                 get_date(get_date_value(ori, 'end', 'year'), get_date_value(ori, 'end', 'month')), ori.get('locationName', 'N/A')]
    else:
        res += ['N/A' for i in range(5)]

    return res


def get_date_value(ori, type, y_m):
    if ori.get('dateRange') and ori['dateRange'][type].get(y_m):
        return ori['dateRange'][type].get(y_m)
    return 1 if y_m == 'month' else 2000


def get_date(y, m):
    if m < 10:
        return '0%d/%d' % (m, y)
    return '%d/%d' % (m, y)


def get_endorse_details(profile_id, url):
    global sheet2_data
    endorse_url = 'https://www.linkedin.com/voyager/api/identity/profiles/%s/featuredSkills?includeHiddenEndorsers=true&count=50' % url.split('/')[-1]
    html = get_request_html(endorse_url)
    data_obj = json.loads(html)

    for item in data_obj.get('elements', []):
        one_row = [profile_id, item['skill']['name'], item['endorsementCount']]
        sheet2_data.append(one_row)


def get_data1():
    for i in range(7, 301):
        url = base_url + str(i)
        print '---', url, '---'
        get_sheet1(url)
    write_excel('sheet1.xls', sheet1_data)


def get_data0(filename):
    global sheet1_data
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]

    for i in range(1, table.nrows):
        row = table.row(i)
        c_id = row[0].value
        name = row[1].value
        url = row[2].value
        try:
            detail = request_profile(c_id, url)
            one_row = [c_id, name, url] + detail
            print one_row
            sheet1_data.append(one_row)
            time.sleep(3)
        except Exception as e:
            print c_id, e
    write_excel('sheet1.xls', sheet1_data)


get_data0('data/sheet0.xls')
