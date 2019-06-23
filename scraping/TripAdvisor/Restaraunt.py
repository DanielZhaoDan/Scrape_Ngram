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

sheet1_data = [['ID', 'URL', 'Name', 'Rank', 'Address', 'Rating', 'Type', 'Number of reviews', 'pricing', 'Reserve Online', 'Delivery by']]
sheet2_data = [['R_ID', 'Handle', 'Location', 'rating', 'comment date', 'Headline', 'Review text', 'Contributor level']]
sheet3_data = [['UID', 'restaurant url', 'restaurant name', 'rating', 'restaurant address', 'restaurant country']]
R_ID = 1

url_bases = [
    # 'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298184&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
    # 'https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=298566&ajax=1&itags=10591&pid=14&sortOrder=relevance&o=%s&availSearchEnabled=false',
    'https://www.tripadvisor.com.my/RestaurantSearch?Action=PAGE&geo=298570&ajax=1&cat=10659,10346&sortOrder=popularity&zfz=10665&o=a0&availSearchEnabled=false&o=%s',
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

cookie = 'TASSK=enc%3AAOXETkGtSLgIR%2BBeKK3mL0jRs%2BDZ056%2F%2BFKdT6GURmBLzpbtZeP71pzSaLEppaD28E6QmzfXrhtI6xRFxRg0P8EZJfHtNijvRhBQF%2Bg835hkQrgJ7Q3MeND1VhSKipUM0A%3D%3D; ServerPool=A; PMC=V2*MS.40*MD.20190622*LD.20190622; TART=%1%enc%3AOCnwr8UMvA4cqnmZjkKzJjjXTcPsH9va%2F3wSG8%2BrItw7bGQzyB6abtrxeGdYx61CUO4ZANeUmCY%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7C; TAUnique=%1%enc%3AIBMFJUdk5zU4KfCvxQy8DrH7ps%2F6uZg4%2Frou20s40KQVAETMq8nxvA%3D%3D; TAReturnTo=%1%%2FRestaurants-g298570-Kuala_Lumpur_Wilayah_Persekutuan.html; PAC=ABFTn9M7cWyq6Kj39_NO1ApIfMscXnvqu98VUzRE_tGB9HEc-CIO7DwL9MAbobO2-j0GQbucR5sqoHdjUslBaMp5UWqdd7I_n45_-s9q6lVXpjAESLKCNNV9_EtV_gcFUGn9JoFFs6MMSSnZcXZBAlDCZ1u6K7MnWQb8tejij6mpN6pqhLE5vKbWt07qsWS4Qf00a0G2zRAw_iJHBnovMFY%3D; SecureLogin2=3.4%3AADf9%2F%2B00839hne5MptlRhG5tXdwiKZm6PBz2LcneLdTvmMwq71RczTDGEi3dEoNzIQ3wafaWxcYct2Q4Hahc2up3IBoExm%2BQcjxmjXIhPvlrtt8MQ%2BIC3%2Frt7sv%2FgmZyOQ256zNnzhAluUzlRS48AqKJP9KN2yv%2FNrbXY%2Bqjzr2ERy0%2FsS91OhX3BFrW4AA%2Bs1%2FuQgGGLXlvN950DF8vP9%2FVvH%2BOuaplCyf%2BDWSqVYVA; TAAuth3=3%3Ae959419dc328c857b0cf8dbae0eb4e5b%3AAGTCfTmCz%2F%2Fmb73j%2FIQlD1wJOpwsKc51LXzM5LFFrB0kgb0qpz42fLwwHOoFEolacLuHaHMYTa7%2F5BLnQ32Za3Rc3U%2FeyHlxvininDxTPiRd%2BU2WLAAu1bA5VREV3T6zRzofiavpO8eZA6Ij5yIW3rraXPA8F7hyLeLXHsM0zIy90EeYjRksvZrM5sDtjYQbqQ%3D%3D; roybatty=TNI1625!AHYZ8F3x5WHhys5uPAzt4%2BzIrkAt2iHE5AQ5rWTnhOQRKR8Oj%2B7msLnlm%2BNHI8iGjtTwDIJ8Ium7B66m1PJApNiFZKsKpylQIM7Cd9yQP5NFSFh3So9YPwkdZBWpFJ4vj78f%2FxW6kSe9ySfQGYoni5BuD9QXAmB8DcGcQv2PDRQP%2C1; SRT=%1%enc%3AOCnwr8UMvA4cqnmZjkKzJjjXTcPsH9va%2F3wSG8%2BrItw7bGQzyB6abtrxeGdYx61CUO4ZANeUmCY%3D; TASession=%1%V2ID.D0B35761A30A6EC9F4D4A8015D144065*SQ.27*PR.40185%7C*LS.Restaurants*GR.67*TCPAR.46*TBR.86*EXEX.59*ABTR.44*PHTB.27*FS.88*CPU.72*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.ABD562818D249697A8AB4E2FFBFCE092*FA.1*DF.0*RT.0*TRA.true*LD.298570; TAUD=LA-1561231929982-1*RDD-1-2019_06_23*LG-466105-2.1.F.*LD-466106-.....'

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
        link = ''
        try:
            id = key_prefix+str(R_ID)
            rank = R_ID
            link = 'https://www.tripadvisor.com.sg' + detail[0]
            name = detail[1]
            avg_rating, review_number = get_ratings(detail[2])
            can_booking = 'Yes'
            if detail[4] == '':
                can_booking = 'No'
            location, review_page_no, cu_type, delivery_by = get_rest_detail_and_comment_page(link)
            # ['ID', 'URL', 'Name', 'Rank', 'Address', 'Rating', 'Type', 'Number of reviews', 'pricing', 'Reserve Online', 'Delivery by']]
            one_row = [id, link, name, rank, location, avg_rating, ','.join(cu_type), review_number, '$$ - $$$', can_booking, delivery_by, review_page_no]
            print one_row
            sheet1_data.append(one_row)
            # if review_page_no > 0:
            #     request_sheet2(id, review_page_no, link, name)
            R_ID += 1
        except Exception as e:
            print 'ERR---level 1---', link, e


def get_comment_date(ori):
    try:
        date = datetime.strptime(ori, '%d %B %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def request_sheet2(hotel_id, number, hotel_url, index):
    global sheet2_data, sheet3_data
    for i in range(0, number):
        if i >= 30:
            break
        try:
            url = hotel_url.replace('-Reviews-', '-Reviews-or%s-' % str(i*10))
            html = get_request(url)
            print('sheet2--300 of ', index, number, i)
            reg = '"review_(.*?)".*?avatar profile_(.*?)".*?usernameClick.*?div>(.*?)<.*?ui_bubble_rating bubble_(.*?)".*?title=\'(.*?)\'.*?noQuotes\'>(.*?)<'

            comment_list = re.compile(reg).findall(html)
            comment_ids = []
            comment_id_data = {}
            for comment in comment_list:
                comment_ids.append(comment[0])
                comment_id_data[comment[0]] = [comment[0], comment[1], comment[2], comment[3], comment[4], comment[5]]
            comment_details = get_comment_detail(comment_ids)
            for k, v in comment_id_data.items():
                uid = v[1]
                name = v[2]
                rating = v[3][0]
                comment_date = v[4]
                title = remove_html_tag(v[5])
                comment_detail = comment_details.get(k)
                level, user_url, location, no_review, no_helpful, travel_style = get_level_of_uid(uid)
                # [['R_ID', 'Handle', 'Location', 'rating', 'comment date', 'Headline', 'Review text', 'Contributor level']]
                one_row = [hotel_id, name, location.replace('From ', ''), rating, get_comment_date(comment_date), title, comment_detail, level]
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
    reg = 'tagsContainer"(.*?)restaurantDescription.*?map-pin-fill">(.*?)</div.*?atf_commerce_and_photos(.*)id="btf_wrap"'
    data = re.compile(reg).findall(html)[0]
    types = get_types(data[0])
    location = remove_html_tag(data[1])
    deliver = get_deliver(data[2])
    eng_comment_no = get_eng_comment_no(html)
    return location, eng_comment_no, types, deliver


def get_types(ori):
    reg = 'href=.*?>(.*?)<'
    data = re.compile(reg).findall(ori)
    return data[1:]


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
            review_no = int(row[11].value)
            name = row[2].value
            if review_no > 0:
                request_sheet2(id, int(review_no), main_url, i)
            R_ID += 1
            if R_ID % 4000 == 0:
                write_excel('sheet2_rest_%d.xls' % R_ID, sheet2_data)
                del sheet2_data
                sheet2_data = []
        except:
            print(i)


reload(sys)

read_excel('data/sheet1.xls')
write_excel('sheet2.xls', sheet2_data)



