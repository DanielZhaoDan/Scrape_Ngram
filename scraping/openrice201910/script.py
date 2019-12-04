# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import HTMLParser
import os
import time

sheet1_data = [['ID', 'Name', 'No. reviews', 'Address', 'Price', 'Cuisine', 'Positives', 'Negatives', 'Bookmarked', 'link']]
sheet2_data = [['ID', 'link', 'No. OK', 'Avg rating', 'Taste', 'Decor', 'Service', 'Hygiene', 'value', 'photo']]
sheet3_data = [['ID', 'link', 'Name', 'No. reviews', 'Address', 'Price', 'Cuisine', 'Positives', 'No. OK', 'Negatives', 'Bookmarked', 'photo', 'restaurant url']]

url_bases = 'https://www.openrice.com/en/hongkong/restaurants?chainId=10000525&page=%d'

cookie = 'DefaultRegionIds=%7B%22hk%22%3A0%7D; RegionId=0; webhash=8d767541-3033-4a12-9e9f-f3191e0c738a; isguest=1; autha=h5dzKU_A32HhpxEzpWClv0FLd--n1W_UgIZz_zyRdB82Tza1tEu2Smg8f72cQo-Z1mwuCMBvKEqvWapMIyAGdWu0GU51_LkyersDL5DtZiFE2YKam9w-Rf1BVs928TfsLh5EGjbp78f_OpeJqQW-sK2DXOkQNtu304UyqN_p7pYwuhQthbUraQGKDZXIJhvwrbIOOac0wGwuf3X02R5JaIgqIrP30dc3FLtCyyqoFN6_eO7vElsacv0iZ3P_C9Otqv-97-ytBLAvenMzjJD9IVikqJhirFAQ4LKFkAq-v6JlEfV2_rIdy4XHR_NDg1-pynAP-UpT9UtPUpyaccQ0uTbt7MeMgqliOnpgCWlRWj0qqgyAWNnsSyckB-2cOf6vWKvPLtFHKC3BtJ6OwLKGLPzTfBU85MIToRSs9Ih8vd_5n15AWeC4NYwGZB43WVpv0aDbew; authr=eajgETXx7kREVybDU8KFe0okrkNAUk6r8dFkBB8FMZ43WVdJk7ugiJcANOczDPkMAR72KLDEJo6udWrlTCCuym0xtYcZ_JFI_VQGj7GjtJ5EHZ--o5jN1y2P47I2ddwsw8yPN2Gl-5hoMu7HWKBV31ZB6l9hW7qS1MXBjtomcT9pB7Y5oQNmB9XJsMHfQlAjGPGh711SvrirxAZFSreS9c2HDtu02oSefyKT2aLluTbFKneIqe75BhtE_hGzSk1dADxcqeNwf3w7uYPHVDyWsF0wLPtdr5iAhI5mHAc3ZRocV1SSRIk3OR2DIz05ERsZc9EUmldrWpMpkDYH5l7C-pz3qHOZjo6f-zJJhoxD9BfRADn9ThwJqcUTdPWdzKM6_1HNDwKsc4_jxQu7IEEXzWfjqV25GT8bMuBvVsty4w1Ug7drRe-ASyfoNuxIUT0-HIdI8EogByUtERu9NfjqiznIAC8; authe=Lk9p6UY15uR3cICBJ2T2uY90sEu7U+mVYV5zTNMr3CoQTyFUIUUykwW4999RLQ8zyt2Fr24WP8CwYVoEWjahgPHfHmopYYlVBWzZxth9bVQ=; _ga=GA1.2.862235096.1572261236; _gid=GA1.2.737304214.1572261236; __utma=183676536.862235096.1572261236.1572261236.1572261236.1; __utmc=183676536; __utmz=183676536.1572261236.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_UA-652541-1=1; __utmb=183676536.10.10.1572261236'

G_ID = 1

sheet2_cache = {}


def request_sheet2(url, g_id):
    global sheet2_data, sheet3_data

    if url not in sheet2_cache:
        html = get_request(url)
        sheet2_cache[url] = html
    html = sheet2_cache.get(url)
    reg = 'class="name">(.*?)<.*?header-score-show-more(.*?)header-popular-info-divider.*?js-header-bookmark-count.*?data-count="(.*?)".*?priceRange.*?href.*?>(.*?)<.*?header-poi-categories(.*?)</div.*?header-smile-section(.*?)promotion-section.*?Photo \((.*?)\)'

    try:
        data = re.compile(reg).findall(html)[0]
        name = data[0]
        avg_rating, no_Review, Taste, Decor, Service, Hygiene, Value = get_rating(data[1])
        benchmark = data[2]
        price = data[3]
        pos, ok, neg = get_pos_ok_neg(data[5])
        photo = data[6]

        one_row = [g_id, url, ok, avg_rating, Taste, Decor, Service, Hygiene, Value, photo]
        sheet2_data.append(one_row)
        print one_row
    except Exception as e:
        print 'sheet2---exception---', g_id, url, e
        one_row = [g_id, url, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
        sheet2_data.append(one_row)
    res_reg = 'li class="item".*?href="(.*?)"'
    res_link = re.compile(res_reg).findall(html)
    for res in res_link:
        if 'offer' not in res:
            request_sheet3('https://www.openrice.com' + res, g_id, url)


def request_sheet3(url, g_id, link):
    global sheet2_data, sheet3_data

    if url not in sheet2_cache:
        html = get_request(url)
        sheet2_cache[url] = html
    html = sheet2_cache.get(url)
    reg = 'class="name">(.*?)<.*?header-score-show-more(.*?)header-popular-info-divider.*?js-header-bookmark-count.*?data-count="(.*?)".*?priceRange.*?href.*?>(.*?)<.*?header-poi-categories(.*?)</div.*?header-smile-section(.*?)promotion-section.*?Photo \((.*?)\)'

    try:
        data = re.compile(reg).findall(html)[0]
        name = data[0]
        avg_rating, no_Review, Taste, Decor, Service, Hygiene, Value = get_rating(data[1])
        benchmark = data[2]
        price = data[3]
        cuisine = get_cuisine(data[4])
        pos, ok, neg = get_pos_ok_neg(data[5])
        photo = data[6]

        addr_reg = 'address-info-section.*?content">(.*?)</div'
        addr = re.compile(addr_reg).findall(html)
        one_row = [g_id, link, name, no_Review, remove_html_tag(addr[0]).strip(), price, cuisine, pos, ok, neg, benchmark, photo, url]
        print one_row
        sheet3_data.append(one_row)
    except Exception as e:
        print 'sheet3---exception---', g_id, url, e
        one_row = [g_id, link, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
        sheet3_data.append(one_row)


def get_pos_ok_neg(ori):
    return re.compile(r'class="score-div">(.*?)<').findall(ori)


def get_cuisine(ori):
    reg = 'href=".*?>(.*?)<'
    return '/'.join(re.compile(reg).findall(ori))


def get_rating(ori):
    if 'reviewCount' not in ori:
        return 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
    reg = 'header-score">(.*?)<.*?reviewCount">(.*?)<.*?header-score-details-right(.*?)$'
    data = re.compile(reg).findall(ori)[0]
    return [data[0], data[1]] + get_details_rating(data[2])


def get_details_rating(ori):
    reg = 'common_rating(.*?)_'
    data = re.compile(reg).findall(ori)

    return [float(i) / 10 for i in data]


def request_sheet1(url):
    global G_ID
    html = get_request(url)
    reg = 'content-cell-wrapper.*?"title-name".*?href="(.*?)".*?>(.*?)<.*?js-bookmark-count.*?data-count="(.*?)".*?subtitle-wrapper(.*?)details-wrapper.*?icon-info address.*?<span>(.*?)</span>.*?icon-info icon-info-food-price.*?<span>(.*?)</span>.*?icon-info icon-info-food-name(.*?)</ul>(.*?)</section'

    data_list = re.compile(reg).findall(html)

    for data in data_list[:-1]:
        link = 'https://www.openrice.com' + data[0]
        name = data[1]
        no_benchmark = data[2]
        no_review = get_review(data[3])
        addr = remove_html_tag(data[4])
        price = data[5]
        cuisine = get_cuisine(data[6])
        no_pos, no_neg = get_pos_neg(data[7])

        one_row = [G_ID, name, no_review, addr, price, cuisine, no_pos, no_neg, no_benchmark, link]
        print one_row
        sheet1_data.append(one_row)

        G_ID += 1


def get_cuisine(ori):
    reg = 'href.*?>(.*?)<'
    data = re.compile(reg).findall(ori)

    return '/'.join(data)


def get_pos_neg(ori):
    if 'emoticon-container' not in ori:
        return 'N/A', 'N/A'
    reg = 'span class="score.*?>(.*?)<'
    return re.compile(reg).findall(ori)


def get_review(ori):
    if 'counters-container' not in ori:
        return 'N/A'
    reg = '<span>\((.*?) '
    return re.compile(reg).findall(ori)[0]


def remove_html_tag(ori):
    try:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', ori)
        return str(HTMLParser.HTMLParser().unescape(dd))
    except Exception as e:
        print ori, e
        return ori


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
    time.sleep(1)
    return res


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    filename = 'data/' + filename
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)

    i = 0
    while len(alldata) > 65500:
        _filename = filename.replace('.xls', '_%s.xls' % i)
        start_index = 0
        end_index = 65500
        data = alldata[start_index:end_index]
        alldata = alldata[end_index:]
        w = xlwt.Workbook(encoding='utf-8')
        ws = w.add_sheet('old', cell_overwrite_ok=True)
        for row in range(0, len(data)):
            one_row = data[row]
            for col in range(0, len(one_row)):
                try:
                    ws.write(row, col, one_row[col][:32766])
                except:
                    try:
                        ws.write(row, col, one_row[col])
                    except:
                        print('===Write excel ERROR===' + str(one_row[col]))
        w.save(_filename)
        print("%s===========over============%d" % (_filename, len(data)))
        i += 1
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col][:32766])
            except:
                try:
                    ws.write(row, col, one_row[col])
                except:
                    print('===Write excel ERROR===' + str(one_row[col]))
    w.save(filename)
    print("%s===========over============%d" % (filename, len(alldata)))


def read_excel(filename, start=1):
    global alldata
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        url = table.row(i)[9].value
        try:
            g_id = table.row(i)[0].value
            request_sheet2(url, str(g_id))
        except Exception as e:
            print 'read excel exception--', e, url
            continue


def for_sheet1():
    for i in range(1, 8):
        url = url_bases % i
        request_sheet1(url)

    write_excel('sheet1.xls', sheet1_data)


def for_sheet2():
    read_excel('data/data.xls')
    write_excel('sheet2.xls', sheet2_data)
    write_excel('sheet3.xls', sheet3_data)


for_sheet2()
# request_sheet2('https://www.openrice.com/en/hongkong/r-kentucky-fried-chicken-mong-kok-american-r648553', '1')