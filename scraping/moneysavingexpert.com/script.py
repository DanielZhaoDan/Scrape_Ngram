import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
import json
from scraping.utils import post_request_json, get_request_html, write_html, write_excel, remove_html_tag

saved_hotel = set()
R_ID = 1
sheet1_data = [
    ['Site', 'Topic', 'Title', 'thread url', 'Replies', 'Views', 'Username', 'Status', 'Date Posted', 'Content',
     'No, of reactions']]

cookie = '__cfduid=dc03bb3be05404f78fff89ef8f3cdb0331606748339; optin_language=en; optin_status=tobe; optin_logged=no; optin_forum_posted=0; _ga=GA1.2.1143317018.1606748341; _gid=GA1.2.2100879828.1606748341; _omappvp=miuTxnh0qTOIcyWw5NYH3qq6X4BOUFHVzaoZYTOkON57E1cdHBSzmjc0FgiOgxOGohB6IuYhzfKhjxZhEQwSkzkHuCUU5MQY; CookiePolicy0618=-1; currentDestinationID=278; recentDestinationIds=a%3A3%3A%7Bi%3A0%3Bs%3A3%3A%22278%22%3Bi%3A1%3Bs%3A2%3A%2258%22%3Bi%3A2%3Bs%3A5%3A%2216656%22%3B%7D; _omappvs=1606749008502'

urls = [
    ('https://forums.moneysavingexpert.com/discussion/6127314/green-ethical-investment-news-and-suggestions', 14),
    ('https://forums.moneysavingexpert.com/discussion/6071905/the-alternative-green-energy-thread', 39),
    ('https://forums.moneysavingexpert.com/discussion/6189544/current-agile-prices', 5),
    ('https://forums.moneysavingexpert.com/discussion/6202200/green-and-ethical-food', 5),
]

uid_level_dict = {}


def request_sheet1(base_url, count):
    global sheet1_data

    base_reg = 'class="PageTitle".*?<h1>(.*?)<.*?datetime="(.*?)T.*?CountComments.*?title="(.*?) .*?title="(.*?) .*?userContent">(.*?)</div'
    comment_reg = 'class="Comment".*?datetime="(.*?)T.*?userContent">(.*?)<div class="Signature'
    replies = 'N/A'
    views = 'N/A'
    title = 'N/A'
    for i in range(1, count+1):
        url = base_url + '/p' + str(i)
        print url
        html = get_request_html(url, cookie)
        if i == 1:
            threads = re.compile(base_reg).findall(html)
            title = threads[0][0].replace('&amp;', '&')
            date = threads[0][1].replace('-','/')
            replies = threads[0][2]
            views = threads[0][3]
            content = remove_html_tag(threads[0][4])
            one_row = [base_url, title, replies, views, content, 'MAIN', date]
            sheet1_data.append(one_row)

        comments = re.compile(comment_reg).findall(html)
        for comment in comments:
            date = comment[0].replace('-', '/')
            content = remove_html_tag(comment[1])
            one_row = [base_url, title, replies, views, content, 'REPLY', date]
            sheet1_data.append(one_row)


def step_1():
    for item in urls:
        request_sheet1(item[0], item[1])

    write_excel('data.xls', sheet1_data, encoding='utf-8')


reload(sys)
sys.setdefaultencoding('utf-8')
step_1()
