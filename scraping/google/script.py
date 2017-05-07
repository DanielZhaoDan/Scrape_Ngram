# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import sys
from datetime import datetime
import HTMLParser
import os
from urlparse import urlparse
import time
import random

sheet1_data = [['Keywords', 'Country', 'No of Articles', 'Page No.', 'News Url', 'Date', 'Name of Publisher', 'Main url of newspaper/magazine', 'Headline', 'Content']]
sheet_dict = {}

url_bases = 'https://www.google.com.sg/search?q="{key_word}"+location:{location}&newwindow=1&safe=strict&hl=en&tbm=nws&start='

key_words = ['HR Information System', 'HR metrics', 'HR Analytics', 'Workforce Analytics', 'Employee Productivity', 'Employee Retention']

locations = ['Singapore', 'USA', 'India']

cookie = [
    'loyal-user=%7B%22date%22%3A%222017-05-05T10%3A42%3A30.417Z%22%2C%22isLoyal%22%3Atrue%7D; user_num=nowset; D_SID=101.127.248.164:hZwo/D7nxTV5c6G7U7OKKi30kCXCeafszRGphpqX+dQ; .SGTOKEN.SIMILARWEB.COM=VnPs5wcW0fTWrxtZ2JeGLXjoGB9VXwcvDsCx7HcU8wVUQsdTvLI9Dr7DWM6ZgOe5zAF88ZHElX0JoPf9XC0Cm6bh3bCXQEkn_dunCaNVi0jzAlH5AE_065I9jjevquuyCAEwWLPjHQsP8R5lvlAeqx7-Mnh0EFEUJrZEMrPUV6KHPO2hA7e41vcOhaw2yinnNPOjGKj8akbob-dJbEPBoJZ-T3rbvRG3UlF_zh94QYQe8zaAWm1PWUoWEuErO4JaVl224CVuLpn-bWSZPY4COg2; loyal-user=%7B%22date%22%3A%222017-05-05T10%3A42%3A30.417Z%22%2C%22isLoyal%22%3Atrue%7D; intercom-id-e74067abd037cecbecb0662854f02aee12139f95=a1d8f8fa-c8ab-4006-a098-dc8bad4c8a61; jaco_uid=d20e0e5b-ad07-476a-907c-d3e375ce3916; _vwo_uuid_v2=8CBF81F644F3B1BE1491484028D1AE94|75541191817cd575562bee7e20e996d5; _uetsid=_uet61e53b7c; _ga=GA1.2.436898580.1493980950; _gid=GA1.2.751046336.1494058137; sc_is_visitor_unique=rx8617147.1494058138.B2C03213D7E94FF953CB1486024EE930.3.3.2.2.2.2.1.1.1; _pk_id.1.fd33=4a1ceb3e328cae31.1493980952.3.1494058138.1494054820.; _pk_ses.1.fd33=*; _bizo_bzid=394f2ad9-dbbc-42eb-9e38-3e2767f97584; _bizo_cksm=D12D7C4D5F3D89C4; D_IID=1237C69B-5331-398F-9442-B5564ECEEEBD; D_UID=69CDC19F-D308-33CA-A9ED-DD98ADFEBA0B; D_ZID=8BC5D89F-1A9A-303F-BA79-909CEDE3823D; D_ZUID=FE342C0C-B34B-369E-B48F-B5CB5E04DDE8; D_HID=6F0974DF-D922-3710-961D-E95A2BFE6BA0; _mkto_trk=id:891-VEY-973&token:_mch-similarweb.com-1493980952670-28952; _we_wk_ss_lsf_=true; _bizo_np_stats=155%3D482%2C; intercom-session-e74067abd037cecbecb0662854f02aee12139f95=bTNjUiszcC9hUDdzb0xiMjNYbDNRSlI4cU14OXBFMkdkUWx3d2J5OE9PNUF1ZTc0bjhCYUlSMERwZmtrRFNkeC0tSTJOVXRVbExWNGo2MTRnL0k4NDJKdz09--cc4c3f8d4c0818d2f45f0c8f6d57bcdddeea5d73',
    'loyal-user=%7B%22date%22%3A%222017-05-05T10%3A42%3A30.417Z%22%2C%22isLoyal%22%3Atrue%7D; user_num=nowset; D_SID=101.127.248.164:hZwo/D7nxTV5c6G7U7OKKi30kCXCeafszRGphpqX+dQ; loyal-user=%7B%22date%22%3A%222017-05-05T10%3A42%3A30.417Z%22%2C%22isLoyal%22%3Atrue%7D; intercom-id-e74067abd037cecbecb0662854f02aee12139f95=a1d8f8fa-c8ab-4006-a098-dc8bad4c8a61; jaco_uid=d20e0e5b-ad07-476a-907c-d3e375ce3916; sgID=9cca268d-c90b-8d72-f8a3-4274c66ebcb8; __utma=107333120.436898580.1493980950.1494058681.1494058681.1; __utmb=107333120.25.9.1494059206440; __utmc=107333120; __utmz=107333120.1494058681.1.1.utmcsr=similarweb.com|utmccn=(referral)|utmcmd=referral|utmcct=/website/tnp.sg; __utmv=107333120.|1=email=danielzhaochina%40gmail.com=1; intercom-session-qoipdbi5=RzM3UXdnSzgwMGFHS2lyU0FKeFQwUFFlZk9VaVpUb3pPTHdpR0ZRTmE5R2R3OVVJdGpBaFFydUJKTURRZWhMNy0tN1lLOUNzMUpiSUZZRFhBR0pES0VjZz09--4c8b9cb65a8ba3727f50b6f801903e20a1fc6ee9; _gat=1; sc_is_visitor_unique=rx8617147.1494060163.B2C03213D7E94FF953CB1486024EE930.3.3.2.2.2.2.1.1.1; _ga=GA1.2.436898580.1493980950; _gid=GA1.2.1664794251.1494060164; _gat_UA-42469261-1=1; D_IID=1237C69B-5331-398F-9442-B5564ECEEEBD; D_UID=69CDC19F-D308-33CA-A9ED-DD98ADFEBA0B; D_ZID=8BC5D89F-1A9A-303F-BA79-909CEDE3823D; D_ZUID=FE342C0C-B34B-369E-B48F-B5CB5E04DDE8; D_HID=6F0974DF-D922-3710-961D-E95A2BFE6BA0; _vwo_uuid_v2=8CBF81F644F3B1BE1491484028D1AE94|75541191817cd575562bee7e20e996d5; _bizo_bzid=394f2ad9-dbbc-42eb-9e38-3e2767f97584; _bizo_cksm=750D4CB6ECADC55A; _uetsid=_uet61e53b7c; _mkto_trk=id:891-VEY-973&token:_mch-similarweb.com-1493980952670-28952; _pk_id.1.fd33=4a1ceb3e328cae31.1493980952.3.1494060165.1494054820.; _pk_ses.1.fd33=*; _bizo_np_stats=155%3D654%2C; _we_wk_ss_lsf_=true; intercom-session-e74067abd037cecbecb0662854f02aee12139f95=Mkl5VkRSTlhkb01ZbjFSK3BmcCtpbVJvdDlZN2tHa1lITjd4eCtxZWtTd2RQZ1NpSm5UdnpkeWNUemVIWnRvQi0tYlZ2K0VOY05tSTNOTjRkTDdOYWUrUT09--4e49087cc71c376d48b313cd94ddb5a5a9af97b7',
    'loyal-user=%7B%22date%22%3A%222017-05-06T08%3A43%3A36.382Z%22%2C%22isLoyal%22%3Afalse%7D; user_num=nowset; _pk_id.1.fd33=123a056b0edfd857.1494060219.0.1494060219..; _gat=1; _ga=GA1.2.273284257.1494060217; _gid=GA1.2.1140844050.1494060219; _gat_UA-42469261-1=1; _vwo_uuid_v2=38866838A30ABE235EA65A95D56BDA86|7e926eaca0da9ecc6b55040f4cdc3aab',
]

agent_ip = [
    '61.153.232.218', '117.90.0.80', '218.86.128.57', '218.95.246.53', '112.95.22.210', '61.139.104.216', '111.20.214.25', '211.142.141.210', '112.95.22.153', '111.202.121.57',
]

API_KEY = '051278798bc5c8d530a33186637244a9'

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


def get_total_count(html):
    reg = 'id="resultStats">.*?(\d.*?) result'
    results = re.compile(reg).findall(html)
    if results:
        return int(results[0].replace(',', ''))
    return 10


def request_sheet1(key_word, location, url_base):
    global sheet1_data
    total_count = 0
    page_no = 1
    while True:
        url = url_base + str(page_no-1) + '0'
        print url
        if page_no > 10:
            break
        html = get_request(url)
        if total_count == 0:
            total_count = get_total_count(html)
        topic_detail_reg = 'class="l _HId".*?href="(.*?)".*?>(.*?)<.*?"_tQb _IId">(.*?)<.*?f nsa _uQb">(.*?)<'
        topic_detail = re.compile(topic_detail_reg).findall(html)
        if not topic_detail:
            break
        for detail in topic_detail:
            url = detail[0]
            o = urlparse(url)
            main_url = o.scheme + '://' + o.netloc
            headline = remove_html_tag(detail[1])
            publisher = detail[2]
            date = get_date(detail[3])
            content = get_raw_content(url)
            one_row = [key_word, location, total_count, page_no, url, date, publisher, main_url, headline, content]
            sheet1_data.append(one_row)
        page_no += 1
        time.sleep(10)


def get_raw_content(url):
    try:
        html = get_request(url)
        reg = '<body.*?>(.*?)</body>'
        contents = re.compile(reg).findall(html)
        if contents:
            content = contents[0]
            step_0 = remove_html_tag(content) # remove html tag
            step_1 = re.sub('[ \t\n\r]+', ' ', step_0) # remove multiple blank, newline and tab
            return step_1
        return html
    except:
        return ''


def request_sheet2(base_url):
    global sheet_dict
    if sheet_dict.get(base_url):
        return sheet_dict[base_url]

    if len(sheet_dict) and len(sheet_dict) % 5 == 0:
        print 'Sleeping 300 seconds'
        time.sleep(60)
    else:
        print 'Sleeping 10 seconds'
        time.sleep(10)
    rank_reg = 'rankingItem--global.*?rankingItem-value.*?>(.*?)<.*?rankingItem--country.*?rankingItem-value.*?>(.*?)<.*?rankingItem--category.*?rankingItem-value.*?>(.*?)<.*?Total Visits.*?countValue">(.*?)<'
    country_tag = 'accordion-toggle.*?countValue">(.*?)<.*?country-name.*?>(.*?)<'

    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[-1]
    print url + ' ' + str(len(sheet_dict))
    html = get_request(url)
    if 'NAME="ROBOTS"' in html:
        print 'ROBOT DETECTED!, sleeping 600 seconds'
        time.sleep(600)
        return None
    global_ranks = re.compile(rank_reg).findall(html)
    if global_ranks:
        ret = [global_ranks[0][0].replace('[#,]', ''), global_ranks[0][1].replace('[#,]', ''), global_ranks[0][2].replace('[#,]', ''), global_ranks[0][3]]
    else:
        ret = [0, 0, 0, 0]

    country_ranks = re.compile(country_tag).findall(html)
    for country in country_ranks:
        ret.append(country[1])
        ret.append(country[0])
    if len(ret) == 4:
        ret += [0 for i in range(10)]
    sheet_dict[base_url] = ret
    return ret


def read_excel(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            main_url = row[7].value
            publisher = row[6].value
            article_url = row[4].value
            country = row[1].value
            details = request_sheet2(main_url)
            if not details:
                i -= 1
                continue
            one_row = [publisher, main_url, article_url, country] + details
            print one_row
            sheet2_data.append(one_row)
        except:
            print(i)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_date(ori):
    try:
        date = datetime.strptime(ori, '%d %b %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_request(get_url):
    ip = random.choice(agent_ip)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': random.choice(cookie),
        'x-client-data': 'CJG2yQEIprbJAQjBtskBCPKZygEI+5zKAQipncoB',
        'User-Agent': ip,
        'Host': 'www.similarweb.com',
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')
# scrape google search result
# urls = []
# for key_word in key_words:
#     for location in locations:
#         urls.append([key_word, location, url_bases.format(key_word=key_word.replace(' ', '+'), location=location)])
# print len(urls)
# for url in urls:
#     request_sheet1(url[0], url[1], url[2])
# write_excel('data/sheet1.xls', sheet1_data)

# scrape rank data
filename = 'data/sheet1.xls'
read_excel(filename, 1)
write_excel('data/sheet2.xls', sheet2_data)
