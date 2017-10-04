# -*- coding: utf-8 -*-
import re
import urllib2
import xlwt
import HTMLParser
import os
import requests

companies = ["American Express", "GE Energy Connections", "T & A Solutions", "NEC India", "Atos", "Resource Infinite", "Metro Jobs Consultancy Private Limited", "Next Step Services Private Limited", "SimSolJobs - Placement Division of SimSol Technologies & Services Pvt Ltd", "Akamai Technologies", "Secure-24", "Vitasta Consulting Pvt Ltd", "Anchorite Recruitment And Marketing Services Private Limited", "Dell", "Winfo", "Open Systems International", "Deloitte", "NTT DATA Corporation", "Eureka Forbes Ltd", "Sanovi, An IBM Company", "ZyloTech", "universalhunt", "Hyper Drive Information Technologies Pvt Ltd", "Total System Services, Inc.", "Experis IT India", "EiQ Networks", "NVIDIA", "ESSEN VISION SOFTWARE PVT LTD.", "IBM", "HEADS2YOU", "BNY Mellon", "Sant Dnyaneshwar Hospital", "Morgan Stanley", "Intersoftkk ( India ) Pvt. Ltd.", "Google", "Medispec", "flydubai", "BT for Global business", "DSM", "Partner in Search B.V.", "Porus", "Sify Technologies Limited.", "ELMEASURE INDIA PVT LTD", "Larsen & Toubro", "GPX Global Systems, Inc.", "ABB", "iSource Online Services Pvt. Ltd.", "Gemalto", "Protonzone Consulting", "DBS Bank", "WE Network", "SYRATRON Marketing Pvt Ltd", "K Power Management Services", "Digital Proficio", "Infosys", "SCOPE T&M", "STPL Global", "ECI Telecom", "HCL Technologies", "Fortinet", "Lumen21, Inc", "ICF Consulting", "Wipro Limited", "Ciena", "FireEye, Inc.", "SECURE HR SERVICES Find The Right Job", "Birlasoft", "Inflow Technologies Pvt Ltd", "Novartis", "HeadHonchos.com", "Texas Instruments", "Vodafone", "Symantec", "IDFC Bank", "Goetze Dental", "Aditya Birla Group", "Investis", "Druva", "Allegion, PLC", "Bank of America", "GSTi Technologies India Pvt. Ltd", "Schneider Electric", "SPECIALITY CHEMICALS LIMITED", "VMware", "Sharp & Score HR Consulting Pvt. Ltd.", "VA TECH WABAG LTD.", "Hortonworks", "Delta Consultancy Limited", "Resil Chemicals", "Extreme Networks", "First Solar", "SBA Info Solutions Pvt. Ltd", "Motilal Oswal Financial Services Ltd", "Sarthee Consultancy", "JPMorgan Chase & Co.", "Cohesity", "Sprint", "The Dow Chemical Company", "UnitForce Technologies Consulting Pvt Ltd", "Happiest Minds Technologies", "Fairfield Inn And Suites", "Zoomcar", "HashtagTalent", "IBM India Private Limited", "Leading Management Consultant", "Ace Turtle Services Ltd", "Ace IT Solutions", "AVTAR Career Creators", "PayPal", "Techniche E-Commerce Solutions Pvt. Ltd.", "Clarivate Analytics", "Saint-Gobain", "IPMS AB", "BCD Travel", "Save the Children, India", "Dinoct Inc", "SDL plc", "HireRight", "Vovantis Laboratories - India", "Rivera Manpower Services", "NetApp", "Exide Life Insurance", "WealthChaser Global Research", "DHFL Pramerica Life Insurance", "Saint-Gobain India Private Limited - Glass Business", "National Bulk Handling Corporation Pvt. Ltd", "Ingersoll Rand", "AZ Group", "BGR Energy Systems", "Infosys BPO", "GloCons Consulting", "Colt Technology Services", "Qualitrol", "Firepro Systems", "Mangalam Placement Private Limited", "BR Raysoft Tech Pvt. Ltd", "Aujas", "Precision Management Services Private Limited", "RedQuanta", "Bombardier Transportation", "Medtronic", "Sammraksha Digital Security Systems - India", "Wipro Consulting", "Airborne Recruiting Pvt. Ltd.", "Experis IT India", "ESSEN VISION SOFTWARE PVT LTD.", "GE Energy Connections", "Vitasta Consulting Pvt Ltd", "Marriott", "Airborne Recruiting Pvt. Ltd.", "Experis IT India", "ESSEN VISION SOFTWARE PVT LTD.", "GE Energy Connections", "Vitasta Consulting Pvt Ltd", "Marriott", "NTT DATA Corporation", "NVIDIA", "American Express", "DSM", "SimSolJobs - Placement Division of SimSol Technologies & Services Pvt Ltd", "ABB", "Ciena", "Sant Dnyaneshwar Hospital", "Anchorite Recruitment And Marketing Services Private Limited", "iSource Online Services Pvt. Ltd.", "Fortinet", "Symantec", "Gemalto", "K Power Management Services", "Porus", "Bank of America", "HeadHonchos.com", "T & A Solutions", "VA TECH WABAG LTD.", "Fortinet", "Symantec", "Gemalto", "K Power Management Services", "Porus", "Bank of America", "HeadHonchos.com", "T & A Solutions", "VA TECH WABAG LTD.", "Texas Instruments", "Clarivate Analytics", "Aditya Birla Group", "universalhunt", "Happiest Minds Technologies", "Sarthee Consultancy", "HCL Technologies", "Exide Life Insurance", "PayPal", "IPMS AB", "UnitForce Technologies Consulting Pvt Ltd", "National Bulk Handling Corporation Pvt. Ltd", "Dell", "BR Raysoft Tech Pvt. Ltd", "RedQuanta", "Delta Consultancy Limited", "IPMS AB", "UnitForce Technologies Consulting Pvt Ltd", "National Bulk Handling Corporation Pvt. Ltd", "Dell", "BR Raysoft Tech Pvt. Ltd", "RedQuanta", "Delta Consultancy Limited", "Cohesity", "Wipro Limited", "ESSEN VISION SOFTWARE PVT LTD.", "Infosys BPO", "Courtyard by Marriott", "Vitasta Consulting Pvt Ltd", "SimSolJobs - Placement Division of SimSol Technologies & Services Pvt Ltd", "Ciena", "ABB", "DSM", "HeadHonchos.com", "Symantec", "Porus", "VA TECH WABAG LTD.", "IPMS AB", "Happiest Minds Technologies", "Sant Dnyaneshwar Hospital", "National Bulk Handling Corporation Pvt. Ltd", "DSM", "HeadHonchos.com", "Symantec", "Porus", "VA TECH WABAG LTD.", "IPMS AB", "Happiest Minds Technologies", "Sant Dnyaneshwar Hospital", "National Bulk Handling Corporation Pvt. Ltd", "Fortinet", "HCL Technologies", "Dell", "Cohesity", "Ekhard Hr Services", "ABB", "DSM", "HeadHonchos.com", "National Bulk Handling Corporation Pvt. Ltd", "Fortinet", "Symantec", "SimSolJobs - Placement Division of SimSol Technologies & Services Pvt Ltd", "Confidential", "DSM", "HeadHonchos.com", "National Bulk Handling Corporation Pvt. Ltd"]

url_template = 'https://www.glassdoor.com/Reviews/company-reviews.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={keyword}&sc.keyword={keyword}&locT=&locId=&jobType='

cookie = 'ARPNTS=1550166208.36895.0000; ARPNTS_AB=441; trs=www.google.com.sg::SEO:2017-08-04+01%3A59%3A02.302:undefined:undefined; optimizelyEndUserId=oeu1501837289139r0.5400456933420208; bm_monthly_unique=true; __gacid=a6276df9-9cf8-416e-8c0b-49a55b1c95fc; __qca=P0-136999423-1501837292507; uc=8F0D0CFA50133D96DAB3D34ABA1B8733A90DB0B7B939732C1892CC5BFCB7F454C877B02CCE3C6B586DE092CC1DE095D5A0E1C04FDCB6385673CC4B7293083E17280D891C93C8FDE0C32B896BCB0E70CBEA6FE2587904CC74AB32243503A7D97F54D52C7BB462DC6D9E78CA0B352BC748AF04B56C7BD16B732520E08E3D6F92100701B5FEB4347AAC9C79331A4BB605F2F0940A1F49F55650; __vrz=1.0.5; bm_last_load_status=BLOCKING; JSESSIONID=D1E23BD389E5AEFBBA1F0E02CA8DF57D; _uac=0000015e17fdcb80bec772dd353a1aff; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%2C%22bizo%22%3A%5B%5D%7D; _gat_UA-2595786-1=1; mp_5d4806b773713d93bd344cf2365e6df0_mixpanel=%7B%22distinct_id%22%3A%20%2215e17ff676cb55-05436dc9eb58b2-31617c01-1fa400-15e17ff676dc5b%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.glassdoor.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.glassdoor.com%22%7D; _ga=GA1.2.274160009.1503641049; _gid=GA1.2.664720309.1503641049; GSESSIONID=D1E23BD389E5AEFBBA1F0E02CA8DF57D; cass=0; gdId=318d3b4d-6d5f-4b9e-a135-3de898d0ae7d; _uetsid=_uet656b5fed'

all_data = [['Company Name', 'Rating', 'Percentage']]

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


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_json_resp(url):
    resp = requests.get(url, headers={
        'Cookie': cookie,
        'csrf-token': 'ajax:0900888224690545225',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    })
    if resp.status_code == 200:
        return resp
    return {}


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.linkedin.com/')
    req.add_header("Cookie", cookie)
    req.add_header('csrf-token', 'ajax:0900888224690545225')
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    return res


def request_result(keyword):
    url = url_template.format(keyword=keyword.replace(' ', '+'))

    html = get_request(url)
    if 'id=\'EmpStats_Recommend\'' in html:
        reg = 'class=\'ratingNum\'>(.*?)<.*?id=\'EmpStats_Recommend\' data-percentage=\'(.*?)\''
    elif 'class=\'minor hideHH margRtLg block margTopXs\'> ' in html:
        reg = 'class=\'bigRating strong margRtSm h1\'>(.*?)<.*?class=\'minor hideHH margRtLg block margTopXs\'> (.*?)% recommended'
    elif 'Try more general keywords' in html:
        one_row = [keyword, 'N/A', 'N/A']
        print one_row
        all_data.append(one_row)
        return
    else:
        one_row = [keyword, 'N/A', 'N/A']
        print one_row
        all_data.append(one_row)
        return
    percentage = re.compile(reg).findall(html)
    if percentage:
        rating = percentage[0][0]
        percentage = percentage[0][1]
        one_row = [keyword, rating, percentage]
    else:
        one_row = [keyword, 'N/A', 'N/A']
    print one_row
    all_data.append(one_row)

for company in companies:
    request_result(company)
write_excel('data/sheet2.xls', all_data)