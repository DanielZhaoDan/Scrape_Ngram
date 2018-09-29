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

base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'

sheet1_data = [['ID', 'url', 'Name', 'Location', 'avg rating', 'Number of reviews', 'pricing', 'Reserve Online', 'cuisine', 'feature', 'good_for']]
sheet2_data = [['UID', 'url', 'Name', 'review Name', 'review Location', 'rating', 'comment date' 'travel style', 'Review text',  'Contributor level', 'Review No.', 'Helpful vote No.']]
sheet3_data = [['UID', 'restaurant url', 'restaurant name', 'rating', 'restaurant address', 'restaurant country']]
R_ID = 1

url_bases = [
    # 'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298184&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
    # 'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298566&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
    'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298564&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
    'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298112&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
    'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298106&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
]

key_prefixs = [
    # 'Tokyo_',
    # 'Osaka_',
    'Kyoto_',
    'Gifu_',
    'Nagoya_',
]

cookie = 'TASSK=enc%3AAH5dcQsPLPDkyrrSj9M%2Bz8qwTsnHuINWyBkBMCBtHpuDU4YR9911PLQiCrtLUXp510pmsBvZumlYMV4mfKw8qnZV%2FbzGN1Cpx%2BlqDMRQL0F6sD3r1fVjMsw7Oevw%2BWCV%2Fw%3D%3D; TAUnique=%1%enc%3AdFWRrhvqgMBfLkar6teR6%2Btv%2BarZM%2FpGd0j3x5%2F3%2FM%2BnJ1iTvWkb0Q%3D%3D; TALanguage=en; BEPIN=%1%16509e329d6%3Bbak210b.b.tripadvisor.com%3A10023%3B; ServerPool=C; PMC=V2*MS.33*MD.20180805*LD.20180811; TART=%1%enc%3Am%2FmKXnKmau2u3%2B7moDID3A2g70jDJDlApZ70d5NG4ZnMZnVfKARquaAfoo4hlEMXkSj9GUxjwoU%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*DSM.1534000341177*AZ.1*RS.1; TAAuth3=3%3A2f4b9230b134f2d72024aa335b17df41%3AAM9KtPHqQfBxeJPltFVdfW5M9QCnXVT7cG99lPDaMPw7mVqdmNkWb103ZGJFTl2Bt4D8BEiNyCBzh00PAVwQ6UDs26Q4gzyHd35zfrM1nHItKxRk5VgvHsZwTB5NIeBpjLEmC21e8AUCQIuiCemFYuD5JgG9VwFicM17JOMgIut%2F43nQmpyd9P5I08FEyfkBzxoikzo9EOQ%2FOS2JZ5%2FoH2U%3D; CM=%1%HanaPersist%2C%2C-1%7Cpu_vr2%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CSPHRSess%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpv%2C4%2C-1%7Cpu_vr1%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C12%2C-1%7CPremiumSURPers%2C%2C-1%7Ctvsess%2C-1%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7Ccatchsess%2C10%2C-1%7Cbrandsess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C1%2C-1%7CCpmPopunder_2%2C5%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2CSGD%2C0%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7C+r_lf_1%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CSPHRPers%2C%2C-1%7CRCSess%2C%2C-1%7C+r_lf_2%2C%2C-1%7Ccatchpers%2C3%2C1534074184%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7Cvr_npu2%2C%2C-1%7CLastPopunderId%2C137-1859-null%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7Cvr_npu1%2C%2C-1%7CCCPers%2C%2C-1%7Ctvpers%2C1%2C1534185195%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cbrandpers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CWarPopunder_Session%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CWarPopunder_Persist%2C%2C-1%7CTheForkORPers%2C%2C-1%7Cr_ta_2%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7Cr_ta_1%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; PAC=AGWf5UvTWjXqK-yoDvNByyFRa_wYtlFrEsn7OLs5Ja90Qyc276R4vUZZS0ZwaSJNzg-gUatWseADHGcrUQSbPdRu2DUBOElDMYTbxiUyO8TB9HPjdAUjKGMCmsWIShROZg%3D%3D; TAReturnTo=%1%%2FRestaurant_Review-g294264-d8683709-Reviews-Streats_Hong_Kong_Cafe-Sentosa_Island.html; roybatty=TNI1625!ABKS%2FR5pbgrG0FwbvBRv5cvd1Wa8iPbZuNBzGL8UZpRLKd5evjx3qPB%2FM8tJV5QhB9yti5QiL648ExcTg2Zs%2BEGFSEo7LZ5oPnIM24sKPUSxthQUcA87q%2FUzdDMs0eNyZ602j3H%2FYhrhZX%2FmRhejKU2NiyzBR8o%2BdU3DXleEIQD0%2C1; TASession=V2ID.A359B1B1C5A00212527116FD7F719C32*SQ.594*LS.DemandLoadAjax*GR.93*TCPAR.65*TBR.23*EXEX.64*ABTR.77*PHTB.90*FS.64*CPU.20*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.C046DDFA89F7DF42D3E2657A089B8B5A*LF.en*FA.1*DF.0*MS.-1*RMS.-1*FLO.304305*TRA.false*LD.8683709; TAUD=LA-1533469189911-1*RDD-1-2018_08_05*G-3265525-2.1.14209292.*HDD-531151254-2018_08_19.2018_08_20*HC-531161959*LG-539675023-2.1.T.*LD-539675024-.....'

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


def request_sheet1(url, key_prefix):
    print key_prefix + 'level1--'+url
    global sheet1_data, R_ID
    # link, name, replies, views
    raw_reg = 'class="title">.*?href="(.*?)".*?>(.*?)<.*?class="rating(.*?)popIndexBlock.*?class="cuisines">(.*?)</div.*?booking">(.*?)</div'
    try:
        html = get_request(url)
    except:
        print 'ERR---level 1---' + url
        return
    topic_body = re.compile(raw_reg).findall(html)
    if not topic_body:
        return
    for detail in topic_body:
        try:
            id = key_prefix+str(R_ID)
            link = 'https://www.tripadvisor.com.sg' + detail[0]
            name = detail[1]
            avg_rating, review_number = get_ratings(detail[2])
            cuisine = get_cuisine(detail[3])
            can_booking = 1
            if detail[4] == '':
                can_booking = 0
            location, review_page_no, feature, good_for = get_rest_detail_and_comment_page(link)
            one_row = [id, link, name, location, avg_rating, review_number, '$$ - $$$', can_booking, cuisine, feature, good_for]
            print one_row
            sheet1_data.append(one_row)
            request_sheet2(id, review_page_no, link, name)
            R_ID += 1
        except:
            print 'ERR---level 1---' + url


def get_comment_date(ori):
    try:
        date = datetime.strptime(ori, '%d %B %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def request_sheet2(hotel_id, number, hotel_url, hotel_name):
    global sheet2_data, sheet3_data
    for i in range(0, number):
        if i >= 30:
            break
        try:
            url = hotel_url.replace('-Reviews-', '-Reviews-or%s-' % str(i*10))
            html = get_request(url)
            print('sheet2', number, i)
            reg = '"review_(.*?)".*?avatar profile_(.*?)".*?user_name_name_click.*?>(.*?)<.*?ui_bubble_rating bubble_(.*?)".*?title=\'(.*?)\''

            comment_list = re.compile(reg).findall(html)
            comment_ids = []
            comment_id_data = {}
            for comment in comment_list:
                comment_ids.append(comment[0])
                comment_id_data[comment[0]] = [comment[0], comment[1], comment[2], comment[3], comment[4]]
            comment_details = get_comment_detail(comment_ids)
            for k, v in comment_id_data.items():
                uid = v[1]
                name = v[2]
                rating = v[3][0]
                comment_date = v[4]
                comment_detail = comment_details.get(k)
                level, user_url, location, no_review, no_helpful, travel_style = get_level_of_uid(uid)
                one_row = [uid, hotel_url, hotel_name, name, location, rating, get_comment_date(comment_date), travel_style, comment_detail, level, no_review, no_helpful]
                sheet2_data.append(one_row)
                if user_url not in user_url_set:
                    sheet3_data.append([uid, user_url])
                    user_url_set.add(user_url)
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
        detail_dict[comment_detail[0]] = remove_html_tag(comment_detail[1])
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
    res = (level, user_url, location, no_review, no_helpful, travel_style)
    uid_level_dict[uid] = res
    return res


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
    reg = 'ui_icon map-pin">(.*?)</div.*?class="listContainer "(.*?)ad_column.*?class="details_tab"(.*?)additional_info'
    data = re.compile(reg).findall(html)[0]
    location = remove_html_tag(data[0])
    eng_comment_no = get_eng_comment_no(data[1])
    feature, good_for = get_feature_good_for(data[2])
    return location, eng_comment_no, feature, good_for


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_eng_comment_no(ori):
    if 'pagination-details' in ori:
        reg = 'pagination-details.*?of <.*?>(.*?)<'
        no = int(re.compile(reg).findall(ori)[0])
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
    if 'item cuisine' in ori:
        reg = 'item cuisine".*?>(.*?)<'
        return ','.join(re.compile(reg).findall(ori))
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

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            main_url = row[1].value
            id = row[0].value
            review_no = int(row[5].value)
            name = row[2].value
            if review_no > 0:
                request_sheet2(id, int(review_no), main_url, name)
            R_ID += 1
            if R_ID % 4000 == 0:
                write_excel('sheet2_with_date_rest_%d.xls' % R_ID, sheet2_data)
                write_excel('sheet3_with_date_rest_%d.xls' % R_ID, sheet3_data)
                del sheet2_data
                del sheet3_data
                sheet2_data = []
                sheet3_data = []
        except:
            print(i)


reload(sys)
sys.setdefaultencoding('utf-8')
read_excel('Restaurant.xlsx', start=1)
write_excel('sheet2_with_date_rest_%d.xls' % R_ID, sheet2_data)
write_excel('sheet3_with_date_rest_%d.xls' % R_ID, sheet3_data)

