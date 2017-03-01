# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
import requests
import gc

alldata = [['Username', 'Email of Profile', 'Url of posts']]
url = 'https://www.instagram.com/query/'
total_count = -1
url_prefix = 'https://www.instagram.com/p/'

cookie = 'mid=V-qN9AAEAAF7CwrDM60ZbWfSmnLE; fbm_124024574287414=base_domain=.instagram.com; ig_dau_dismiss=1475075974794; s_network=True; sessionid=IGSC885636c12738327bf5f96751a0d5f3304f688667d80955cca748f69f0f2f95c3%3ASlCdr7sRz5jMcm24NIRNjskKQOtzvag3%3A%7B%22_token_ver%22%3A2%2C%22_auth_user_id%22%3A1106215210%2C%22_token%22%3A%221106215210%3AESbWwEaY8pPzmBKXtTVnhByzbcTtltDQ%3A272410dbc3ce7419467506094bc55d9d80b522f7e97d0a4511b3ac1da27bfd54%22%2C%22asns%22%3A%7B%22119.74.13.134%22%3A9506%2C%22time%22%3A1476023753%7D%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22last_refreshed%22%3A1476023754.25982%2C%22_platform%22%3A4%2C%22_auth_user_hash%22%3A%22%22%7D; ig_pr=2; ig_vw=1234; fbsr_124024574287414=hLS-YKHPKMmLrvajw0RuOQhQDAnam2VIDO7hbNzvIPA.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUJUZWhzNnN0dHRKYXE5U1ZoLTdKcFhHWmdTN2tjSEVlODh3REtQUUwtUFdUUXhhRTM0d0Q4ZWk0NjdUdmpWWDMyMXlQd1FHbmpDeG4zSGs1UGFMQlVGWDFob2IyWUpaUnJGcG15SWRmRjRmQ1MtcGQ4NWhjNzZzcWszenRfZWdaOUdkMS0zc0lmeDdLSTVucHhOLTl4bkl2cVBxbk5FOThxV2pzMGMwblY4U1F0YXVIVDNhZEpicWJoYkJaSGc3TUZhNWQ4cVl6aHJBUm8ydFJhUmRTaEJmWUNWRzBFMld6TVd6andCOXhCbDZKeENEWktHS2JTZWRQZEhVMklqakNhSENTTTkxUzQwVFEtcWIxSW9ZN05KcVdxcTU0WW1PWTlCa3UzYmhIS1pfODlSRnpfY1gwbU1paDJPaEQ1WGNnNEdpMEZTTERpNW9DeUIyZDRLRF8zeiIsImlzc3VlZF9hdCI6MTQ3NjAyMzc1NiwidXNlcl9pZCI6IjEwMDAwNjk1NzczODEyNSJ9; csrftoken=IpkMwbAaHEnJAs2u4egrCqfhSimJ4wmA; ds_user_id=1106215210'
crsf = 'IpkMwbAaHEnJAs2u4egrCqfhSimJ4wmA'

def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename):
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
        'referer': 'https://www.instagram.com/explore/tags/startup/',
    }
    params = {
        'q': 'ig_hashtag(startup) { media.after(' + media_after + ', 6) {  count,  nodes {    caption,    code,    comments {      count    },    comments_disabled,    date,    dimensions {      height,      width    },    display_src,    id,    is_video,    likes {      count    },    owner {      id    },    thumbnail_src,    video_views  },  page_info} }',
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


reload(sys)
sys.setdefaultencoding('utf-8')

i = 0
media_after = 'J0HV_pVuAAAAF0HV_pTEAAAAFkIA'
while i <= 20000:
    try:
        param = media_after
        media_after = request_html(param, i)
        i += 1
        if i % 50 == 0:
            write_excel(str(i)+'_Ins_startup.xls')
            del alldata
            gc.collect()
            alldata = []
    except:
        write_excel(str(i)+'_Ins_startup.xls')
        break
