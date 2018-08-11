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
from hyper.contrib import HTTP20Adapter

base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'
cookie = 'TASSK=enc%3AAH5dcQsPLPDkyrrSj9M%2Bz8qwTsnHuINWyBkBMCBtHpuDU4YR9911PLQiCrtLUXp510pmsBvZumlYMV4mfKw8qnZV%2FbzGN1Cpx%2BlqDMRQL0F6sD3r1fVjMsw7Oevw%2BWCV%2Fw%3D%3D; TAUnique=%1%enc%3AdFWRrhvqgMBfLkar6teR6%2Btv%2BarZM%2FpGd0j3x5%2F3%2FM%2BnJ1iTvWkb0Q%3D%3D; TART=%1%enc%3Am%2FmKXnKmau2u3%2B7moDID3A2g70jDJDlApZ70d5NG4ZnMZnVfKARquaAfoo4hlEMXkSj9GUxjwoU%3D; TALanguage=en; BEPIN=%1%16509e329d6%3Bbak210b.b.tripadvisor.com%3A10023%3B; PMC=V2*MS.33*MD.20180805*LD.20180809; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*DSM.1533830036720*AZ.1*RS.1; CM=%1%HanaPersist%2C%2C-1%7Cpu_vr2%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CSPHRSess%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpv%2C4%2C-1%7Cpu_vr1%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C8%2C-1%7CPremiumSURPers%2C%2C-1%7Ctvsess%2C-1%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7Ccatchsess%2C10%2C-1%7Cbrandsess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCpmPopunder_1%2C1%2C1533918288%7CCCSess%2C1%2C-1%7CCpmPopunder_2%2C5%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2CSGD%2C0%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7C+r_lf_1%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CSPHRPers%2C%2C-1%7CRCSess%2C%2C-1%7C+r_lf_2%2C%2C-1%7Ccatchpers%2C3%2C1534074184%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7Cvr_npu2%2C%2C-1%7CLastPopunderId%2C137-1859-null%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7Cvr_npu1%2C%2C-1%7CCCPers%2C%2C-1%7Ctvpers%2C1%2C1534185195%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cbrandpers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CWarPopunder_Session%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CWarPopunder_Persist%2C%2C-1%7CTheForkORPers%2C%2C-1%7Cr_ta_2%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7Cr_ta_1%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; ServerPool=C; TAReturnTo=%1%%2FRestaurant_Review%3Fg%3D294264%26reqNum%3D1%26puid%3DW2x2uwoQLGYAAcK6cB4AAAA4%26isLastPoll%3Dfalse%26d%3D3354291%26paramSeqId%3D0%26changeSet%3DREVIEW_LIST; PAC=AHJ4YoFxP25C31Msz0b0Nm7Elxlm7sv1bxTSa-H0LzmztbIf0Yx-ZJuVMIRwuHRAGUd0-4eQJkwUiEdje0iCodRa3aknwyuIMShnEWYYsmZ9oHeIzUIR4xqQcnJe0kMZ3EgUuyIU0fEKU0xwwIeFBjXGn7l8gDiw7PibjS8XbYIc; roybatty=TNI1625!APRrLT2EW%2B1h2KHDYG2jn49oUkVUtlwkGAfLJqOdrpX5CZrelshwTI2RYyOw68wBjJx9st9NOc6ZwuHSykc2eiAcWlmqzyD47TU0P13LjVsM5iKZWH4K10WdB0uhXsXkegThjGPHXSf1aamoHgOlVnZdzTcVtD0in6Ft6QF%2BX1gY%2C1; TASession=V2ID.A359B1B1C5A00212527116FD7F719C32*SQ.490*LS.ModuleAjax*GR.93*TCPAR.65*TBR.23*EXEX.64*ABTR.77*PHTB.90*FS.64*CPU.20*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*MS.-1*RMS.-1*FLO.304305*TRA.false*LD.3354291; TAUD=LA-1533469189911-1*RDD-1-2018_08_05*G-3265525-2.1.14209292.*HC-135546666*HDD-360835634-2018_08_19.2018_08_20*LG-368240319-2.1.T.*LD-368240320-.....'

uid_set = set()

sheet3_data = [['UID', 'restaurant url', 'restaurant name', 'rating', 'restaurant address', 'restaurant country']]


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

def post_request_2(url, data):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Referer': base_url,
        'Cookie': cookie,
        ':authority': 'www.tripadvisor.com.sg',
        ':method': 'POST',
        ':path': '/ModuleAjax?',
        ':scheme': 'https',
    }
    s = requests.Session()
    s.mount("https://www.tripadvisor.com.sg", HTTP20Adapter())
    resp = s.post(url, data=data, headers=headers)
    return resp.content.replace('\n', '').replace('\r', '')


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def read_excel(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            profile_id = row[0].value
            profile_url = row[1].value
            if profile_id not in uid_set:
                request_sheet3(profile_id, profile_url)
        except Exception as e:
            print(i, e)


def request_sheet3(uid, user_url):
    global sheet3_data
    html = get_request(user_url)
    reg = 'data-filter="REVIEWS_RESTAURANTS".*?\((.*?)\).*?member_id":"(.*?)"'
    data = re.compile(reg).findall(html)
    member_id = data[0][1]
    no_review = int(data[0][0])

    page_no = no_review / 50
    if no_review % 50 !=0 :
        page_no += 1

    for i in range(page_no):
        offset = str(i*50)
        data = {
            'token': 'TNI1625!ALLlbuwEjo0KgvUIpccYwBF/5Oc5Tdbaa8Wm2mIqXVTIiVvGz00u1N27aAa452BEajxlq5DCeFLebEYwf5jyEM6N4oUl6wbIxJY4Xq9g1rApsRfaHgxkiS3Nk/kYr32ySKTdzbhRDkjL82rW6QlJQIXhKLSWJ6TA7XHU5K7vcIuB',
            'version': '5',
            'authenticator': 'DEFAULT',
            'context': '{"modules.achievements.model.Level":[{"memberId":"' + member_id + '"}],"modules.common.model.LoggedInMember":[{}],"modules.membercenter.collection.MemberTags":[{"memberId":"' + member_id + '"}],"modules.common.model.Config":[{}],"modules.achievements.model.Badges":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.ContentStreamComposite":[{"offset":' + offset + ',"limit":50,"page":"PROFILE","memberId":"' + member_id + '"}],"modules.achievements.model.BadgeFlyoutView":[{}],"modules.membercenter.model.ProfileData":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.ContributionChecks":[{"memberId":"' + member_id + '"}],"modules.travelmap.model.TravelMapModel":[{"memberId":"' + member_id + '"}],"modules.achievements.model.Counts":[{"memberId":"' + member_id + '"}],"modules.achievements.model.EarnPointsCTA":[{}],"modules.social.model.SocialUser":[{}],"modules.achievements.model.LevelProgress":[{"memberId":"' + member_id + '"}],"modules.common.collection.PageLinks":[{}],"modules.common.model.Member":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.AboutMeView":[{}],"modules.membercenter.model.ContributionView":[{"memberId":"' + member_id + '"}],"modules.social.model.CompositeMember":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.MemberTagsView":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.ContributionCounts":[{"memberId":"' + member_id + '"}],"modules.membercenter.collection.DestinationExpert":[{"memberId":"' + member_id + '"}],"modules.common.model.Errors":[{}],"modules.achievements.model.NextAchievement":[{"memberId":"' + member_id + '"}],"modules.membercenter.collection.MemberInteractionInfo":[{"memberId":"' + member_id + '"}]}',
            'actions': '[{"name":"FETCH","resource":"modules.membercenter.model.ContentStreamComposite","params":{"offset":' + offset + ',"limit":50,"page":"PROFILE","memberId":"' + member_id + '","filter":"REVIEWS_RESTAURANTS"},"id":"clientaction664"}]',
        }
        resp = post_request('https://www.tripadvisor.com.sg/ModuleAjax?', data)
        get_comment_details(uid, resp)
    uid_set.add(uid)


def get_comment_details(uid, html):
    global sheet3_data
    write(html, '2.html')
    detail_reg = '"cuisine":.*?"url":"(.*?)","parent_string":"(.*?)".*?"name":"(.*?)"'
    rating_reg = '"url":(.*?)".*?"rating":(.*?),'
    url_rating_dict = {}
    rating_list = re.compile(rating_reg).findall(html)
    for rating in rating_list:
        url = rating[0]
        rating = rating[1]
        url_rating_dict[url] = rating
    detail_list = re.compile(detail_list).findall(html)
    for detail in detail_list:
        url = detail[1]
        rating = url_rating_dict.get(url, 0)
        address = remove_html_tag(detail[1])
        country = address.split(',')[-1]
        one_row = [uid, url, detail[2], rating, address, country]
        print(one_row)
        sheet3_data.append(one_row)


reload(sys)
sys.setdefaultencoding('utf-8')
# read_excel('/Users/zhaodan/Documents/personal/code/Scrape_Ngram/scraping/TripAdvisor/data/sheet3.xls')
# write_excel('data/sheet3.xls', sheet3_data)
member_id = 'S8+9ikaA6fBOaS6cfwcYOg=='
data = {
    'token': 'TNI1625!ALLlbuwEjo0KgvUIpccYwBF/5Oc5Tdbaa8Wm2mIqXVTIiVvGz00u1N27aAa452BEajxlq5DCeFLebEYwf5jyEM6N4oUl6wbIxJY4Xq9g1rApsRfaHgxkiS3Nk/kYr32ySKTdzbhRDkjL82rW6QlJQIXhKLSWJ6TA7XHU5K7vcIuB',
    'version': '5',
    'authenticator': 'DEFAULT',
    'context': '{"modules.achievements.model.Level":[{"memberId":"' + member_id + '"}],"modules.common.model.LoggedInMember":[{}],"modules.membercenter.collection.MemberTags":[{"memberId":"' + member_id + '"}],"modules.common.model.Config":[{}],"modules.achievements.model.Badges":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.ContentStreamComposite":[{"offset":' + '0' + ',"limit":50,"page":"PROFILE","memberId":"' + member_id + '"}],"modules.achievements.model.BadgeFlyoutView":[{}],"modules.membercenter.model.ProfileData":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.ContributionChecks":[{"memberId":"' + member_id + '"}],"modules.travelmap.model.TravelMapModel":[{"memberId":"' + member_id + '"}],"modules.achievements.model.Counts":[{"memberId":"' + member_id + '"}],"modules.achievements.model.EarnPointsCTA":[{}],"modules.social.model.SocialUser":[{}],"modules.achievements.model.LevelProgress":[{"memberId":"' + member_id + '"}],"modules.common.collection.PageLinks":[{}],"modules.common.model.Member":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.AboutMeView":[{}],"modules.membercenter.model.ContributionView":[{"memberId":"' + member_id + '"}],"modules.social.model.CompositeMember":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.MemberTagsView":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.ContributionCounts":[{"memberId":"' + member_id + '"}],"modules.membercenter.collection.DestinationExpert":[{"memberId":"' + member_id + '"}],"modules.common.model.Errors":[{}],"modules.achievements.model.NextAchievement":[{"memberId":"' + member_id + '"}],"modules.membercenter.collection.MemberInteractionInfo":[{"memberId":"' + member_id + '"}]}',
    'actions': '[{"name":"FETCH","resource":"modules.membercenter.model.ContentStreamComposite","params":{"offset":' + '0' + ',"limit":50,"page":"PROFILE","memberId":"' + member_id + '","filter":"REVIEWS_RESTAURANTS"},"id":"clientaction664"}]',
}
resp = post_request_2('https://www.tripadvisor.com.sg/ModuleAjax?', data)
print resp