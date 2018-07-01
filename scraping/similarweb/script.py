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

sheet2_data = [['Name of Publisher', 'Main url', 'Url of article', 'Country', 'Global Rank', 'Country Rank', 'Category Rank', 'Engagement', 'Top Country 1', 'Traffic 1', 'Top Country 2', 'Traffic 2', 'Top Country 3', 'Traffic 3', 'Top Country 4', 'Traffic 4', 'Top Country 5', 'Traffic 5']]
sheet_dict = {}
sleep_time = 3
stop = False
proxy = [
    '223.243.176.211:38132'
]

cookie = '_ga=GA1.2.444179720.1525487464; _gid=GA1.2.1525450094.1525487464; D_SID=121.7.108.6:P42PjWyIy3SxhSDU2eGb3EHxFkKmrzsTy9noOMcWycc; sgID=7ddad102-9ee6-4746-bf99-252f69a565d9; __RequestVerificationToken=wg-JpZGHeTpqJ5Z5Okdvmjnv06NFF6UtF-hd2j_HdDP9bs_3tw_8wEKgjzyyuPE8QlgiuzVlMVYFT6Ahglj2XfCOLk0r4mjnIE9kpXtvBvQ1; user_num=nowset; _vwo_uuid_v2=DCD22940F987909340CE970423DC808EE|389d706875fcb49d85866e2f34333d04; D_IID=A28664D6-FA00-3DCA-ABF0-7AD515A55D90; D_UID=7669E727-9381-3CE3-ABAB-E092B4F805FC; D_ZID=5FA79EBF-C004-3315-BAF2-F33B4D10D9C5; D_ZUID=D927FDA6-DC13-31C9-BE89-F09EF4699855; D_HID=91132E34-90B9-34E6-AB1A-391716BB2A99; sgID=ca850aff-8a2f-5294-a996-14e248556aa2; __utmc=107333120; _mkto_trk=id:891-VEY-973&token:_mch-similarweb.com-1525487573979-16916; intercom-id-e74067abd037cecbecb0662854f02aee12139f95=2710c585-6583-4c6d-bbf9-0a6dea2769b0; .SGTOKEN.SIMILARWEB.COM=u7oVmwV1BULizH5ifI1f6ayuSgFgJUj8JN7cXm8ZFJgAlJUNcxH9cJpW0OyKWOmdAzztjOUwjHSwyPDAeIThfcH77dU1qpGm7iyOiiBd4bNn9AZpVeFxOvp9GlIandjumvhxOprIpRPD-Y83PUqV8Zza0XGfTdwsBVKZnDD8oHOymxzgG3DejIVraMWkVh3Q_hsu7UbymxmSZgYi99ZodmlD66W2bjFgyxcZeSzQQ5szdgw8CvjqxoqQA9L6agG_N_K2ghUUw2FLCcAazxKA6jXl6pODJy8zq7y9L1khfDYSMHzjkZQAJF7W3YDv0w2fc65378rKD9Wpgq2KGzIgyI68-8gBSvhX9MbjI1zs1tM; _vis_opt_s=1%7C; _vis_opt_test_cookie=1; jaco_uid=5a3d3d41-2127-47ca-83b0-af82eb9e34c1; jaco_provided_id_4316adc2-eb98-4130-828f-0352f2dac395=danielzhaochina%40gmail.com; _vwo_uuid=D9DD13D2ADE32B01CB07B47552B83AF21; _vis_opt_exp_260_combi=2; intercom-lou-e74067abd037cecbecb0662854f02aee12139f95=1; PHPSESSID=04c9es4qspfggv6q444gchoqg2; _vis_opt_exp_255_combi=2; _vis_opt_exp_255_goal_4=1; _vis_opt_exp_255_goal_2=1; locale=zh-cn; _omappvp=1G9i9Do83q43sTran3awdhtcmPZp67mr9zN3tnxdYvHKGtnGgVwDLA63A75ZWfYSIIJAtVk316fTNDaW5G2ZdAxSSQxXzm3S; _omappvs=true; loyal-user=%7B%22date%22%3A%222018-05-05T02%3A32%3A26.802Z%22%2C%22isLoyal%22%3Atrue%7D; __utma=107333120.444179720.1525487464.1525531906.1525535984.4; __utmz=107333120.1525535984.4.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmb=107333120.2.10.1525535984; _pk_ses.1.fd33=*; intercom-session-e74067abd037cecbecb0662854f02aee12139f95=MGVTZ3ZMVk5HTnk3bmwxS2lyVHVoUkUrYWwxaHpMWGxsREtJVmtiM3Y3ZTNWYTRqWlV5RDMxTmpSYk9qZ3dJZy0tdTJZVDBMK3pUMkRnR2d3T2tGa1B3Zz09--c13e9224f669e588bb0d06a1cf92093891a2e384; _gat=1; _uetsid=_ueta4abfeb7; _pk_id.1.fd33=4a1ceb3e328cae31.1525487548.3.1525536954.1525534253.; _gat_UA-42469261-1=1; sc_is_visitor_unique=rx8617147.1525536954.E9AD1064AF654F74A6B8FD70E8B91469.4.3.3.3.3.3.2.2.2'


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
        # options = Options()
        # options.add_argument('--proxy-server=%s', random.choice(proxy))
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
    global sheet_dict, sleep_time, stop

    # rank_reg = 'rankingItem--global.*?rankingItem-value.*?>(.*?)<.*?rankingItem--country.*?rankingItem-value.*?>(.*?)<.*?rankingItem--category.*?rankingItem-value.*?>(.*?)<.*?Total Visits(.*?)Traffic Source'
    rank_reg = 'js-globalRank.*?js-websiteRanksValue.*?>(.*?)</div.*?js-countryRank.*?js-websiteRanksValue.*?>(.*?)</div.*?js-categoryRank.*?js-websiteRanksValue.*?>(.*?)</div.*?websitePage-engagementInfoContainer.*?>(.*?)Engagement body'
    country_tag = 'accordion-toggle.*?countValue">(.*?)<.*?country-name.*?>(.*?)<'

    url = 'https://www.similarweb.com/website/' + base_url.replace('http://', '').replace('https://', '').split('www.')[-1]
    # html = open_browser_scroll(url)
    html = get_request(url)
    if 'Unable To Identify Your Browser' in html or 'Pardon Our Interruption' in html:
        stop = True
        return [0, 0, 0, 0]
    global_ranks = re.compile(rank_reg).findall(html)
    if global_ranks:
        ret = [remove_html_tag(global_ranks[0][0]), remove_html_tag(global_ranks[0][1]), remove_html_tag(global_ranks[0][2])]
        if 'engagementInfo-valueNumber js-countValue' in global_ranks[0][3]:
            count_value_reg = 'engagementInfo-valueNumber js-countValue">(.*?)<'
            count_value = re.compile(count_value_reg).findall(global_ranks[0][3])[0]
            ret.append(count_value)
        else:
            ret.append(0)
        sleep_time = 5

    else:
        sleep_time = 25
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


filename_prefix = 'sheet2'
# filename = 'data/sheet1.xls'
# read_excel_filter_duplicated(filename, start=1)
# write_excel('data/sheet2.xls', sheet2_data)
read_excel_get_data('data/%s.xls' % filename_prefix, filename_prefix, start=1, length=2000)
write_excel('data/%s_end.xls' % filename_prefix, sheet2_data)



