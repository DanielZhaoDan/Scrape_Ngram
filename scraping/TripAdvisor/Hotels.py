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
from scraping.utils import get_request_html

saved_hotel = set()
R_ID = 1
sheet1_data = [['ID', 'Hotel URL', 'Hotel Name', 'Address', 'Rating', 'Number of reviews', 'Star', 'Amenities']]
sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Review Date' 'Rating', 'Text Review', 'Reviewer Location', 'Contributor Level', 'Travel Style']]
sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]

cookie = 'TAUnique=%1%enc%3Au%2FKH8yQEGOTpTvEC%2FTHhGLajhyk61rGpblhg%2FIANva5QcF0be502LA%3D%3D; TASSK=enc%3AAB0K%2BNdZOqOGCtUTbstCNL5vY2gZLdpBZQUEc7E0qRuBvYIyTKfOqtUbY4e3K0Oc9iAidXprKZXGn5p2QGgGVtGgVB6X4kYK%2BV6I7YLn3o8L3jSl5I4pa6nHkqTV8o%2FpAQ%3D%3D; ServerPool=B; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; TART=%1%enc%3ApOeYHLVHxrVrWjk5CVfZhpAltc8Pj6KW0H3fDqxSXS%2B4mMqWzCigQdC2rgwCZb6gAUtuxWemFUE%3D; PMC=V2*MS.22*MD.20210611*LD.20210612; TATravelInfo=V2*AY.2021*AM.7*AD.4*DY.2021*DM.7*DD.5*A.2*MG.-1*HP.2*FL.3*DSM.1623472512725*RS.1; VRMCID=%1%V1*id.10568*llp.%2FHotels-g255055-Australia-Hotels%5C.html*e.1624077506410; TADCID=w-rrveYyvrwmuZW6ABQCFdpBzzOuRA-9xvCxaMyI12YZWZkPkcgUMTZ9EAaQXMSJRkCsC5Y1e_ND1KTBJjExC_7w-WWT5oPkuLQ; TAAUTHEAT=NkmTlIyUVO-yGefbABQCab7fMZ8ORguCqJF_E5GxfSXwWRNqSqahUgu3FhYlKyiXjobqtSfznpZPQesJu_m2ruTlYDiyjiSBSH7oaEv6wXuW0SJ7swIaDkojXL3clyBxDWb47CvoIg2GWBVcJjTl61B2pp3uwsmjHTeIOaA3vj9tODsP1Hn_9J_vL3xeDwtPWuEy-S7ZcMQ7TicvK9HuKyOljSH5t78UuoY; TASID=DB401263AF174A449023706E95763D55; ak_bmsc=E2BCF2EE0BC176ADF24EA8AE6F132AF4170F0E373B140000ED64C4609CA0A15F~plJ8M1WUpJXtsVBNupt4aL2mYYEJrIl33kMSOBD4Rha8q3pwm3r4AxFryS63kDS/59nEvkks4QuPJ/lLq6olTY8F5oPCHJS5sk5qc+Ggume16d0ssWUtNP72wCbq2A19RM4dwMEHq93ooDpz/0tFFQYFckw1T+jo6ATv3NMxdY5cIqyycyTQGhcdn/DFH9mBCEWeYXHslSvdidHGMm0YU2XBXsi/2bjut50FsjaTbhdVU=; PAC=AB5Mf6_jnr_X07B_2xAVaqwHmLu5CDfDl-3gc-_mX63WEpSXal_HihIdFCHV3YcvFus8n-q4HL9JWLlz7M62ltQaa7FnXqJvqjqDlv_z3kWyfiHVr7g3yzbOGwjUn2bMF-D_6_DCJ66NwlMVnAQx58NipyV6sbnOhXoykbRv5aSzPcRhwVR8pmjd3DhmJAfJOg%3D%3D; bm_sv=D2832FD81952C4946401C4CAEA2179EC~it3y8x019Z/BfrtaxMVBxpbW0HC1P7CHxGXlq1PaF20Cnzb44NMki4eQBUSD6QhhUXzpqAxw7UjoXHcDPq15cvmQM1zVZGcgF+2+5otGds3VP7W/8OZkH4Mh3sslzbTHTiSkUrwgur9h+DpwiMaRqQdXRpykOFlAVGyur6zpIgU=; roybatty=TNI1625!AF6a5wpL0lcw%2BHab58x4JLN1UIaebfbrhp47CXJ%2F2K09qGi4e3IcbImt30CwPX3D4OkLVQDOrLMOLt%2B6hyp8ZQx4754oXNGvfs0ndkxfuOPrdyCKMJMDfXhi4TOTMt%2B76NnkBIJTax5JH2TpIYCCXa4VCNAqHRiUTVn9RQOxYHG3%2C1; SRT=%1%enc%3ApOeYHLVHxrVrWjk5CVfZhpAltc8Pj6KW0H3fDqxSXS%2B4mMqWzCigQdC2rgwCZb6gAUtuxWemFUE%3D; TASession=%1%V2ID.DB401263AF174A449023706E95763D55*SQ.139*PR.40185%7C*LS.PageMoniker*GR.20*TCPAR.61*TBR.47*EXEX.69*ABTR.63*PHTB.85*FS.2*CPU.38*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.ABD562818D249697A8AB4E2FFBFCE092*LF.en*FA.1*DF.0*TRA.false*LD.294232; TAUD=LA-1623389669618-1*RDD-1-2021_06_11*HDD-82842988-2021_07_04.2021_07_05.1*LD-96254764-2021.7.4.2021.7.5*LG-96254766-2.1.F.; TAReturnTo=%1%%2FHotels%3Fg%3D294232%26offset%3D180%26reqNum%3D1%26puid%3DYMRtxAokJX4AA3MSKsUAAAJr%26isLastPoll%3Dfalse%26plSeed%3D1895301258%26waitTime%3D49%26paramSeqId%3D5%26changeSet%3DMAIN_META%2CPAGE_OFFSET'

base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'

all_hotel_url = [
    ('https://www.tripadvisor.in/Hotels-g294232-Japan-Hotels.html', 884),
    # ('https://www.tripadvisor.com.sg/Hotels-g298566-oa%s-Osaka_Osaka_Prefecture_Kinki-Hotels.html', 11, 'OSAKA'),
    # ('https://www.tripadvisor.com.sg/Hotels-g298564-oa%s-Kyoto_Kyoto_Prefecture_Kinki-Hotels.html', 14, 'Kyoto'),
    # ('https://www.tripadvisor.com.sg/Hotels-g298112-oa%s-Gifu_Gifu_Prefecture_Tokai_Chubu-Hotels.html', 2, 'Gifu'),
    # ('https://www.tripadvisor.com.sg/Hotels-g298106-oa%s-Nagoya_Aichi_Prefecture_Tokai_Chubu-Hotels.html', 4, 'NAGOYA'),
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


def get_category_urls(url, is_second_level=False):
    html = get_request(url)
    if is_second_level:
        html = re.compile(r'class="filter_list_1"(.*?)id="CHILD_GEO_FILTER"').findall(html)[0]
    reg = 'class="jfy_checkbox ap_filter_.*?href="(.*?)".*?>(.*?)\((.*?)\)'
    lists = re.compile(reg).findall(html)
    ret = []
    for item in lists:
        ret.append({
            'url': 'https://www.tripadvisor.com.sg' + item[0],
            'name': item[1].strip(),
            'count': int(item[2])
        })
    return ret


def request_sheet1(url):
    global sheet1_data
    raw_reg = 'class="listing_title".*?href="(.*?)".*?="(.*?)".*?>(.*?)<.*?common_responsive_rating_and_review_count(.*?)"ReviewCount">(.*?) revi'
    html = get_request(url)
    hotel_list = re.compile(raw_reg).findall(html)
    for hotel in hotel_list:
        try:
            hotel_url = 'https://www.tripadvisor.com.sg' + hotel[0]
            id = hotel[1]
            name = hotel[2]
            rating = global_rating_details(hotel[3])
            no_review = hotel[4]
            amenaties, review_page_no, star, location = get_hotel_details(hotel_url)
            one_row = [id, hotel_url, name, location, rating, no_review, star, amenaties]
            print('sheet1', one_row)
            sheet1_data.append(one_row)
            if no_review > 0:
                request_sheet2(id, review_page_no, hotel_url)
        except Exception as e:
            print('ERROR-sheet1-', url, e)


def global_rating_details(ori):
    if 'of 5 bubbles' in ori:
        reg = "alt='(.*?) of 5 bubbles'"
        data = re.compile(reg).findall(ori)
        return data[0]
    return 0


def get_hotel_details(url):
    html = get_request_html(url, cookie)
    reg = 'class="overview_card".*?cardTitle">(.*?)<(.*?)class="separator"'
    review_page_no = get_review_page_no(html)
    star = get_star(html)
    overview_list = re.compile(reg).findall(html)
    location = ''
    amenaties = ''
    for overview in overview_list:
        title = overview[0]
        if title == 'Location and contact':
            location = get_location(overview[1])
        elif title == 'What\'s included':
            amenaties = get_amenaties(overview[1])

    return amenaties, review_page_no, star, location


def get_amenaties(ori):
    reg = 'class="detailListItem"><span.*?span>(.*?)<'
    amenaties = re.compile(reg).findall(ori)
    return ','.join(amenaties)


def get_review_page_no(html):
    if 'filters_detail_language_filterLang_en' not in html:
        return 0
    reg = 'filters_detail_language_filterLang_en.*?count">\((.*?)\)'
    return int(re.compile(reg).findall(html)[0].replace(',', ''))


def get_star(html):
    if 'ui_star_rating star_' not in html:
        return 0
    reg = 'ui_star_rating star_(.*?)"'
    return re.compile(reg).findall(html)[0][0]


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


def get_location(ori):
    reg = '<div class="address">(.*?)<div class="container_content'
    location = re.compile(reg).findall(ori)
    if location:
        return remove_html_tag(location[0])
    return ''


def request_sheet2(hotel_id, number, hotel_url):
    global sheet2_data,  sheet3_data
    page_no = number / 5
    if number % 5 != 0:
        page_no += 1
    for i in range(0, page_no):
        if i >= 40:
            break
        try:
            url = hotel_url.replace('-Reviews-', '-Reviews-or%s-' % str(i*10))
            html = get_request(url)
            print('sheet2', page_no, i)
            reg = '"review_(.*?)".*?avatar profile_.*?usernameClick.*?div>(.*?)<(.*?)UID_(.*?)-.*?ui_bubble_rating bubble_(.*?)".*?title=\'(.*?)\''

            comment_list = re.compile(reg).findall(html)
            comment_ids = []
            comment_id_data = {}
            for comment in comment_list:
                comment_ids.append(comment[0])
                comment_id_data[comment[0]] = [comment[0], comment[1], get_user_location(comment[2]), comment[3], comment[4], comment[5]]
            comment_details = get_comment_detail(comment_ids)
            for k, v in comment_id_data.items():
                comment_detail = comment_details.get(k)
                level, travel_style, user_url = get_level_of_uid(v[3])
                one_row = [hotel_id, hotel_url, v[1], v[-2][0], get_comment_date(v[-1]), comment_detail, v[2], level, travel_style]
                sheet2_data.append(one_row)
                sheet3_data.append([v[1], user_url])
        except Exception as e:
            print('ERROR-sheet2-', hotel_id, i, e)


def get_comment_date(ori):
    try:
        date = datetime.strptime(ori, '%d %B %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_user_location(ori):
    if 'strong' in ori:
        reg = 'strong>(.*?)<'
        data = re.compile(reg).findall(ori)
        return data[0]
    return ''


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


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_date(ori):
    d = datetime.strptime(ori, '%a %b %d, %Y %I:%M %p')
    date = d.strftime('%d/%m/%Y')
    return date, d.weekday() + 1


def get_location_amenaties(url):
    html = get_request(url)
    location_reg = 'class="detail">(.*?)</di'
    location_data = re.compile(location_reg).findall(html)
    location = 'N/A'
    if location_data:
        location = remove_html_tag(location_data[0])
    amenaties_reg = 'detailListItem">(.*?)<'
    amenaties = ','.join(re.compile(amenaties_reg).findall(html))
    return location, amenaties


def request_location_amenaties(filename):
    res = []
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(0, table.nrows):
        row = table.row(i)
        if i == 0:
            res.append([row[i].value for i in range(table.ncols)])
        try:
            hotel_id = row[0].value
            hotel_url = row[1].value
            hotel_name = row[2].value
            location = row[3].value
            rating = row[4].value
            no_review = row[5].value
            star = row[6].value
            amenaties = row[7].value
            city = row[8].value
            if location == '' or amenaties == '':
                location, amenaties = get_location_amenaties(hotel_url)
            one_row = [hotel_id, hotel_url, hotel_name, location, rating, no_review, star, amenaties, city]
            print(one_row)
            res.append(one_row)
        except Exception as e:
            print(i, e)
    write_excel('hotel_1.xls', res)


def get_all_hotels():
    global sheet1_data, sheet2_data, sheet3_data
    for entry in all_hotel_url:
        url_base = entry[0]
        for i in range(entry[1]):
            url = url_base % str(i*30)
            print(url)
            request_sheet1(url)
        write_excel(entry[2]+'_1.xls', sheet1_data)
        write_excel(entry[2]+'_2.xls', sheet2_data)
        write_excel(entry[2]+'_3.xls', sheet3_data)
        sheet1_data = [['ID', 'Hotel URL', 'Hotel Name', 'Address', 'Rating', 'Number of reviews', 'Star', 'Amenities']]
        sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Rating', 'Text Review', 'Reviewer Location', 'Contributor Level', 'Travel Style']]
        sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]


def read_excel(filename, start=1):
    global R_ID, sheet2_data, sheet3_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            main_url = row[1].value
            id = row[0].value
            if id in saved_hotel:
                continue
            review_no = int(row[5].value)
            if review_no > 0:
                request_sheet2(id, int(review_no), main_url)
            R_ID += 1
            if R_ID % 2000 == 0:
                write_excel('sheet2_with_date_hotels_%d.xls' % R_ID, sheet2_data)
                write_excel('sheet3_with_date_hotels_%d.xls' % R_ID, sheet3_data)
                del sheet2_data
                del sheet3_data
                sheet2_data = []
                sheet3_data = []
        except:
            print(i)


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


reload(sys)
sys.setdefaultencoding('utf-8')
print get_hotel_details('https://www.tripadvisor.com.my/Hotel_Review-g14134875-d308070-Reviews-Yokohama_Royal_Park_Hotel-Minatomirai_Nishi_Yokohama_Kanagawa_Prefecture_Kanto.html')
# pre_load('data/Hotel_with_date.xlsx')
# print('saved: ', len(saved_hotel))
# read_excel('data/data/Hotel.xlsx', start=1)
# write_excel('sheet2_with_date_hotel.xls', sheet2_data)
# write_excel('sheet3_with_date_hotel.xls', sheet3_data)


