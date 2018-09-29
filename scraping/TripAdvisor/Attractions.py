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

R_ID = 1
sheet1_data = [['ID', 'Attraction URL', 'Attraction Name', 'Address', 'Rating', 'Number of reviews', 'Booking online', 'Description']]
sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Rating', 'review date' 'Text Review', 'Reviewer Location', 'Contributor Level', 'Travel Style']]
sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]

base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'
cookie = 'TASSK=enc%3AAH5dcQsPLPDkyrrSj9M%2Bz8qwTsnHuINWyBkBMCBtHpuDU4YR9911PLQiCrtLUXp510pmsBvZumlYMV4mfKw8qnZV%2FbzGN1Cpx%2BlqDMRQL0F6sD3r1fVjMsw7Oevw%2BWCV%2Fw%3D%3D; TAUnique=%1%enc%3AdFWRrhvqgMBfLkar6teR6%2Btv%2BarZM%2FpGd0j3x5%2F3%2FM%2BnJ1iTvWkb0Q%3D%3D; TALanguage=en; TAAuth3=3%3A2f4b9230b134f2d72024aa335b17df41%3AAM9KtPHqQfBxeJPltFVdfW5M9QCnXVT7cG99lPDaMPw7mVqdmNkWb103ZGJFTl2Bt4D8BEiNyCBzh00PAVwQ6UDs26Q4gzyHd35zfrM1nHItKxRk5VgvHsZwTB5NIeBpjLEmC21e8AUCQIuiCemFYuD5JgG9VwFicM17JOMgIut%2F43nQmpyd9P5I08FEyfkBzxoikzo9EOQ%2FOS2JZ5%2FoH2U%3D; ServerPool=C; TATravelInfo=V2*AY.2019*AM.2*AD.21*DY.2019*DM.2*DD.24*A.2*MG.-1*HP.2*FL.3*DSM.1535551954933*AZ.1*RS.1; BEPIN=%1%165aa473061%3Bbak210b.b.tripadvisor.com%3A10023%3B; PAC=AGGlzr7Y8yQDbfSfdTO45ArdKNGYS6uwhffQ-ysnEqRTw7CcUXG106MvTXftFLDZzWq9vjnrsQd4j5-xrH3leoSFooAGMxavLT_mjj-RO6h2l95-3k3HHsXJNHHXqOOlug%3D%3D; PMC=V2*MS.33*MD.20180805*LD.20180905; roybatty=TNI1625!AGwcyChDYlxGQgb3IqkCfXEh04QOkE37FZXnh3XVqcDTJ5R1xryTwTF%2BDc6wZ1TLTCNq2ZtY9QJjbgvNpWOXOGi09D1g%2FFLCIkodBKj%2BQ%2FJfBZ1G6SPshjJghYusBxsU4Zn7fhd44%2BWOljO0nnIQshvQLRp7DRf4MPWkHZBBIAIE%2C1; TART=%1%enc%3Am%2FmKXnKmau2u3%2B7moDID3A2g70jDJDlApZ70d5NG4ZnMZnVfKARquaAfoo4hlEMXkSj9GUxjwoU%3D; TAReturnTo=%1%%2FHotel_Review%3Fg%3D1066457%26reqNum%3D2%26puid%3DW4-xdAoQK3gAAICO7uMAAAA%40%26isLastPoll%3Dfalse%26d%3D6987624%26paramSeqId%3D0%26changeSet%3D; TASession=V2ID.BE2CC03D155E1ECA19579FFEADFC2E94*SQ.7*LS.PageMoniker*GR.99*TCPAR.70*TBR.68*EXEX.26*ABTR.37*PHTB.27*FS.30*CPU.4*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.C046DDFA89F7DF42D3E2657A089B8B5A*LF.en*FA.1*DF.0*TRA.false*LD.6987624; CM=%1%pu_vr2%2C%2C-1%7CHanaPersist%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpu_vr1%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7Ccatchsess%2C5%2C-1%7Cbrandsess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7C%24%2CSGD%2C0%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7C+r_lf_1%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7C+r_lf_2%2C%2C-1%7Ccatchpers%2C1%2C1536764921%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7Cvr_npu2%2C%2C-1%7CLastPopunderId%2C104-771-null%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7Cvr_npu1%2C%2C-1%7CCCPers%2C%2C-1%7Cbrandpers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CWarPopunder_Session%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CWarPopunder_Persist%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7Cr_ta_2%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7Cr_ta_1%2C%2C-1%7CTARSWBSess%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TAUD=LA-1533469189911-1*RDD-1-2018_08_05*G-3265525-2.1.14209292.*HC-531161959*ADD-2082767823-2019_02_21*HDD-2690930762-2018_09_16.2018_09_17*LG-2690931324-2.1.T.*LD-2690931325-.....'
uid_level_dict = {}
base_url_list = [
    # ('https://www.tripadvisor.com.sg/Attractions-g298112-Activities-oa%s-Gifu_Gifu_Prefecture_Tokai_Chubu.html', 5, 'Gifu'),
    # ('https://www.tripadvisor.com.sg/Attractions-g298106-Activities-oa%s-Nagoya_Aichi_Prefecture_Tokai_Chubu.html', 16, 'Nagoya'),
    # ('https://www.tripadvisor.com.sg/Attractions-g298566-Activities-oa%s-Osaka_Osaka_Prefecture_Kinki.html', 44, 'Osaka'),
    # ('https://www.tripadvisor.com.sg/Attractions-g298564-Activities-oa%s-Kyoto_Kyoto_Prefecture_Kinki.html', 47, 'Kyoto'),
    ('https://www.tripadvisor.com.sg/Attractions-g298184-Activities-oa%s-Tokyo_Tokyo_Prefecture_Kanto.html', 159, 'Tokyo'), 
]


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


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


def get_category_urls(url, is_second_level=False):
    html = get_request(url)
    if is_second_level:
        html = re.compile(r'class="filter_list_1"(.*?)class="ap_filter_wrap').findall(html)[0]
    reg = 'class="taLnk" href="/(.*?)".*?>(.*?)\((.*?)\)'
    lists = re.compile(reg).findall(html)
    ret = []
    for item in lists[:-1]:
        ret.append({
            'url': 'https://www.tripadvisor.com.sg/' + item[0],
            'name': item[1].strip(),
            'count': int(item[2])
        })
    return ret

def request_sheet1(category, url):
    global sheet1_data, R_ID
    raw_reg = 'class="listing_title.*?href="(.*?)".*?>(.*?)</div.*?class="listing_rating"(.*?)class="tag_line".*?listing_commerce(.*?)</div'
    html = get_request(url)
    topic_body = re.compile(raw_reg).findall(html)
    if not topic_body:
        return
    for detail in topic_body:
        try:
            hotel_id = category + str(R_ID)
            link = 'https://www.tripadvisor.com.sg' + detail[0]
            if '-c' in link or '-t' in link:
                continue
            name = remove_html_tag(detail[1])

            avg_rating, review_number = global_rating_details(detail[2])
            can_booking = 0
            if 'experience it' in detail[3]:
                can_booking = 1
            location, description, extra = get_attraction_details(link)
            one_row = [hotel_id, link, name, location, avg_rating, review_number, can_booking, description] + extra
            sheet1_data.append(one_row)
            if review_number > 0:
                request_sheet2(hotel_id, review_number, link, R_ID)
            R_ID += 1
        except:
            print('ERR---level 1---' + url)


def global_rating_details(ori):
    reg = 'alt="(.*?) of 5 bubbles".*?#REVIEW.*?>(.*?) review'
    if 'of 5 bubbles' in ori and '#REVIEW' in ori:
        data = re.compile(reg).findall(ori)
        return data[0][0], int(data[0][1].replace(',', ''))
    return 0, 0


def get_attraction_details(link):
    if 'AttractionProduct' in link:
        return get_attraction_product_review(link)
    return get_attraction_review(link)


def get_attraction_product_review(link):
    html = get_request(link)
    location = description = 'N/A'
    extra = ['N/A', 'N/A', 'N/A']
    reg = 'class="product_cta_wrapper"(.*?)id="INTRO_WRAPPER"(.*?)id="MAIN".*?attraction_product_detail_overview_section(.*?)class="section".*?id="DETAILS".*?>(.*?)</div'
    raw_data = re.compile(reg).findall(html)[0]
    if 'href="#important_info"' in raw_data[0]:
        reg = 'href="#important_info">(.*?)<'
        extra[0] = remove_html_tag(re.compile(reg).findall(raw_data[0])[0])
    if 'class="subsection intro"' in raw_data[1]:
        reg = 'class="subsection intro">(.*?)</div'
        data = re.compile(reg).findall(raw_data[1])
        extra[1] = ','.join([remove_html_tag(item) for item in data])
    if 'class="list"' in raw_data[3]:
        reg = 'item.*?>(.*?)</li'
        data = re.compile(reg).findall(raw_data[3])
        extra[2] = ','.join([remove_html_tag(item) for item in data])
    if 'subsection tap_content' in raw_data[2]:
        reg = 'class="subsection tap_content collapse">(.*?)</'
        description = remove_html_tag(re.compile(reg).findall(raw_data[2])[0])
    return location, description, extra

def get_attraction_review(link):
    html = get_request(link)
    if 'descriptionRow"' in html:
        reg = 'ui_icon map-pin">(.*?)</div.*?class="description.*?class="text">(.*?)<'
        data = re.compile(reg).findall(html)[0]
        location = remove_html_tag(data[0])
        description = remove_html_tag(data[1])
        return location, description, ['N/A', 'N/A', 'N/A']
    else:
        reg = 'ui_icon map-pin">(.*?)</div.*?'
        data = re.compile(reg).findall(html)[0]
        location = remove_html_tag(data)
        description = 'N/A'
        return location, description, ['N/A', 'N/A', 'N/A']

def get_review_url(root_url, i):
    if 'AttractionProduct' not in root_url:
        return root_url.replace('-Reviews-', '-Reviews-or%s-' % str(i*10))
    url_slices = root_url.split('-')
    return '-'.join(url_slices[:3] + ['or%s' % str(i*10)] + url_slices[3:])

def get_user_location(ori):
    if 'userLocation' in ori:
        reg = 'userLocation">(.*?)<'
        data = re.compile(reg).findall(ori)
        return data[0]
    if 'strong' in ori:
        reg = 'strong>(.*?)<'
        data = re.compile(reg).findall(ori)
        return data[0]
    return ''

def request_sheet2(hotel_id, number, hotel_url, R_ID):
    page_no = number / 10
    if number % 10 != 0:
        page_no += 1
    for i in range(0, page_no):
        if i >= 30:
            break
        try:
            url = get_review_url(hotel_url, i)
            print('sheet2', R_ID, page_no, i, url)
            request_one_sheet2(hotel_id, hotel_url, url)
        except Exception as e:
            print('ERROR-sheet2-', hotel_id, i, e)


def request_one_sheet2(hotel_id, hotel_url, url):
    global sheet2_data,  sheet3_data
    html = get_request(url)
    reg = 'avatar profile_(.*?)".*?onclick=.*?">(.*?)</div(.*?)ui_bubble_rating bubble_(.*?)".*?title=\'(.*?)\'.*?class="entry">(.*?)</div'

    comment_list = re.findall(reg, html)
    for comment in comment_list:
        username = remove_html_tag(comment[1])
        location = get_user_location(comment[2])
        uid = comment[0]
        rating = comment[3]
        date = get_comment_date(comment[4])
        text = remove_html_tag(comment[5]).replace('.More', '')
        level, travel_style, user_url = get_level_of_uid(uid)
        one_row = [hotel_id, hotel_url, username, rating[0], date, text, location, level, travel_style]
        sheet2_data.append(one_row)
        sheet3_data.append([uid, user_url])    


def get_comment_date(ori):
    try:
        date = datetime.strptime(ori, '%d %B %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_level_of_uid(uid):
    if uid_level_dict.get(uid):
        return uid_level_dict.get(uid)
    html = get_request('https://www.tripadvisor.com.sg/MemberOverlay?uid=' + uid)
    reg = 'href="(.*?)".*?Level.*?>(.*?)<'
    data = re.compile(reg).findall(html)
    if not data:
        return 0, '', 'N/A'
    level = data[0][1]
    user_url = 'https://www.tripadvisor.com.sg' + data[0][0]
    res = (level, get_travel_style(user_url), user_url)
    uid_level_dict[uid] = res
    return res

def get_travel_style(url):
    html = get_request(url)
    reg = 'name="view-all-tags"><.*?>(.*?)<'
    data = re.compile(reg).findall(html)
    return ','.join(data)

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
    req.add_header("Referer", base_url)
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


def get_all():
    global sheet1_data, sheet2_data, sheet3_data
    for entry in base_url_list:
        url_base = entry[0]
        for i in range(entry[1]):
            url = url_base % str(i*30)
            print(url)
            request_sheet1(entry[2], url)
        write_excel(entry[2]+'_1.xls', sheet1_data)
        write_excel(entry[2]+'_2.xls', sheet2_data)
        write_excel(entry[2]+'_3.xls', sheet3_data)
        sheet1_data = [['ID', 'Attraction URL', 'Attraction Name', 'Address', 'Rating', 'Number of reviews', 'Booking online', 'Description']]
        sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Rating', 'Text Review', 'Reviewer Location', 'Contributor Level', 'Travel Style']]
        sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]
        R_ID = 1


def read_excel(filename, start=1):
    global R_ID, sheet2_data, sheet3_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows - 1):
        row = table.row(i)
        try:
            main_url = row[1].value
            id = row[0].value
            review_no = int(row[5].value)
            if review_no > 0:
                request_sheet2(id, int(review_no), main_url, R_ID)
            R_ID += 1
            if R_ID % 2000 == 0:
                write_excel('sheet2_with_date_attractions_%d.xls' % R_ID, sheet2_data)
                write_excel('sheet3_with_date_attractions_%d.xls' % R_ID, sheet3_data)
                del sheet2_data
                del sheet3_data
                sheet2_data = []
                sheet3_data = []
        except:
            print(i)


reload(sys)
sys.setdefaultencoding('utf-8')
read_excel('data/data/Attractions.xlsx', start=3508)
write_excel('sheet2_with_date_attractions.xls', sheet2_data)
write_excel('sheet3_with_date_attractions.xls', sheet3_data)
