# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime
import HTMLParser, urllib2
import xlrd
from scraping.utils import get_request_html, write_excel

saved_hotel = set()
R_ID = 1
sheet1_data = [['ID', 'Hotel URL', 'Hotel Name', 'Address', 'Rating', 'Number of reviews', 'Star', 'Amenities']]
sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Review Date' 'Rating', 'Text Review', 'Reviewer Location',
                'Contributor Level', 'Travel Style']]
sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]

whilte_list_state = {'Kuala_Lumpur'}

cookie = 'TAUnique=%1%enc%3ASLqk%2B6khUnzArkIWpky3yAfBM5Uq3N0u36Bu3YaBBnSRqDIW%2BjDBvQ%3D%3D; TASSK=enc%3AAJV0znQAi190Y2FwWBbr%2FWkHmjUPreYrqWhcXgDHdP896aKkgasX%2FDbb3MqkDZqcNwAC2HmMBz2pmRDdSfDZakf6gzCjLv3IioR%2BVNux3lVRLS%2FbPyD%2BJi502ZqBoIMhvg%3D%3D; ServerPool=X; TART=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; BEPIN=%1%173ad2014fe%3Bweb225a.a.tripadvisor.com%3A30023%3B; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*DSM.1596337427798*AZ.1*RS.1; TADCID=sQXR1Qrep2rrzJlGABQCjnFE8vTET66GHuEzPi7KfV9DztLy9S7pFTGdOJfzUz38qYLAmiLTKJCZ_---qz0eY0vOmgWIzpu1KOM; TAAUTHEAT=-1IuaWaZSkLbEnxfABQC5pMD6MhQQX22iUWVeLafiR8azr3ocsRAxPjiH7Sm-5xyUGmlv9kNagHMMlmEZz-3s7w14kU81TZGYS5vAC3c4nnA6Uj2iA-zD8UyAmb0St4RcoBCBrQvGKTh0wST3MqK9ErozzhF2Lb8XTS2euuhvHmQtAck7U1Hwr4HGkEx0ew5OX5nHysQhy0h8Rn3p4ThBVfi4g; __vt=BLaYJtYA4J0UWae1ABQCq4R_VSrMTACwWFvfTfL3vw8hbu0Hq2heDIXhUwbQueJFNxT68sfeCfQztvBXPL6yBwBE8spYLtjeBu_TbJ2luv3Kt4P5i9qI5C2iZsR0NAfdFjC-n0wBXUcibYi3rpzgbQi44Q; PAC=AB_iu3akpEn2dJrAvnGcwvA6cRKARN24OfRTyTjwL4ApYsD-C-KsKNZIzqa0E8QAxc-ZvuJ0M08YzBdRmUlsdudXcuDmLbwLDum83ey4NlOf7gAdPVmrF5LLyMx83C2dZq7Vrp_hBumiROu_aZVHlJp1bADTTDokfzYaKs0PyomJAHeg4yVGWhQubK2DZFnQ1ihNwbpaTNtp801C7en28frkNCVvSMUcUT-f8h_J-2YN; PMC=V2*MS.30*MD.20200801*LD.20200805; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpv%2C16%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CCrisisSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CRepTarMCSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7CTSMCPers%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CCOVIDMCSess%2C%2C-1%7CTARSWBPers%2C%2C-1%7CListMCSess%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7Cmdpers%2C1%2C1596871674%7CSPACMCSess%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7CRevHubRMPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCrisisPers%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7CRepTarMCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CTSMCSess%2C%2C-1%7CSPMCPers%2C%2C-1%7CRevHubRMSess%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CCOVIDMCPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CSPACMCPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CListMCPers%2C%2C-1%7Cmdsess%2C-1%2C-1%7C; TAReturnTo=%1%%2FRestaurants-g298278-Johor_Bahru_Johor_Bahru_District_Johor.html; roybatty=TNI1625!APCbexsdVzF%2FRIVZ5ASdzk5DBKIwlQWhXJvHVmw9lZsrGYjlvUWw3TCJlxM1wcPFgJCiSEd%2FwLganbW%2FSKA%2B7O%2ByUNBJc95zvVcvK5VjxcT%2FuLbKj33r5Wmgjbz93daHi2yQsdX9DI0D78fAArLGPDSovZnKhfPF%2FaSPyLv3Ptf%2B%2C1; SRT=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; TASession=%1%V2ID.9A53E4DA9B8FF660066B23DE9688140E*SQ.474*LS.DemandLoadAjax*GR.96*TCPAR.26*TBR.50*EXEX.16*ABTR.24*PHTB.24*FS.68*CPU.18*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.ABD562818D249697A8AB4E2FFBFCE092*FA.1*DF.0*FLO.298277*TRA.true*LD.298278*EAU.%5B; TAUD=LA-1596265332138-1*RDD-1-2020_08_01*ARDD-960203-2020_09_30.2020_10_01*HD-6893344-2020_08_04.2020_10_01.298305*G-6893345-2.1.298305.*HDD-72095550-2020_08_09.2020_08_10.1*HC-73283048*LG-345363598-2.1.T.*LD-345363599-.....'

urls = [
    # ('https://www.tripadvisor.com.my/Restaurants-g298277-Johor.html', 'Johor'),
    # ('https://www.tripadvisor.com.my/Restaurants-g298281-Kedah.html', 'Kedah'),
    # ('https://www.tripadvisor.com.my/Restaurants-g298284-Kelantan.html', 'Kelantan'),
    # ('https://www.tripadvisor.com.my/Restaurants-g306997-Melaka_Central_Melaka_District_Melaka_State.html', 'Melaka'),
    # ('https://www.tripadvisor.com.my/Restaurants-g298291-Pahang.html', 'Pahang'), #
    # ('https://www.tripadvisor.com.my/Restaurants-g298297-Perak.html', 'Perak'), #
    # ('https://www.tripadvisor.com.my/Restaurants-g298301-Perlis.html', 'Perlis'),
    # ('https://www.tripadvisor.com.my/Restaurants-g298306-Sabah.html', 'Sabah'), #
    # ('https://www.tripadvisor.com.my/Restaurants-g298308-Sarawak.html', 'Sarawak'),
    # ('https://www.tripadvisor.com.my/Restaurants-g298310-Selangor.html', 'Selangor'), #120 * 5, 80 * 2, 40
    # ('https://www.tripadvisor.com.my/Restaurants-g298318-Terengganu.html', 'Terengganu'),
    # ('https://www.tripadvisor.com.my/Restaurants-g298570-Kuala_Lumpur_Wilayah_Persekutuan.html', 'Kuala_Lumpur'), #160
    # ('https://www.tripadvisor.com.my/Restaurants-g298286-Labuan_Island_Sabah.html', 'Labuan'),
    # ('https://www.tripadvisor.com.my/Restaurants-g298305-Putrajaya_Wilayah_Persekutuan.html', 'Putrajaya'),
    ('https://www.tripadvisor.com.my/Restaurants-g660694-Penang_Island_Penang.html', 'Penang')
]

uid_location_dict = {}


def get_page_no(html):
    if 'class="pageNumbers"' not in html:
        return 1
    page_reg = 'data-page-number="(.*?)"'

    data = re.compile(page_reg).findall(html)

    if data:
        return int(data[-1])


def get_request(get_url, timeout=10):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.tripadvisor.com.my/Restaurants-g298278-Johor_Bahru_Johor_Bahru_District_Johor.html')
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=timeout)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


def request_sheet0(item):
    url, state = item
    html = get_request(url)

    if 'id="LOCATION_LIST"' in html:
        reg = 'class="geo_name".*?href="(.*?)".*?>(.*?)<'
        urls = re.compile(reg).findall(html)
        for url in urls:
            request_sheet1('https://www.tripadvisor.com.my' + url[0], url[1].replace('Restaurants', '').strip(), state)
    else:
        request_sheet1(url, state, state)


def request_sheet1(ori_url, city, state):
    global sheet1_data

    gid = ori_url.split('-g')[-1].split('-')[0]

    url = 'https://www.tripadvisor.com.my/RestaurantSearch?Action=PAGE&ajax=1&availSearchEnabled=false&sortOrder=popularity&geo=' \
          + gid + '&o=a'

    page_no = None
    i = 0

    hotel_reg = 'class="wQjYiB7z".*?href="(.*?)".*?>(.*?)</a.*?MIajtJFg _1cBs8huC(.*?)MIajtJFg _1cBs8huC _3d9EnJpt(.*?)</div'

    while True:
        try:

            html = get_request(url + str(i * 30))

            if not page_no:
                page_no = get_page_no(html)

            if (i + 1) > page_no:
                break

            data = re.compile(hotel_reg).findall(html)
            print i, page_no, city, state, ori_url

            for item in data:
                hote_url = 'https://www.tripadvisor.com.my' + item[0]
                name = remove_html_tag(item[1]).replace('amp;', '')
                no_reviews, rating = get_classification(item[2])
                Cuisines, price = get_cuisine_price(item[3])

                location = get_hotel_details(hote_url)
                one_row = [state, city, name, hote_url, no_reviews, rating, Cuisines, price, location]
                sheet1_data.append(one_row)

            i += 1
        except Exception as e:
            print 'ERR---', url, i, e


def get_cuisine_price(ori):

    cuisine = 'N/A'
    price = 'N/A'

    if 'class="_1p0FLy4t">'  in ori:
        reg = 'class="_1p0FLy4t">(.*?)<'

        data_list = re.compile(reg).findall(ori)

        for data in data_list:
            if '$' in data:
                price = data
            else:
                cuisine = data
    return cuisine, price


def get_classification(ori):

    rating = 'N/A'
    no_review = 0

    if 'Be the first to review this restaurant' not in ori:
        star_css_score = {
            '_19bYFj6V': 0.5,
            '_3kNoie7g': 1.0,
            '_2SkXD1ea': 1.5,
            '_36WMQ-A0': 2.0,
            '_2Icfy9b1': 2.5,
            '_3RqovlMp': 3.0,
            '_2n4wJlqY': 3.5,
            '_1-HtLqs3': 4.0,
            '_1RZqMyqR': 4.5,
            '_2vB__cbb': 5.0,
        }

        for k, v in star_css_score.items():
            if k in ori:
                rating = str(v)
                break
        review_Reg = 'class="w726Ki5B">(.*?)<'
        no_review = re.compile(review_Reg).findall(ori)[0]
    return no_review, rating


def get_hotel_details(url):
    html = get_request_html(url, cookie)
    location = 'N/A'
    if 'class="_15QfMZ2L"' in html:
        reg = 'class="_15QfMZ2L">(.*?)<'
        locations = re.compile(reg).findall(html)
        for loca in locations:
            if len(loca) > 1:
                location = loca

    return location


def request_sheet2(row, number, hotel_url):
    global sheet2_data
    page_no = number / 5
    if number % 10 != 0:
        page_no += 1

    terminate = False
    for i in range(0, page_no):
        if terminate:
            break
        try:
            url = hotel_url.replace('-Reviews-', '-Reviews-or%s-' % str(i * 10))
            print page_no, i, row, url

            html = get_request_html(url, cookie)

            reg = 'avatar profile_(.*?)".*?usernameClick.*?div>(.*?)<.*?ui_bubble_rating bubble_(.*?)".*?title=\'(.*?)\''

            comment_list = re.compile(reg).findall(html)
            for comment in comment_list:
                uid = comment[0]
                name = comment[1]
                # country = get_user_location(uid)
                country = uid
                rating = int(comment[2]) / 10.0
                review_date = get_comment_date(comment[3])

                if int(review_date.split('/')[-1]) <= 2018:
                    terminate = True
                    break

                one_row = [hotel_url, name, review_date, rating, country]
                sheet2_data.append(one_row)

        except Exception as e:
            print('ERROR-sheet2-', hotel_url, i, e)


def get_comment_date(ori):
    try:
        date = datetime.strptime(ori, '%d %B %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_user_location(uid):

    if uid in uid_location_dict:
        return uid_location_dict[uid]

    html = get_request('https://www.tripadvisor.com.sg/MemberOverlay?uid=' + uid)

    reg = 'href="(.*?)"(.*?)memberdescriptionReviewEnhancements(.*?)countsReviewEnhancements'
    data = re.compile(reg).findall(html)
    if not data:
        return 'N/A'

    location = get_reviewer_location(data[0][2]).split('from ')[-1]

    uid_location_dict[uid] = location
    return location


def get_reviewer_location(ori):
    reg = '<li>(.*?)<'
    data = re.compile(reg).findall(ori)
    if len(data) < 2:
        return 'N/A'
    return data[1]


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def read_excel_for_comments(filename, start=1):
    global R_ID, sheet2_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        main_url = row[3].value
        state = row[0].value
        try:
            if state in whilte_list_state:
                review_no = int(row[4].value)
                if review_no > 0:
                    request_sheet2(i, review_no, main_url)

                    if i % 5000 == 0:
                        write_excel('Res_sheet2_%d.xls' % i, sheet2_data)
                        sheet2_data = []
        except Exception as e:
            print main_url, e
    write_excel('Res_sheet2_end.xls', sheet2_data)


def read_for_user_location(filename, start=1):
    global R_ID, sheet2_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    uids = set()
    for i in range(start, table.nrows):
        row = table.row(i)
        uid = row[4].value
        uids.add(uid)

    print 'total', len(uids)

    for i in range(start, table.nrows):
        row = table.row(i)
        uid = row[4].value
        try:
            location = get_user_location(uid)
            one_row = [row[j].value for j in range(table.ncols-1)]
            one_row.append(location)
            if i % 20 == 0:
                print i
            sheet2_data.append(one_row)

            if i % 5000 == 0:
                write_excel('Res_sheet2_%d.xls' % i, sheet2_data)
                sheet2_data = []
        except Exception as e:
            print uid, e
    write_excel('Res_sheet2_end.xls', sheet2_data)


def read_valid_comments(filename, start=1):
    global R_ID, sheet2_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    valid_urls = set()

    for i in range(start, table.nrows):
        row = table.row(i)
        main_url = row[3].value
        state = row[0].value
        price = row[7].value
        try:
            if state in whilte_list_state and price == '$$ - $$$':
                valid_urls.add(main_url)
        except Exception as e:
            print i, e

    print len(valid_urls)

    data = xlrd.open_workbook('data/res/Restaurant_review_6states.xlsm', encoding_override="utf-8")
    table = data.sheets()[0]

    sheet_data = []

    for i in range(start, table.nrows):
        row = table.row(i)
        main_url = row[0].value
        try:
            if main_url in valid_urls:
                one_row = [row[i].value for i in range(table.ncols)]
                sheet_data.append(one_row)
        except Exception as e:
            print i, e
    write_excel('Res_sheet2_KL.xls', sheet_data)


def step_1():
    global sheet1_data
    for item in urls:
        request_sheet0(item)
        write_excel(item[1] + '.xls', sheet1_data)


reload(sys)
sys.setdefaultencoding('utf-8')
# step_1()
# read_excel_for_comments('data/res/Restaurant2.xls')
read_for_user_location('data/res/Restaurant_review_6states.xlsm')
# read_valid_comments('data/res/Restaurant.xlsm')