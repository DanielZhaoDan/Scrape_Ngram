# -*- coding: utf-8 -*-

import re
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import requests
from BeautifulSoup import BeautifulSoup

import requests.packages.urllib3.util.ssl_

sheet0_data = [['Topic ID', 'Title', 'Title URL', 'User Name', 'Year Joined',
                'Thread created date', 'Likes', 'No. of replies', 'No. of posts by user', 'Text']]

cookie = '__cfduid=d2f1bba88c8850fd003677778101aa0511532013645; gxhk_columns=2; _ga=GA1.2.1448790967.1532013648; _gid=GA1.2.1604228491.1532013648; b3_lastvisit=1532013648; b3_lastactivity=0; em_cdn_uid=t%3D1532013658865%26u%3D5e97c2c2947c408695ff4ce7a2e276f6; __gads=ID=d62a2e62818e75cb:T=1532013690:S=ALNI_MZF63pbsOfPROR1P30GXJIZozxcNw; 9929ede844ba873398186deedd6c8d3a=e932a48375f1634f4f7a712cf834902e; __atuvc=12%7C29; em_p_uid=l:1532015855753|t:1532014310329|u:1b2ddfa4fbb44da2a00d62395fcaf836'

Topic_ID = 1


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xlsx', '_'+str(flag)+'.xls')
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


def request_sheet0():
    global Topic_ID
    for i in range(0, 10):
        url = 'https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=4aa0772189af4c17ea7ec181af2bca15&start=' + str(i*10) + '&cx=013423769980278394801:e8p-__zgdwq&q=insurance&cse_tok=AF14hliLiMOV86__BgjdOrqFCoUk-iT84Q:1532777357936&sort=&googlehost=www.google.com&callback=google.search.Search.apiary2382&nocache=1532777359013'
        html = get_request(url)
        reg = '"formattedUrl":"(.*?)"'
        lists = re.compile(reg).findall(html)
        for list in lists:
            if 'http' not in list:
                list = 'https://' + list
            if 'thread' not in list:
                continue
            if 'geoexpat' in list:
                scrape_gexexpat(list)
            elif 'geobaby' in list:
                scrape_gexbaby(list)
            Topic_ID += 1

    write_excel('data/2.xls', sheet0_data)


def scrape_gexexpat(main_url):
    data_of_url = []
    no_replies = 0
    html = get_request(main_url)
    page_no_reg = 'popupctrl">Page.*?of (.*?)<.*?vbseo-likes-count.*?/>(.*?)<.*?threadtitle">(.*?)<'
    main_data = re.compile(page_no_reg).findall(html)
    if not main_data:
        page_no_reg = 'vbseo-likes-count.*?/>(.*?)<.*?threadtitle">(.*?)<'
        main_data = re.compile(page_no_reg).findall(html)
        if main_data:
            page_no = 1
            like_no = main_data[0][0]
            title = main_data[0][1]
        else:
            page_no_reg = 'popupctrl">Page.*?of (.*?)<.*?threadtitle">(.*?)<'
            main_data = re.compile(page_no_reg).findall(html)
            if main_data:
                page_no = int(main_data[0][0])
                like_no = 0
                title = main_data[0][1]
            else:
                page_no_reg = 'threadtitle">(.*?)<'
                main_data = re.compile(page_no_reg).findall(html)
                page_no = 0
                like_no = 0
                title = main_data[0][0]
    else:
        page_no = int(main_data[0][0])
        like_no = main_data[0][1]
        title = main_data[0][2]

    for i in range(1, page_no + 1):
        url = main_url.split('-')[0]
        if 'html' not in url:
            url = url + '-' + str(i) + '.html'
        else:
            url = url.replace('.html', '-' + str(i) + '.html')
        html = get_request(url)
        reg = '"postbitlegacy postbitim postcontainer.*?posthead.*?date">(.*?),.*?postcounter">#(.*?)<.*?itemprop="name">(.*?)<.*?Join Date<.*?>.*?>(.*?)<.*?Posts.*?dd>(.*?)<.*?postcontent.*?>(.*?)</blockquote>'

        post_list = re.compile(reg).findall(html)
        for post in post_list:
            no_replies = post[1]
            one_row = ['GE_%d' % Topic_ID, title, main_url, remove_html_tag(post[2]), post[3].split(' ')[-1],
                       post[0].replace('-', '/'), like_no, post[1], post[4], get_pure_text(post[5])]
            print(one_row)
            data_of_url.append(one_row)
    for data in data_of_url:
        data[-3] = no_replies
        sheet0_data.append(data)


def scrape_gexbaby(main_url):
    posts_no = 0
    data_of_url = []
    reg = 'class="above_postlist"(.*?)class="pagetitle"(.*?)id="thread_controls"'
    html = get_request(main_url)
    reg_list = re.compile(reg).findall(html)[0]
    page_list = reg_list[0]
    title_list = reg_list[1]
    page_no = 1
    no_likes = 0

    if 'pagination_top hidden' not in page_list:
        page_no_reg = '"popupctrl">.*?of (.*?)<'
        page_posts_no = re.compile(page_no_reg).findall(page_list)[0]
        page_no = page_posts_no[0]

    if 'vbseo-likes' in title_list:
        title_reg = '"Like Tree".*?>(.*?)<em.*?<h1>(.*?)<'
        like_title = re.compile(title_reg).findall(title_list)[0]
        no_likes = like_title[0]
        title = like_title[1]
    else:
        title = re.compile('<h1>(.*?)<').findall(title_list)[0]

    for i in range(1, int(page_no) + 1):
        url = main_url.split('-')[0]
        if 'html' not in url:
            url = url + '-' + str(i) + '.html'
        else:
            url = url.replace('.html', '-' + str(i) + '.html')

        html = get_request(url)
        data_reg = 'class="postdate old".*?.*?date">(.*?),.*?class="username_container.*?href.*?>(.*?)<.*?class="userstats".*?<dd>(.*?)</.*?Posts.*?<dd>(.*?)<.*?<p>(.*?)</p'

        data_list = re.compile(data_reg).findall(html)

        for data in data_list:
            one_row = ['GE_%d' % Topic_ID, title, main_url, remove_html_tag(data[1]), data[2].split(' ')[-1],
                       data[0].replace('-', '/'), no_likes, posts_no, data[3], get_pure_text(data[4])]
            posts_no += 1
            print(one_row)
            data_of_url.append(one_row)

    for row in data_of_url:
        row[-3] = posts_no
        sheet0_data.append(row)


def get_pure_text(ori):
    soup = BeautifulSoup(ori)
    [div.extract() for div in soup.findAll('div')]
    return remove_html_tag(str(soup))


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_date(ori):
    d = datetime.strptime(ori, '%b %d, %Y')
    date = d.strftime('%d/%m/%Y')
    return date


def get_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'referer': 'https://geoexpat.com/forum/135/thread344040-3.html',
    }
    req = requests.get(get_url, headers=headers)
    res = req.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')
request_sheet0()