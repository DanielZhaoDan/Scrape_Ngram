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
sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Rating', 'Text Review', 'Reviewer Location', 'Contributor Level', 'Travel Style']]
sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]

base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'
cookie = 'TASSK=enc%3AAEWqEz6PSzC%2B0mEdDhD8TYdzehbp3E5yYPS6IU82xNhZCWs42WFVupCN6TIq%2BDwmTQFLrFrGKXbjWkFV%2BOeOlqTuYZrVuC5PIwN05CmlOlt9VSjr08IEjSvs%2BcHUn1J3RA%3D%3D; ServerPool=B; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; TAUnique=%1%enc%3AdFWRrhvqgMB4WP%2FjIpESou4ikPqkoGPefimZEtCaTt9KQSq%2B20wPGQ%3D%3D; QSI_HistorySession=https%3A%2F%2Fwww.tripadvisor.com.sg%2FRestaurants~1533811522547; TAAuth3=3%3Aa1e20af987caf9b7f2e3d715d71cd8d4%3AABwR3pxNIStPrcA7Zi46RsfsujSNA3I7GJk169ieF9cfJlnAOA2sHRrbJzS0dcMxegnf%2FN%2F2U2NKFU4EB3yJpMbpPOZb0eIN1NJg17NlouXzWMFkTL9V4SbxrAuOo%2F9HH%2F9S6LS3VHPRXTVy1M7a7xFBn%2FenvwiN7zMUXibBkVTMgw533gBhKsJWI1hd1n61oumSV45qrk%2F5%2F6KYUFET4Jg%3D; PAC=AKlo368cQeby8aGk0VnZljir1BEGGqmVA3Iymn-e1QuFW7y7r8oArkHc2xiu8i9fNW-jeR4euvlJLrGHLDwmVxMmC7R4_R8p__XSvvg04kGJlUVAAvVt06GefL92kttoLw%3D%3D; PMC=V2*MS.96*MD.20180809*LD.20180819; TAReturnTo=%1%%2FAttractions-g298184-Activities-Tokyo_Tokyo_Prefecture_Kanto.html; TART=%1%enc%3Aw6QMi5j164r1aaWxJY9JxnCElH0GEYgfNKuWfmwSDQ5I%2FNSbY1dvaDmjnRZPfKWWF4MXNLqS0zE%3D; CM=%1%HanaPersist%2C%2C-1%7Cpu_vr2%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7Cpv%2C2%2C-1%7Cpu_vr1%2C%2C-1%7CFtrPers%2C%2C-1%7Ctvsess%2C-1%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7Cbrandsess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7CTARSWBPers%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestPartPers%2C%2C-1%7Cvr_npu2%2C%2C-1%7CLastPopunderId%2C104-771-null%2C-1%7Csh%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7Cvr_npu1%2C%2C-1%7CCCPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CWarPopunder_Persist%2C%2C-1%7Cr_ta_2%2C%2C-1%7Cr_ta_1%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CSPHRSess%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C4%2C-1%7CPremiumSURPers%2C%2C-1%7Ccatchsess%2C9%2C-1%7CCpmPopunder_1%2C%2C-1%7CCCSess%2C%2C-1%7CCpmPopunder_2%2C4%2C-1%7CRestAdsPers%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CHomeAPers%2C%2C-1%7C+r_lf_1%2C%2C-1%7CSPHRPers%2C%2C-1%7CRCSess%2C%2C-1%7C+r_lf_2%2C%2C-1%7Ccatchpers%2C3%2C1535292739%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7Cpssamex%2C%2C-1%7Cbrandpers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CWarPopunder_Session%2C%2C-1%7CSCA%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CTARSWBSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; roybatty=TNI1625!AFqR7ATFCf5BGUAXxbLKloOxq3ijkVYf0DRPU3MnogjptORJ20l7mvo9cz4qHCK1FtCZQYJpUlyB7gQAfYB%2B4UHck4ZZUD4ltlidfRM0Bir%2FYKDREbwphF7TnkEwk7vQj9vPd%2Fz%2BLDUMz5wEc8q%2BIycZYpJz3eceMRx60q3RfuiU%2C1; TASession=V2ID.075847DC4F66A5B0EA7DFFC570929807*SQ.185*LS.PageMoniker*GR.68*TCPAR.37*TBR.35*EXEX.55*ABTR.57*PHTB.99*FS.91*CPU.31*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.C046DDFA89F7DF42D3E2657A089B8B5A*LF.en*FA.1*DF.0*MS.-1*RMS.-1*FLO.298184*TRA.true*LD.298184; TAUD=LA-1533811506689-1*RDD-1-2018_08_09*LG-876436396-2.1.F.*LD-876436397-.....'

base_url_list = [
    ('https://www.tripadvisor.com.sg/Attractions-g298184-Activities-oa%s-Tokyo_Tokyo_Prefecture_Kanto.html', 159, 'Tokyo'), 
    ('https://www.tripadvisor.com.sg/Attractions-g298566-Activities-oa%s-Osaka_Osaka_Prefecture_Kinki.html', 44, 'Osaka'),
    ('https://www.tripadvisor.com.sg/Attractions-g298564-Activities-oa%s-Kyoto_Kyoto_Prefecture_Kinki.html', 47, 'Kyoto'),
    ('https://www.tripadvisor.com.sg/Attractions-g298112-Activities-oa%s-Gifu_Gifu_Prefecture_Tokai_Chubu.html', 5, 'Gifu'),
    ('https://www.tripadvisor.com.sg/Attractions-g298106-Activities-oa%s-Nagoya_Aichi_Prefecture_Tokai_Chubu.html', 16, 'Nagoya'),
]


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


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
                    print('===Write excel ERROR===', str(one_row[col]))
    w.save(filename)
    print(filename+"===========over============")


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
            print(one_row)
            sheet1_data.append(one_row)
            if review_number > 0:
                request_sheet2(hotel_id, review_number, link)
            R_ID += 1
        except:
            raise
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
    return ''

def request_sheet2(hotel_id, number, hotel_url):
    global sheet2_data,  sheet3_data
    page_no = number / 5
    if number % 10 != 0:
        page_no += 1
    for i in range(0, page_no):
        if i >= 30:
            break
        try:
            url = get_review_url(hotel_url, i)
            html = get_request(url)
            print('sheet2', page_no, i, url)
            reg = '"review_(.*?)".*?avatar profile_.*?onclick=.*?>(.*?)<(.*?)UID_(.*?)-.*?ui_bubble_rating bubble_(.*?)".*?class="partial_entry">(.*?)<'

            comment_list = re.compile(reg).findall(html)
            for comment in comment_list:
                comment_ids.append(comment[0])
                username = comment[1]
                location = get_user_location(comment[2])
                uid = comment[3]
                rating = comment[4]
                text = commment[5]
                level, travel_style, user_url = get_level_of_uid(uid)
                [['ID', 'Hotel URL', 'Reviewer Name', 'Rating', 'Text Review', 'Reviewer Location', 'Contributor Level', 'Travel Style']]
                one_row = [hotel_id, hotel_url, username, rating[0], text, location, level, travel_style]
                sheet2_data.append(one_row)
                print(one_row)
                sheet3_data.append([uid, user_url])
        except Exception as e:
            print('ERROR-sheet2-', hotel_id, i, e)

def get_comment_detail(ids):
    url = 'https://www.tripadvisor.com.sg/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS'
    data = {
        'reviews': ','.join(ids),
        'widgetChoice': 'EXPANDED_REVIEW_RESPONSIVE'
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



reload(sys)
sys.setdefaultencoding('utf-8')

get_all()