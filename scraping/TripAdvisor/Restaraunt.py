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

cookie = 'TAUnique=%1%enc%3As%2BYXT9FjuYfX4GCNWewjScq5nXQZFLzt1xVuzcww%2BTU%3D; TASSK=enc%3AALjC%2FTpEb5QPFAizzhNQ5wfKEqpfXmk5zqhq1DqovLNNV%2BV1%2FBsNpuXTA%2FszMd%2FL3IqC3Mx8vfDNl%2F7VyKc2InqLThwMKanbY8LiCF01%2BzVtWCVKwgvZcHCYJofOk7VyVg%3D%3D; TAAuth3=3%3A48fc7124816b1162f720832116be3cd3%3AAEIiA6UU5DE3cuneh0Uh%2BOfhijHyTA3qq%2F2uhdP2CAdnHfqa4g5nDJQhQLbRtLjeZtnU%2BEsbdnsezQD6j3KY6zrMwVDDXVgVD8XF99eey570yOdTwLW0OtDqeyDyT6djl%2Bw2b1LX85ouJntLld82ksQOw4bkjk4BCesEGIcWAXLKjm3tD641LjQ94%2Bk3mr%2Bvww%3D%3D; TADCID=iALg6oKA3Um0Vf8VABQC5UI2n8iqRdCoS-RMXjJFU1oxu7TSCnd4L6zCEt6Vd6jUld5h0KOTYkzVYCRt9bzAuyh3KXXhpKgY43s; ServerPool=X; PAC=APLcU8DEj3w9FUJS3Mc9APnjMYaqqw6oYGuB7DMedMBt5uJlIaGPh_U9RyoMqA1dUkMiIO5zJd8Sg8CSFbOc-KZmq7-k-cL8lYHx9ICXzGV0NxqTHomncgvZZgyrzmOBOuBnrgiozMOvIRSHLivmm627WQ4xj2B8VdVSdMD5R5gj; PMC=V2*MS.30*MD.20191206*LD.20191219; __vt=Z7_sgiy-tpT1RxzLABQCKh0bQ-d8T96qptG7UVr_ZQoYUOAEqqlSimmsj1PHxm5nD83rQq2ryNBRNEQFQQj6ogmWFaKy0CGTqEKIyMC5kC3iHuiczONIVp_KTVzeufe92TidJ54Hmg06qiSDGZQptqIElA; TART=%1%enc%3A1%2BBgjVnsI0mOfiZVJBN4AJDxyzL119NfgmJY4Xf%2BxOw91DO8OUyF1di5omuSPkL4Nox8JbUSTxk%3D; TAReturnTo=%1%%2FRestaurant_Review-g294265-d3856071-Reviews-Wine_Universe_Restaurant_Tapas_Bar-Singapore.html; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*DSM.1576052738656*RS.1*RY.2019*RM.12*RD.19*RH.20*RG.2; roybatty=TNI1625!AAooajk%2FgexqBbXQZNAN%2B7G6bon8oAvRuHLLgGK%2BeGNr9cfykstJrlVg1mqadAO3Oasb0R7KxRZlW36LUD6jB%2FVZQJCUc%2F0U7vYbMgImbHpkkIIGkdvbyNlALJjrYsEi04xekSDugD9T9px1Y817v9wHExBVGZcIkVfyXa2JpMtL%2C1; SRT=%1%enc%3A1%2BBgjVnsI0mOfiZVJBN4AJDxyzL119NfgmJY4Xf%2BxOw91DO8OUyF1di5omuSPkL4Nox8JbUSTxk%3D; CM=%1%HanaPersist%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7Csesstch15%2C%2C-1%7CFtrPers%2C%2C-1%7CCYLPUSess%2C%2C-1%7Ctvsess%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7C%24%2CSGD%2C0%7Csesssticker%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csesshours%2C%2C-1%7CTARSWBPers%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7Csesslaf%2C%2C-1%7CCYLPUPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7CRevHubRMPers%2C%2C-1%7Cperslaf%2C%2C-1%7Csh%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7Cperswifi%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CRevHubRMSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTrayssess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7Cbooksticks%2C%2C-1%7CSPMCWBSess%2C%2C-1%7Cbookstickp%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Csesswifi%2C%2C-1%7Ct4b-pc%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumSURPers%2C%2C-1%7CTBPers%2C%2C-1%7Cperstch15%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7Cpershours%2C%2C-1%7CPremiumORSess%2C%2C-1%7CRestAdsPers%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CTrayspers%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CMCPPers%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7Cpers_rev%2C%2C-1%7Cmdpers%2C%2C-1%7CMetaFtrSess%2C%2C-1%7Cmds%2C1576809860342%2C1576896260%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CRCSess%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7Cpssamex%2C%2C-1%7CCYLPers%2C%2C-1%7Ctvpers%2C%2C-1%7CTBSess%2C%2C-1%7CAdsRetSess%2C%2C-1%7CMCPSess%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7Cmdsess%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TASession=V2ID.9C1A5F0302D1A14D973DCD4E6EFD0E46*SQ.9*LS.DemandLoadAjax*GR.56*TCPAR.69*TBR.35*EXEX.9*ABTR.77*PHTB.38*FS.96*CPU.86*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.ABD562818D249697A8AB4E2FFBFCE092*LF.en*FA.1*DF.0*TRA.false*LD.3856071; TAUD=LA-1575646157999-1*RDD-1-2019_12_07*HDD-406580650-2019_12_22.2019_12_23*RD-406590325-2019_12_11.18190065*LG-1163716354-2.1.F.*LD-1163716355-.....'

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

read_excel('data/sheet1_end.xls')