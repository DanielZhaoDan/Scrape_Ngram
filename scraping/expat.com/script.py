import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
import json
from scraping.utils import post_request_json, get_request_html, write_html, write_excel, remove_html_tag

saved_hotel = set()
R_ID = 1
sheet1_data = [['Site', 'Topic', 'Title', 'thread url', 'Replies', 'Views', 'Username', 'Status', 'Date Posted', 'Content', 'No, of reactions']]

cookie = '__cfduid=dc03bb3be05404f78fff89ef8f3cdb0331606748339; optin_language=en; optin_status=tobe; optin_logged=no; optin_forum_posted=0; _ga=GA1.2.1143317018.1606748341; _gid=GA1.2.2100879828.1606748341; _omappvp=miuTxnh0qTOIcyWw5NYH3qq6X4BOUFHVzaoZYTOkON57E1cdHBSzmjc0FgiOgxOGohB6IuYhzfKhjxZhEQwSkzkHuCUU5MQY; CookiePolicy0618=-1; currentDestinationID=278; recentDestinationIds=a%3A3%3A%7Bi%3A0%3Bs%3A3%3A%22278%22%3Bi%3A1%3Bs%3A2%3A%2258%22%3Bi%3A2%3Bs%3A5%3A%2216656%22%3B%7D; _omappvs=1606749008502'

urls = [
    ('https://www.expat.com/forum/268-22-cost-of-living-in-england.html', 'Cost of living'),
    ('https://www.expat.com/forum/268-22-cost-of-living-in-england-p2.html', 'Cost of living'),
    ('https://www.expat.com/forum/268-20-children-in-england.html', 'Children'),
    ('https://www.expat.com/forum/268-10-health-care-in-england.html', 'Health System'),
    ('https://www.expat.com/forum/268-8-bank-england.html', 'Banks and Finance'),
]

uid_level_dict = {}


def request_sheet1(url, topic, site):
    global sheet1_data

    base_reg = 'post-title.*?href="(.*?)" title="(.*?)".*?col-md-3 col-xs-6 answers.*?"value".*?>(.*?)<.*?"value".*?>(.*?)<'
    comment_reg = 'id="p.*?class="row".*?user-title.*?span>(.*?)<.*?"name">.*?>(.*?)<.*?datetime="(.*?)".*?itemprop="articleBody">(.*?)</div>.*?likeHeart-container.*?</div(.*?)</div'

    html = get_request_html(url, cookie)
    # write_html(html, '0.html')
    threads = re.compile(base_reg).findall(html)

    for thread in threads:
        title = thread[1].replace('&amp;', '')
        thread_url = 'https://www.expat.com' + thread[0]
        # thread_url = 'https://www.expat.com/forum/viewtopic.php?id=631844'
        replies = int(thread[2].replace('k', '000'))
        views = thread[3].replace('k', '000')

        page_no = 1 if replies <= 40 else (replies / 40 + 1)
        i = 1
        print thread_url, len(threads), page_no
        while i <= page_no:
            page_url = thread_url + '&p=' + str(i)

            try:
                html = get_request_html(page_url, cookie)

                comments = re.compile(comment_reg).findall(html)

                one_row = None
                for comment in comments:
                    status = comment[0]
                    username = comment[1]
                    time = comment[2].split('T')[0]
                    content = remove_html_tag(comment[3].decode('cp1252')).strip()
                    no_reactions = 0 if 'recommend-count' not in comment[4] else get_reactions(comment[4])

                    one_row = [site, topic, title, thread_url, replies, views, username, status, time, content, no_reactions]

                    sheet1_data.append(one_row)
                print one_row
                i+=1
            except Exception as e:
                print 'ERR--', page_url, e


def get_reactions(ori):

    reg = 'class="recommend-count">(.*?)<'
    return re.compile(reg).findall(ori)[0]


def step_1():
    for item in urls:
        request_sheet1(item[0], item[1], 'expat.com')
    write_excel('expat.xls', sheet1_data, encoding='cp1252')


reload(sys)
sys.setdefaultencoding('utf-8')
step_1()