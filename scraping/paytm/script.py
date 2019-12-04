from scraping import utils
import re
import urllib
import xlrd
import time

sheet1 = [['UID', 'index', 'Logo', 'title', 'url', 'img_url']]
sheet2 = [['UID', 'url', 'Logo', 'Title', 'Spec First Row', 'Spec Others', 'img_url']]

cookie = 'connect.sid=s%3A8xJAuH3zIzRbvvSXc1eTLxq77z19IReK.G0yKYhjskwQqTvRzd%2BqIlxLY%2BrqLT33aHIBeA9AF%2F1o; tvc_vid=51571456689845; cto_lwid=9b5b5c01-33da-4084-b421-82b3effd6f57; _ga=GA1.2.1795197323.1571456690; referrer=; secure=true; returning_usr=1; _gid=GA1.2.1122184111.1572756242; acw_tc=95818c0515727657610593538e7b95b80d806479d17b69eb14417a99dca418; queenoftarts=pawslmktshopapp2028; XSRF-TOKEN=Wpc1Vi2U-_0CbUdsWZVl-Ule0A9zqwbnvPpQ; AWSELB=97B3358B1C150AC96AC74F39ED34D289809132006F7BA5B2F25F07E55154F8085275EA0D2F39DF8BB21744F830D89ECD43579653C4ACCDBBCD4A4C7F9CD6A9DF1E13415F53; _gat_UA-36768858-21=1'
G_ID = 1

base_url = 'https://paytmmall.com/laptops-glpid-6453?use_mw=1&src=store&from=storefront&page='


def request_sheet1(page_no):

    global G_ID

    url = base_url + str(page_no)
    print url
    html = utils.get_request_html(url, cookie)

    reg = 'class="_3WhJ".*?href="(.*?)".*?title="(.*?)".*?img.*?src="(.*?)\?'
    data_list = re.compile(reg).findall(html)

    for i in range(len(data_list)):
        rank = str(page_no) + '.' + str(i+1)
        img_url = data_list[i][2]
        detail_url = 'https://paytmmall.com' + data_list[i][0].replace('&amp;', '/')
        title = data_list[i][1][:66]
        one_row = ['PT_%d' % G_ID, rank, 0, title, detail_url, img_url]

        sheet1.append(one_row)
        print one_row
        G_ID += 1
        # request_sheet2(one_row[0], detail_url)


def request_sheet2(uid, url):
    html = utils.get_request_html(url, cookie)

    reg = 'class="_3v_O" src="(.*?)\?.*?class="NZJI">(.*?)<(.*?)class="_3a59"'

    data = re.compile(reg).findall(html)

    img_url = data[0][0]
    title = data[0][1].strip()
    first, other = get_spec(data[0][2])
    one_row = [uid, url, 0, title, first, other, img_url]

    sheet2.append(one_row)
    print one_row


def get_spec(ori):

    if 'Product Highlights' not in ori:
        return 'NIL', 'NIL'

    reg = 'li>(.*?)</'

    data_list = re.compile(reg).findall(ori)
    return utils.remove_html_tag(data_list[0]), ';'.join([utils.remove_html_tag(data_list[i]) for i in range(1, len(data_list))])


def read_excel(filename, start=1):
    global alldata
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        url = table.row(i)[4].value
        g_id = table.row(i)[0].value
        if g_id not in ['PT_151', 'PT_110']:
            continue
        try:
            request_sheet2(g_id, url)
        except Exception as e:
            print 'read excel exception--', e, g_id



# for i in range(1, 6):
#     request_sheet1(i)

# utils.write_excel('sheet1.xls', sheet1)
read_excel('data/sheet1.xls')
utils.write_excel('sheet2.xls', sheet2)