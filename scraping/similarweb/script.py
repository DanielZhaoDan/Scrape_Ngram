import time
from selenium import webdriver
import re
import string
import HTMLParser
import urllib2, urllib
import xlwt, xlrd
import sys
import os
import random
import requests
from datetime import datetime

sheet2_data = [['Name of Publisher', 'Main url', 'Url of article', 'Country', 'Global Rank', 'Country Rank', 'Category Rank', 'Engagement', 'Top Country 1', 'Traffic 1', 'Top Country 2', 'Traffic 2', 'Top Country 3', 'Traffic 3', 'Top Country 4', 'Traffic 4', 'Top Country 5', 'Traffic 5']]
sheet_dict = {}
sleep_time = 3
failed_count = 0
stop = False
proxy = [
    '223.243.176.211:38132'
]

cookie = 'D_SID=118.200.75.55:yC35iQB81X4INdYU2WIUVIgYEQfxWYtgEHeddbZV7So; sgID=849c32e2-f2d7-4169-ae2b-91ff29399725; .AspNetCore.Antiforgery.xd9Q-ZnrZJo=CfDJ8O3KJbQZozVFjBEXXPUInFJUiGhwucnScBNYWs4pSGX2VhjA1VIMQs0heJ-bFbSrPraOFLwkKKd3e6IV8ihC1j6qeg6LxfqU0IH5YxI3G1_udTELenisyI__GU4OXtSJhhSOWwQwXRAlCn1FZp60_iE; _vwo_uuid_v2=DABB1CC285DA0944113E6EC22332167B5|8e96436c3dc2c7689e562339097e1012; _ga=GA1.2.1227054292.1555214227; _gcl_au=1.1.1942965607.1555214228; user_num=nowset; sw-cookies-consent=1; intercom-id-e74067abd037cecbecb0662854f02aee12139f95=3690d29b-4599-4463-9283-a01d6e549dfe; visitor_id597341=343626332; visitor_id597341-hash=e023cb87892efb4f136145abed745df6ce87f29db5824d3b1a0f96a981d094f43f48dfa1e171664c4de463f495f527d770f476b0; loyal-user={%22date%22:%222019-04-14T03:57:06.612Z%22%2C%22isLoyal%22:true}; _pk_id.1.8c7a=16ce8bbd14c0f626.1555217293.1.1555217295.1555217294.; _gid=GA1.2.300442759.1556272553; _pk_ses.1.fd33=*; D_IID=CA001F9C-C2E4-3745-8D4F-B3850C6AF218; D_UID=799F360E-BA7F-308B-AE9E-60B48F32E221; D_ZID=AD829BB5-0AA9-3B59-9DE9-89C0D1B27EE9; D_ZUID=2D5114AF-226C-3BE7-800A-028203D9CD8F; D_HID=65AB865E-6C03-345C-AF6B-749FE3B06E28; _pk_id.1.fd33=9c7298165d514a12.1555214228.2.1556272597.1556272554.; sc_is_visitor_unique=rx8617147.1556272597.34CF0B6D91F14F6AD13B197373803E03.2.2.2.2.2.2.2.2.2; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=%7B%22distinct_id%22%3A%20%2216a19fdd67c368-0f7d6d35a7e4ee-366d7e04-13c680-16a19fdd67d5de%22%2C%22%24device_id%22%3A%20%2216a19fdd67c368-0f7d6d35a7e4ee-366d7e04-13c680-16a19fdd67d5de%22%2C%22sgId%22%3A%20%22849c32e2-f2d7-4169-ae2b-91ff29399725%22%2C%22Site%20Type%22%3A%20%22Lite%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.similarweb.com%2Fwebsite%2Ftechwireasia.com%22%2C%22%24initial_referring_domain%22%3A%20%22www.similarweb.com%22%2C%22session%20ID%22%3A%20%220c0948ff-46f2-4568-a951-8050d4676843%22%2C%22section%22%3A%20%22website%22%2C%22last%20event%20time%22%3A%201556272597454%7D'

# driver = webdriver.Chrome(executable_path=r'./chromedriver')  # Optional argument, if not specified will search path.


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
    global html_name, driver
    try:
        # options = Options()
        # options.add_argument('--proxy-server=%s', random.choice(proxy))
        driver.get(url)
        time.sleep(sleep_time)
        html_source = driver.page_source
        data = html_source.encode('utf-8').replace('\t', '').replace('\r', '').replace('\n', '')
    except Exception as e:
        raise e
    return data


def request_sheet2(base_url):
    global sheet_dict, sleep_time, stop

    # rank_reg = 'rankingItem--global.*?rankingItem-value.*?>(.*?)<.*?rankingItem--country.*?rankingItem-value.*?>(.*?)<.*?rankingItem--category.*?rankingItem-value.*?>(.*?)<.*?Total Visits(.*?)Traffic Source'
    rank_reg = 'js-globalRank.*?js-websiteRanksValue.*?>(.*?)</div.*?js-countryRank.*?js-websiteRanksValue.*?>(.*?)</div.*?js-categoryRank.*?js-websiteRanksValue.*?>(.*?)</div.*?websitePage-engagementInfoContainer.*?>(.*?)Engagement body'
    country_tag = 'accordion-toggle.*?countValue">(.*?)<.*?country-name.*?>(.*?)<'

    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[-1]
    # html = open_browser_scroll(url)
    html = get_request(url)
    if 'Unable To Identify Your Browser' in html or 'Pardon Our Interruption' in html:
        stop = True
    #     return [0, 0, 0, 0]
    global_ranks = re.compile(rank_reg).findall(html)
    if global_ranks:
        ret = [remove_html_tag(global_ranks[0][0]), remove_html_tag(global_ranks[0][1]), remove_html_tag(global_ranks[0][2])]
        if 'engagementInfo-valueNumber js-countValue' in global_ranks[0][3]:
            count_value_reg = 'engagementInfo-valueNumber js-countValue">(.*?)<'
            count_value = re.compile(count_value_reg).findall(global_ranks[0][3])[0]
            ret.append(count_value)
        else:
            ret.append(0)
        sleep_time = 1
    else:
        sleep_time = 10
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

    for i in range(start, table.nrows):
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
                time.sleep(sleep_time)
                if stop:
                    break
                one_row = [row[0].value, row[1].value, row[2].value, row[3].value] + details
                print i, one_row
                sheet2_data.append(one_row)
            else:
                one_row = []
                for j in xrange(table.ncols):
                    one_row.append(row[j].value)
                sheet2_data.append(one_row)
            if i % length == 0:
                write_excel('data/%s_%d.xls' % (filename_prefix, i), sheet2_data)
                del sheet2_data
                sheet2_data = [['Name of Publisher', 'Main url', 'Url of article', 'Country', 'Clobal Rank', 'Country Rank', 'Category Rank', 'Engagement', 'Top Country 1', 'Traffic 1', 'Top Country 2', 'Traffic 2', 'Top Country 3', 'Traffic 3', 'Top Country 4', 'Traffic 4', 'Top Country 5', 'Traffic 5']]
        except Exception as e:
            print i, e


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res

def get_date(ori):
    ori = ori.replace('Mei', 'May')
    if 'hour' in ori:
        return datetime.now().strftime('%d/%m/%Y')
    try:
        date = datetime.strptime(ori, '%b %d, %Y')
        return date.strftime('%d/%m/%Y')
    except:
        raise
        return ori


filename_prefix = 'sheet2'
# filename = 'data/sheet1.xls'
# read_excel_filter_duplicated(filename, start=1)
# write_excel('data/sheet2.xls', sheet2_data)
read_excel_get_data('data/%s.xls' % filename_prefix, filename_prefix, start=1, length=50)
write_excel('data/%s_end.xls' % filename_prefix, sheet2_data)