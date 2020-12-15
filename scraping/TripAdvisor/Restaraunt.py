# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import xlrd
import sys
from datetime import datetime
import HTMLParser
import os
import requests
from scraping.utils import timeout

base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'

sheet0_data = [[]]
sheet1_data = [['ID', 'Name', 'Rest. Url', 'website url', 'address', 'cuisine', 'price range', 'pricing', 'can reserve', 'special diet', 'Number of reviews', 'Rating', 'Rank', 'Food rating', 'Service rating', 'Value rating', 'Traveller type', 'Excellent', 'V. good', 'Avg', 'Poor', 'Terrible']]
sheet2_data = [['ID', 'Rest. Url', 'Reviewer name', 'reviewer country', 'rating', 'comment date', 'Contributor level', 'Excellent', 'V. good', 'Avg', 'Poor', 'Terrible', 'Headline', 'Review text']]
sheet3_data = [['UID', 'restaurant url', 'restaurant name', 'rating', 'restaurant address', 'restaurant country']]
R_ID = 1

url_bases = [
    # 'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298184&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
    # 'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298566&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
    # 'https://www.tripadvisor.com.my/RestaurantSearch?Action=PAGE&geo=298570&ajax=1&cat=10346&itags=10591&sortOrder=popularity&availSearchEnabled=false&o=a%s',
    # 'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298112&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
    'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=294262&ajax=1&sortOrder=relevance&o=a%s&availSearchEnabled=false&pid=8',
]

error_url = [
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d878178-Reviews-Hai_Tien_Lo-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d2538710-Reviews-Tandoori_Culture-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d3359846-Reviews-KENG_ENG_KEE_SEAFOOD-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d15086890-Reviews-Rizu-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d3855842-Reviews-Din_Tai_Fung-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d3543833-Reviews-Tiong_Bahru_Bakery-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d17171783-Reviews-Fu_Lin_Men_Seafood_NSRCC-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d817015-Reviews-StraitsKitchen-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d1863524-Reviews-Stellar_at_1_Altitude-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d5429851-Reviews-Common_Man_Coffee_Roasters-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d3194658-Reviews-Nylon_Coffee_Roasters-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d4007798-Reviews-Lime_Restaurant-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d3383759-Reviews-Arteastiq_Boutique_Tea_House-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d941652-Reviews-RAS_The_Essence_of_India-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d2459079-Reviews-Luke_s_Oyster_Bar_Chop_House-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d4079480-Reviews-Wine_Connection_Cheese_Bar-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d14923574-Reviews-Papi_s_Tacos_Singapore-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d1466538-Reviews-Basilico-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d13075207-Reviews-Merci_Marcel-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d13322650-Reviews-The_Dim_Sum_Place-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d1937704-Reviews-CE_LA_VI_Restaurant-Singapore.html',
    'https://www.tripadvisor.com.my/Restaurant_Review-g294265-d2338744-Reviews-The_Lobby_Lounge_at_InterContinental_Singapore-Singapore.html',
]

key_prefixs = [
    # 'Tokyo_',
    # 'Osaka_',
    'Kyoto_',
    'Gifu_',
    'Nagoya_',
]

cookie = 'TADCID=c2bevLVd4OPVw503ABQCjnFE8vTET66GHuEzPi7KfV8tUou66XdIemKmPKfsCPHQfdv4PInKBM8C97eUZrB6Eqeg3IC34pkFTk8; TAAUTHEAT=SauzFQK9qlqNoDiJABQC5pMD6MhQQX22iUWVeLafiR8EUuGQddQ1WIBUET49l7qV_Jr2uIAf3avgX9lHkuxKj-oW9jOdB5kLy_cOJxLD6Nr5FCxY13i-Y3wH1LxBaeHNiHxJEyh3nPVmlYixDfdqjmWVa-IxIRulyacayIDETTWZQ4TwH-zNWtg2ShTeQfPMseEyhzdm7wkisMyW-VFChGEFRg; TAUnique=%1%enc%3ASLqk%2B6khUnzArkIWpky3yAfBM5Uq3N0u36Bu3YaBBnSRqDIW%2BjDBvQ%3D%3D; TASSK=enc%3AAJV0znQAi190Y2FwWBbr%2FWkHmjUPreYrqWhcXgDHdP896aKkgasX%2FDbb3MqkDZqcNwAC2HmMBz2pmRDdSfDZakf6gzCjLv3IioR%2BVNux3lVRLS%2FbPyD%2BJi502ZqBoIMhvg%3D%3D; ServerPool=X; PMC=V2*MS.30*MD.20200801*LD.20200801; TART=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; health_notice_dismissed=1; PAC=ABv6OOeS5Ee3a8SVtxpWuywMbX9HaE0CCm1BY822rlizMqmO8TT2FRPFXbU1qm-9I5c7DUz1YCOzILGUo2MkIXbHmGYpeIc4AJ1Uk5lSQeMMNKrlAXDGKsF4mQEOnUDpI6P23lIdxYz3oKv53H656cf19g9MQ5TDI6aMAJCzBYJYHlf5R_-BFAUuNRyMPRA9XO_JGx_BDOOf_4RGCARcA-Q%3D; BEPIN=%1%173ad2014fe%3Bweb225a.a.tripadvisor.com%3A30023%3B; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*DSM.1596337427798*AZ.1*RS.1; TAReturnTo=%1%%2FRestaurants-g298278-Johor_Bahru_Johor_Bahru_District_Johor.html; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpv%2C16%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CCrisisSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CRepTarMCSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7CTSMCPers%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CCOVIDMCSess%2C%2C-1%7CTARSWBPers%2C%2C-1%7CListMCSess%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7Cmdpers%2C1%2C1596871674%7CSPACMCSess%2C%2C-1%7Cmds%2C1596272225474%2C1596358625%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7CRevHubRMPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2CRuleBasedPopup%2C1596353274%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCrisisPers%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7CRepTarMCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CTSMCSess%2C%2C-1%7CSPMCPers%2C%2C-1%7CRevHubRMSess%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CCOVIDMCPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CSPACMCPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CListMCPers%2C%2C-1%7Cmdsess%2C-1%2C-1%7C; roybatty=TNI1625!AGKOA7ERJVU7MFIRtmQ36dAA3J1RqClu4xiildbM060ZLEXkSniJQkOh6%2B7dez2kX5scVAxSZ9eHt5g0X6wP1ObIKWhAmmIoS6MpzCxZKdhEb5aXQavTW48h7gs2KZXRaACbRf%2B52vYGNP3sdUqQur%2FbHLQuYfwemFEjWE1c9JVs%2C1; SRT=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; TASession=%1%V2ID.9A53E4DA9B8FF660066B23DE9688140E*SQ.448*LS.DemandLoadAjax*GR.96*TCPAR.26*TBR.50*EXEX.16*ABTR.24*PHTB.24*FS.68*CPU.18*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.ABD562818D249697A8AB4E2FFBFCE092*FA.1*DF.0*FLO.298277*TRA.true*LD.298278*EAU.%5B; TAUD=LA-1596265332138-1*RDD-1-2020_08_01*ARDD-960203-2020_09_30.2020_10_01*HD-6893344-2020_08_04.2020_10_01.298305*G-6893345-2.1.298305.*HDD-72095550-2020_08_09.2020_08_10.1*HC-73283048*LG-74403033-2.1.T.*LD-74403034-.....; __vt=Cr9Fra_v50R54_kdABQCq4R_VSrMTACwWFvfTfL3vw8Pzezx-H80FBxArsRn2vJ5W2ruoQunhAToL2AXq1Bno67lxGmg5BD-SMgDKCSY7_X-dWs7LWPjxlrEXsqgmtGCHYo4CYBtA6NgoFlvnvqNNY_gvA'

uid_level_dict = {}
user_url_set = set()


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


def request_sheet0(url, key_prefix):
    print key_prefix + 'level1--'+url
    global sheet1_data, R_ID
    # link, name, replies, views
    raw_reg = 'restaurants-list-ListCell__nameBlock--1hL7F.*?href="(.*?)".*?>(.*?)<.*?restaurants-list-ListCell__infoRowElement--2E6E3.*?restaurants-list-ListCell__infoRowElement--2E6E3.*?restaurants-list-ListCell__infoRowElement--2E6E3.*?restaurants-list-ListCell__infoRowElement--2E6E3">(.*?)<.*?restaurants-list-components-ReviewSnippets__snippetWrapper--2M8Bw(.*?)</div></div><div(.*?)</div></div><div></div></div>'
    try:
        html = get_request(url)
    except Exception as e:
        print 'ERR---level 1---' + url, e
        return
    topic_body = re.compile(raw_reg).findall(html)
    if not topic_body:
        return
    for detail in topic_body:
        link = ''
        try:
            id = key_prefix+str(R_ID)
            link = 'https://www.tripadvisor.com.sg' + detail[0]
            name = detail[1]
            pricing = detail[2]

            is_reserved = 'YES'
            if 'Reserve' not in detail[4]:
                is_reserved = 'NO'

            request_sheet1(id, name, link, pricing, is_reserved)

            R_ID += 1
        except Exception as e:
            print 'ERR---level 1---', link, e


def request_sheet1(R_ID, name, url, pricing, is_reserved):
    # link, name, replies, views
    try:
        html = get_request(url)
        process_html(R_ID, name, html, url, pricing, is_reserved)
    except Exception as e:
        print 'ERR---level 1---' + url, e
        return


@timeout(2)
def process_html(R_ID, name, html, url, overall_pricing, is_reserved):
    global sheet1_data
    raw_reg = 'class="rating(.*?)popInde.*?RATINGS_INFO.*?span.*?>(.*?)<.*?header_links">(.*?)</div.*?onAddressClicked.*?<span class="detail ">(.*?)</div.*?restaurants-detail-overview-cards-DetailOverviewCards__wrapperDiv--1Dfhf(.*?)restaurants-detail-overview-cards-DetailOverviewCards__cardColumn--1BmXT(.*?)restaurants-detail-overview-cards-DetailOverviewCards__cardColumn--1BmXT.*?taplc_detail_filters_rr_resp_0(.*?)noncollapsible'

    topic_body = re.compile(raw_reg).findall(html)
    if topic_body:
        try:
            avg_rating, review_number = get_ratings(topic_body[0][0])
            rank = topic_body[0][1].replace('#', '').replace(',', '')
            cuisine = get_cuisine(topic_body[0][2])
            address = remove_html_tag(topic_body[0][3])
            food_rating, service_rating, value_rating = get_detail_rating(topic_body[0][4])
            price, special_diet = get_details(topic_body[0][5])
            excellent, v_good, avg, poor, terrible = get_comment_no(topic_body[0][6])

            website = get_website(html)
            eng_comment_no = get_eng_comment_no(html)

            one_row = [R_ID, name, url, website, address, cuisine, price, overall_pricing, is_reserved, special_diet, review_number, avg_rating, rank,
                       food_rating, service_rating, value_rating, 'N/A', excellent, v_good, avg, poor, terrible,
                       eng_comment_no]
            print one_row
            sheet1_data.append(one_row)

        except Exception as e:
            print 'ERR---level 1---', url, e


def get_website(ori):
    if '"website":"http' in ori:
        return 'http' + re.compile('"website":"http(.*?)"').findall(ori)[0]
    return 'N/A'


def get_detail_rating(ori):
    reg = 'restaurants-detail-overview-cards-RatingsOverviewCard__ratingText.*?>(.*?)<.*?ui_bubble_rating bubble_(.*?)"'

    items = re.compile(reg).findall(ori)

    res = ['N/A', 'N/A', 'N/A']

    for item in items:
        if item[0] == 'Food':
            res[0] = str(float(item[1]) / 10)
        if item[0] == 'Service':
            res[1] = str(float(item[1]) / 10)
        if item[0] == 'Value':
            res[2] = str(float(item[1]) / 10)

    return res


def get_details(ori):
    reg = 'restaurants-detail-overview-cards-DetailsSectionOverviewCard__categoryTitle.*?>(.*?)<.*?restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText.*?>(.*?)<'
    items = re.compile(reg).findall(ori)

    res = ['N/A', 'N/A']

    for item in items:
        if item[0] == 'PRICE RANGE':
            res[0] = item[1].replace('\xc2\xa5', 'Y ')
        if item[0] == 'Special Diets':
            res[1] = item[1]
    return res


def get_comment_no(ori):
    reg = '"filters_detail_checkbox_trating_.*?row_num.*?>(.*?)<'
    items = re.compile(reg).findall(ori)

    if items:
        return items[0:5]
    return ['N/A' for i in range(5)]


def get_comment_date(ori):
    try:
        date = datetime.strptime(ori, '%d %B %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def request_sheet2(hotel_id, number, hotel_url, index):
    global sheet2_data, sheet3_data
    if number > 50:
        number = 50
    for i in range(0, number):
        try:
            url = hotel_url.replace('-Reviews-', '-Reviews-or%s-' % str(i*10))
            html = get_request(url)
            print 'sheet2-- of ', hotel_id, number, i
            reg = '"review_(.*?)".*?avatar profile_(.*?)".*?usernameClick.*?div>(.*?)<.*?ui_bubble_rating bubble_(.*?)".*?title=\'(.*?)\'.*?noQuotes\'>(.*?)<'

            comment_list = re.compile(reg).findall(html)
            comment_ids = []
            comment_id_data = {}
            for comment in comment_list:
                comment_ids.append(comment[0])
                comment_id_data[comment[0]] = [comment[0], comment[1], comment[2], comment[3], comment[4], comment[5]]
            # comment_details = get_comment_detail(comment_ids)
            comment_details = {}
            for k, v in comment_id_data.items():
                uid = v[1]
                name = v[2]
                rating = v[3][0]
                comment_date = v[4]
                title = remove_html_tag(v[5])
                comment_detail = comment_details.get(k, '-')
                level, user_url, location, no_review, no_helpful, travel_style, excellent, v_good, avg, poor, terrible = get_level_of_uid(uid)
                # [['ID', 'Rest. Url', 'Reviewer name', 'reviewer country', 'rating', 'comment date', 'Contributor level', 'Excellent', 'V. good', 'Avg', 'Poor', 'Terrible', 'Headline', 'Review text']]
                one_row = [hotel_id, hotel_url, name, location.replace('From ', ''), rating, get_comment_date(comment_date), level, travel_style, excellent, v_good, avg, poor, terrible, title, comment_detail]
                # print one_row
                sheet2_data.append(one_row)
                # if user_url not in user_url_set:
                #     sheet3_data.append([uid, user_url])
                #     user_url_set.add(user_url)
        except Exception as e:
            print('ERROR-sheet2-', hotel_id, i, e)


def get_user_location(ori):
    if 'strong' in ori:
        reg = 'strong>(.*?)<'
        data = re.compile(reg).findall(ori)
        return data[0]
    return ''


def get_comment_detail(ids):
    url = 'https://www.tripadvisor.com.sg/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP'
    data = {
        'reviews': ','.join(ids),
        'contextChoice': 'DETAIL_HR'
    }
    html = post_request(url, data)
    reg = 'reviewListingId="(.*?)".*?partial_entry">(.*?)<'
    comment_detail_list = re.compile(reg).findall(html)
    detail_dict = {}
    for comment_detail in comment_detail_list:
        detail_dict[comment_detail[0]] = remove_html_tag(comment_detail[1].replace('&amp;', '&').replace('&quot;', '"'))
    return detail_dict


def post_request(url, data):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': base_url,
        'Cookie': cookie,
    }
    resp = requests.post(url, data=data, headers=headers)
    return resp.content.replace('\n', '').replace('\r', '')


def get_level_of_uid(uid):
    if uid_level_dict.get(uid):
        return uid_level_dict.get(uid)
    html = get_request('https://www.tripadvisor.com.sg/MemberOverlay?uid=' + uid)
    reg = 'href="(.*?)"(.*?)memberdescriptionReviewEnhancements(.*?)countsReviewEnhancements(.*?)</ul.*?<div class="wrap(.*?)$'
    data = re.compile(reg).findall(html)
    if not data:
        return 0, '', 'N/A', 0, 0, 'N/A'
    user_url = 'https://www.tripadvisor.com.sg' + data[0][0]
    level = get_level(data[0][1])
    location = get_reviewer_location(data[0][2]).split('from ')[-1]
    no_review, no_helpful = get_review_helpful(data[0][3])
    travel_style = get_travel_style(data[0][4])
    rating = get_user_rating(data[0][4])
    res = [level, user_url, location, no_review, no_helpful, travel_style] + rating
    uid_level_dict[uid] = res
    return res


def get_user_rating(ori):
    reg = 'rowCellReviewEnhancements">(.*?)<'

    data = re.compile(reg).findall(ori)

    if data:
        return [data[i] for i in range(len(data)) if i % 3 == 2]
    return ['N/A', 'N/A', 'N/A', 'N/A', 'N/A']


def get_level(ori):
    if 'Level' in ori:
        reg = 'Level <.*?>(.*?)<'
        return re.compile(reg).findall(ori)[0]
    return 'N/A'


def get_reviewer_location(ori):
    reg = '<li>(.*?)<'
    data = re.compile(reg).findall(ori)
    if len(data) < 2:
        return 'N/A'
    return data[1]


def get_review_helpful(ori):
    reg = 'badgeTextReviewEnhancements">(.*?) (.*?)<'
    data_list = re.compile(reg).findall(ori)
    no_review = no_helpful = 0
    for data in data_list:
        if 'Contributions' in data[1]:
            no_review = data[0]
        elif 'Helpful' in data[1]:
            no_helpful = data[0]
    return no_review, no_helpful


def get_travel_style(ori):
    if 'memberTagsReviewEnhancements' not in ori:
        return 'N/A'
    reg = 'class="memberTagReviewEnhancements">(.*?)<'
    return ','.join(re.compile(reg).findall(ori))


def get_user_info(ori):
    user_reg = 'username mo"><span.*?>(.*?)<.*?"location">(.*?)<.*?class="memberBadging(.*)<div '
    level_reg = 'levelBadge badge lvl_(.*?)"'
    if 'username mo' in ori and 'location in ori':
        detail = re.compile(user_reg).findall(ori)[0]
        contri_name = detail[0]
        contri_location = 'N/A'
        if '' != detail[1]:
            contri_location = detail[1]
        contri_country = contri_location.split(',')[-1]
        contri_level = 'N/A'
        if 'levelBadge badge' in detail[2]:
            contri_level = int(re.compile(level_reg).findall(detail[2])[0])
        return [contri_name, contri_location, contri_country, contri_level]
    else:
        return ['N/A' for i in range(4)]


def get_review_detail(url_prefix, ori_url, review_ids):
    reviews = ','.join(review_ids)
    url = url_prefix+'?target='+str(review_ids[0])+'&context=1&servlet=Restaurant_Review&expand=1&reviews='+reviews
    reg = '<div class="entry">(.*?)</div>(.*?)class="note"'
    try:
        html = get_request(url)
    except:
        print 'EXC---'+url
        return [0 for i in range(4)]
    details = re.compile(reg).findall(html)
    res = []
    for detail in details:
        value = 0
        service = 0
        food = 0
        text = remove_html_tag(detail[0])
        if 'rate sprite-rating_ss rating_ss' in detail[1]:
            rating_reg = 'rate sprite-rating_ss rating_ss.*?alt="(.*?) of 5 bubbles.*?class="recommend-description">(.*?)<'
            ratings = re.compile(rating_reg).findall(detail[1])
            for rating in ratings:
                if rating[1] == 'Value':
                    value = rating[0]
                elif rating[1] == 'Service':
                    service = rating[0]
                elif rating[1] == 'Food':
                    food = rating[0]
        res.append([text, int(value), int(service), int(food)])
    return res


def get_review_date(ori):
    if 'relativeDate' in ori:
        date_reg = 'relativeDate.*?title=\'(.*?)\''
        date = re.compile(date_reg).findall(ori)[0]
    elif 'Reviewed' in ori:
        date = ori.split('Reviewed ')[-1]
    else:
        date = 'N/A'
    d = datetime.strptime(date, '%d %B %Y')
    date = d.strftime('%d/%m/%Y')
    return date


def get_rest_detail_and_comment_page(link):
    html = get_request(link)
    reg = 'tagsContainer"(.*?)restaurantDescription.*?map-pin-fill">(.*?)</div.*?atf_commerce_and_photos(.*)id="btf_wrap"'
    data = re.compile(reg).findall(html)[0]
    pricing, types = get_types(data[0])
    location = remove_html_tag(data[1])
    deliver = get_deliver(data[2])
    eng_comment_no = get_eng_comment_no(html)
    return location, eng_comment_no, types, deliver, pricing


def get_types(ori):
    reg = 'href=.*?>(.*?)<'
    data = re.compile(reg).findall(ori)
    return data[0], data[1:]


def get_deliver(ori):
    if 'restaurants-detail-commerce-DetailCommerce__logo_region--2Im4c' not in ori:
        return 'N/A'

    reg = 'restaurants-detail-commerce-DetailCommerce__logo_region--2Im4c(.*?)/div'
    data = re.compile(reg).findall(ori)

    if 'foodpanda' in data[0]:
        return 'Food Panda'
    if 'Eatigo' in data[0]:
        return 'Eatigo'
    if 'TABLEAPP' in data[0]:
        return 'TABLEAPP'
    if 'https://static.tacdn.com/img2/eateries/Logo_horizontal_RGB-1000x232.png' in data[0]:
        return 'OpenTable'
    return data[0]


def remove_html_tag(ori):
    try:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', ori)
        return str(HTMLParser.HTMLParser().unescape(dd))
    except Exception as e:
        print ori, e
        return ori


def get_eng_comment_no(ori):
    if '"pagination-details"' in ori:
        reg = '"pagination-details".*?of <.*?>(.*?)<'
        no = int(re.compile(reg).findall(ori)[0].replace(',', ''))
        res = no / 10
        if no % 10 != 0:
            res += 1
        return res
    return 1


def get_feature_good_for(ori):
    reg = 'title">(.*?)<.*?content">(.*?)<'
    data_list = re.compile(reg).findall(ori)
    feature = good_for = 'N/A'
    for data in data_list:
        if data[0] == 'Restaurant features':
            feature = remove_html_tag(data[1])
        elif data[0] == 'Good for':
            good_for = remove_html_tag(data[1])
    return feature, good_for


def get_cuisine(ori):
    reg = 'href=.*?>(.*?)<'
    datas = re.compile(reg).findall(ori)
    if datas:
        return ','.join(datas[1:])
    return 'N/A'


def get_ratings(ori):
    if 'of 5 bubbles' in ori:
        reg = 'alt=\'(.*?) .*?reviewCount">(.*?) '
        entry = re.compile(reg).findall(ori)[0]
        return entry[0], entry[1]
    return 0, 0


def get_rank_bali(ori):
    if 'popIndex popIndexDefault' in ori:
        reg = 'popIndex popIndexDefault">(.*?) of'
        return re.compile(reg).findall(ori)[0].replace('#', '').replace(',', '')
    return 'N/A'


def get_location(ori):
    if 'class="parentName"' in ori:
        reg = 'class="parentName">\((.*?)\)<'
        return re.compile(reg).findall(ori)[0]
    return 'N/A'


def get_date(ori):
    d = datetime.strptime(ori, '%a %b %d, %Y %I:%M %p')
    date = d.strftime('%d/%m/%Y')
    return date, d.weekday() + 1


def get_request(get_url, timeout=10):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.tripadvisor.com.sg/Restaurants-g294226-Bali.html')
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=timeout)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


def request_1_2():
    global sheet1_data, sheet2_data, sheet3_data, R_ID
    for i in range(len(url_bases)):
        sizes = [12, 2, 12]
        size = sizes[i]
        url_base = url_bases[i]
        key_prefix = key_prefixs[i]
        for i in range(size):
            print key_prefix + '-----Level 1 Page ' + str(i) + '-----'
            url = url_base % str(i*30)
            request_sheet1(url, key_prefix)
        write_excel('data/sheet1.xls'.replace('sheet', key_prefix), sheet1_data)
        write_excel('data/sheet2.xls'.replace('sheet', key_prefix), sheet2_data)
        write_excel('data/sheet3.xls'.replace('sheet', key_prefix), sheet3_data)
        del sheet2_data
        del sheet1_data
        del sheet3_data
        sheet1_data = [['ID', 'Name', 'Location', 'Overall rating', 'Rank all Bali', 'Number of reviews', 'Cuisine', 'Reserve Online', 'Excellent', 'Very good', 'Average', 'Poor', 'Terrible', 'Families', 'Couples', 'Solo', 'Business', 'Friends', 'Mar-May', 'Jun-Aug', 'Sep-Nov', 'Dec-Feb']]
        sheet2_data = [['ID', 'Contributor Name', 'Contributor Location', 'Contributor country', 'Contributor level', 'Review headline', 'rating', 'Review date', 'Review text', 'Reviewer Value', 'Reviewer Service', 'Reviewer Food']]
        sheet3_data = [['UID', 'restaurant url', 'restaurant name', 'rating', 'restaurant address', 'restaurant country']]
        R_ID = 1


def read_excel(filename, start=1):
    global R_ID, sheet2_data, sheet3_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    i = start
    while i < table.nrows:
        row = table.row(i)
        try:
            main_url = row[2].value
            id = row[0].value
            comment_no = int(row[20].value)
            request_sheet2(id, comment_no, main_url, i)
            i += 1
        except Exception as e:
            print i, e

        if i % 30 == 0:
            write_excel('sheet2_%d.xls' % i, sheet2_data)

    write_excel('sheet2_end.xls', sheet2_data)


def request_pricing(url):
    res = get_rest_detail_and_comment_page(url)
    return res[-1]


def get_name_from_url(url):
    return url.split('-')[-2].replace('_', ' ')


def get_sheet1():
    global sheet1_data
    for i in range(0, 12):
        request_sheet0(url_bases[0] % str(i*30), 'TR_')

        if (i+1) % 20 == 0:
            write_excel('data/sheet1_%d.xls' % i, sheet1_data)
            del sheet1_data
            sheet1_data = []

    write_excel('data/sheet1_end.xls', sheet1_data)


def do_retry():
    global R_ID
    for url in error_url:
        try:
            if 'RestaurantSearch' in url:
                request_sheet0(url, 'TR_')
            else:
                name = get_name_from_url(url)
                request_sheet1('TR_' + str(R_ID), name, url)
                R_ID += 1
        except Exception as e:
            print 'err-', url, e
    write_excel('data/sheet1_retry.xls', sheet1_data)

# read_excel('data/sheet1_end.xls')
write(get_request('https://www.tripadvisor.com.my/RestaurantSearch?Action=PAGE&ajax=1&availSearchEnabled=false&sortOrder=popularity&geo=298278&itags=10591&o=a30'), '1.html')