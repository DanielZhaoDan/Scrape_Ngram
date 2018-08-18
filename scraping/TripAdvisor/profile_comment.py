# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
import HTMLParser
import os
import xlrd
import requests


base_url = 'https://www.tripadvisor.com.sg/Attractions-g293961-Activities-Sri_Lanka.html'
cookie = 'TASSK=enc%3AAD81SzjY4jrIQcPkjzJz7Cp8v5NGL0I3x3IA2yERdvV9ltUkEWMS69q8lEHwus9jgcICVOthH%2FB9uX2T4DuUjt6GiMprs0o%2Fzr3%2FNWMfxAdVzKlXihxIaYKXQYtEsoCGbQ%3D%3D; ServerPool=A; TART=%1%enc%3Ah4YqXu170Xo7RSAeAP4BAsRNHeuCiWOwpgl9dT5Cb52o9IJZof%2BLP4ccuFB07TXofTM2Cx7kRNA%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; TAUnique=%1%enc%3AJmHUk8pWi6mHhipe7XvReuOD6W%2FcxQckcmqn%2BbhjfG02jHwltRJPGQ%3D%3D; CM=%1%HanaPersist%2C%2C-1%7Cpu_vr2%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CSPHRSess%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpu_vr1%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C2%2C-1%7CPremiumSURPers%2C%2C-1%7Ctvsess%2C1%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7Ccatchsess%2C3%2C-1%7Cbrandsess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCpmPopunder_1%2C2%2C1534215420%7CCCSess%2C%2C-1%7CCpmPopunder_2%2C2%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7C+r_lf_1%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CSPHRPers%2C%2C-1%7CRCSess%2C%2C-1%7C+r_lf_2%2C%2C-1%7Ccatchpers%2C3%2C1534392618%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7Cvr_npu2%2C%2C-1%7Csh%2C%2C-1%7CLastPopunderId%2C137-1859-null%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7Cvr_npu1%2C%2C-1%7CCCPers%2C%2C-1%7Ctvpers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cbrandpers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CWarPopunder_Session%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CWarPopunder_Persist%2C%2C-1%7CTheForkORPers%2C%2C-1%7Cr_ta_2%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7Cr_ta_1%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TAReturnTo=%1%%2FRestaurant_Review-g294265-d3470146-Reviews-Tiong_Bahru_Food_Centre-Singapore.html; PAC=AES-H73s8AVamHwCLYxQRwUsn7uNqJJzjFj1YEz0_uL6HVdgq35rrQynLVkU3iG19xmvz-lW4xSYOIFDyew0Y5e0v84odiFqkDX8miSG3gzuIM4F4wOkHZCithT2T2fNPQ%3D%3D; PMC=V2*MS.26*MD.20180809*LD.20180813; roybatty=TNI1625!AGUVBNdaWXIRQ%2BbZ08HCL74xFqZ6asE2otjYZ5TdDC%2BFz8tp26ileVd%2Fce44%2BU9StiB4lgjYDx3P38aohfeaZSod9J6afe1%2FdbxrWWzFBH9NRVHTB9gP1Rppidh7yV85EmcnZ0J14dDU%2F%2BldR3qRep4cDjBWe3BdzS1bsyxQzVYM%2C1; TASession=V2ID.8920266B5D93BEAB025E27EE87F403DB*SQ.82*LS.DemandLoadAjax*GR.88*TCPAR.62*TBR.30*EXEX.37*ABTR.97*PHTB.31*FS.69*CPU.44*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*MS.-1*RMS.-1*TRA.true*LD.3470146; TAUD=LA-1533787806048-1*RDD-1-2018_08_09*LG-383584131-2.1.F.*LD-383584132-.....'

uid_set = set()

sheet3_data = [['UID', 'restaurant url', 'restaurant name', 'rating', 'restaurant address', 'restaurant country']]


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    if 'data' not in filename:
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


def post_request(url, data):
    headers = {
        'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
        'origin': 'https://www.tripadvisor.com.sg',
        'pragma': 'no-cache',
        'referer': 'https://www.tripadvisor.com.sg/members/JoyceGKK',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'x-puid': 'W28eFQoQL4cAAi1njkcAAADA',
        'x-requested-with': 'XMLHttpRequest',
    }

    resp = requests.post(url, data=data, headers=headers)
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


def pre_load(filename, start=1):
    global uid_set
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            profile_id = row[0].value
            uid_set.add(profile_id)
        except Exception as e:
            print(i, e)


def request_sheet3(uid, user_url):
    global sheet3_data
    print user_url,
    html = get_request(user_url)
    reg = 'JS_SECURITY_TOKEN = "(.*?)".*?data-filter="REVIEWS_RESTAURANTS".*?\((.*?)\).*?member_id":"(.*?)"'
    data = re.compile(reg).findall(html)
    member_id = data[0][2]
    no_review = int(data[0][1].replace(',',''))
    token = data[0][0]

    page_no = no_review / 50
    if no_review % 50 != 0:
        page_no += 1
        try:
            request_one(member_id, page_no, uid, token)
        except:
            print('EXCEPTION--', uid, member_id)


def request_one(member_id, page_no, uid, token):
    length = 0
    for i in range(page_no):
        offset = str(i*50)
        context ='{"modules.achievements.model.Level":[{"memberId":"' + member_id + '"}],"modules.common.model.LoggedInMember":[{}],"modules.membercenter.collection.MemberTags":[{"memberId":"' + member_id + '"}],"modules.common.model.Config":[{}],"modules.achievements.model.Badges":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.ContentStreamComposite":[{"offset":' + offset + ',"limit":50,"page":"PROFILE","memberId":"' + member_id + '"}],"modules.achievements.model.BadgeFlyoutView":[{}],"modules.membercenter.model.ProfileData":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.ContributionChecks":[{"memberId":"' + member_id + '"}],"modules.travelmap.model.TravelMapModel":[{"memberId":"' + member_id + '"}],"modules.achievements.model.Counts":[{"memberId":"' + member_id + '"}],"modules.achievements.model.EarnPointsCTA":[{}],"modules.social.model.SocialUser":[{}],"modules.achievements.model.LevelProgress":[{"memberId":"' + member_id + '"}],"modules.common.collection.PageLinks":[{}],"modules.common.model.Member":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.AboutMeView":[{}],"modules.membercenter.model.ContributionView":[{"memberId":"' + member_id + '"}],"modules.social.model.CompositeMember":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.MemberTagsView":[{"memberId":"' + member_id + '"}],"modules.membercenter.model.ContributionCounts":[{"memberId":"' + member_id + '"}],"modules.membercenter.collection.DestinationExpert":[{"memberId":"' + member_id + '"}],"modules.common.model.Errors":[{}],"modules.achievements.model.NextAchievement":[{"memberId":"' + member_id + '"}],"modules.membercenter.collection.MemberInteractionInfo":[{"memberId":"' + member_id + '"}]}'
        actions = '[{"name":"FETCH","resource":"modules.membercenter.model.ContentStreamComposite","params":{"offset":' + offset + ',"limit":50,"page":"PROFILE","memberId":"' + member_id + '","filter":"REVIEWS_RESTAURANTS"},"id":"clientaction741"}]'
        data = {
            'token': token,
            'version': '5',
            'authenticator': 'DEFAULT',
            'context': context,
            'actions': actions,
        }
        resp = post_request('https://www.tripadvisor.com.sg/ModuleAjax?', data)
        length += get_comment_details(uid, resp)
    if length > 0:
        uid_set.add(uid)
    print(length)


def get_comment_details(uid, html):
    global sheet3_data
    detail_reg = '"cuisine":.*?"url":"(.*?)","parent_string":"(.*?)".*?parent_id":(.*?),.*?"name":"(.*?)"'
    rating_reg = '"locationId":(.*?),.*?"rating":(.*?),'
    url_rating_dict = {}
    rating_list = re.compile(rating_reg).findall(html)
    for rating in rating_list:
        url = rating[0]
        rating = rating[1]
        url_rating_dict[url] = rating
    detail_list = re.compile(detail_reg).findall(html)
    for detail in detail_list:
        url = 'https://www.tripadvisor.com.sg' + detail[0].replace('\u002F', '/')
        key = url.split('-')[2].replace('d', '')
        rating = url_rating_dict.get(key, 0)
        address = remove_html_tag(detail[1])
        country = address.split(',')[-1]
        one_row = [uid, url, detail[3], rating, address, country]
        sheet3_data.append(one_row)
    return len(detail_list)


reload(sys)
sys.setdefaultencoding('utf-8')
pre_load('/Users/zhaodan/Documents/personal/code/Scrape_Ngram/scraping/TripAdvisor/data/sheet3_comment.xlsx')
print('preload size: ', len(uid_set))
read_excel('/Users/zhaodan/Documents/personal/code/Scrape_Ngram/scraping/TripAdvisor/data/sheet3.xls')
write_excel('/Users/zhaodan/Documents/personal/code/Scrape_Ngram/scraping/TripAdvisor/data/sheet3_.xls', sheet3_data)