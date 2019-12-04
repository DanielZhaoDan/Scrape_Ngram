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
sleep_time = 1
failed_count = 0
stop = False
proxy = [
    '223.243.176.211:38132'
]

cookie = '.AspNetCore.Antiforgery.xd9Q-ZnrZJo=CfDJ8P7q8u2iyLhHnGjyS00LkJr5q591Sse1XyPmyHT0onWK_db8DNlfUp_MoUz8zEs67554Wgm6Ixj2AR5NTAMmqVLSu5JqDALXxfODYhL6XyBnpfXkTXZUGTmTUtHjlMEmcWqWDQkE10pOo9OEzhlEPe8; _ga=GA1.2.82153105.1564392021; _gid=GA1.2.1992988524.1564392021; _vwo_uuid_v2=D6B9795E33B8AA40D68297689793B48FB|c7ba77ab9f42b5f819863e5256ab080a; _gcl_au=1.1.565111866.1564392021; sgID=153cec4f-1ae3-9646-7262-fda58c4cd2c3; _pk_ref.1.fd33=%5B%22%22%2C%22%22%2C1564392023%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.1.fd33=*; D_SID=47.88.134.117:nXqYa2jyDRQwyHaXGHPg9Hl/XXjAW2gqpjtpzIujOOg; user_num=nowset; visitor_id597341=386271307; visitor_id597341-hash=ea3d8434d754ab57c5e5105a34a3a03df45242012532cf9eaf0c0a363d852da659704170953ae1c2dea14a7a706409ad0cd56679; sw-cookies-consent=1; _hjid=0705b538-047e-4e9c-986b-022aca8d465c; loyal-user={%22date%22:%222019-07-29T09:20:21.495Z%22%2C%22isLoyal%22:true}; _hjIncludedInSample=1; _pk_id.1.8c7a=7075a810d47f9b76.1564393865.1.1564393867.1564393865.; _pk_ses.1.8c7a=*; D_IID=879341C7-AE74-35ED-8CE9-85799A00DA32; D_UID=BAC651B9-BC73-3553-B21E-36DC22BF1FFD; D_ZID=80511FD1-0A52-3653-B35C-D9C61CC079CE; D_ZUID=7AAA8773-FFA9-340A-9722-6C79FE80B8E1; D_HID=7614D935-E5A4-3E31-8249-7CF1A2DF6ECF; sc_is_visitor_unique=rx8617147.1564394693.B62B459BF2164F658D7BDB3A6479240B.1.1.1.1.1.1.1.1.1; _gat=1; _gat_UA-42469261-1=1; _pk_id.1.fd33=e09aacad73ceab74.1564392023.1.1564394695.1564392023.; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=%7B%22distinct_id%22%3A%20%2216c3d07e1d1dad-01c619c63e5b18-37667c02-1fa400-16c3d07e1d2bb4%22%2C%22%24device_id%22%3A%20%2216c3d07e1d1dad-01c619c63e5b18-37667c02-1fa400-16c3d07e1d2bb4%22%2C%22sgId%22%3A%20%22153cec4f-1ae3-9646-7262-fda58c4cd2c3%22%2C%22site_type%22%3A%20%22Lite%22%2C%22session_id%22%3A%20%229b712a95-c0fe-4d2e-8954-d0c26eb1363d%22%2C%22session_first_event_time%22%3A%20%222019-07-29T09%3A20%3A22.489Z%22%2C%22url%22%3A%20%22https%3A%2F%2Fwww.similarweb.com%2Fwebsite%2Fmayfieldrecorder.com%22%2C%22is_sw_user%22%3A%20false%2C%22language%22%3A%20%22en%22%2C%22section%22%3A%20%22website%22%2C%22first_time_visitor%22%3A%20false%2C%22last_event_time%22%3A%201564394694845%2C%22%24search_engine%22%3A%20%22yahoo%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22page_number%22%3A%20%221%22%2C%22entity_name%22%3A%20%22mayfieldrecorder.com%22%2C%22entity_id%22%3A%20%22mayfieldrecorder.com%22%2C%22main_category%22%3A%20%22Unknown%22%2C%22sub_category%22%3A%20%22%22%7D'

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


def read_excel_filter_duplicated(filename, main_index, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            main_url = row[main_index].value
            if sheet_dict.get(main_url):
                continue
            one_row = [main_url]
            sheet2_data.append(one_row)
            sheet_dict[main_url] = True
        except Exception as e:
            print(i, e)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def request_category(base_url):
    global stop
    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[
        -1]
    html = get_request(url)
    if 'Unable To Identify Your Browser' in html or 'Pardon Our Interruption' in html:
        stop = True
    reg = 'js-categoryRank.*?websiteRanks-nameText.*?>(.*?)<.*?js-websiteRanksValue.*?>(.*?)</div'
    data = re.compile(reg).findall(html)

    if data:
        return [data[0][0], remove_html_tag(data[0][1])]
    return ['N/A', 'N/A']


def read_excel_get_data(filename, filename_prefix, type='', start=1, length=350):
    global sheet2_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in xrange(start, table.nrows):
        row = table.row(i)
        try:
            global_rank = row[2].value
            if global_rank == '' or global_rank == 0 or global_rank == 'N/A':
                main_url = row[0].value
                if 'category' == type:
                    details = request_category(main_url)
                else:
                    details = request_sheet2(main_url)
                one_row = [row[0].value] + details
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
# read_excel_filter_duplicated(filename, 8, start=1)
# write_excel('data/sheet2.xls', sheet2_data)
read_excel_get_data('data/%s.xls' % filename_prefix, filename_prefix, start=1, type='category')
write_excel('data/%s_end.xls' % filename_prefix, sheet2_data)