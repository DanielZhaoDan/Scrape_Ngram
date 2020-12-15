from scraping import utils
import re
import urllib
import xlrd
import time
from selenium import webdriver
import json

sheet1 = [['UID', 'index', 'Logo', 'title', 'url', 'img_url', 'Rank']]
sheet2_title = ['Product Name', 'Brand', 'Color', 'Touch Screen', 'Screen Size', 'Storage Type', 'Hard Drive Capacity', 'RAM Memory', 'Graphics', 'Processor Type', 'Battery Life']
sheet2 = []
sheet2.append(sheet2_title)

cookie = 'com.wm.reflector="reflectorid:0000000000000000000000@lastupd:1590806193449@firstcreate:1590806193449"; next-day=1590868800|true|false|1590926400|1590806193; location-data=94066%3ASan%20Bruno%3ACA%3A%3A0%3A0|21k%2C46y%2C1kf%2C1rc%2C46q%2C2nz%2C2b1%2C4bu%2C2er%2C1o1|2|7|1|1xun%3B16%3B0%2C1xtf%3B16%3B1%2C1xwj%3B16%3B2%2C1ygu%3B16%3B3%2C1xwq%3B16%3B4; DL=94066%2C%2C%2Cip%2C94066%2C%2C; nd_sess=0|1; TB_DNS_Perf_Test=1; TB_DC_Dist_Test=1; TB_DC_Flap_Test=1; vtc=SRHf4JnV83hWv8i1JxphwU; bstc=SRHf4JnV83hWv8i1JxphwU; mobileweb=0; xpa=-qAzN|2M2jW|8ftLP|9OWmX|BnGdF|ME715|Modqx|PPcYg|Uhvy5|aqGJP|c1-9M|lyrHR|mzi22|q4fxq|qacLZ|wyHEU|z9Zjz|zfQif; exp-ck=8ftLP19OWmX1ME7153Modqx3PPcYg1Uhvy51aqGJP1c1-9M1lyrHR2q4fxq2wyHEU2z9Zjz1zfQif1; bifrost-sb=true; go-xpa=-qAzN|2M2jW|8ftLP|9OWmX|BnGdF|ME715|Modqx|PPcYg|Uhvy5|aqGJP|c1-9M|lyrHR|mzi22|q4fxq|qacLZ|wyHEU|z9Zjz|zfQif; go-exp-ck=8ftLP19OWmX1ME7153Modqx3PPcYg1Uhvy51aqGJP1c1-9M1lyrHR2q4fxq2wyHEU2z9Zjz1zfQif1; TS01b0be75=01538efd7c26ab2dcafb657954d11aeea5ed8e87d42bb3caeec23347fb46fad1802b0fa2b2b73fac1db2d30db594b588e25ff45f59; TS013ed49a=01538efd7c26ab2dcafb657954d11aeea5ed8e87d42bb3caeec23347fb46fad1802b0fa2b2b73fac1db2d30db594b588e25ff45f59; xpm=1%2B1590806193%2BSRHf4JnV83hWv8i1JxphwU~%2B0; go-xpm=1%2B1590806193%2BSRHf4JnV83hWv8i1JxphwU~%2B0; go-bifrost-sb=true; TBV=7; adblocked=true; ndcache=b; akavpau_p0=1590806797~id=e618916cf149bafce71f9db640261204; cart-item-count=0; s_vi=[CS]v1|2F68E35B0515989E-6000081ACA32A8DA[CE]; viq=Walmart; _gcl_au=1.1.1944183111.1590806199; _uetsid=a8d9b372-8d71-39b5-4c0b-2325f475c88d; _internal.verticalId=default; _internal.verticalTheme=default; s_pers=%20s_fid%3D74B07A31570F6E87-06F05A80C379DDFF%7C1653878258649%3B%20s_v%3DY%7C1590808058653%3B%20gpv_p11%3DSearch%2520Results%2520Search%7C1590808058675%3B%20gpv_p44%3DSearch%7C1590808058684%3B%20s_vs%3D1%7C1590808058694%3B; s_sess=%20ent%3DSearch-SearchResults%3B%20cp%3DY%3B%20cps%3D1%3B%20ps%3D7%3B%20chan%3Dorg%3B%20v59%3DElectronics%3B%20v54%3DSearch%2520Results%2520Search%3B%20s_sq%3D%3B; TS011baee6=01c5a4e2f95bb81818328e07485633846ae70e4f2928551c349bd5b407fb0c7cc4eda02e9e4f914a89031d42cfdd364f629d64d022; TS01e3f36f=01c5a4e2f95bb81818328e07485633846ae70e4f2928551c349bd5b407fb0c7cc4eda02e9e4f914a89031d42cfdd364f629d64d022; TS018dc926=01c5a4e2f95bb81818328e07485633846ae70e4f2928551c349bd5b407fb0c7cc4eda02e9e4f914a89031d42cfdd364f629d64d022; akavpau_p8=1590806866~id=2dfdcb36d6d8e9debac4aeea44bf1b10'
G_ID = 1

base_url = 'https://www.walmart.com/search/?grid=false&ps=40&query=laptop&sort=best_seller&page='

prefix = ''


def request_sheet1(page_no):

    global G_ID, driver

    url = base_url + str(page_no)
    print url
    html = utils.get_request_html(url, cookie)

    reg = '<script id="searchContent" type="application/json">(.*?)</script>'

    raw_json = re.compile(reg).findall(html)

    if not raw_json:
        print 'error1-nojson-', url

    json_list = json.loads(raw_json[0])

    items = json_list.get('searchContent', {}).get('preso', {}).get('items', [])

    if not items:
        print 'error1-noitems-', url

    for item in items:
        id = item['usItemId']
        item_url = 'https://www.walmart.com' + item['productPageUrl']
        title = item['title']
        img_url = item['imageUrl']

        no_review = item.get('numReviews', 0)
        rating = item.get('customerRating', 0)

        is_sponsored = False
        is_new = False

        price = item.get('primaryOffer', {}).get('offerPrice', 'N/A')

        # details = request_sheet2(item_url)

        one_row = [prefix + id, item_url, img_url, is_sponsored, is_new, title, rating, no_review, G_ID, price]

        sheet1.append(one_row)
        G_ID += 1
        print one_row


def request_sheet2(url):
    global sheet2
    html = utils.get_request_html(url, cookie)

    details = ['N/A' for i in range(11)]
    category_dict = {}

    reg = 'class="product-specification-row".*?<td.*?>(.*?)<.*?<td.*?>(.*?)</td'

    data_list = re.compile(reg).findall(html)

    for data in data_list:
        category_dict[utils.remove_html_tag(data[0]).strip()] = utils.remove_html_tag(data[1])

    for i in range(len(sheet2_title)):
        details[i] = category_dict.get(sheet2_title[i], category_dict.get(sheet2_title[i]+'Info', 'N/A'))
    return details


def get_spec(ori):

    reg = 'class="a-list-item">(.*?)<'

    data_list = re.compile(reg).findall(ori)
    return data_list[0], ';'.join(data_list[1:])


def read_excel(filename, start=1):
    global sheet2
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        url = table.row(i)[1].value
        try:
            details = request_sheet2(url)
            one_row = [table.row(i)[j].value for j in range(table.ncols)] + details
            print one_row
            sheet2.append(one_row)
        except Exception as e:
            print 'read excel exception--', e, url


# for i in range(1, 26):
#     request_sheet1(i)
# utils.write_excel("sheet1.xls", sheet1)
read_excel('data/sheet1.xls')
utils.write_excel("sheet2.xls", sheet2)