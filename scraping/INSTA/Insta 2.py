# -*- coding: utf-8 -*-
import datetime
import re
import urllib2
import xlwt,xlrd
import sys
import requests
import gc
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys

alldata = [['Username', 'Email of Profile', 'Url of posts']]
url = 'https://www.instagram.com/query/'
total_count = -1
url_prefix = 'https://www.instagram.com/p/'
files = []

crsf = 'EZivZDBYFjvO2jaKW4HdvMV0Qqbev3xQ'

def send_mail(filename, receiver):
    emaillist = receiver
    msg = MIMEMultipart()
    msg['Subject'] = filename
    msg['From'] = 'danielzhaochina@gmail.com'
    msg['Reply-to'] = 'danielzhaochina@gmail.com'
    msg.preamble = 'Multipart massage.\n'
    part = MIMEText("Hi, please find the attached file")
    msg.attach(part)
    part = MIMEApplication(open(filename,"rb").read())
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)

    if True:
        server = smtplib.SMTP('smtp.dev.garenanow.com', 465)
        server.sendmail(msg['From'], emaillist , msg.as_string())
        print 'send email success to ' + receiver + ' with: ' + filename
        server.close()
    else:
        print 'send email failed to ' + receiver + ' with: ' + filename

def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"

def write_excel(filename):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)
    print filename+"===========over============"

def request_html(media_after, i):
    global url, total_count, alldata
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'x-csrftoken': crsf,
        'referer': 'https://www.instagram.com/explore/tags/danielwellington/',
    }
    params = {
        'q': 'ig_hashtag(danielwellington) { media.after(' + media_after + ', 6) {  count,  nodes {    caption,    code,    comments {      count    },    comments_disabled,    date,    dimensions {      height,      width    },    display_src,    id,    is_video,    likes {      count    },    owner {      id    },    thumbnail_src,    video_views  },  page_info} }',
        'ref': 'tags::show'
    }
    print str(i) + ' -> ' + media_after
    try:
        request_res = requests.get(url, params=params, headers=headers, timeout=5)
        data = request_res.json()
        new_media_after = data['media']['page_info']['end_cursor']
        if data.get('status', 'NotOK') == 'ok':
            if total_count == -1:
                total_count = data['media']['count']
            nodes = data['media']['nodes']
            for node in nodes:
                post_url = url_prefix + node['code']+'/'
                try:
                    entries = get_details(post_url)
                    alldata += entries
                except:
                    print('ERROR=====', post_url)
                    continue
            return new_media_after
    except:
        print('ERROR=======', media_after)
        return media_after
    return media_after

def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res

def get_details(post_url):
    ret = []
    html = get_request(post_url)
    owner_reg = '<meta content=".*?@(.*?) '
    owner_url = re.compile(owner_reg).findall(html)
    if len(owner_url) > 0:
        name = owner_url[0]
        own_url = 'https://www.instagram.com/' + owner_url[0]
        own_html = get_request(own_url)
        own_reg = '<meta content="(.*?)" name="description" />'
        contents = re.compile(own_reg).findall(own_html)
        if len(contents) > 0:
            content = contents[0]
            emails = get_emails(content)
            for email in emails:
                ret.append([name, email, own_url])
            return ret
    return None

def get_emails(s):
    """Returns an iterator of matched emails found in string s."""
    regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
    return (email[0] for email in re.findall(regex, s) if not email[0].startswith('//'))

def get_folder_name_date():
    today = datetime.date.today()
    return str(today.month)+'_'+str(today.day) + '/'

def read_excel(filename):
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(0, table.nrows):
        row = table.row(i)
        try:
            name = row[0].value
            email = row[1].value
            url = row[2].value
            if email != 'N/A':
                alldata.append([name, email, url])
        except:
            print(i)

def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path or 'txt' in path:
            if 'result' not in path:
                files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files

reload(sys)
sys.setdefaultencoding('utf-8')
folder_name = get_folder_name_date()
i = 1
cookie = 'mid=V-o8CAAEAAF4WqfpAIxYW8j3GdBj; fbm_124024574287414=base_domain=.instagram.com; ig_dau_dismiss=1476864917691; sessionid=IGSC9050b9e55e8b51d9c523e299aec6f3a74cc0cd845279f5e9ef4768c25e8ba1ad%3AQJFpARI9e3y2GE6HJojEuQ3zV6uhjSAH%3A%7B%22_token_ver%22%3A2%2C%22_auth_user_id%22%3A1106215210%2C%22_token%22%3A%221106215210%3A1ahmvxAUtx9hVXoB613r4rO119opU6HK%3A378f84445d43da1646d3638681ac60fdae8627acbc447d6e81ff2243a629312a%22%2C%22asns%22%3A%7B%22101.127.248.164%22%3A4657%2C%22time%22%3A1477287505%7D%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22last_refreshed%22%3A1477287506.121387%2C%22_platform%22%3A4%2C%22_auth_user_hash%22%3A%22%22%7D; ig_pr=2; ig_vw=1655; s_network=; fbsr_124024574287414=sBeREsZyvIEi_l1-3L2m0TNC7SdVReFrOw3H6o_kZCk.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURHNU9nUUx6bDhFTGVYSk04N2x6THIyallwQ1RObTdfSG1leGpIejdPVEVjdEw0dk4tVVIyenFlTXdacWkxM0YyNGlvVTZXV3MtWnlpanpsUDM2eER0cnJhWlJ6TTVGbTdaVXBTVnNUSmt0SERwMlNCSEFxX2JFbEgwOW85UTNQM2ZDeXhIdzB1WHlUMURienhqS0ZvTHE2T2ExWF9obklvRml6UFM4eFR5RlN2OUhxa19VWTlfU1QwdllScVFCdzVMeXFwZ0lGSVB4ckxrQVpydXVMTHlWN1BuYVEwVTNrN0p4ckNwaWpsWV95aE5LVGtERVZHdWt2QmxxOHUxOGdNOTlBOTVpcXo3VnU0MF9uUDlGZUh1Z0R4ZF9ROWMtM2RrZmtPNzF6YWhTN3JPUERDQkRxdW1XckFJVkFjWE1oS3IxNDF5YUszSlpTTGlIRWYwWWFWayIsImlzc3VlZF9hdCI6MTQ3NzI4NzUwNywidXNlcl9pZCI6IjEwMDAwNjk1NzczODEyNSJ9; csrftoken=EZivZDBYFjvO2jaKW4HdvMV0Qqbev3xQ; ds_user_id=1106215210'
media_after = 'J0HWA2dvAAAAF0HWA2SHwAAAFkIA'


while i <= 1500:
    try:
        param = media_after
        media_after = request_html(param, i)
        i += 1
        if i % 100 == 0:
            if i == 100:
                write_excel(folder_name + '0' + str(i)+'_Ins_startup.xls')
            else:
                write_excel(folder_name + str(i)+'_Ins_startup.xls')
            del alldata
            gc.collect()
            alldata = []
    except:
        write_excel(folder_name + str(i)+'_Ins_startup.xls')
        break
del alldata
gc.collect()
alldata = []
folder = get_folder_name_date()
files = walk(folder)
for fi in files:
    try:
        read_excel(fi)
    except:
        print('ERROR open: ' + fi)
write_name = folder + folder[:-1]  + '-result.xls'
write_excel(write_name)
send_mail(write_name, 'danielzhaochina@gmail.com')
