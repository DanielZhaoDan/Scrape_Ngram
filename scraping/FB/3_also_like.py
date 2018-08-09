# coding: utf-8
import sys, urllib
import urllib2
import re
import HTMLParser
import time, datetime
from selenium import webdriver
import xlwt
import os
import httplib
import xlrd

end_index = 8
alldata = [['Profile ID', 'Name', 'Also Likes', 'Category', 'URL of also Likes']]

cookie = 'sb=6ST_WtOPfg79wHi2665Bsh6V; datr=6ST_WoDL7rHIezUJzF7ngsbe; dpr=2; locale=en_GB; lh=en_GB; c_user=100026249853067; xs=35%3AhiHc9vr9W2M9-g%3A2%3A1526678445%3A-1%3A-1; pl=n; fr=0UaA3QtnOrdwqneVH.AWUd_UJEGCCN2n9_YaE8jAy3gu8.Ba_yTp.BE.AAA.0.0.Ba_1Hi.AWXb7VeP; presence=EDvF3EtimeF1526684266EuserFA21B26249853067A2EstateFDutF1526684266116CEchFDp_5f1B26249853067F15CC; act=1526684286374%2F7; wd=1234x427'

page_id_data = {}
FB_ACCOUNT = ['delakalib@travala10.com'][0]


def get_ori_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    page.close()
    return html


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_request_of_url(url):
    res = get_ori_request(url)
    res = HTMLParser.HTMLParser().unescape(res).decode('unicode-escape').replace('\\', '')
    return res


def get_ori_request(url):
    print url
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
    req.add_header("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res


def save_value(row_id, profile_name, profile_url, driver):
    global alldata
    if 'profile.php' in profile_url:
        like_url = profile_url.split('ref')[0] + 'sk=likes'
    else:
        like_url = profile_url.split('?')[0] + '/likes'
    html = request_one(like_url, driver)
    reg = 'class="fsl fwb fcb".*?href="(.*?)".*?>(.*?)<.*?fsm fwn fcg">(.*?)<'
    like_list = re.compile(reg).findall(html)
    print row_id, 'length:', len(like_list)
    like_list = like_list[:201]
    for like in like_list:
        one_row = [row_id, profile_name, like[1], remove_html_tag(like[2]), like[0]]
        alldata.append(one_row)


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
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    driver = init_browser('https://www.facebook.com/profile.php?id=100004900566910&lst=100006957738125%3A100004900566910%3A1526572401&sk=likes')

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            profile_id = row[0].value
            profile_name = row[1].value
            profile_url = row[2].value
            save_value(profile_id, profile_name, profile_url, driver)
        except Exception as e:
            print(i, e)


def init_browser(url):
    driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
    driver.get(url)
    time.sleep(2)

    username = driver.find_element_by_name("email")
    password = driver.find_element_by_name("pass")
    username.send_keys(FB_ACCOUNT)  ##your username, need to be replaced
    password.send_keys("happy2018")  ##your password, need to be replaced
    time.sleep(1)

    try:
        driver.find_element_by_id("loginbutton").click()
    except:
        driver.find_element_by_id("u_0_0").click()
    time.sleep(2)
    return driver


def request_one(url, driver):
    driver.get(url)
    time.sleep(1)

    for i in range(0, end_index):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print i,
        time.sleep(1.6)
    html_source = driver.page_source
    data = html_source.encode('utf-8')
    return data


def get_page_like_follower(url):
    global page_id_data
    url = url.split('?')[0]
    if page_id_data.get(url):
        return page_id_data.get(url)
    reg = 'class="_4bl9">.*?>(.*?) people'
    html = get_ori_request(url)
    datas = re.compile(reg).findall(html)
    like_follow = []
    for data in datas:
        data = data.split('<div>')[-1]
        like_follow.append(data)
    page_id_data[url] = like_follow
    return like_follow


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    read_excel('data/profile.xls')
    write_excel('also_like.xls', alldata)

