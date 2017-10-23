# -*- coding: utf-8 -*-
import xlsxwriter
import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd
import gc
import sets

sheet1_data = [['Keyword', 'Forum topic', 'Forum link', 'Sub-forum topic', 'Sub-forum link', 'Text']]
sheet2_data = [['ID', 'Google Headline', 'Forum Thread URL', 'Sub-Forum Thread', 'Sub-Forum URL', 'Replies', 'Views']]
sheet3_data = [['ID', 'Google Headline', 'Forum Thread', 'Comment text', 'Date']]

keywords = ['Singtel', 'PC show']
scraped = set()

cookie = '__qca=P0-982849710-1481340442304; __qca=P0-1694046292-1481340463367; bbvbsessionhash=cfaae69fcb9401422608134678dd2cbd; bbvbthread_lastview=96ba3d0002c1d60c689240492816c86986db7a42a-12-%7Bi-5627992_i-1496244450_i-5538296_i-1483437174_i-5575396_i-1488265200_i-5575360_i-1488262429_i-5624354_i-1495771260_i-5650762_i-1499326771_i-5119483_i-1490343436_i-5519417_i-1495178966_i-5640802_i-1497900350_i-3251747_i-1500511528_i-5329393_i-1488414916_i-5517298_i-1482593166_%7D; bbvblastvisit=1481340439; bbvblastactivity=0; NSC_JO3kmqhuelqozbsbirjghwbnv43b3cq=ffffffff09a3640b45525d5f4f58455e445a4a423660; _ga=GA1.3.1033476444.1481340442; _gid=GA1.3.1741745025.1500741768; hwzbt_7b450bc2082de9d1650c211e1641a19e=e5a0b504df9481281b3533e2d1f36079; _gat=1; _gali=thread_title_5657474'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlsxwriter.Workbook(filename)
    ws = w.add_worksheet()
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write_string(row, col, (one_row[col]))
            except:
                ws.write(row, col, (one_row[col]))
    w.close()
    print filename+"===========over============"


def request_sheet1(keyword, url):
    global sheet1_data
    # link, name, replies, views
    start_index = [0, 20, 40, 60, 80]
    reg_1 = 'GsearchResultClass.*?"title":"(.*?)".*?"url":"(.*?)"'

    for start in start_index:
        real_url = url
        print '---'+keyword+'--'+str(start)+'---'
        req_url = real_url.replace('#start#', str(start))
        try:
            html = get_request(req_url)
            title_url_list = re.compile(reg_1).findall(html)
            for title_url in title_url_list:
                one_row = [keyword, remove_html_tag(title_url[0]), title_url[1]]
                if 'special-events' in title_url[1]:
                    sub_forum = get_special_event(title_url[1])
                    for item in sub_forum:
                        sheet1_data.append(one_row + item)
                        if item[1].endswith('.html'):
                            m = re.search(r'index\d{1,2}\.html$', url)
                            if m:
                                request_sheet2(item[0], item[1])
                            elif item[1].endswith('index.html'):
                                request_sheet2(item[0], item[1])
                            else:
                                request_sheet3(item[0], item[1])
                            request_sheet3(item[0], item[1])
                        else:
                            request_sheet2(item[0], item[1])
                else:
                    sheet1_data.append(one_row + ['N/A', 'N/A', 'N/A'])
                    if title_url[1].endswith('.html'):
                        request_sheet3(title_url[0], title_url[1])
                    else:
                        request_sheet2(title_url[0], title_url[1])
        except:
            print 'ERROR--sheet1---'+url


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


def request_sheet2(url, payload):
    m = re.search(r'index\d{1,2}\.html$', url)
    if m:
        url = url[:m.start()]+'.html'
    try:
        html = get_request(url)
    except Exception as e:
        print 'ERROR---sheet2--'+url
        print e
        return
    page_number = get_total_page(html)
    if page_number > 100:
        page_number = 100
    print payload.get('id', ''), ' -> sheet2--' + url + '  ' + page_number
    get_sheet2_body(payload, html)
    for i in range(2, page_number+1):
        next_url = url+'/index'+str(i)+'.html'
        try:
            html = get_request(next_url)
            get_sheet2_body(payload, html)
        except Exception as e:
            print e
            print 'ERROR--sheet2---'+next_url


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
    ori = unicode(ori, 'unicode-escape')
    s = ori.encode('utf-8')
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', s)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", get_url)
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


def read_excel(filename, start):
    global alldata, sheet2_data, sheet3_data
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        if i < 44:
            continue
        try:
            google_headline = table.row(i)[0].value.strip()
            google_url = table.row(i)[1].value.strip()
            url_list = google_url.split('/')
            if len(url_list) == 5:
                topic_url = '/'.join(url_list[:-1])
                if topic_url in scraped:
                    continue
                scraped.add(topic_url)
                request_sheet2(topic_url, payload={'google_headline': google_headline, 'id': i+1, 'thread_url': topic_url})
                write_excel('data/sheet_%d_2.xls' % i, sheet2_data)
                write_excel('data/sheet_%d_3.xls' % i, sheet3_data)
                del sheet2_data
                del sheet3_data
                sheet2_data = [['ID', 'Google Headline', 'Forum Thread URL', 'Sub-Forum Thread', 'Sub-Forum URL', 'Replies', 'Views']]
                sheet3_data = [['ID', 'Google Headline', 'Forum Thread', 'Comment text', 'Date']]
        except Exception as e:
            print 'ERROR--' + str(i)
            print(e)
            continue


reload(sys)
sys.setdefaultencoding('utf-8')

# i = 0
# for i in range(len(keywords)):
#     site = 'site%3Aforums.hardwarezone.com.sg%2F%20' + keywords[i].replace(' ', '%20')
#     url = 'https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=en&prettyPrint=false&source=gcsc&gss=.sg&sig=0c3990ce7a056ed50667fe0c3873c9b6&start=#start#&cx=011134908705750190689:daz50x-t54k&q=#site#&googlehost=www.google.com&callback=google.search.Search.apiary19428&nocache=1481290177512'.replace('#site#', site)
#     request_sheet1(keywords[i], url)
#     write_excel(keywords[i].replace(' ', '_')+'_1.xls', sheet1_data)
#     write_excel(keywords[i].replace(' ', '_')+'_2.xls', sheet2_data)
#     write_excel(keywords[i].replace(' ', '_')+'_3.xls', sheet3_data)
#     del sheet1_data
#     sheet1_data = [['Keyword', 'Forum topic', 'Forum link', 'Sub-forum topic', 'Sub-forum link', 'Text']]
#     del sheet2_data
#     sheet2_data = [['Thread in forum', 'Thread', 'Url of Thread', 'Replies', 'Views']]
#     del sheet3_data
#     sheet3_data = [['Thread title', 'Date', 'Comment text']]
#     gc.collect()
read_excel('data/input.xlsx', 0)
