# -*- coding: utf-8 -*-
import re
import requests
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd
import gc
import sets

sheet1_data = [['URL Main', 'Page1 URL', 'Page Last URL', 'Title of Forum', 'Likes']]
sheet2_data = [['UID', 'URL Main', 'Thread URL', 'Comment text', 'Date']]

uid = 1

page1_url_set = set()

keywords = [
    'Citi MaxiGain', #

    # 'OCBC Monthly Savings',
    # 'CIMB StarSaver',
    # 'RHB Savings Account',
    # 'Citibank InterestPlus',
    # 'POSB Multiplier',
    # 'UOB One Account',
    # 'POSB eSavings',
    # 'Maybank Privilege Plus',
]
scraped = set()

cookie = '_ga=GA1.3.525834821.1549895617; _gid=GA1.3.1387476243.1549895617; __qca=P0-2060707478-1549895620383; bbvblastvisit=1549945889; bbvblastactivity=0; _gat=1; __atuvc=7%7C7; __atuvs=5c624c3a89f08d77006'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    filename = 'data/' + filename
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)

    i = 0
    while len(alldata) > 65500:
        _filename = filename.replace('.xls', '_%s.xls' % i)
        start_index = 0
        end_index = 65500
        data = alldata[start_index:end_index]
        alldata = alldata[end_index:]
        w = xlwt.Workbook(encoding='utf-8')
        ws = w.add_sheet('old', cell_overwrite_ok=True)
        for row in range(0, len(data)):
            one_row = data[row]
            for col in range(0, len(one_row)):
                try:
                    ws.write(row, col, one_row[col][:32766])
                except Exception as e1:
                    try:
                        ws.write(row, col, one_row[col])
                    except Exception as e:
                        pass
                        # print '===Write excel ERROR===', e1, e
        w.save(_filename)
        print("%s===========over============%d" % (_filename, len(data)))
        i += 1
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col][:32766])
            except Exception as e1:
                try:
                    ws.write(row, col, one_row[col])
                except Exception as e:
                    pass
                    # print '===Write excel ERROR===', one_row[col], e1, e
    w.save(filename)
    print("%s===========over============%d" % (filename, len(alldata)))


def request_sheet1(keyword, url):
    global sheet1_data
    # link, name, replies, views
    start_index = [0, 20, 40, 60, 80]
    reg_1 = 'title": "(.*?)".*?"url": "(.*?)"'

    url_main = 'https://www.hardwarezone.com.sg/search/forum/' + keyword.replace(' ', '+')

    for start in start_index:
        real_url = url
        print '---'+keyword+'--'+str(start)+'---'
        req_url = real_url.replace('#start#', str(start))
        try:

            html = get_request(req_url)
            title_url_list = re.compile(reg_1).findall(html)
            for title_url in title_url_list:
                sub_url = title_url[1]
                if '.html' not in sub_url:
                    continue
                page1_url, no_pages, title, likes = get_detail(sub_url)
                if not title:
                    continue
                pagelast_url = page1_url.replace('.html', '-' + str(no_pages) + '.html')
                one_row = [url_main, page1_url, pagelast_url, title, likes]
                # print one_row
                sheet1_data.append(one_row)
                request_sheet2(url_main, page1_url, no_pages)
                # break
        except Exception as e:
            print 'ERROR--sheet1---', req_url, e


def get_detail(url):
    html = get_request(url)
    has_like = False
    has_page = False
    reg = 'header-gray.*?>(.*?)<'
    if 'vbseo-likes-count-image' in html:
        reg += '.*?vbseo-likes-count-image.*?span>(.*?)<'
        has_like = True
    if 'class="pagination"' in html:
        reg += '.*?class="pagination"(.*?)</tbody'
        has_page = True

    data = re.compile(reg).findall(html)
    if data:
        if not has_like and not has_page:
            title = data[0]
        else:
            title = data[0][0]
            if has_like:
                likes = data[0][1]
            else:
                likes = 0
            if has_page:
                pagenation = data[0][-1]
                reg = 'Page.*?of (.*?)<.*?li.*?href="(.*?)"'
                urls = re.compile(reg).findall(pagenation)
                if urls:
                    page1_url = 'https://forums.hardwarezone.com.sg' + urls[0][1]
                    if re.search(r'-\d{1,3}\.html$', page1_url):
                        page1_url = '-'.join(page1_url.split('-')[:-1]) + '.html'
                    no_pages = urls[0][0]
                    return page1_url, int(no_pages), title, likes
            return url, 1, title, likes
        return url, 1, title, 0
    return url, 1, None, None


def get_special_event(url):
    html = get_request(url)
    ret = []
    reg = '<div><a href="(.*?)".*?<strong>(.*?)</strong>.*?smallfont.*?>(.*?)<.*?<strong>'
    temp_list = re.compile(reg).findall(html)
    for temp in temp_list:
        name = temp[1]
        link = temp[0]
        if 'http://forums.hardwarezone.com.sg' not in link:
            link = 'http://forums.hardwarezone.com.sg' + link
        text = temp[2]
        ret.append([name, link, text])
    return ret


def total_page(html):
    reg = 'pagination popupmenu nohovermenu.*?Page.*?of (.*?)<'
    temp = re.compile(reg).findall(html)
    if temp:
        return int(temp[0])
    return 1


def get_total_page(html):
    reg_number = 'pagination.*?of (.*?)<.'
    page_number = 0
    if 'pagination' in html:
        number_body = re.compile(reg_number).findall(html)
        if number_body:
            page_number = int(number_body[0])
    if page_number > 50:
        page_number = 50
    return page_number


def request_sheet2(url_main, page_url, page_number):
    global page1_url_set, uid, sheet2_data
    if page_url in page1_url_set:
        return
    if page_number > 100:
        page_number = 100

    reg = '<a name="post\d*?">.*?</a>(.*?)<.*?id="post_message_.*?>(.*?)<div class="vbseo_buttons"'

    for i in range(1, page_number+1):
        url = page_url.replace('.html', '-' + str(i) + '.html')
        try:
            html = get_request(url)

            text_list = re.compile(reg).findall(html)
            print 'sheet2--', url, page_number, len(text_list)
            for text in text_list:
                try:
                    date = get_date(text[0])
                    if 'class="quote"' in text[1]:
                        reg_quote = 'class="quote".*?</div>(.*?)</div'
                        text = remove_html_tag(re.compile(reg_quote).findall(text[1])[0])
                    else:
                        text = remove_html_tag(text[1]).split('<')[0]
                    one_row = [uid, url_main, url, text, date]
                    # print one_row
                    sheet2_data.append(one_row)
                except:
                    print 'sheet2_exception--', text
        except:
            print 'sheet2_exception--', url
    uid += 1

    page1_url_set.add(page_url)


def get_sheet2_body(payload, html):
    global sheet2_data
    reg = 'id="td_threadtitle_.*?href="(.*?)".*?id="thread_title_.*?>(.*?)</a.*?Replies: (.*?), Views: (.*?)"'
    thread_list = re.compile(reg).findall(html)
    for thread in thread_list:
        id = payload.get('id', '')
        google_headline = payload.get('google_headline', '')
        forum_url = payload.get('thread_url', '')
        sub_link = thread[0]
        if 'http://forums.hardwarezone.com.sg' not in sub_link:
            sub_link = 'http://forums.hardwarezone.com.sg' + sub_link
        t_name = remove_html_tag(thread[1].replace('**', ''))
        forum_thread = remove_html_tag(t_name)
        reply = thread[2].replace(',', '')
        view = thread[3].replace(',', '')
        one_row = [id, google_headline, forum_url, forum_thread, sub_link, reply, view]

        sheet2_data.append(one_row)
        payload['sub_thread'] = forum_thread
        request_sheet3(payload, sub_link)


def request_sheet3(payload, url):
    if 'record-breaking' in url:
        return
    m = re.search(r'-\d{1,2}\.html$', url)
    if m:
        url = url[:m.start()]+'.html'
    print payload.get('id', ''), 'sheet3--' + url
    try:
        html = get_request(url)
    except Exception as e:
        print 'ERROR---sheet3--'+url
        print e
        return
    get_sheet3_body(payload, html)
    page_number = get_total_page(html)
    for i in range(2, page_number+1):
        next_url = url.replace('.html', '-'+str(i)+'.html')
        try:
            html = get_request(next_url)
            get_sheet3_body(payload, html)
        except Exception as e:
            print 'ERROR--sheet3---'+next_url
            print e


def get_sheet3_body(payload, html):
    global sheet3_data
    reg = '<a name="post\d*?">.*?</a>(.*?)<.*?id="post_message_.*?>(.*?)<div class="vbseo_buttons"'
    text_list = re.compile(reg).findall(html)
    for text in text_list:
        id = payload.get('id', '')
        google_headline = payload.get('google_headline', '')
        sub_thread = payload.get('sub_thread', '')
        date = get_date(text[0])
        if 'class="quote"' in text[1]:
            reg_quote = 'class="quote".*?</div>(.*?)<'
            text = remove_html_tag(re.compile(reg_quote).findall(text[1])[0])
        else:
            text = remove_html_tag(text[1]).split('<')[0]
        one_row = [id, google_headline, sub_thread, text.replace('=', ''), date]
        sheet3_data.append(one_row)


def get_date(ori):
    try:
        d = datetime.strptime(ori, '%d-%m-%Y, %I:%M %p')
        date = d.strftime('%-d/%-m/%Y')
        return date
    except:
        return datetime.now().strftime('%-d/%-m/%Y')


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    try:
        return str(HTMLParser.HTMLParser().unescape(dd)).strip()
    except:
        return str(dd).strip()


def get_request(get_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'cookie': cookie,
    }
    req = requests.get(get_url, headers=headers, timeout=8)
    res = req.content
    res = str(res).replace('\t', '').replace('\r', '').replace('\n', '').replace('&amp;', '&').replace('\\t', '').replace('\\r', '').replace('\\n', '')
    return res


def read_excel(filename, start=1):
    global alldata, sheet2_data, sheet3_data
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        # if i < 44:
        #     continue
        try:
            url_main = table.row(i)[0].value.strip()
            page1_url = table.row(i)[1].value.strip()
            pagelast_url = table.row(i)[2].value.strip()
            page_no = int(pagelast_url.split('-')[-1].replace('.html', ''))
            request_sheet2(url_main, page1_url, page_no)
            # print url_main, page1_url, page_no
        except Exception as e:
            print 'ERROR--' + str(i)
            print(e)
            continue


reload(sys)
sys.setdefaultencoding('utf-8')

# i = 0
# for i in range(len(keywords)):
#     site = 'site%3Aforums.hardwarezone.com.sg%2F%20' + keywords[i].replace(' ', '%20')
#     url = 'https://cse.google.com/cse/element/v1?rsz=20&num=20&hl=en&source=gcsc&gss=.sg&start=#start#&cx=011134908705750190689:daz50x-t54k&safe=off&cse_tok=AKaTTZjRHf0Vp7IovsuUIT4FmfHG:1550037717901&sort=date&exp=csqr,4231019&callback=google.search.cse.api18880&q=#site#'.replace('#site#', site)
#     request_sheet1(keywords[i], url)
#     write_excel(keywords[i].replace(' ', '_')+'_1.xls', sheet1_data)
#     write_excel(keywords[i].replace(' ', '_')+'_2.xls', sheet2_data)
#     del sheet1_data
#     del sheet2_data
#     sheet1_data = [['URL Main', 'Page1 URL', 'Page Last URL', 'Title of Forum', 'Likes']]
#     sheet2_data = [['UID', 'URL Main', 'Thread URL', 'Comment text', 'Date']]

# print get_detail('https://forums.hardwarezone.com.sg/credit-cards-line-credit-facilities-243/youtrip-pay-overseas-no-fees-do-not-ask-post-referral-5885608-4.html')
# request_sheet2('', 'https://forums.hardwarezone.com.sg/money-mind-210/citibank-maxigain-savings-account-5311537.html', 3)
read_excel('data/sheet1.xls')
write_excel('sheet2.xls', sheet2_data)