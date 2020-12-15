# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
from scraping.utils import post_request_json, get_request_html, write_html, write_excel

saved_hotel = set()
R_ID = 1
sheet1_data = [['ID', 'Hotel URL', 'Hotel Name', 'Address', 'Rating', 'Number of reviews', 'Star', 'Amenities']]
sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Review Date' 'Rating', 'Text Review', 'Reviewer Location',
                'Contributor Level', 'Travel Style']]
sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]

cookie = 'TAUnique=%1%enc%3ASLqk%2B6khUnzArkIWpky3yAfBM5Uq3N0u36Bu3YaBBnSRqDIW%2BjDBvQ%3D%3D; TASSK=enc%3AAJV0znQAi190Y2FwWBbr%2FWkHmjUPreYrqWhcXgDHdP896aKkgasX%2FDbb3MqkDZqcNwAC2HmMBz2pmRDdSfDZakf6gzCjLv3IioR%2BVNux3lVRLS%2FbPyD%2BJi502ZqBoIMhvg%3D%3D; ServerPool=X; TART=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; BEPIN=%1%173ad2014fe%3Bweb225a.a.tripadvisor.com%3A30023%3B; TADCID=sQXR1Qrep2rrzJlGABQCjnFE8vTET66GHuEzPi7KfV9DztLy9S7pFTGdOJfzUz38qYLAmiLTKJCZ_---qz0eY0vOmgWIzpu1KOM; TAAUTHEAT=-1IuaWaZSkLbEnxfABQC5pMD6MhQQX22iUWVeLafiR8azr3ocsRAxPjiH7Sm-5xyUGmlv9kNagHMMlmEZz-3s7w14kU81TZGYS5vAC3c4nnA6Uj2iA-zD8UyAmb0St4RcoBCBrQvGKTh0wST3MqK9ErozzhF2Lb8XTS2euuhvHmQtAck7U1Hwr4HGkEx0ew5OX5nHysQhy0h8Rn3p4ThBVfi4g; PMC=V2*MS.30*MD.20200801*LD.20200805; PAC=ANYal4eOuB3QhQ1vzSX4wsmOg_lqY1Gn_rOiMBZKHsDZZh5DDZlyRAQdppbQO9MUNu2TRYIrC8zlWK_pG54jF3uYaAfRQ1RUG8fgSF5ajfEYZ00obxtTZZX4QpuD9QqNKbTe6-GxKHGkPq5KLCfBkC0NzbSFExksVCducEQvfal-yOq20ZB5sGCs7cVK56MsNBXqMiAXsZaJrIOq6ysJZX4nr07Cs-tiiUPVtrzRmQ8w; CM=%1%RestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7Csesstch15%2C%2C-1%7Cpv%2C16%2C-1%7CCYLPUSess%2C%2C-1%7Ctvsess%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CRepTarMCSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7CTSMCPers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7CCOVIDMCSess%2C%2C-1%7Csesshours%2C%2C-1%7CTARSWBPers%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7CSPACMCSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7Csesslaf%2C%2C-1%7CCYLPUPers%2C%2C-1%7CRevHubRMPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Cperslaf%2C%2C-1%7Csh%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCrisisPers%2C%2C-1%7CCCPers%2C%2C-1%7CRepTarMCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7Cperswifi%2C%2C-1%7CRevHubRMSess%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CSPACMCPers%2C%2C-1%7CTrayssess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7Cbooksticks%2C%2C-1%7CListMCPers%2C%2C-1%7Cbookstickp%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Csesswifi%2C%2C-1%7Ct4b-pc%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CCrisisSess%2C%2C-1%7CTBPers%2C%2C-1%7Cperstch15%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7Cpershours%2C%2C-1%7CPremiumORSess%2C%2C-1%7CRestAdsPers%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CTrayspers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CMCPPers%2C%2C-1%7CListMCSess%2C%2C-1%7CSPMCSess%2C%2C-1%7Cpers_rev%2C%2C-1%7Cmdpers%2C1%2C1596871674%7CRBAPers%2C%2C-1%7CHomeAPers%2C%2C-1%7CRCSess%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7Cpssamex%2C%2C-1%7CCYLPers%2C%2C-1%7Ctvpers%2C%2C-1%7CTBSess%2C%2C-1%7CTSMCSess%2C%2C-1%7CAdsRetSess%2C%2C-1%7CCOVIDMCPers%2C%2C-1%7CMCPSess%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7Cmdsess%2C-1%2C-1%7C; TATravelInfo=V2*AY.2020*AM.9*AD.30*DY.2020*DM.10*DD.1*A.2*MG.-1*HP.2*FL.3*DSM.1596622597266*AZ.1*RS.1; __vt=g3zWqS9oj9vqi6QPABQCq4R_VSrMTACwWFvfTfL3vw8iRnmGk2NfzdVpgwJ08sHp99oOLQ9TTAKiJ5-XCylZQTPqq8QPm70T4aH-_YklwEnamz2Ms5-hEU2BFVjUiEfSDcmC5DjbW7G7Y36cQNaSbs_JCg; TAReturnTo=%1%%2FAttractions-g306997-Activities-oa30-Melaka_Central_Melaka_District_Melaka_State.html; roybatty=TNI1625!ANjC88DZWFCYzQz5Bqk0QXiL1dRLHUGByYWd6lO%2Fjvw%2BNKKRvUO5Y%2Fk7AgY1vsgbtxBMvs447eAVs0%2BBUTxJxnu9L5EbPl5X4eWaYAb88CF8%2FEZ9uC8TR0O3Uh0ZrdQgT4aS3wTlxkqjdzXeFVrhN7iPZ2v4rQxo5anDEuSjoI2r%2C1; SRT=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; TASession=%1%V2ID.9A53E4DA9B8FF660066B23DE9688140E*SQ.771*LS.DemandLoadAjax*GR.96*TCPAR.26*TBR.50*EXEX.16*ABTR.24*PHTB.24*FS.68*CPU.18*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.ABD562818D249697A8AB4E2FFBFCE092*LF.en*FA.1*DF.0*FLO.298277*TRA.false*LD.306997*EAU.%5B; TAUD=LA-1596265332138-1*RDD-1-2020_08_01*ARDD-960203-2020_09_30.2020_10_01*HD-6893344-2020_08_04.2020_10_01.298305*G-6893345-2.1.298305.*HC-356610453*HDD-357271503-2020_09_30.2020_10_01.1*LD-358348293-2020.9.30.2020.10.1*LG-358348296-2.1.T.'

urls = [
    # ('https://www.tripadvisor.com.my/Attractions-g306997-Activities-Melaka_Central_Melaka_District_Melaka_State.html',
    #     'Melaka'),
    # ('https://www.tripadvisor.com.my/Attractions-g298277-Activities-Johor.html', 'Johor'),
    # ('https://www.tripadvisor.com.my/Attractions-g298281-Activities-Kedah.html', 'Kedah'),
    # ('https://www.tripadvisor.com.my/Attractions-g298284-Activities-Kelantan.html', 'Kelantan'),
    # ('https://www.tripadvisor.com.my/Attractions-g298289-Activities-Negeri_Sembilan.html', 'Negeri_Sembilan'),
    # ('https://www.tripadvisor.com.my/Attractions-g298291-Activities-Pahang.html', 'Pahang'),
    # ('https://www.tripadvisor.com.my/Attractions-g298297-Activities-Perak.html', 'Perak'),
    # ('https://www.tripadvisor.com.my/Attractions-g298301-Activities-Perlis.html', 'Perlis'),
    # ('https://www.tripadvisor.com.my/Attractions-g298306-Activities-Sabah.html', 'Sabah'),
    # ('https://www.tripadvisor.com.my/Attractions-g298308-Activities-Sarawak.html', 'Sarawak'),
    # ('https://www.tripadvisor.com.my/Attractions-g298310-Activities-Selangor.html', 'Selangor'),
    # ('https://www.tripadvisor.com.my/Attractions-g298318-Activities-Terengganu.html', 'Terengganu'),
    # ('https://www.tripadvisor.com.my/Attractions-g298570-Activities-Kuala_Lumpur_Wilayah_Persekutuan.html',
    #  'Kuala_Lumpur'),
    # ('https://www.tripadvisor.com.my/Attractions-g298286-Activities-Labuan_Island_Sabah.html', 'Labuan'),
    # ('https://www.tripadvisor.com.my/Attractions-g298305-Activities-Putrajaya_Wilayah_Persekutuan.html',
    #  'Putrajaya'),
    ('https://www.tripadvisor.com.my/Attractions-g298302-Activities-Penang.html', 'Penang'),
]

special_set = {'Kuala_Lumpur', 'Melaka'}

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
    html = get_request_html(url, cookie)

    reg = 'attractionInformation.*?name\\\\":\\\\"(.*?)\\\\.*?count\\\\":(.*?),\\\\"rating\\\\":(.*?)\}.*?Attraction_Review(.*?)html.*?label\\\\":\\\\"(.*?)\\\\'

    page_reg = 'pageLink.*?Attractions(.*?)html'

    page_list = re.compile(page_reg).findall(html)

    data_list = re.compile(reg).findall(html)

    print 1, state

    for data in data_list:
        name = data[0]
        no_review = data[1]
        rating = data[2]
        attr_url = 'https://www.tripadvisor.com.my/Attraction_Review' + data[3] + 'html'
        classification = data[4]
        location = get_location(attr_url)

        one_row = [state, name, attr_url, no_review, rating, classification, location]
        sheet1_data.append(one_row)

    i = 2
    if state in special_set:
        for page in page_list[2:]:

            print 'special', i, state

            url = 'https://www.tripadvisor.com.my/Attractions' + page + 'html'

            html = get_request_html(url, cookie)

            reg = 'class="_21qUqkJx">(.*?)<.*?href="(.*?)".*?<h2>(.*?)<(.*?)_2jOg7aGD'
            data = re.compile(reg).findall(html)

            for item in data:
                classification = item[0]
                attr_url = 'https://www.tripadvisor.com.my' + item[1]
                name = item[2].replace('amp;', '')

                rating, no_review = get_review(item[3])
                location = get_location(attr_url)

                one_row = [state, name, attr_url, no_review, rating, classification, location]
                sheet1_data.append(one_row)
            i += 1


def get_location(url):
    html = get_request_html(url, cookie)
    reg = '"fullAddress":"(.*?)"'
    if '"fullAddress":"' in html:
        return re.compile(reg).findall(html)[0]
    return 'N/A'


def get_review(ori):
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

    rating = 'N/A'
    no_review = 0

    if 'review' in ori:
        for k, v in star_css_score.items():
            if k in ori:
                rating = str(v)
                break
        review_Reg = 'class="_82HNRypW".*?>(.*?)<'
        no_review = re.compile(review_Reg).findall(ori)[0]
    return no_review, rating


def request_sheet2(number, hotel_url):
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
            print page_no, i, url

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


def get_date(ori):
    d = datetime.strptime(ori, '%a %b %d, %Y %I:%M %p')
    date = d.strftime('%d/%m/%Y')
    return date, d.weekday() + 1


def read_excel(filename, start=1):
    global R_ID, sheet2_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        main_url = row[2].value

        try:
            review_no = int(row[3].value.replace(',', ''))
            if review_no > 0:
                request_sheet2(review_no, main_url)
        except Exception as e:
            print main_url, e
    write_excel('Things_sheet2.xls', sheet2_data)


def step_1():
    for item in urls:
        request_sheet1(item)
        write_excel(item[1] + '_things.xls', sheet1_data)


reload(sys)
sys.setdefaultencoding('utf-8')
# step_1()
read_excel('data/Penang_things.xls')
