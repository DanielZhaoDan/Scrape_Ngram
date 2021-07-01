from scraping import utils
import re
import urllib
import xlrd
import time

sheet1 = [['UID', 'index', 'Logo', 'title', 'url', 'img_url']]
sheet2 = [['UID', 'url', 'Logo', 'Title', 'Spec First Row', 'Spec Others', 'img_url']]

cookie = 'session-id=261-7798790-7898928; i18n-prefs=INR; ubid-acbin=262-3210966-1370101; x-wl-uid=18ob6vcFRowaOEgwMO58JY5A+MJNn5RzJattrm0ULpFrYRcnii3kNfAMTunI5tWStOH9noqDo/Fc=; session-token=svTVW5lWAgKGDMPgYXcjAPtjlgYd4M3V+fDc9wiQaiNYhZhvSTbaKl7/AyUhOit0NQSc8Jucy9KeD2QD4PZPJh62Q5G03mLEE32+L1KPsJQ299IrZJT8Y15qImzg51RMpP0m22ZBmww04D/yUSIJ5q5nRO2qAyva9izPE1+EyVVYzSl7Ii1zXiezHZLP/bwp; session-id-time=2082758401l; visitCount=17; csm-hit=tb:W8RRNJY3FQEKA3PWD3BX+s-KW45XX0PEX9MXW2E9D6W|1572755607657&t:1572755607657&adb:adblk_yes'
G_ID = 1

base_url = 'https://www.amazon.in/s?i=computers&bbn=1375424031&rh=n:976392031,n:976393031,n:1375424031,p_n_feature_thirteen_browse-bin:12598143031|12598144031|12598145031|12598146031|12598147031|12598151031|12598159031|12598161031|12598162031|12598163031|12598164031|12598165031|16757429031|16757430031&dc&fst=as:off&qid=1572661643&rnid=12598141031&ref=sr_pg_2&page='


def request_sheet1(page_no):

    global G_ID

    url = base_url + str(page_no)
    print url
    html = utils.get_request_html(url, cookie)
    utils.write_html(html, '0.html')

    reg = 'a-section aok-relative s-image-fixed-height.*?src="(.*?)".*?a-link-normal a-text-normal.*?href="(.*?)".*?a-size-medium a-color-base a-text-normal">(.*?)<'
    data_list = re.compile(reg).findall(html)

    for i in range(len(data_list)):
        rank = str(page_no) + '.' + str(i+1)
        img_url = data_list[i][0]
        detail_url = ger_url(data_list[i][1].replace('&amp;', '/'))
        title = data_list[i][2][:179]
        one_row = ['AM_%d' % G_ID, rank, 0, title, detail_url, img_url]

        sheet1.append(one_row)
        print one_row
        G_ID += 1
        # request_sheet2(one_row[0], detail_url, data_list[i][2])


def ger_url(ori):
    return 'https://www.amazon.in' + urllib.unquote(ori.split('url=')[-1])


def request_sheet2(uid, url):
    html = utils.get_request_html(url, cookie)

    reg = 'id="imgTagWrapperId".*?data-old-hires="(.*?)".*?id="productTitle".*?>(.*?)<.*?id="feature-bullets"(.*?)</ul'

    data = re.compile(reg).findall(html)

    img_url = data[0][0]
    title = data[0][1].strip()
    first, other = get_spec(data[0][2])
    one_row = [uid, url, 0, title, first, other, img_url]

    sheet2.append(one_row)
    print one_row


def get_spec(ori):

    reg = 'class="a-list-item">(.*?)<'

    data_list = re.compile(reg).findall(ori)
    return data_list[0], ';'.join(data_list[1:])


def read_excel(filename, start=1):
    global alldata
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        url = table.row(i)[4].value
        g_id = table.row(i)[0].value
        if g_id not in ['AM_140']:
            continue
        try:
            request_sheet2(g_id, url)
        except Exception as e:
            print 'read excel exception--', e, g_id
        time.sleep(2)


read_excel('data/sheet1.xls')

utils.write_excel('sheet2.xls', sheet2)