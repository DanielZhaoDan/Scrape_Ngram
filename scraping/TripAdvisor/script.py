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

sheet1_data = [['ID', 'Name', 'Location', 'Overall rating', 'Rank all Bali', 'Number of reviews', 'Cuisine', 'Reserve Online', 'Excellent', 'Very good', 'Average', 'Poor', 'Terrible', 'Families', 'Couples', 'Solo', 'Business', 'Friends', 'Mar-May', 'Jun-Aug', 'Sep-Nov', 'Dec-Feb']]
sheet2_data = [['ID', 'Contributor Name', 'Contributor Location', 'Contributor country', 'Contributor level', 'Review headline', 'rating', 'Review date', 'Review text', 'Reviewer Value', 'Reviewer Service', 'Reviewer Food']]

url_bases = [
    'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298184&ajax=1&itags=10591&pid=8&sortOrder=relevance&o=a%s&availSearchEnabled=false',
    'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298564&ajax=1&itags=10591&pid=8&sortOrder=relevance&o=a%s&availSearchEnabled=false',
    'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298566&ajax=1&itags=10591&pid=8&sortOrder=relevance&o=a%s&availSearchEnabled=false',
]

key_prefixs = [
    'Tokyo_',
    'kyoto_',
    'Osaka_',
]

cookie = 'VRMCID=%1%V1*id.10568*llp.%2FAttraction_Review-g293916-d3336466-Reviews-Dinner_Cruise_by_White_Orchid_River_Cruise-Bangkok%5C.html*e.1483353587117; TAUnique=%1%enc%3At96UkzAMTdkW6lFiox1vtOF0G7JUC0o%2B8PrsszjkOhv6gCLwstQoGQ%3D%3D; ServerPool=A; TALanguage=ALL; __gads=ID=5ef55ea1605b7b15:T=1486869665:S=ALNI_Mbbc923rnxCTOoA0IgyOXeoJpNFnw; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RVL.294265_63*RS.1; TAReturnTo=%1%%2FRestaurants-g294265-Singapore.html; PAC=AMVw9YCjoCGDylIDswh4dOnN52jSKtxEO1L8AHMakmaFLr4nLuGY0PTjzB9d9ozVldNX4IqoC3aDH0ZYODSxBhXJi4hMKilr8ZW9jr6m9_dNZ1LySPtxgECFTLRnZJTC_2_hNsIX7lhPOFo74IPonm_nk_qMJwRSHfJowbbtc-6EYzXj46rHzYnUQRkMi3A04FCOCibuYOv_q4FcuCanGjYOWX7a22DYSGdGIfxn1LOyOmCb971LLB9Xtf4XyIO5WYJxkUbQHS7hX2nwlcbi-Pk-UfAxyzlCsGHx4ryGcOxHfLEINuvwGGfVv-flXBo96A%3D%3D; CommercePopunder=SuppressAll*1488685970520; TASSK=enc%3AAMau%2F7V8wE2mM7CXhzdZD2HEL5ya1SQVEbgZ1OunWzUAqdY2%2BV0%2BI9JsGDDcIFZIpbcaiRPuWBVtjSsOoeGSg%2B4nYMG6D%2FPptkONGMxcaxuLZLsysdF5%2F0RScLA9S0M2MQ%3D%3D; TART=%1%enc%3AFupRYqMdb7TxNDCw1wDMXxO02jVEYcSKyjLoawJdTC%2FVpFvWgpRrGMsPF7rdWymNg1ukKbolbFs%3D; CM=%1%HanaPersist%2C%2C-1%7Cpu_vr2%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CHanaSession%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpv%2C8%2C-1%7Cpu_vr1%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumSURPers%2C%2C-1%7CPCBSess%2C-1%2C-1%7CPremiumMCSess%2C%2C-1%7Ccatchsess%2C5%2C-1%7Cbrandsess%2C%2C-1%7Csesscoestorem%2C%2C-1%7CCCSess%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7Cperscoestorem%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CHomeAPers%2C%2C-1%7C+r_lf_1%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7C+r_lf_2%2C%2C-1%7Ccatchpers%2C2%2C1489290790%7CPCBPers%2C1%2C1489286828%7CLaFourchette+MC+Banners%2C%2C-1%7Cbookstickcook%2C%2C-1%7Cvr_npu2%2C%2C-1%7CLastPopunderId%2C104-771-null%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7Cvr_npu1%2C%2C-1%7CCCPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cbrandpers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CWarPopunder_Session%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CWarPopunder_Persist%2C%2C-1%7CTakeOver%2C%2C-1%7Cr_ta_2%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7Cr_ta_1%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRBASess%2C%2C-1%7Cbookstickpers%2C%2C-1%7Cperssticker%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; roybatty=TNI1625!AGzJsYwffDBcZKGJ1pqNscg3g3e1ZWfFuhenAZnVIy1Ind3cv32c12vxK2JWpDYQQyNzxyjHKtUO6Uh056QoOF8girWOUTnvzoWDUCjbES6AFL67510V%2F0TvR5WQ6Q5krzv7sSgnddbqHobI6UvnOeeEoooufrsw%2FNOEjHSJEQ82%2C1; TASession=%1%V2ID.DE3CDF1E546AD0E9625CC34A20CA937B*SQ.188*PR.39415%7C*LS.Restaurants*GR.66*TCPAR.33*TBR.80*EXEX.69*ABTR.28*PPRP.22*PHTB.86*FS.26*CPU.34*HS.popularity*ES.relevance*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*FBH.2*MS.-1*RMS.-1*RT.0*FLO.8130842*TRA.false*LD.294265; TAUD=LA-1488685984228-1*LG-43696-2.1.F.*LD-43697-.....; PMC=V2*MS.100*MD.20170304*LD.20170304'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_'+str(flag)+'.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
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
                    print '===Write excel ERROR==='+str(one_row[col])
    w.save(filename)
    print filename+"===========over============"


def request_sheet1(url, key_prefix, R_ID):
    print key_prefix + 'level1--'+url
    global sheet1_data
    # link, name, replies, views
    raw_reg = '<h3 class="title">.*?href="(.*?)".*?>(.*?)<(.*?)</h3>.*?class="popIndexBlock"(.*?)class="rating"(.*?)class="priceBar"(.*?)class="booking">(.*?)</div'
    html = get_request(url)
    topic_body = re.compile(raw_reg).findall(html)
    if not topic_body:
        return
    for detail in topic_body:
        try:
            link = 'https://www.tripadvisor.com.sg' + detail[0]
            name = detail[1]
            location = get_location(detail[2])
            rank_bali = get_rank_bali(detail[3])
            avg_rating, review_number = get_ratings(detail[4])
            cuisine = get_cuisine(detail[5])
            can_booking = 1
            if detail[6] == '':
                can_booking = 0
            rating_details, comment_page = get_rating_detail_and_comment_page(link)
            one_row = [key_prefix+str(R_ID), name, location, avg_rating, rank_bali, review_number, cuisine, can_booking] + rating_details
            sheet1_data.append(one_row)
            get_contributor_details(key_prefix+str(R_ID), link, comment_page)
            R_ID += 1
        except:
            print 'ERR---level 1---' + url


def get_contributor_details(r_id, link, number):
    reg = 'id="review_(.*?)".*?class="col1of2"(.*?)class="col2of2".*?class=\'noQuotes\'>(.*?)<.*?class="rate sprite-rating_s rating_s.*?alt="(.*?) of.*?class="ratingDate(.*?)<'
    url_prefix = link.split('-Reviews-')[0].replace('Restaurant_Review', 'ExpandedUserReviews')
    print 'level2--' + link + '   ' + str(number)
    if number == 0:
        number = 1
    for i in range(int(number)):
        contri_detail = []
        review_ids = []
        if '-Reviews-or' not in link:
            url = link.replace('-Reviews-', '-Reviews-or'+str(i*10)+'-')
        else:
            url = link.replace('-Reviews-or', '-Reviews-or'+str(i*10)+'-')
        try:
            html = get_request(url)
        except:
            print 'EXC--'+url
            continue
        details = re.compile(reg).findall(html)
        for detail in details:
            review_id = detail[0]
            review_ids.append(str(review_id))
            contri_info = get_user_info(detail[1])
            headline = remove_html_tag(detail[2])
            individual_rating = int(detail[3])
            date = get_review_date(detail[4])
            contri_detail.append([r_id] + contri_info +[headline, individual_rating, date])
        if review_ids:
            rating_detail = get_review_detail(url_prefix, link, review_ids)
            for i in range(len(contri_detail)):
                one_row = contri_detail[i]+rating_detail[i]
                sheet2_data.append(one_row)


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


def get_rating_detail_and_comment_page(link):
    html = get_request(link)
    reg = 'class="row_label">Excellent<.*?<span>(.*?)<.*?class="row_label">Very good<.*?<span>(.*?)<.*?class="row_label">Average<.*?<span>(.*?)<.*?class="row_label">Poor<.*?<span>(.*?)<.*?class="row_label">Terrible<.*?<span>(.*?)<.*?'
    reg += 'Traveller type.*?>Families.*?\((.*?)\).*?>Couples.*?\((.*?)\).*?>Solo.*?\((.*?)\).*?>Business.*?\((.*?)\).*?>Friends.*?\((.*?)\).*?'
    reg += 'Time of year.*?Mar-May.*?\((.*?)\).*?Jun-Aug.*?\((.*?)\).*?Sep-Nov.*?\((.*?)\).*?Dec-Feb.*?\((.*?)\).*'
    if 'unified pagination' in html:
        reg += 'data-page-number="(.*?)"'
        details = re.compile(reg).findall(html)
        return list(details[0][:-1]), details[0][-1]
    else:
        details = re.compile(reg).findall(html)
        if details:
            return list(details[0]), 0
        else:
            return ['N/A' for i in range(14)], 0


def get_cuisine(ori):
    if 'class="cuisines"' in ori:
        reg = '<a class="cuisine".*?>(.*?)<'
        return '&'.join(re.compile(reg).findall(ori))
    return 'N/A'


def get_ratings(ori):
    if 'of 5 bubbles' in ori:
        reg = 'alt="(.*?) of 5 bubbles.*?reviewCount">.*?>(.*?) review'
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


def request_sheet2(topic, number, url2_base):
    global sheet2_data
    reg = 'class="postbody".*?class="author".*?&raquo; (.*?) <.*?class="content">(.*?)</div>'
    for i in range(number):
        url = url2_base + '&start=' + str(i*10)
        print url
        html = get_request(url)
        reply_lists = re.compile(reg).findall(html)
        for reply in reply_lists:
            date, day = get_date(reply[0])
            content = remove_html_tag(reply[1])
            one_row = [topic, content, date, str(day)]
            sheet2_data.append(one_row)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_date(ori):
    d = datetime.strptime(ori, '%a %b %d, %Y %I:%M %p')
    date = d.strftime('%d/%m/%Y')
    return date, d.weekday() + 1


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.tripadvisor.com.sg/Restaurants-g294226-Bali.html')
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')

sizes = [35, 8, 7]

for i in range(len(url_bases)):
    size = sizes[i]
    url_base = url_bases[i]
    key_prefix = key_prefixs[i]
    R_ID = 1
    for i in range(size):
        print key_prefix + '-----Level 1 Page ' + str(i) + '-----'
        url = url_base % str(i*30)
        request_sheet1(url, key_prefix, R_ID)
    write_excel('data/sheet1.xls'.replace('sheet', key_prefix), sheet1_data)
    write_excel('data/sheet2.xls'.replace('sheet', key_prefix), sheet2_data)
    del sheet2_data
    del sheet1_data
    sheet1_data = [['ID', 'Name', 'Location', 'Overall rating', 'Rank all Bali', 'Number of reviews', 'Cuisine', 'Reserve Online', 'Excellent', 'Very good', 'Average', 'Poor', 'Terrible', 'Families', 'Couples', 'Solo', 'Business', 'Friends', 'Mar-May', 'Jun-Aug', 'Sep-Nov', 'Dec-Feb']]
    sheet2_data = [['ID', 'Contributor Name', 'Contributor Location', 'Contributor country', 'Contributor level', 'Review headline', 'rating', 'Review date', 'Review text', 'Reviewer Value', 'Reviewer Service', 'Reviewer Food']]
