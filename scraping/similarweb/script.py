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

cookie = 'sgID=e453ee44-a01a-4631-a91c-e7817ea66399; __RequestVerificationToken=FxIVqTliSrNiTjBK9hVuHA1yOG21RynBf-NHn4awqIhdIHM0N3mAhz_BQF-VievyjxDr4U6WSyylmC0qQ5QQeY0uOCtNJ2gzFbCbNGBbLhw1; _ga=GA1.2.290070144.1535452671; _vwo_uuid_v2=DA740CE19A9A4ADB3E2F4F69EF8A7A753|5f6c070d96007040dd3d8d1f50b726b8; D_IID=5123994B-BDD6-372B-BE74-3FC15B476AF6; D_UID=791D6C54-80C8-3575-9B8B-15B9348AABED; D_SID=140.205.147.44:2Cd46dEVoY5gM1R3TR44jo7zyuo1HGwe/REpOw3biFs; loyal-user=%7B%22date%22%3A%222018-08-28T10%3A37%3A51.668Z%22%2C%22isLoyal%22%3Atrue%7D; user_num=nowset; _mkto_trk=id:891-VEY-973&token:_mch-similarweb.com-1535472703150-77360; intercom-id-e74067abd037cecbecb0662854f02aee12139f95=ba8ba923-48bc-4ee1-9ffd-34ccf19d097e; _gid=GA1.2.1665423203.1536379870; D_ZID=8E9F23C0-B4D8-3D9B-9A9D-EBEC06FA4E4D; D_ZUID=7FB6661D-1FAA-3E73-8EB1-5E72119D5D98; D_HID=E12585B9-8D29-366C-91D0-3BC1A17EA576; _pk_ses.1.fd33=*; .SGTOKEN.SIMILARWEB.COM=u7oVmwV1BULizH5ifI1f6ayuSgFgJUj8JN7cXm8ZFJgAlJUNcxH9cJpW0OyKWOmdAzztjOUwjHSwyPDAeIThfUykvZpF_qwqi22B2AC2F_JC6Y9R2sSluXo4E2yF4LeLVg2cZZDCJdMiYEKQ4H1qlY-DnTTajJIlXytGHux9C5gjau9RL4MO8RR2czf_qhMmXbGomx01Q7Y6RPprbmKFd5SnSyhV7PZCkkxIby-A2CDnM0583mYgG4dgTB3x_bEDIu8z5TC9zZDa8p8_g0IDfK2GajRhSLaqU7VLdwn42FiNB0WqDA7p5Z82LaAo1MmhSnPaPly1ZJ68Seg5QD_nmwqifIg-6mW2SDxkekWWYvc; locale=zh-cn; sgID=78b44adf-2a9a-4586-8184-b29b8b82c14e; _vis_opt_s=1%7C; _vis_opt_test_cookie=1; jaco_uid=edabef00-5a4c-4501-8678-54aadf100912; jaco_provided_id_4316adc2-eb98-4130-828f-0352f2dac395=danielzhaochina%40gmail.com; _vwo_uuid=D0F5AD64E46A4CBB4F040975B1A399CB6; _vis_opt_exp_260_combi=2; intercom-session-e74067abd037cecbecb0662854f02aee12139f95=d2FJMTg3NWxtVW04eXdmMndJTkxRQUFVN0ErWmVzMnlVRUptcDIrRmhtc0pwWVVIWTFoYm1qTGl2U3RzZUFDVi0tQURsVm5UZmVPckJXalJvOW9JWVliZz09--03773056d529d2efcc24891cb14b36c5cdd4b1a0; intercom-lou-e74067abd037cecbecb0662854f02aee12139f95=1; _gat=1; sc_is_visitor_unique=rx8617147.1536425491.EFC14FD416734FF62B4A91344EF87B9A.6.5.5.5.4.3.3.2.2; _pk_id.1.fd33=4a1ceb3e328cae31.1535452673.6.1536425492.1536424139.'


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
    html = open_browser_scroll(url)
    # html = get_request(url)
    # if 'Unable To Identify Your Browser' in html or 'Pardon Our Interruption' in html:
    #     stop = True
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
                # if stop:
                #     break
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
filename = 'data/sheet1.xls'
# read_excel_filter_duplicated(filename, start=1)
# write_excel('data/sheet2.xls', sheet2_data)
read_excel_get_data('data/%s.xls' % filename_prefix, filename_prefix, start=1, length=50)
write_excel('data/%s_end.xls' % filename_prefix, sheet2_data)