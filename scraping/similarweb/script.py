import time
from selenium import webdriver
import re
import string
import HTMLParser
import urllib2, urllib
import xlwt, xlrd
import sys
import os

sheet2_data = [['Name of Publisher', 'Main url', 'Url of article', 'Country', 'Clobal Rank', 'Country Rank', 'Category Rank', 'Engagement', 'Top Country 1', 'Traffic 1', 'Top Country 2', 'Traffic 2', 'Top Country 3', 'Traffic 3', 'Top Country 4', 'Traffic 4', 'Top Country 5', 'Traffic 5']]
sheet_dict = {}
sleep_time = 3

def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, data):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(data)):
        one_row = data[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)
    print filename + "===========over============"


def open_browser_scroll(url):
    global html_name
    driver = webdriver.Chrome(executable_path=r'./chromedriver')  # Optional argument, if not specified will search path.
    driver.get(url)
    time.sleep(sleep_time)
    html_source = driver.page_source
    data = html_source.encode('utf-8').replace('\t', '').replace('\r', '').replace('\n', '')
    driver.close()
    return data


def request_sheet2(base_url):
    global sheet_dict, sleep_time
    if sheet_dict.get(base_url):
        return None

    rank_reg = 'rankingItem--global.*?rankingItem-value.*?>(.*?)<.*?rankingItem--country.*?rankingItem-value.*?>(.*?)<.*?rankingItem--category.*?rankingItem-value.*?>(.*?)<.*?Total Visits(.*?)Traffic Source'
    country_tag = 'accordion-toggle.*?countValue">(.*?)<.*?country-name.*?>(.*?)<'

    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[-1]
    html = open_browser_scroll(url)
    global_ranks = re.compile(rank_reg).findall(html)
    if global_ranks:
        sleep_time = 3
        ret = [global_ranks[0][0].replace('[#,]', ''), global_ranks[0][1].replace('[#,]', ''), global_ranks[0][2].replace('[#,]', '')]
        if 'countValue">' in global_ranks[0][3]:
            count_value_reg = 'countValue">(.*?)<'
            count_value = re.compile(count_value_reg).findall(global_ranks[0][3])[0]
            ret.append(count_value)
        else:
            ret.append(0)
    else:
        sleep_time = 20
        ret = [0, 0, 0, 0]

    country_ranks = re.compile(country_tag).findall(html)
    for country in country_ranks:
        ret.append(country[1])
        ret.append(country[0])
    if len(ret) == 4:
        ret += [0 for i in range(10)]
    sheet_dict[base_url] = ret
    return ret


def redo_scrape():
    filename = 'data/sheet2.xls'
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    for i in range(1, table.nrows):
        row = table.row(i)
        try:
            main_url = row[1].value
            publisher = row[0].value
            article_url = row[2].value
            country = ''
            if row[4].value == '0' or row[4].value == 0:
                details = request_sheet2(main_url)
                if not details:
                    continue
                one_row = [publisher, main_url, article_url, country] + details
                print i, one_row
                sheet2_data.append(one_row)
            else:
                one_row = [row[i].value for i in range(18)]
                sheet2_data.append(one_row)
        except:
            print(i)
    write_excel('data/sheet2_2.xls', sheet2_data)


def mapping_local_file():
    filename = 'data/sheet2.xls'
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    url_details = {}
    for i in range(1, table.nrows):
        row = table.row(i)
        try:
            main_url = row[1].value
            if row[4].value != '0' and row[4].value != 0:
                if not url_details.get(main_url):
                    url_details[main_url] = [row[i].value for i in range(4, 18)]
        except:
            print(i)
    for i in range(1, table.nrows-1):
        row = table.row(i)
        try:
            main_url = row[1].value
            publisher = row[0].value
            article_url = row[2].value
            country = ''
            if row[4].value == '0' or row[4].value == 0:
                details = url_details.get(main_url)
                if not details:
                    continue
                one_row = [publisher, main_url, article_url, country] + details
                print i, one_row
                sheet2_data.append(one_row)
            else:
                one_row = [row[i].value for i in range(18)]
                sheet2_data.append(one_row)
        except:
            print(i)
    write_excel('data/sheet3.xls', sheet2_data)


def read_excel(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            main_url = row[8].value
            publisher = row[7].value
            article_url = row[5].value
            country = row[2].value
            details = request_sheet2(main_url)
            if not details:
                continue
            one_row = [publisher, main_url, article_url, country] + details
            print i, one_row
            sheet2_data.append(one_row)
        except Exception as e:
            print(i, e)

redo_scrape()
mapping_local_file()


filename = 'data/sheet1.xls'
# read_excel(filename, start=1,)
# write_excel('data/sheet2.xls', sheet2_data)

