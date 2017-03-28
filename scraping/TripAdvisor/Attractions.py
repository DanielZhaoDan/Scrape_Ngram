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
sheet1_data = [['ID', 'Category Name', 'Sub-category Name', 'link', 'Name', 'Overall rating', 'Number of reviews', 'Reserve Online', 'Excellent', 'Very good', 'Average', 'Poor', 'Terrible', 'Families', 'Couples', 'Solo', 'Business', 'Friends', 'Mar-May', 'Jun-Aug', 'Sep-Nov', 'Dec-Feb']]
sheet2_data = [['ID', 'Contributor Name', 'Contributor Location', 'Contributor country', 'Contributor level', 'Review headline', 'rating', 'Review date', 'Review text']]

cookie = 'TAUnique=%1%enc%3At96UkzAMTdkW6lFiox1vtOF0G7JUC0o%2B8PrsszjkOhv6gCLwstQoGQ%3D%3D; TALanguage=ALL; __gads=ID=5ef55ea1605b7b15:T=1486869665:S=ALNI_Mbbc923rnxCTOoA0IgyOXeoJpNFnw; BEPIN=%1%15b09c0cf96%3Bbak92a.a.tripadvisor.com%3A10023%3B; ServerPool=A; TASSK=enc%3AAKox3FSR%2BNtLTvMA%2BD%2BvYBM5wgOGF8fpCmRVbisB4dHK4zgX3kcgEaYINdiesPjjvp2WL3Z%2B4UK2B5d9fts6rlzS0%2B44b0OscCB1ntuQbrdtmEbM8GUE5Tg6uB0xKvVVvA%3D%3D; PMC=V2*MS.74*MD.20170305*LD.20170326; PAC=AENveR8DQ2uYTl_wjOzxJKOPSXkRL6HY-zt5EEOdDEWdznjcMN9aVBZJw9FZUyIkRtXSbHplHJ5NYIsqH6NidVDqZU9Q11HXzj6R3nd1YyTziNywN5NAoA8DDawA37dsC5cNABlZHgGQdyRDvXJa1zXFTh95cqHUWYXDvmvWovtd-I_FbfcZxZatp4-oPF6CHwcUrhEkiToPQE0gB1BZgPpwCf5XY4eM96OBpStPQBbORNTk3GK7mE9XcM5p-b_86dSGDxEgm3Qz7KNEAFaMgti8w829FbRf-h8_h25IXlcDK8Vq5y7FAD8frTsr1IYiqqmigIWQ-OTtsejz8RSYTlJVqaqwOz61ZQ-NPY5Ce0M1DOuyELuXVbQQf2ASprTN2Cq-V1c4b-bG3YmPaX9JMwdrXgS2jOzyW9lVQBhcwEa46Lk_xjARYXcYnN72vAFR6FKJYOTHe5f4GWUxamryc1BMAeTO3CMIh58I0kAYAOIuJTx3ZIk1AhpTLC0a9MiSSvCYwwPolWf4qz3n9bdbv0g%3D; VRMCID=%1%V1*id.13873*llp.%2FUpdateSessionDatesAjax%3Fsupli%3D%26gclid%3DCj0KEQjwzd3GBRDks7SYuNHi3JEBEiQAIm6EIwAUWUpCGI_s3ESLk4nsl3fhEXHa4r5gdkvhNIcjLj0aAgC48P8HAQ%26supsc%3Ds%26supap%3D1t1%26supti%3Dkwd-119671122%26suplp%3D9062542%26supdv%3Dc%26supbk%3D1%26m%3D13873%26supai%3D38980285917%26supnt%3Dg%26supci%3D695518186-a_supli%5C.-a_supti%5C.kwd__2D__119671122-a_supdv%5C.c-m13873-a_gclid%5C.Cj0KEQjwzd3GBRDks7SYuNHi3JEBEiQAIm6EIwAUWUpCGI__5F__s3ESLk4nsl3fhEXHa4r5gdkvhNIcjLj0aAgC48P8HAQ-a_supsc%5C.s-a_supap%5C.1t1-a_suplp%5C.9062542-a_supbk%5C.1-a_supai%5C.38980285917-a_supci%5C.695518186-a_supnt%5C.g*e.1491122084813; TART=%1%enc%3AFupRYqMdb7TxNDCw1wDMXxO02jVEYcSKyjLoawJdTC%2FVpFvWgpRrGMsPF7rdWymNg1ukKbolbFs%3D; CommercePopunder=SuppressAll*1490517439791; TATravelInfo=V2*AC.SIN*A.2*MG.-1*HP.2*FL.3*RVL.294226_85l2137226_85l814892_85l3220900_85l293961_85*RS.1; TAReturnTo=%1%%2FAttractions-g293961-Activities-Sri_Lanka.html; TASession=%1%V2ID.70060A328778B4F03545A960A5B0CC68*SQ.59*PR.39415%7C*LS.AttractionProductDetail*GR.92*TCPAR.21*TBR.25*EXEX.33*ABTR.67*PHTB.77*FS.53*CPU.86*HS.popularity*ES.relevance*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*FBH.2*MS.-1*RMS.-1*FLO.293961*TRA.true*LD.293962; CM=%1%HanaPersist%2C%2C-1%7Cpu_vr2%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CHanaSession%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpv%2C8%2C-1%7Cpu_vr1%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C2%2C-1%7CPremiumSURPers%2C%2C-1%7CPCBSess%2C-1%2C-1%7Ctvsess%2C2%2C-1%7CPremiumMCSess%2C%2C-1%7Ccatchsess%2C5%2C-1%7Cbrandsess%2C%2C-1%7Csesscoestorem%2C%2C-1%7CCpmPopunder_1%2C%2C-1%7CCCSess%2C%2C-1%7CCpmPopunder_2%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7Cperscoestorem%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CHomeAPers%2C%2C-1%7C+r_lf_1%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7C+r_lf_2%2C%2C-1%7Ccatchpers%2C3%2C1491122090%7CPCBPers%2C1%2C1493109411%7CLaFourchette+MC+Banners%2C%2C-1%7Cbookstickcook%2C%2C-1%7Cvr_npu2%2C%2C-1%7Csh%2CRuleBasedPopup%2C1490603811%7CLastPopunderId%2C104-771-null%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7C2016sticksess%2C%2C-1%7Cvr_npu1%2C%2C-1%7CCCPers%2C%2C-1%7Ctvpers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cbrandpers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7C2016stickpers%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CWarPopunder_Session%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CWarPopunder_Persist%2C%2C-1%7CTakeOver%2C%2C-1%7Cr_ta_2%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7Cr_ta_1%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRBASess%2C%2C-1%7Cbookstickpers%2C%2C-1%7Cperssticker%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TAUD=LA-1490517283415-1*LG-3889947-2.1.F.*LD-3889948-.....; roybatty=TNI1625!AJiYxe2oLqHutcStpPZFJOO%2BrnaGuQuYGFq5b84s7g%2BLHG3h8trI5ZZJItxwNPHYfVwapjOa79DDuJ3lal9gRTKnUoh7TN9NkiX5x0q45a8SJfw46IdanmzHeZzWBI5JTk2vVMjg%2BXp8PW8Jb1%2F6HXzdu30W2gUwPr6bHR0Mg%2BNX%2C1'

base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'
parsed_url = [base_url]


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


def request_sheet1(category, url, sub_category):
    print category, url, sub_category
    global sheet1_data, R_ID
    raw_reg = 'class="listing_title".*?href="(.*?)".*?>(.*?)</div.*?class="listing_rating"(.*?)class="tag_line".*?listing_commerce.*?</div(.*?)</div'
    html = get_request(url)
    topic_body = re.compile(raw_reg).findall(html)
    if not topic_body:
        return
    for detail in topic_body:
        try:
            hotel_id = category + str(R_ID)
            link = 'https://www.tripadvisor.com.sg' + detail[0]
            name = remove_html_tag(detail[1])

            avg_rating, review_number = global_rating_details(detail[2])
            can_booking = 0
            if 'booking option' in detail[3]:
                can_booking = 1
            rating_details, comment_page = get_rating_detail_and_comment_page(link)
            one_row = [hotel_id, category, sub_category, link, name, avg_rating, review_number, can_booking] + rating_details
            sheet1_data.append(one_row)
            get_contributor_details(hotel_id, link, comment_page)
            R_ID += 1
        except:
            raise
            print 'ERR---level 1---' + url


def global_rating_details(ori):
    reg = 'alt="(.*?) of 5 bubbles".*?#REVIEW.*?>(.*?) review'
    if 'of 5 bubbles' in ori and '#REVIEW' in ori:
        data = re.compile(reg).findall(ori)
        return data[0][0], data[0][1].replace(',', '')
    return 0, 0


def get_contributor_details(r_id, link, number):
    reg = 'div id="review_(.*?)".*?class="col1of2"(.*?)class="col2of2".*?class=\'noQuotes\'>(.*?)<.*?class="rate sprite-rating_s rating_s.*?alt="(.*?) of.*?class="ratingDate(.*?)<'
    url_prefix = link.split('-Reviews-')[0].replace('Attraction_Review', 'ExpandedUserReviews')
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
            if len(rating_detail) == len(contri_detail):
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
    url = url_prefix+'?target='+str(review_ids[0])+'&context=1&servlet=Attraction_Review&expand=1&reviews='+reviews
    reg = '<div class="entry">(.*?)</div>(.*?)class="note"'
    try:
        html = get_request(url)
    except:
        print 'EXC---'+url
        return ['']
    details = re.compile(reg).findall(html)
    res = []
    for detail in details:
        text = remove_html_tag(detail[0])
        res.append([text])
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
        return [x.replace('(', '').replace(')', '') for x in details[0][:-1]], details[0][-1]
    else:
        details = re.compile(reg).findall(html)
        if details:
            return [x.replace('(', '').replace(')', '') for x in details[0]], 0
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
    req.add_header("Referer", base_url)
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


reload(sys)
sys.setdefaultencoding('utf-8')

first_levels = get_category_urls(base_url)
for first_level in first_levels:
    print first_level.get('url', '')
    second_levels = get_category_urls(first_level.get('url', ''), is_second_level=True)
    for second_level in second_levels:
        if second_level.get('count', 0) >= 10:
            request_sheet1(first_level['name'], second_level['url'], second_level['name'])
    write_excel('data/sheet1.xls'.replace('sheet', first_level['name']), sheet1_data)
    write_excel('data/sheet2.xls'.replace('sheet', first_level['name']), sheet2_data)
    del sheet1_data
    del sheet2_data
    R_ID = 1
    sheet1_data = [['ID', 'Category Name', 'Sub-category Name', 'link', 'Name', 'Overall rating', 'Number of reviews',
                    'Reserve Online', 'Excellent', 'Very good', 'Average', 'Poor', 'Terrible', 'Families', 'Couples',
                    'Solo', 'Business', 'Friends', 'Mar-May', 'Jun-Aug', 'Sep-Nov', 'Dec-Feb']]
    sheet2_data = [['ID', 'Contributor Name', 'Contributor Location', 'Contributor country', 'Contributor level',
                    'Review headline', 'rating', 'Review date', 'Review text']]



