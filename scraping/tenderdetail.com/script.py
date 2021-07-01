import re
import sys
from datetime import datetime
import HTMLParser
import xlrd, time
from selenium import webdriver
import json
from scraping.utils import post_request_json, get_request_html, write_html, write_excel, remove_html_tag, post_request_html

saved_hotel = set()
R_ID = 1
sheet1_data = [
    ['Site', 'Topic', 'Title', 'thread url', 'Replies', 'Views', 'Username', 'Status', 'Date Posted', 'Content',
     'No, of reactions']]

cookie = 'ASP.NET_SessionId=nknsjxggoni5nwdfh3ei5kfk; _ga=GA1.2.1869154036.1622216854; _gid=GA1.2.1317661398.1622216854; _gat_gtag_UA_33412460_1=1'

urls = [
    ('https://www.tenderdetail.com/Projects-News/hospital-in-india', 4),
]

uid_level_dict = {}


def open_browser_scroll(url, count):
    driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
    driver.get(url)

    for i in range(1, count+1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


    html_source = driver.page_source
    html = html_source.replace('\n', '').replace('\r', '')
    write_html(html, '1.html')
    reg = 'class="tender_row".*?num">(.*?)<.*?workDesc">.*?>(.*?)<.*?<p.*?>(.*?)</p.*?"state">(.*?)<.*?class="price".*?>(.*?)<.*?class="idno".*?>(.*?)<.*?class="viewnotice".*?"(.*?)"'
    data_list = re.compile(reg).findall(html)
    for data in data_list:
        r_id = data[0]
        name = remove_html_tag(data[1])
        desp = remove_html_tag(data[2])
        state = remove_html_tag(data[3])
        price = remove_html_tag(data[4])
        ID_num = remove_html_tag(data[5])
        detail_url = data[6]

        one_row = [r_id, name, desp, state, price, ID_num, detail_url] + request_detail(detail_url)
        print r_id
        sheet1_data.append(one_row)


def request_detail(url):
    html = get_request_html(url, cookie)
    reg = 'class="col-sm-9".*?>(.*?)<'
    data = re.compile(reg).findall(html)

    return [remove_html_tag(o) for o in data]


def step_1():
    for item in urls:
        open_browser_scroll(item[0], item[1])

    write_excel('data.xls', sheet1_data, encoding='utf-8')


reload(sys)
sys.setdefaultencoding('utf-8')
step_1()