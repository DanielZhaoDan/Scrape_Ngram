# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
from scraping.utils import post_request_html, get_request_html, write_html, write_excel

saved_hotel = set()
R_ID = 1
sheet1_data = [['ID', 'Hotel URL', 'Hotel Name', 'Address', 'Rating', 'Number of reviews', 'Star', 'Amenities']]
sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Review Date' 'Rating', 'Text Review', 'Reviewer Location',
                'Contributor Level', 'Travel Style']]
sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]

cookie = 'TADCID=c2bevLVd4OPVw503ABQCjnFE8vTET66GHuEzPi7KfV8tUou66XdIemKmPKfsCPHQfdv4PInKBM8C97eUZrB6Eqeg3IC34pkFTk8; TAAUTHEAT=SauzFQK9qlqNoDiJABQC5pMD6MhQQX22iUWVeLafiR8EUuGQddQ1WIBUET49l7qV_Jr2uIAf3avgX9lHkuxKj-oW9jOdB5kLy_cOJxLD6Nr5FCxY13i-Y3wH1LxBaeHNiHxJEyh3nPVmlYixDfdqjmWVa-IxIRulyacayIDETTWZQ4TwH-zNWtg2ShTeQfPMseEyhzdm7wkisMyW-VFChGEFRg; TAUnique=%1%enc%3ASLqk%2B6khUnzArkIWpky3yAfBM5Uq3N0u36Bu3YaBBnSRqDIW%2BjDBvQ%3D%3D; TASSK=enc%3AAJV0znQAi190Y2FwWBbr%2FWkHmjUPreYrqWhcXgDHdP896aKkgasX%2FDbb3MqkDZqcNwAC2HmMBz2pmRDdSfDZakf6gzCjLv3IioR%2BVNux3lVRLS%2FbPyD%2BJi502ZqBoIMhvg%3D%3D; ServerPool=X; PMC=V2*MS.30*MD.20200801*LD.20200801; TART=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; PAC=AJqxIMK5VMoQs3BYez76fiWqnRE1rPRWEyK5Kg2PmPwUiCUVVS9AO3KRJtvv_tvv1C5wi-IF0v3rgtdvsHte_1B8KOhWmt-6Ej0WcBsDbSCUpSj9J22n572UpGuHYuSorg%3D%3D; health_notice_dismissed=1; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpv%2C2%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CCrisisSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CRepTarMCSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7CTSMCPers%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CCOVIDMCSess%2C%2C-1%7CTARSWBPers%2C%2C-1%7CListMCSess%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7Cmdpers%2C1%2C1596871674%7CSPACMCSess%2C%2C-1%7Cmds%2C1596267201900%2C1596353601%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7CRevHubRMPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2CRuleBasedPopup%2C1596353274%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCrisisPers%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7CRepTarMCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CTSMCSess%2C%2C-1%7CSPMCPers%2C%2C-1%7CRevHubRMSess%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CCOVIDMCPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CSPACMCPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CListMCPers%2C%2C-1%7Cmdsess%2C-1%2C-1%7C; roybatty=TNI1625!AJyadj5RVnZNah4DgM2X5anohUOAnxcziQ2cNCLOsczG5YzlrPuVWMbk01Dv%2FTACgBk66bREsR5FGxziKM42tjoYtAQdkVezoJr5ij9hmxP4FiclKKDKbA7sMte%2Bbd0f%2BSBDcx%2FJQxdmNNETca%2BAyXKjyhn8GnrL8ydagf8DXwuQ%2C1; SRT=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; __vt=HxTl2PIYChv8-PokABQCq4R_VSrMTACwWFvfTfL3vw8LExjnakEKeRr5D38LyaiGHHLMsvFM06-UC_2G0gqlnkxyMdQkTj_C98wTYdULZ8im3LsVZRruns9H7Y_qGxs7SsxALSHFIOYL1QmM1773LpBjsw; TASession=%1%V2ID.9A53E4DA9B8FF660066B23DE9688140E*SQ.209*LS.DemandLoadAjax*GR.96*TCPAR.26*TBR.50*EXEX.16*ABTR.24*PHTB.24*FS.68*CPU.18*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.ABD562818D249697A8AB4E2FFBFCE092*FA.1*DF.0*TRA.true*LD.298277*EAU.%5B; TATravelInfo=V2*AY.2020*AM.8*AD.9*DY.2020*DM.8*DD.10*A.2*MG.-1*HP.2*FL.3*DSM.1596267436507*AZ.1*RS.1; TAUD=LA-1596265332138-1*RDD-1-2020_08_01*ARDD-960203-2020_09_30.2020_10_01*HD-1869770-2020_08_04.2020_10_01.298301*G-1869771-2.1.298301.*LD-2104113-2020.8.4.2020.10.1*LG-2104116-2.1.T.*HDD-2104117-2020_08_09.2020_08_10; TAReturnTo=%1%%2FHotels%3Fzfn%3D%26reqNum%3D1%26ns%3D%26isLastPoll%3Dfalse%26pop%3D%26g%3D298277%26bs%3D%26puid%3DXyUa3QokLIsAA6QLD%40wAAAAg%26distFrom%3D%26c%3D1%2C2%2C3%26catTag%3D9200%2C9212%2C9230%2C9235%2C9250%2C9256%2C9261%2C9672%2C16545%2C21371%2C21372%2C21373%26blender_tag%3D%26paramSeqId%3D9%26distFromPnt%3D%26offset%3D0%26changeSet%3DFILTERS%2CMAIN_META%26zfc%3D%26zfb%3D%26amen%3D%26zfd%3D%26trating%3D%26plSeed%3D898352206%26hsf%3D%26zff%3D%26waitTime%3D287'

urls = [
    # ('https://www.tripadvisor.com.my/Hotels-g298277-Johor-Hotels.html', 'Johor'),
    # ('https://www.tripadvisor.com.my/Hotels-g298281-Kedah-Hotels.html', 'Kedah'),
    # ('https://www.tripadvisor.com.my/Hotels-g298284-Kelantan-Hotels.html', 'Kelantan'),
    # ('https://www.tripadvisor.com.my/Hotels-g306997-Melaka_Central_Melaka_District_Melaka_State-Hotels.html', 'Melaka'),
    # ('https://www.tripadvisor.com.my/Hotels-g298289-Negeri_Sembilan-Hotels.html', 'Negeri_Sembilan'),
    # ('https://www.tripadvisor.com.my/Hotels-g298291-Pahang-Hotels.html', 'Pahang'),
    # ('https://www.tripadvisor.com.my/Hotels-g298297-Perak-Hotels.html', 'Perak'),
    # ('https://www.tripadvisor.com.my/Hotels-g298301-Perlis-Hotels.html', 'Perlis'),
    # ('https://www.tripadvisor.com.my/Hotels-g298306-Sabah-Hotels.html', 'Sabah'),
    # ('https://www.tripadvisor.com.my/Hotels-g298308-Sarawak-Hotels.html', 'Sarawak'),
    # ('https://www.tripadvisor.com.my/Hotels-g298310-Selangor-Hotels.html', 'Selangor'),
    # ('https://www.tripadvisor.com.my/Hotels-g298318-Terengganu-Hotels.html', 'Terengganu'),
    # ('https://www.tripadvisor.com.my/Hotels-g298570-Kuala_Lumpur_Wilayah_Persekutuan-Hotels.html', 'Kuala_Lumpur'),
    # ('https://www.tripadvisor.com.my/Hotels-g298286-Labuan_Island_Sabah-Hotels.html', 'Labuan'),
    # ('https://www.tripadvisor.com.my/Hotels-g298305-Putrajaya_Wilayah_Persekutuan-Hotels.html', 'Putrajaya'),
    ('https://www.tripadvisor.com.my/Hotels-g298302-Penang-Hotels.html', 'Penang')

]

uid_level_dict = {}


def get_page_no(html):
    if 'class="pageNumbers"' not in html:
        return 1
    page_reg = 'data-page-number="(.*?)"'

    data = re.compile(page_reg).findall(html)

    if data:
        return int(data[-1])


def request_sheet1(item):
    global sheet1_data
    url, state = item

    page_no = None
    i = 1

    hotel_reg = 'class="listing_title".*?href="(.*?)".*?>(.*?)<.*?info-col(.*?)prw_common_rating_and_review_count_with_popup(.*?)"ReviewCount">(.*?) revi'
    body = {
        'plSeed': '898352206',
        'reqNum': 1,
        'isLastPoll': 'false',
        'waitTime': 43,
        'catTag': '9193,9200,9212,9230,9235,9250,9256,9261,9469,9672,16545,21371,21372,21373',
        'changeSet': 'MAIN_META, PAGE_OFFSET',
        'puid': 'XyUa3QokLIsAA6QLD@wAAAAg',
        'cat': '1,2,3',
    }
    headers = {
        'x-puid': 'XyUa3QokLIsAA6QLD@wAAAAg',
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'text/html, */*',
    }

    while True:
        try:
            body['paramSeqId'] = i
            body['offset'] = (i - 1) * 30,

            html = post_request_html(url, cookie, data=body, add_header=headers)

            if not page_no:
                page_no = get_page_no(html)

            if (i + 1) > page_no:
                break

            data = re.compile(hotel_reg).findall(html)
            print i, page_no, state

            for item in data:
                hote_url = 'https://www.tripadvisor.com.my' + item[0]
                name = item[1]
                classification = get_classification(item[2])
                rating = global_rating_details(item[3])
                no_reviews = int(item[4].replace(',', ''))

                location, star = get_hotel_details(hote_url)
                one_row = [state, name, hote_url, no_reviews, rating, classification, star, location]
                sheet1_data.append(one_row)

            i += 1
        except Exception as e:
            print 'ERR---', url, i, e


def get_classification(ori):
    if 'class="label"' in ori:
        reg = 'class="label">(.*?)<'
        return re.compile(reg).findall(ori)[0]
    return 'HOTEL'


def global_rating_details(ori):
    if 'of 5 bubbles' in ori:
        reg = "alt='(.*?) of 5 bubbles'"
        data = re.compile(reg).findall(ori)
        return data[0]
    return 0


def get_hotel_details(url):
    html = get_request_html(url, cookie)
    location = 'N/A'
    if '_3ErVArsu jke2_wbp' in html:
        reg = '_3ErVArsu jke2_wbp">(.*?)<'
        location = re.compile(reg).findall(html)[0]

    star = 'N/A'
    star_css_score = {
        '_3jV1TJf9': 0.5,
        '_2cO8x-C-': 1.0,
        'SPwwulfU': 1.5,
        '_2MgVjxWG': 2.0,
        '_3ll0ja_Z': 2.5,
        '_3RprXHxE': 3.0,
        '_2JbAlMbb': 3.5,
        '_30WZSV_9': 4.0,
        '_2LYcDtDf': 4.5,
        'f33bWmtw': 5.0,
    }
    for k, v in star_css_score.items():
        if k in html:
            star = str(v)
            break
    if star == 'N/A':
        if 'class="_31OQP7s_' in html:
            reg = 'class="_31OQP7s_.*?aria-label="(.*?) '
            star = re.compile(reg).findall(html)[0]
    return location, star


def request_sheet2(row, number, hotel_url):
    global sheet2_data
    page_no = number / 5
    if number % 5 != 0:
        page_no += 1

    terminate = False
    for i in range(0, page_no):
        if terminate:
            break
        try:
            url = hotel_url.replace('-Reviews-', '-Reviews-or%s-' % str(i * 10))
            print page_no, i, row, url

            html = get_request_html(url, cookie)

            reg = 'ui_header_link _1r_My98y.*?>(.*?)<(.*?)ui_bubble_rating bubble_(.*?)".*?Date of .*?>(.*?)<'

            comment_list = re.compile(reg).findall(html)
            for comment in comment_list:
                name = comment[0]
                country = get_user_location(comment[1])
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
        date = datetime.strptime(ori, ' %B %Y')
        return date.strftime('1/%m/%Y')
    except:
        return ori


def get_user_location(ori):
    if 'ui_icon map-pin-fill _2kj8kWkW' in ori:
        reg = 'ui_icon map-pin-fill _2kj8kWkW">.*?>(.*?)<'
        data = re.compile(reg).findall(ori)
        return data[0]
    return 'N/A'


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def read_excel(filename, start=1):
    global R_ID, sheet2_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        main_url = row[2].value

        try:
            review_no = int(row[3].value)
            if review_no > 0:
                request_sheet2(i, review_no, main_url)
        except Exception as e:
            print main_url, e
    write_excel('Hotel_sheet2.xls', sheet2_data)


def step_1():
    for item in urls:
        request_sheet1(item)
        write_excel(item[1] + '_hotel.xls', sheet1_data)

reload(sys)
sys.setdefaultencoding('utf-8')
# step_1()
# read_excel('data/Penang_hotel1.xls')

if True:
    data = xlrd.open_workbook('data/Penang_hotel1.xls', encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(1, table.nrows):
        row = table.row(i)
        main_url = row[2].value

        try:
            _, star = get_hotel_details(main_url)
            print star
        except Exception as e:
            print main_url, e