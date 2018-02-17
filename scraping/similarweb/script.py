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
    try:
        driver = webdriver.Chrome(executable_path=r'./chromedriver')  # Optional argument, if not specified will search path.
        driver.get(url)
        time.sleep(sleep_time)
        html_source = driver.page_source
        data = html_source.encode('utf-8').replace('\t', '').replace('\r', '').replace('\n', '')
    except Exception as e:
        raise e
    finally:
        driver.close()
    return data


def request_sheet2(base_url):
    global sheet_dict, sleep_time

    # rank_reg = 'rankingItem--global.*?rankingItem-value.*?>(.*?)<.*?rankingItem--country.*?rankingItem-value.*?>(.*?)<.*?rankingItem--category.*?rankingItem-value.*?>(.*?)<.*?Total Visits(.*?)Traffic Source'
    rank_reg = 'js-globalRank.*?js-websiteRanksValue.*?>(.*?)</div.*?js-countryRank.*?js-websiteRanksValue.*?>(.*?)</div.*?js-categoryRank.*?js-websiteRanksValue.*?>(.*?)</div.*?websitePage-engagementInfoContainer.*?>(.*?)Engagement body'
    country_tag = 'accordion-toggle.*?countValue">(.*?)<.*?country-name.*?>(.*?)<'

    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[-1]
    html = open_browser_scroll(url)
    global_ranks = re.compile(rank_reg).findall(html)
    if global_ranks:
        sleep_time = 1
        ret = [remove_html_tag(global_ranks[0][0]), remove_html_tag(global_ranks[0][1]), remove_html_tag(global_ranks[0][2])]
        if 'engagementInfo-valueNumber js-countValue' in global_ranks[0][3]:
            count_value_reg = 'engagementInfo-valueNumber js-countValue">(.*?)<'
            count_value = re.compile(count_value_reg).findall(global_ranks[0][3])[0]
            ret.append(count_value)
        else:
            ret.append(0)

    else:
        sleep_time = 30
        ret = [0, 0, 0, 0]

    country_ranks = re.compile(country_tag).findall(html)
    for country in country_ranks:
        ret.append(country[1])
        ret.append(country[0])
    if len(ret) == 4:
        ret += [0 for i in range(10)]
    return ret


def read_excel_filter_duplicated(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            main_url = row[8].value
            publisher = row[7].value
            article_url = row[5].value
            country = row[2].value
            if sheet_dict.get(main_url):
                continue
            one_row = [publisher, main_url, article_url, country] + []
            sheet2_data.append(one_row)
            sheet_dict[main_url] = True
        except Exception as e:
            print(i, e)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def read_excel_get_data(filename, filename_prefix, start=1, length=150):
    global sheet2_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in xrange(start, table.nrows):
        row = table.row(i)
        try:
            global_rank = row[4].value
            if global_rank == '' or global_rank == 0:
                main_url = row[1].value
                details = request_sheet2(main_url)
                one_row = [row[0].value, row[1].value, row[2].value, row[3].value] + details
                print i, one_row
                sheet2_data.append(one_row)
            else:
                one_row = []
                for j in xrange(table.ncols):
                    one_row.append(row[j].value)
                sheet2_data.append(one_row)
            if i % length == 0:
                write_excel('data/%s_%d.xls'%(filename_prefix, i), sheet2_data)
                del sheet2_data
                sheet2_data = [['Name of Publisher', 'Main url', 'Url of article', 'Country', 'Clobal Rank', 'Country Rank', 'Category Rank', 'Engagement', 'Top Country 1', 'Traffic 1', 'Top Country 2', 'Traffic 2', 'Top Country 3', 'Traffic 3', 'Top Country 4', 'Traffic 4', 'Top Country 5', 'Traffic 5']]
        except Exception as e:
            print i, e


filename_prefix = 'sheet2'
# filename = 'data/sheet1.xls'
# read_excel_filter_duplicated(filename, start=1)
# write_excel('data/sheet2.xls', sheet2_data)
read_excel_get_data('data/%s.xls' % filename_prefix, filename_prefix, start=1, length=150)
write_excel('data/%s_end.xls' % filename_prefix, sheet2_data)



