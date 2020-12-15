# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
import json
from scraping.utils import post_request_json, get_request_html, write_html, write_excel

saved_hotel = set()
R_ID = 1
sheet1_data = [['ID', 'Hotel URL', 'Hotel Name', 'Address', 'Rating', 'Number of reviews', 'Star', 'Amenities']]
sheet2_data = [['Hotel URL', 'Reviewer Name', 'Review Date' 'Rating', 'Reviewer Location']]
sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]

cookie = 'TADCID=c2bevLVd4OPVw503ABQCjnFE8vTET66GHuEzPi7KfV8tUou66XdIemKmPKfsCPHQfdv4PInKBM8C97eUZrB6Eqeg3IC34pkFTk8; TAAUTHEAT=SauzFQK9qlqNoDiJABQC5pMD6MhQQX22iUWVeLafiR8EUuGQddQ1WIBUET49l7qV_Jr2uIAf3avgX9lHkuxKj-oW9jOdB5kLy_cOJxLD6Nr5FCxY13i-Y3wH1LxBaeHNiHxJEyh3nPVmlYixDfdqjmWVa-IxIRulyacayIDETTWZQ4TwH-zNWtg2ShTeQfPMseEyhzdm7wkisMyW-VFChGEFRg; TAUnique=%1%enc%3ASLqk%2B6khUnzArkIWpky3yAfBM5Uq3N0u36Bu3YaBBnSRqDIW%2BjDBvQ%3D%3D; TASSK=enc%3AAJV0znQAi190Y2FwWBbr%2FWkHmjUPreYrqWhcXgDHdP896aKkgasX%2FDbb3MqkDZqcNwAC2HmMBz2pmRDdSfDZakf6gzCjLv3IioR%2BVNux3lVRLS%2FbPyD%2BJi502ZqBoIMhvg%3D%3D; ServerPool=X; PMC=V2*MS.30*MD.20200801*LD.20200801; TART=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; health_notice_dismissed=1; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7Cpv%2C2%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CCrisisSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CRepTarMCSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7CTSMCPers%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CCOVIDMCSess%2C%2C-1%7CTARSWBPers%2C%2C-1%7CListMCSess%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7Cmdpers%2C1%2C1596871674%7CSPACMCSess%2C%2C-1%7Cmds%2C1596272225474%2C1596358625%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7CRevHubRMPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2CRuleBasedPopup%2C1596353274%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCrisisPers%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7CRepTarMCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CTSMCSess%2C%2C-1%7CSPMCPers%2C%2C-1%7CRevHubRMSess%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CCOVIDMCPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CSPACMCPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CListMCPers%2C%2C-1%7Cmdsess%2C-1%2C-1%7C; PAC=ABv6OOeS5Ee3a8SVtxpWuywMbX9HaE0CCm1BY822rlizMqmO8TT2FRPFXbU1qm-9I5c7DUz1YCOzILGUo2MkIXbHmGYpeIc4AJ1Uk5lSQeMMNKrlAXDGKsF4mQEOnUDpI6P23lIdxYz3oKv53H656cf19g9MQ5TDI6aMAJCzBYJYHlf5R_-BFAUuNRyMPRA9XO_JGx_BDOOf_4RGCARcA-Q%3D; SRT=%1%enc%3AwK5CFqZMt8hZj%2FKKyrMOeoLrh8%2BBxYvbZT82T5c4m%2BK1WaVQSdYSBg4vruuMvsFrIU%2BEqedIMpQ%3D; BEPIN=%1%173ad2014fe%3Bweb225a.a.tripadvisor.com%3A30023%3B; TATravelInfo=V2*AY.2020*AM.8*AD.9*DY.2020*DM.8*DD.10*A.2*MG.-1*HP.2*FL.3*DSM.1596337427798*AZ.1*RS.1; TAReturnTo=%1%%2FHotel_Review-g4327828-d13286407-Reviews-Permatang_Village_Homestay-Ayer_Hitam_Johor.html; roybatty=TNI1625!APNLRl50294EEtmdTJC5SZrDwQUGkiP29kJE1QXV8xlqBfWpmRHIRXlfr5v0xzTtymbe1aWeFosuii0U8IPcz26PuzC%2BooXwlW90GGM3Z47Crtk51NUl4BtxHW%2BmRE44FD8hIJUBqtGQ2neSRjZ8Aj8uaJm5i1U5ExulMEbEynxo%2C1; TASession=%1%V2ID.9A53E4DA9B8FF660066B23DE9688140E*SQ.356*LS.DemandLoadAjax*GR.96*TCPAR.26*TBR.50*EXEX.16*ABTR.24*PHTB.24*FS.68*CPU.18*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.ABD562818D249697A8AB4E2FFBFCE092*FA.1*DF.0*TRA.true*LD.13286407*EAU.%5B; TAUD=LA-1596265332138-1*RDD-1-2020_08_01*ARDD-960203-2020_09_30.2020_10_01*HD-6893344-2020_08_04.2020_10_01.298305*G-6893345-2.1.298305.*HC-71305081*HDD-72095550-2020_08_09.2020_08_10.1*LD-72100807-2020.8.9.2020.8.10*LG-72100810-2.1.T.; __vt=K8ITwbhufVclNAW8ABQCq4R_VSrMTACwWFvfTfL3vw8Pq1X4wCspI_XLoHhJ1N6oVIGpuLE5q13Oye-tDRE3NUThsibOvkvNzQpFDWzwFzYtjOrGGwD1cPteYqQOPiGSnDQjdAy_eOARtcCQWiEWUpD10g'

urls = [
    # ('https://www.tripadvisor.com.my/VacationRentals-g298277-Johor-Vacation_Rentals.html', 'Johor'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298281-Kedah-Vacation_Rentals.html', 'Kedah'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298284-Kelantan-Vacation_Rentals.html', 'Kelantan'),
    # (
    #     'https://www.tripadvisor.com.my/VacationRentals-g306997-Melaka_Central_Melaka_District_Melaka_State-Vacation_Rentals.html',
    #     'Melaka'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298289-Negeri_Sembilan-Vacation_Rentals.html', 'Negeri_Sembilan'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298291-Pahang-Vacation_Rentals.html', 'Pahang'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298297-Perak-Vacation_Rentals.html', 'Perak'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298301-Perlis-Vacation_Rentals.html', 'Perlis'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298306-Sabah-Vacation_Rentals.html', 'Sabah'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298308-Sarawak-Vacation_Rentals.html', 'Sarawak'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298310-Selangor-Vacation_Rentals.html', 'Selangor'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298318-Terengganu-Vacation_Rentals.html', 'Terengganu'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298570-Kuala_Lumpur_Wilayah_Persekutuan-Vacation_Rentals.html',
    #  'Kuala_Lumpur'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298286-Labuan_Island_Sabah-Vacation_Rentals.html', 'Labuan'),
    # ('https://www.tripadvisor.com.my/VacationRentals-g298305-Putrajaya_Wilayah_Persekutuan-Vacation_Rentals.html',
    #  'Putrajaya'),
    ('https://www.tripadvisor.com.my/VacationRentals-g298302-Reviews-Penang-Vacation_Rentals.html', 'Penang'),
]

uid_level_dict = {}


def get_page_no(html):
    if 'class="pageNumbers"' not in html:
        return 1
    page_reg = 'data-page-number="(.*?)"'

    data = re.compile(page_reg).findall(html)

    if data:
        return int(data[-1])


def request_sheet1(item):
    global sheet1_data
    url, state = item
    gid = url.split('-g')[-1].split('-')[0]

    page_no = None
    i = 1
    url = 'https://www.tripadvisor.com.my/data/graphql/batched'

    headers = {
        'x-requested-by': 'TNI1625!ABYOrkIW0bgTX+m40IrHpHzz4crc0PJ9ShJyQoDVvo4qbckqTjbHPfiNgiLQ0MukWpyV/eRzPc8N4SD7oAtTa4k80Mnxsn1MjOrZRw3KIRFmUqN1I/2C7AIZu2wxQE52mkTnfVv7bec9TJsPZrKx7rJR+6lHnKCl5KDhwOmNH6fk',
        'content-type': 'application/json',
        'accept': '*/*',
    }

    while True:
        try:
            body = [{
                "query": "query ListingsForGeo($geoId: Int!, $offset: Int!, $rentalCountLimit: Int!, $guests: Int, $bathrooms: Int, $bedrooms: Int, $arrival: String, $departure: String, $minPrice: Int, $maxPrice: Int, $amenities: [Int], $communities: [Int], $distinctiveFeatures: [Int], $neighborhoods: [Int], $propertyTypes: [Int], $suitability: [Int], $poiDistance: Int, $poiLocationId: Int, $poiUnits: RentalInformation_LegacyPOIFilterUnit, $showHomeAway: Boolean, $showMoreHomeAway: Boolean, $currencyCode: String, $urlParams: [RentalInformation_URLParamInput], $sortOrder: RentalInformation_LegacySortOrder, $orderingId: Int) {\n  RentalInformation_legacyRentalSearch(requests: {geoId: $geoId, servletName: \"VacationRentals\", pageSize: $rentalCountLimit, orderingId: $orderingId, paginationStart: $offset, currencyCode: $currencyCode, travelerInfo: {guests: $guests, minBedrooms: $bedrooms, minBathrooms: $bathrooms, arrival: $arrival, departure: $departure}, filterParameters: {sortOrder: $sortOrder, showHomeAway: $showHomeAway, showMoreHomeAway: $showMoreHomeAway, urlParams: $urlParams}, filters: {minPrice: $minPrice, maxPrice: $maxPrice, amenities: $amenities, communities: $communities, distinctiveFeatures: $distinctiveFeatures, neighborhoods: $neighborhoods, propertyTypes: $propertyTypes, suitability: $suitability, poiFilter: {distance: $poiDistance, locationId: $poiLocationId, unit: $poiUnits}}}) {\n    listings {\n      locationId\n      rate {\n        ...RentalRateFields\n      }\n      rental {\n        ...RentalFields\n      }\n    }\n    ...FilteredRentalInfoFields\n    ...BreadcrumbsFields\n    ...AvailableFiltersFields\n    pollingDone\n  }\n}\n\nfragment RentalFields on RentalInformation_LegacyRental {\n  id\n  name\n  url\n  bathCount\n  sleepCount\n  roomCount\n  userReviewCount\n  averageRatingNumber\n  hasCOE\n  hasPaymentProtection\n  isAffiliate\n  affiliateLogoUrl\n  travelersChoice {\n    hasTravelersChoice\n    header\n    url\n  }\n  titleInfo {\n    title\n    reqLang\n    srcLang\n  }\n  photos {\n    description\n    jumboUrl\n    landscape\n    largeUrl\n    largestHeight\n    largestWidth\n    medUrl\n    stdHeight\n    stdWidth\n    thumbHeight\n    thumbWidth\n    thumbnailUrl\n  }\n  paymentStats {\n    totalPayments\n  }\n  geoCoordinates {\n    lat\n    lng\n  }\n  quickView {\n    address\n    description\n    rentalCategory\n    mostRecentReviews {\n      text\n      rating\n      title\n      isMT\n      mtMarkUp\n      url\n    }\n    amenities {\n      key\n      value {\n        localizedText\n        value\n      }\n    }\n  }\n}\n\nfragment AvailableFiltersFields on RentalInformation_LegacyRentalSearchResponseBody {\n  availableFilters {\n    histogramBuckets\n    checkboxFilters {\n      suitability {\n        localizedName\n        list {\n          localizedName\n          ordinal\n          count\n        }\n      }\n      amenities {\n        localizedName\n        list {\n          localizedName\n          ordinal\n          count\n        }\n      }\n      propertyType {\n        localizedName\n        list {\n          localizedName\n          ordinal\n          count\n        }\n      }\n      distinctiveFeatures {\n        localizedName\n        list {\n          localizedName\n          ordinal\n          count\n        }\n      }\n      communities {\n        localizedName\n        list {\n          localizedName\n          ordinal\n          count\n        }\n      }\n      neighborhoods {\n        localizedName\n        list {\n          localizedName\n          ordinal\n          count\n        }\n      }\n    }\n  }\n}\n\nfragment RentalRateFields on RentalInformation_LegacyRate {\n  total {\n    amount\n    currency\n  }\n  isInstantBook\n  minStay\n  details {\n    name\n    type\n    isOptional\n    rate {\n      amount\n      currency\n    }\n  }\n  checkoutUrls {\n    key\n    value\n  }\n}\n\nfragment BreadcrumbsFields on RentalInformation_LegacyRentalSearchResponseBody {\n  breadcrumbs {\n    url\n    name\n    index\n  }\n}\n\nfragment FilteredRentalInfoFields on RentalInformation_LegacyRentalSearchResponseBody {\n  filteredRentalInfo {\n    averagePrice\n    totalRentals\n    totalUnfilteredRentals\n    centerLatitude\n    centerLongitude\n    rentalMatchData {\n      matchData {\n        key\n        value {\n          matchNames\n          neighborhood\n        }\n      }\n    }\n  }\n}\n",
                "variables": {"offset": (i - 1) * 50, "rentalCountLimit": 50, "currencyCode": "MYR", "locale": "en_MY",
                              "urlParams": [{"key": "g", "value": gid}, {"key": "geo", "value": gid},
                                            {"key": "page", "value": "VacationRentals"}],
                              "sortOrder": "TRAVELERRATINGHIGH", "orderingId": 160, "showHomeAway": 'false',
                              "showMoreHomeAway": 'false', "guests": 2, "geoId": int(gid)}}]

            json_obj = post_request_json(url, cookie, data=json.dumps(body), add_header=headers)

            if not page_no:
                page_no = json_obj[0].get('data', {}).get('RentalInformation_legacyRentalSearch', {}).get(
                    'filteredRentalInfo', {}).get('totalRentals')

            print i, page_no, state
            if (i + 1) > page_no:
                break

            data = json_obj[0].get('data', {}).get('RentalInformation_legacyRentalSearch', {}).get('listings', [])

            for item in data:
                hotel = item.get('rental')
                if hotel:
                    hote_url = 'https://www.tripadvisor.com.my' + hotel['url']
                    name = hotel['name']
                    classification = 'HOLIDAY RENTAL'
                    rating = hotel['averageRatingNumber']
                    if rating < 0:
                        rating = 0
                    no_reviews = hotel['userReviewCount']

                    one_row = [state, name, hote_url, no_reviews, rating, classification]
                    sheet1_data.append(one_row)

            i += 1
        except Exception as e:
            print 'ERR---', url, i, e


def request_sheet2(number, hotel_url):
    global sheet2_data, sheet3_data
    page_no = number / 5
    if number % 5 != 0:
        page_no += 1
    for i in range(0, page_no):
        if i >= 40:
            break
        try:
            url_list = hotel_url.split('-')
            url = '-'.join(url_list[:3]) + '-or%s-' % str(i * 10) + '-'.join(url_list[3:])
            print i, page_no, url

            html = get_request_html(url, cookie)

            reg = 'class="username mo">.*?>(.*?)<(.*?)class="mainContent".*?ui_bubble_rating bubble_(.*?)".*?relativeDate" title=\'(.*?)\''

            comment_list = re.compile(reg).findall(html)
            for comment in comment_list:
                name = comment[0]
                country = get_user_location(comment[1])
                rating = int(comment[2]) / 10.0
                review_date = get_comment_date(comment[3])
                one_row = [hotel_url, name, review_date, rating, country]
                sheet2_data.append(one_row)

        except Exception as e:
            print('ERROR-sheet2-', url, i, e)


def get_comment_date(ori):
    try:
        date = datetime.strptime(ori, '%d %B %Y')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_user_location(ori):
    if 'expand_inline userLocation' in ori:
        reg = 'expand_inline userLocation">(.*?)<'
        data = re.compile(reg).findall(ori)
        return data[0]
    return 'N/A'


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def read_excel(filename, start=1):
    global R_ID, sheet2_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        main_url = row[2].value

        try:
            review_no = int(row[3].value)
            if review_no > 0:
                request_sheet2(review_no, main_url)
        except Exception as e:
            print main_url, e
    write_excel('Holiday_sheet2.xls', sheet2_data)


def step_1():
    for item in urls:
        request_sheet1(item)
        write_excel(item[1] + '_holiday.xls', sheet1_data)


reload(sys)
sys.setdefaultencoding('utf-8')
# step_1()
read_excel('data/Penang_holiday.xls')