# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
from datetime import datetime
import HTMLParser
import os
import xlrd
import requests
from bs4 import BeautifulSoup

saved_user = set()
R_ID = 1
sheet1_data = [['ID', 'topic URL', 'topic headline', 'forum', 'author', 'Number of comments', 'post date', 'topic text']]
sheet2_data = [['ID', 'comment date', 'comment text']]
sheet3_data = [['author name', 'author profile url', 'topic url', 'contribution level', 'hotel expert', 'restaurant expert', 'attraction expert', 'point']]

cookie = 'TASSK=enc%3AAN9lAayJHu6zymcBEPiLJGEjtRbulb0ah4RuMUvvgUwOnK9JQUZ68imxvbhTTPp4zqaRfHfWwb0leXged%2Fkr23xs8uRrCStOSBcx0142LYmv5q4UBXjPpKW49hYu5cvtTA%3D%3D; ServerPool=A; PMC=V2*MS.54*MD.20190222*LD.20190222; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; TAUnique=%1%enc%3AXnBid%2FUoJ%2FxpV3gABz9d9kKtNo8JTTco7J4x5FuvyWc1jFGw1G8Jhw%3D%3D; TART=%1%enc%3AbiYu%2F2hIUs6OJ9fpGY8SDuCePIUs%2Bu1MGehr%2BB%2BaecBAPUT5DNbp%2FQIKSCcfFQDJ9v44sG1ePyI%3D; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CCCUVOwnPers%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7CCCUVOwnSess%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7C; TAReturnTo=%1%%2FProfile%2FKVE1005%3Ftab%3Dforum; PAC=AM9L36NPKzPuHOuVKmmwT0THXFgq_Aq8k2GbpQxAQvifZiS4OmEfVh64hKITexU0D7YEjhq5KY1TusTdCjTWj2efKOZNEfNHbjzFmM6kU6ldDf-Mrpgu0Id-mCl1CXAv0z3IbkFj0016NyKcWTRzVwH04v7KMCk10KBHdCio2soGsHziiOK-Y6Fc_cj-stkZuw%3D%3D; roybatty=TNI1625!APBGHE9dEBGdWe4gDq69uT69WYL3tEGrgpDR%2Bu7NijlnLf%2FSv51P7NfVRrXRaMBvPM43%2BRXfZRiRtnkp3%2BILf69YOJsS9aE4JigQwbg3keAftFFZzwko2DGcW6dkPsw%2BrFlTP1FIjm9VYCXJgGeEXWpG3Fmexu9Fum7%2FKz8llCks%2C1; TASession=V2ID.9BDA45C4BB64070F8E401790A923CC9D*SQ.143*LS.DemandLoadAjax*GR.61*TCPAR.91*TBR.10*EXEX.33*ABTR.75*PHTB.85*FS.43*CPU.76*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.255055; TAUD=LA-1550852347181-1*RDD-1-2019_02_23*LG-7921073-2.1.F.*LD-7921074-.....'

base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'

all_hotel_url = [
    ('https://www.tripadvisor.com.sg/Hotels-g298184-oa%s-Tokyo_Tokyo_Prefecture_Kanto-Hotels.html', 21, 'Tokyo'),
    ('https://www.tripadvisor.com.sg/Hotels-g298566-oa%s-Osaka_Osaka_Prefecture_Kinki-Hotels.html', 11, 'OSAKA'),
    ('https://www.tripadvisor.com.sg/Hotels-g298564-oa%s-Kyoto_Kyoto_Prefecture_Kinki-Hotels.html', 14, 'Kyoto'),
    ('https://www.tripadvisor.com.sg/Hotels-g298112-oa%s-Gifu_Gifu_Prefecture_Tokai_Chubu-Hotels.html', 2, 'Gifu'),
    ('https://www.tripadvisor.com.sg/Hotels-g298106-oa%s-Nagoya_Aichi_Prefecture_Tokai_Chubu-Hotels.html', 4, 'NAGOYA'),
]

uid_level_dict = {}


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


def remove_html_tag(ori):
    soup = BeautifulSoup(ori, 'lxml')
    for script in soup(["script", "style"]):
        script.decompose()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text


def get_date(ori):
    d = datetime.strptime(ori, '%d %b %Y')
    date = d.strftime('%d/%m/%Y')
    return date


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", base_url)
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=5)
    res = res_data.read()
    res = HTMLParser.HTMLParser().unescape(res).decode('unicode-escape').replace('\\', '')
    return res.replace('\n', '').replace('\r', '')


def post_request(url, data):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': base_url,
        'Cookie': cookie,
    }
    resp = requests.post(url, data=data, headers=headers)
    return resp.content.replace('\n', '').replace('\r', '')


def request_sheet1(url):
    global sheet1_data, R_ID
    html = get_request(url)
    reg = 'topofgroup".*?href="(.*?)">(.*?)</.*?searchresultgrid">.*?>(.*?)<.*?searchresultgrid">.*?>(.*?)<'
    base_list = re.compile(reg).findall(html)

    for base in base_list:
        url = 'https://www.tripadvisor.com.sg' + base[0]
        try:
            title = remove_html_tag(base[1])
            forum = base[2]
            author = base[3]
            post_date, content, comment_no = request_forum_detail(url, R_ID)
            one_row = ['ID_%d' % R_ID, url, title, forum, author, comment_no, post_date, content]
            sheet1_data.append(one_row)
            print one_row
            R_ID += 1
        except Exception as e:
            print 'EXCEPT--1', url, e


def request_forum_detail(url, R_ID):
    global sheet2_data
    html = get_request(url)
    reg = 'postDate.>(.*?)<.*?class=.postBody.>(.*?)<div class="postTools".*?class="pgCount".*?of<.*?> (.*?) '
    detail = re.compile(reg).findall(html)
    post_date = get_date(detail[0][0].split(',')[0])
    content = remove_html_tag(detail[0][1])
    comment_no = int(detail[0][2])

    comment_reg = 'class=.post (.*?)postDate.>(.*?)<.*?postBody.>(.*?)<div class="postTools"'

    comment_list = re.compile(comment_reg).findall(html)
    for comment in comment_list[1:]:
        user_url = get_user_url(comment[0])
        date = get_date(comment[1].split(',')[0])
        text = remove_html_tag(comment[2])
        # print user_url, date, text
        sheet2_data.append([R_ID, date, text])

        request_user_detail(url, user_url)

    i = 10
    while comment_no > 10:
        temp = url.split('-')
        next_url = '-'.join(temp[0:4]+['o%d'%i]+temp[4:])
        print next_url
        html = get_request(next_url)

        comment_list = re.compile(comment_reg).findall(html)
        for comment in comment_list[1:]:
            user_url = get_user_url(comment[0])
            date = get_date(comment[1].split(',')[0])
            text = remove_html_tag(comment[2])
            sheet2_data.append([R_ID, date, text])
            # print user_url, date, text

            if user_url:
                request_user_detail(url, user_url)
        i += 10
        comment_no -= 10

    return post_date, content, comment_no


def get_user_url(ori):
    reg = 'href="(.*?)"'
    data = re.compile(reg).findall(ori)
    if not data:
        return None
    return 'https://www.tripadvisor.com.sg/members-badgecollection/' + data[0].split('?')[0].split('/')[-1]


def request_user_detail(url, user_url):
    global sheet3_data, saved_user
    if user_url in saved_user:
        return
    sheet3_data.append([url, user_url])
    saved_user.add(user_url)
    return []


def request_sheet3(url, user_url):
    global sheet3_data
    html = get_request(user_url)
    reg = 'class="points"> (.*?) .*?class="level .*?<span>(.*?)<'
    data = re.compile(reg).findall(html)
    point = data[0][0]
    level = data[0][1]
    hotel = 0
    attraction = 0
    restaurant = 0

    item_reg = 'class="badgeText">(.*?)<.*?subText">(.*?)<'
    item_list = re.compile(item_reg).findall(html)

    for item in item_list:
        if 'Hotel Expert' in item[0]:
            hotel = item[1].split(' ')[-1]
        elif 'Restaurant Expert' in item[0]:
            restaurant = item[1].split(' ')[-1]
        elif 'Attraction Expert' in item[0]:
            attraction = item[1].split(' ')[-1]

    one_row = [user_url.split('/')[-1], user_url, url, level, hotel, restaurant, attraction, point]
    sheet3_data.append(one_row)
    print one_row


def read_excel(filename, start=1):
    global R_ID, sheet3_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    count_map = {}

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            id = int(row[0].value)
            print 'ID_%d' % id
        except:
            print(i)
    for k, v in count_map.items():
        print v


def pre_load(filename):
    global saved_hotel
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(1, table.nrows):
        row = table.row(i)
        try:
            id = row[0].value
            if id not in saved_hotel:
                saved_hotel.add(id)
        except:
            print(i)


def request_sheet1_2():
    for i in range(0, 16):
        url = 'https://www.tripadvisor.com.sg/SearchForums?q=agoda&s=D&ff=120&geo=255055&o=%d' % (i * 10)
        print url
        request_sheet1(url)
    write_excel('sheet1.xls', sheet1_data)
    write_excel('sheet2.xls', sheet2_data)
    write_excel('sheet3.xls', sheet3_data)


reload(sys)
sys.setdefaultencoding('utf-8')
# request_sheet1_2()
read_excel('data/sheet2.xls')
# write_excel('sheet33.xls', sheet3_data)