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
sheet1_data = [['ID', 'Hotel URL', 'Hotel Name', 'Address', 'Rating', 'Number of reviews', 'Star', 'Amenities']]
sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Rating', 'Text Review', 'Reviewer Location', 'Contributor Level', 'Travel Style']]
sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]

cookie = 'TASSK=enc%3AAH5dcQsPLPDkyrrSj9M%2Bz8qwTsnHuINWyBkBMCBtHpuDU4YR9911PLQiCrtLUXp510pmsBvZumlYMV4mfKw8qnZV%2FbzGN1Cpx%2BlqDMRQL0F6sD3r1fVjMsw7Oevw%2BWCV%2Fw%3D%3D; ServerPool=B; PMC=V2*MS.33*MD.20180805*LD.20180805; TAUnique=%1%enc%3AdFWRrhvqgMBfLkar6teR6%2Btv%2BarZM%2FpGd0j3x5%2F3%2FM%2BnJ1iTvWkb0Q%3D%3D; TART=%1%enc%3Am%2FmKXnKmau2u3%2B7moDID3A2g70jDJDlApZ70d5NG4ZnMZnVfKARquaAfoo4hlEMXkSj9GUxjwoU%3D; BEPIN=%1%16509e329d6%3Bbak100b.b.tripadvisor.com%3A10023%3B; TATravelInfo=V2*AY.2018*AM.8*AD.19*DY.2018*DM.8*DD.20*A.2*MG.-1*HP.2*FL.3*DSM.1533470477427*AZ.1*RS.1; PAC=ABMlZcnne_4nA-39y-lfGWBJJ2z6NIgk0oaahc2HQwBIyFGPm6bFH1KID20RWK2b8pqINizqSrZJIYW1owh99tvmpJFSQGKn9mbS_7SaMzuZkCHaImHQXx4iaWXOeoKvQstIG3k72bPR4v4qxiVdTquB21gSR0223jkgMdTaJHL7; CM=%1%HanaPersist%2C%2C-1%7Cpu_vr2%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CSPHRSess%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpu_vr1%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C2%2C-1%7CPremiumSURPers%2C%2C-1%7Ctvsess%2C1%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7Ccatchsess%2C10%2C-1%7Cbrandsess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCpmPopunder_1%2C%2C-1%7CCCSess%2C1%2C-1%7CCpmPopunder_2%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2CSGD%2C0%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7Cmds%2C1533472455425%2C1533558855%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7C+r_lf_1%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CSPHRPers%2C%2C-1%7CRCSess%2C%2C-1%7C+r_lf_2%2C%2C-1%7Ccatchpers%2C3%2C1534074184%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7Cvr_npu2%2C%2C-1%7Csh%2C%2C-1%7CLastPopunderId%2C104-771-null%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7Cvr_npu1%2C%2C-1%7CCCPers%2C%2C-1%7Ctvpers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cbrandpers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CWarPopunder_Session%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CWarPopunder_Persist%2C%2C-1%7CTheForkORPers%2C%2C-1%7Cr_ta_2%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7Cr_ta_1%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TASession=V2ID.A359B1B1C5A00212527116FD7F719C32*SQ.134*LS.PageMoniker*GR.93*TCPAR.65*TBR.23*EXEX.64*ABTR.77*PHTB.90*FS.64*CPU.20*HS.recommended*ES.relevance*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*MS.-1*RMS.-1*TRA.false*LD.298184; TAUD=LA-1533469189911-1*RDD-1-2018_08_05*HC-34117*HDD-1066575-2018_08_19.2018_08_20.1*G-3265525-2.1.14209292.*LD-47403891-2018.8.19.2018.8.20*LG-47403894-2.1.T.; TAReturnTo=%1%%2FHotels-g298184-Tokyo_Tokyo_Prefecture_Kanto-Hotels.html; roybatty=TNI1625!AFttDrQJgx5h94odG8WZbntaagRD%2FWfj5TpHLoIt1cPITkCEgV%2F%2B4D4Y9lfdhvoPW4B%2FVJDAbnpj5cV1XcyZ6IlaYw5q%2FJ4AzyAfd2%2FZH8fa19GtWdtFgttwopgIXJSZUuaBpgacwm3VvLqj57EfAs9ZOSxMU2TASZqeVKnJpf%2BL%2C1'

base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'

all_hotel_url = [
    ('https://www.tripadvisor.com.sg/Hotels-g298184-oa%s-Tokyo_Tokyo_Prefecture_Kanto-Hotels.html', 21, 'Tokyo'),
    ('https://www.tripadvisor.com.sg/Hotels-g298566-oa%s-Osaka_Osaka_Prefecture_Kinki-Hotels.html', 11, 'OSAKA'),
    ('https://www.tripadvisor.com.sg/Hotels-g298564-oa%s-Kyoto_Kyoto_Prefecture_Kinki-Hotels.html', 14, 'Kyoto'),
    ('https://www.tripadvisor.com.sg/Hotels-g298112-oa%s-Gifu_Gifu_Prefecture_Tokai_Chubu-Hotels.html', 2, 'Gifu'),
    ('https://www.tripadvisor.com.sg/Hotels-g298106-oa%s-Nagoya_Aichi_Prefecture_Tokai_Chubu-Hotels.html', 4, 'NAGOYA'),
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
    html = get_request(url)
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
        if i >= 40 :
            break
        try:
            url = hotel_url.replace('-Reviews-', '-Reviews-or%s-' % str(i*10))
            html = get_request(url)
            print('sheet2', page_no, i)
            reg = '"review_(.*?)".*?avatar profile_.*?usernameClick.*?div>(.*?)<(.*?)UID_(.*?)-.*?ui_bubble_rating bubble_(.*?)"'

            comment_list = re.compile(reg).findall(html)
            comment_ids = []
            comment_id_data = {}
            for comment in comment_list:
                comment_ids.append(comment[0])
                comment_id_data[comment[0]] = [comment[0], comment[1], get_user_location(comment[2]), comment[3], comment[4]]
            comment_details = get_comment_detail(comment_ids)
            for k, v in comment_id_data.items():
                comment_detail = comment_details.get(k)
                level, travel_style, user_url = get_level_of_uid(v[3])
                one_row = [hotel_id, hotel_url, v[1], v[-1][0], comment_detail, v[2], level, travel_style]
                sheet2_data.append(one_row)
                sheet3_data.append([v[1], user_url])
        except Exception as e:
            print('ERROR-sheet2-', hotel_id, i, e)


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


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", base_url)
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=5)
    res = res_data.read()
    res = HTMLParser.HTMLParser().unescape(res).decode('unicode-escape').replace('\\', '')
    return res.replace('\n', '').replace('\r', '')


def post_request(url, data):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': base_url,
        'Cookie': cookie,
    }
    resp = requests.post(url, data=data, headers=headers)
    return resp.content.replace('\n', '').replace('\r', '')


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


reload(sys)
sys.setdefaultencoding('utf-8')
request_location_amenaties('data/Hotel.xlsx')



