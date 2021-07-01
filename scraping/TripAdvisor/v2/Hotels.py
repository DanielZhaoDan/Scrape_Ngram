# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
from scraping.utils import post_request_html, get_request_html, write_html, write_excel, remove_html_tag, timeout, post_request_json

saved_hotel = set()
R_ID = 1
sheet1_data = [['ID', 'Hotel URL', 'Hotel Name', 'Address', 'Rating', 'Number of reviews', 'Star', 'Amenities']]
sheet2_data = [['ID', 'Hotel URL', 'Reviewer Name', 'Review Date' 'Rating', 'Text Review', 'Reviewer Location',
                'Contributor Level', 'Travel Style']]
sheet3_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]
sheet4_data = [['Reviewer Name', 'Reviewer url', 'Category', 'Name', 'Rating', 'Text']]

cookie = 'TADCID=mTSTSmON-ZcJ-rADABQCFdpBzzOuRA-9xvCxaMyI12YZl775cNbEKvygFD-YFnz5uGYEDIZf9E8RsUkZaD7K1Z90eeTIUIebZBU; TAUnique=%1%enc%3A5EPBin1ZXG7pTvEC%2FTHhGLajhyk61rGprewN1%2FNwhmgiC9mUUqh3Gg%3D%3D; TASSK=enc%3AAGo87dKTTcwUHfbbtbZqoZnHGiilhV5a3Lxv4dEOHG7j%2B4JF%2BEMrXlfWmf7i0PKv0RRZ2bpxYxutyFImsg0niWmVqP9FmCpLukOQpPHH1HQEOsUUzBSpYasgeYUzaAkzLA%3D%3D; ServerPool=A; PMC=V2*MS.29*MD.20210612*LD.20210612; TART=%1%enc%3ApOeYHLVHxrVrWjk5CVfZhpAltc8Pj6KW0H3fDqxSXS%2B4mMqWzCigQdC2rgwCZb6gAUtuxWemFUE%3D; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; TAAUTHEAT=sHJPzWOTz1XksZaVABQCab7fMZ8ORguCqJF_E5GxfSXwl6ElhlVkVZ6J8-r81AheAlD1cF4yUjCeEvBoAAimPBEG1SfiW33GJCmTOVDTgg3U2KKHI70ZnMIJrcvu4-J4V_rt_M_5viTQxJjpYwj5Q7IEoN_HYeMz1hqkRwixEvp2Pi29Q5JW8_xkggv0WFjjEk-D9dYzhHS313C2O-AM-trHp-TbuSQ93iiH5rcG; PAC=ANMM1471r4ykvtbqgEmdoyTU8cpTBIwTIePSGLI5XJWtPdg3uSouPpl6M_7FLJnFjmtLSYHp1fGRzC4N7dA3mJaAys9fGMdsRjddra5ne9-tTEXQG0oR5knFHnA-CWpxHVuHVZ3Iey1H_eHWc4bb_suPqa-2hEyU6GJd2Uyv2pT5n1AMMsAQthBmcjFTtLlqTmCqKnlyZMZr8LdenfdMjs5HlMUHNeKAiuF6_VTcWaesdQaks6LfbHvF0JWwerp_rckVwOnDvYloUmBgKkipj1MI0lxTsz4lHrS0a3xlYhvH; TATravelInfo=V2*AY.2021*AM.7*AD.15*DY.2021*DM.7*DD.16*A.2*MG.-1*HP.2*FL.3*DSM.1623512048661*RS.1; TAReturnTo=%1%%2FHotel_Review-g14134875-d308070-Reviews-Yokohama_Royal_Park_Hotel-Minatomirai_Nishi_Yokohama_Kanagawa_Prefecture_Kanto.html; roybatty=TNI1625!AI2hEMLqV2qIgwA4QO%2BXksH3XS6gGDR5UJ%2FPRQDqjz%2B6N2AZr0t5ZM%2Bp8AH0upXFBRHvk9Vx3JNJrSvZtGw%2BH9ZBSwKlbnnc1Jc4KJlgtyTOrfOjst2MrsiCH%2Ft0F5bEeHTybrWjp3dUUPgGQowAkDscwrbTOLarbkT5McyF0VPK%2C1; TASession=%1%V2ID.79738FBCDBBB442BB1618BD9DC774A1C*SQ.52*PR.40185%7C*LS.DemandLoadAjax*GR.36*TCPAR.54*TBR.48*EXEX.94*ABTR.32*PHTB.19*FS.81*CPU.9*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.ABD562818D249697A8AB4E2FFBFCE092*LF.en*FA.1*DF.0*TRA.false*LD.308070*EAU.A; TAUD=LA-1623487350128-1*RDD-1-2021_06_12*HDD-24767433-2021_07_15.2021_07_16.1*LD-24773603-2021.7.15.2021.7.16*LG-24773605-2.1.F.; TASID=1BBA4BDA3C954F48A1207E51311C0183; ak_bmsc=47F5630A28D031662BF9B5BC88F5C6FEB81A35241D5E0000BA73C5607F612040~plI1bFyvlNw6X3Kim8hSRjiWGdoL1lXLnrRlBHf8lEhCp+rQrO2BchP54i3pt8P7mG8uQjsbAWq/BiavYOVguuyPJl5PwOBnuUS/Txgm7IO1jFiktBzwFC36Um4cdLSAmXwl/kgY0DtVMKMlxpC6/f1hlCcg+L8eVigCF7FYAuBDY6cEjfT58ybOJCibaRFPzz8OVxDBbwjtQL45yuG4ZBLvr+mFxTzFPALGu8nA2xUqQ=; bm_sv=A4797D803F23C7A2A686C6DBDF6279A3~9apF8uLHXyw+9IMhfSBjvsGzMAjmSFTu1dGo90FN3Pesl8IPTEXAlQ2KE+DZ84pmFse5z58dCOWSGiPMQLlucm5gLX4wv6tGTtVFiiLwwETjOjjnj2JLlElflQbazRDDzhI0QGY9GZHsU3Y3dIETBv6rnC4w0gYDYhhidkfR0Iw='

urls = [
    # ('https://www.tripadvisor.com.my/Hotels-g298277-Johor-Hotels.html', 'Johor'),
    # ('https://www.tripadvisor.com.my/Hotels-g298281-Kedah-Hotels.html', 'Kedah'),
    # ('https://www.tripadvisor.com.my/Hotels-g298284-Kelantan-Hotels.html', 'Kelantan'),
    # ('https://www.tripadvisor.com.my/Hotels-g306997-Melaka_Central_Melaka_District_Melaka_State-Hotels.html', 'Melaka'),
    # ('https://www.tripadvisor.com.my/Hotels-g298289-Negeri_Sembilan-Hotels.html', 'Negeri_Sembilan'),
    # ('https://www.tripadvisor.com.my/Hotels-g298291-Pahang-Hotels.html', 'Pahang'),
    # ('https://www.tripadvisor.com.my/Hotels-g298297-Perak-Hotels.html', 'Perak'),
    # ('https://www.tripadvisor.com.my/Hotels-g298301-Perlis-Hotels.html', 'Perlis'),
    # ('https://www.tripadvisor.com.my/Hotels-g298306-Sabah-Hotels.html', 'Sabah'),
    # ('https://www.tripadvisor.com.my/Hotels-g298308-Sarawak-Hotels.html', 'Sarawak'),
    # ('https://www.tripadvisor.com.my/Hotels-g298310-Selangor-Hotels.html', 'Selangor'),
    # ('https://www.tripadvisor.com.my/Hotels-g298318-Terengganu-Hotels.html', 'Terengganu'),
    # ('https://www.tripadvisor.com.my/Hotels-g298570-Kuala_Lumpur_Wilayah_Persekutuan-Hotels.html', 'Kuala_Lumpur'),
    # ('https://www.tripadvisor.com.my/Hotels-g298286-Labuan_Island_Sabah-Hotels.html', 'Labuan'),
    # ('https://www.tripadvisor.com.my/Hotels-g298305-Putrajaya_Wilayah_Persekutuan-Hotels.html', 'Putrajaya'),
    ('https://www.tripadvisor.in/Hotels-g294232-Japan-Hotels.html', 'Japan'),
    ('https://www.tripadvisor.in/Hotels-g255055-Australia-Hotels.html', 'Australia'),

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
    global sheet1_data, sheet2_data
    url, state = item

    page_no = None
    i = 1

    hotel_reg = 'class="listing_title".*?href="(.*?)".*?>(.*?)<(.*?)info-col(.*?)prw_common_rating_and_review_count_with_popup(.*?)"ReviewCount">(.*?) revi.*?#(.*?) Bes(.*?)prw_bl_h_special_offer'
    body = {
        'plSeed': '898352206',
        'reqNum': 1,
        'isLastPoll': 'false',
        'waitTime': 43,
        'catTag': '9193,9200,9212,9230,9235,9250,9256,9261,9469,9672,16545,21371,21372,21373',
        'changeSet': 'MAIN_META, PAGE_OFFSET',
        'puid': 'XyUa3QokLIsAA6QLD@wAAAAg',
        'cat': '1,2,3',
    }
    headers = {
        'x-puid': 'XyUa3QokLIsAA6QLD@wAAAAg',
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'text/html, */*',
    }

    while True:
        try:
            body['paramSeqId'] = i
            body['offset'] = (i - 1) * 30,

            html = post_request_html(url, cookie, data=body, add_header=headers)

            if not page_no:
                page_no = get_page_no(html)

            if (i + 1) > page_no:
                break

            data = re.compile(hotel_reg).findall(html)
            print i, page_no, state

            for item in data:
                hote_url = 'https://www.tripadvisor.com.my' + item[0]
                try :
                    name = remove_html_tag(item[1])
                    meta = item[2]
                    free_cancel = 'No'
                    if 'Free cancellation' in meta:
                        free_cancel = 'Yes'
                    pay_later = 'No'
                    if 'Reserve now, pay at stay' in meta:
                        pay_later = 'Yes'
                    # classification = get_classification(item[2])
                    rating = global_rating_details(item[4])
                    no_reviews = int(item[5].replace(',', ''))
                    rank = item[6]
                    covid_meta = 'No'
                    if 'Taking safety measures' in item[7]:
                        covid_meta = 'Yes'
                    h_id = state + '_' + rank

                    print item[0],
                    travel_safe_list, star, rate_list, amenities_list, feature_list, types_list, hotel_style, great_list, Choice, no_tips = get_hotel_details(hote_url)

                    for t in travel_safe_list:
                        one_row = [h_id, name, hote_url, rank, covid_meta, free_cancel, pay_later, t,
                                   no_reviews, no_tips, rating, Choice, star, hotel_style] + great_list + rate_list[1:]
                        print one_row
                        sheet1_data.append(one_row)

                    for l in amenities_list:
                        sheet2_data.append([h_id, name, l, 'Property Amenities'])
                    for l in feature_list:
                        sheet2_data.append([h_id, name, l, 'Room Features'])
                    for l in types_list:
                        sheet2_data.append([h_id, name, l, 'Room Types'])
                except Exception as e:
                    print '\n===err===', hote_url, e

            i += 1
        except Exception as e:
            print 'ERR---', url, i, e
            i += 1


def global_rating_details(ori):
    if 'of 5 bubbles' in ori:
        reg = "alt='(.*?) of 5 bubbles'"
        data = re.compile(reg).findall(ori)
        return data[0]
    return 0

@timeout(3)
def get_hotel_details(url):
    html = get_request_html(url, cookie)
    reg = 'id="taplc_hr_covid_react_above_about_0(.*?)class="_3cjYfwwQ">(.*?)<(.*?)class="ui_column  ".*?Property amenities(.*?)Room features(.*?)Room types(.*?)Good to know.*?class="AZd6Ff4E".*?title="(.*?) (.*?)ui_column is-6.*?id="LOCATION"(.*?)ui_column is-4 _3UwHh_yY.*?CC_TAB_RoomTips_LABEL.*?_1aRY8Wbl">(.*?)<'
    raw_data = re.compile(reg).findall(html)[0]

    covid_raw = raw_data[0]
    detail_rate_raw = raw_data[2]
    amenities_raw = raw_data[3]
    room_feature = raw_data[4]
    room_type = raw_data[5]
    star = raw_data[6]
    hotel_style_raw = raw_data[7]
    location_raw = raw_data[8]
    no_tips = raw_data[9]

    travel_safe_reg = 'class="_1AOUUeGM">(.*?)<'
    if 'class="_1AOUUeGM">' in covid_raw:
        travel_safe_list = re.compile(travel_safe_reg).findall(covid_raw)
    else:
        travel_safe_list = ['N/A']

    rate_reg = 'ui_bubble_rating bubble_(.*?)"'
    rate_list = re.compile(rate_reg).findall(detail_rate_raw)
    rate_list = [float(i) / 10 for i in rate_list]

    amenities_reg = 'amenity_text.*?/span>(.*?)<'
    amenities_list = re.compile(amenities_reg).findall(amenities_raw)
    feature_list = re.compile(amenities_reg).findall(room_feature)
    types_list = re.compile(amenities_reg).findall(room_type)

    hotel_reg = 'class="_2dtF3ueh">(.*?)<'
    if 'class="_2dtF3ueh"' in hotel_style_raw:
        hotel_style = re.compile(hotel_reg).findall(hotel_style_raw)
        hotel_style = '|'.join(hotel_style)
    else:
        hotel_style = 'N/A'

    great_list = ['N/A' for i in range(3)]

    if 'Great for walkers' in location_raw:
        great_reg = 'class="oPMurIUj _1iwDIdby">(.*?)<.*?oPMurIUj TrfXbt7b">(.*?)<.*?oPMurIUj _1WE0iyL_">(.*?)<'
        great_list = re.compile(great_reg).findall(location_raw)[0]
        great_list = [i for i in great_list]

    return travel_safe_list, star, rate_list, amenities_list, feature_list, types_list, hotel_style, great_list, 'Yes' if "Travellers' Choice" in html else 'No', no_tips


def request_sheet2_old(row, number, hotel_url):
    global sheet2_data
    page_no = number / 5
    if number % 5 != 0:
        page_no += 1

    terminate = False
    for i in range(0, page_no):
        if terminate:
            break
        try:
            url = hotel_url.replace('-Reviews-', '-Reviews-or%s-' % str(i * 10))
            print page_no, i, row, url

            html = get_request_html(url, cookie)

            reg = 'ui_header_link _1r_My98y.*?>(.*?)<(.*?)ui_bubble_rating bubble_(.*?)".*?Date of .*?>(.*?)<'

            comment_list = re.compile(reg).findall(html)
            for comment in comment_list:
                name = comment[0]
                country = get_user_location(comment[1])
                rating = int(comment[2]) / 10.0
                review_date = get_comment_date(comment[3])

                if int(review_date.split('/')[-1]) < 2020:
                    terminate = True
                    break

                one_row = [hotel_url, name, review_date, rating, country]
                sheet2_data.append(one_row)

        except Exception as e:
            print('ERROR-sheet2-', hotel_url, i, e)


def get_comment_date(ori):
    try:
        date = datetime.strptime(ori, '%Y-%m-%d')
        return date.strftime('%d/%m/%Y')
    except:
        return ori


def get_user_location(ori):
    if 'ui_icon map-pin-fill _2kj8kWkW' in ori:
        reg = 'ui_icon map-pin-fill _2kj8kWkW">.*?>(.*?)<'
        data = re.compile(reg).findall(ori)
        return data[0]
    return 'N/A'


def read_excel(filename, start=1):
    global R_ID, sheet2_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    visited_hotel = {}

    for i in range(start, table.nrows):
        row = table.row(i)
        hotel_id = row[0].value
        if hotel_id in visited_hotel:
            continue
        main_url = row[2].value
        hotel_name = row[1].value

        try:
            review_no = int(row[8].value)
            tip_no = int(row[9].value)
            # if review_no > 0:
            #     request_reviews_new(hotel_id, hotel_name, main_url)
            if tip_no > 0:
                request_tips(hotel_id, hotel_name, main_url, tip_no)
            visited_hotel[hotel_id] = True
        except Exception as e:
            print main_url, e

    # write_excel('sheet3.xls', sheet3_data)
    write_excel('sheet4.xls', sheet4_data)


def request_reviews_new(hotel_id, hotel_name, hotel_url):
    url = 'https://www.tripadvisor.com.my/data/graphql/batched'

    g_id, item_id = get_id_from_url(hotel_url)
    i = 0
    terminate = False
    page_size = 5
    header = {
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'x-requested-by': 'TNI1625!AK1qauweEB/vQdtumi/1GgOSlXgaEaXb6OH52zft8h889v5gcc4zScVn/2ZvhANVw7X9s2SGV02EBpceyoBjG70DHi51390O4JpQV9XNXpqOoydIc2JpzDZQ8jSkipWuRWtGqpwcFO/+9Tcfn/sg6vsklsgZHGx/9sDPqrEeceGS',
    }
    while not terminate and i <= 10:

        data = '[{"query":"mutation LogBBMLInteraction($interaction: ClientInteractionOpaqueInput!) {\\n  logProductInteraction(interaction: $interaction)\\n}\\n","variables":{"interaction":{"productInteraction":{"interaction_type":"CLICK","site":{"site_name":"ta","site_business_unit":"Hotels","site_domain":"www.tripadvisor.com.my"},' \
               '"pageview":{"pageview_request_uid":"YMTUNQokKWYAAYssfJUAAAAi","pageview_attributes":{"location_id":' + item_id +',"geo_id":' + g_id +'' \
               ',"servlet_name":"Hotel_Review"}},"user":{"user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36","site_persistent_user_uid":"web115a.47.88.134.109.179FF62F95D","unique_user_identifiers":{"session_id":"79738FBCDBBB442BB1618BD9DC774A1C"}},"search":{},' \
               '"item_group":{"item_group_collection_key":"YMTUNQokKWYAAYssfJUAAAAi"},"item":{"product_type":"Hotels","item_id_type":"ta-location-id","item_id":' + item_id +',"item_attributes":{"element_type":"number","action_name":"REVIEW_NAV","page_number":' + str(i+1) + ',"offset":'+ str(page_size*i) +',"limit":'+ str(page_size) +'}}}}}},' \
               '{"query":"query ReviewListQuery($locationId: Int!, $offset: Int, $limit: Int, $filters: [FilterConditionInput!], $prefs: ReviewListPrefsInput, $initialPrefs: ReviewListPrefsInput, $filterCacheKey: String, $prefsCacheKey: String, $keywordVariant: String!, $needKeywords: Boolean = true) {\\n  cachedFilters: personalCache(key: $filterCacheKey)\\n  cachedPrefs: personalCache(key: $prefsCacheKey)\\n  locations(locationIds: [$locationId]) {\\n    locationId\\n    parentGeoId\\n    name\\n    placeType\\n    reviewSummary {\\n      rating\\n      count\\n    }\\n    keywords(variant: $keywordVariant) @include(if: $needKeywords) {\\n      keywords {\\n        keyword\\n      }\\n    }\\n    ... on LocationInformation {\\n      parentGeoId\\n    }\\n    ... on LocationInformation {\\n      parentGeoId\\n    }\\n    ... on LocationInformation {\\n      name\\n      currentUserOwnerStatus {\\n        isValid\\n      }\\n    }\\n    ... on LocationInformation {\\n      locationId\\n      currentUserOwnerStatus {\\n        isValid\\n      }\\n    }\\n    ... on LocationInformation {\\n      locationId\\n      parentGeoId\\n      accommodationCategory\\n      currentUserOwnerStatus {\\n        isValid\\n      }\\n      url\\n    }\\n    reviewListPage(page: {offset: $offset, limit: $limit}, filters: $filters, prefs: $prefs, initialPrefs: $initialPrefs, filterCacheKey: $filterCacheKey, prefsCacheKey: $prefsCacheKey) {\\n      totalCount\\n      preferredReviewIds\\n      reviews {\\n        ... on Review {\\n          id\\n          url\\n          location {\\n            locationId\\n            name\\n          }\\n          createdDate\\n          publishedDate\\n          provider {\\n            isLocalProvider\\n          }\\n          userProfile {\\n            id\\n            userId: id\\n            isMe\\n            isVerified\\n            displayName\\n            username\\n            avatar {\\n              id\\n              photoSizes {\\n                url\\n                width\\n                height\\n              }\\n            }\\n            hometown {\\n              locationId\\n              fallbackString\\n              location {\\n                locationId\\n                additionalNames {\\n                  long\\n                }\\n                name\\n              }\\n            }\\n            contributionCounts {\\n              sumAllUgc\\n              helpfulVote\\n            }\\n            route {\\n              url\\n            }\\n          }\\n        }\\n        ... on Review {\\n          title\\n          language\\n          url\\n        }\\n        ... on Review {\\n          language\\n          translationType\\n        }\\n        ... on Review {\\n          roomTip\\n        }\\n        ... on Review {\\n          tripInfo {\\n            stayDate\\n          }\\n          location {\\n            placeType\\n          }\\n        }\\n        ... on Review {\\n          additionalRatings {\\n            rating\\n            ratingLabel\\n          }\\n        }\\n        ... on Review {\\n          tripInfo {\\n            tripType\\n          }\\n        }\\n        ... on Review {\\n          language\\n          translationType\\n          mgmtResponse {\\n            id\\n            language\\n            translationType\\n          }\\n        }\\n        ... on Review {\\n          text\\n          publishedDate\\n          username\\n          connectionToSubject\\n          language\\n          mgmtResponse {\\n            id\\n            text\\n            language\\n            publishedDate\\n            username\\n            connectionToSubject\\n          }\\n        }\\n        ... on Review {\\n          id\\n          locationId\\n          title\\n          text\\n          rating\\n          absoluteUrl\\n          mcid\\n          translationType\\n          mtProviderId\\n          photos {\\n            id\\n            statuses\\n            photoSizes {\\n              url\\n              width\\n              height\\n            }\\n          }\\n          userProfile {\\n            id\\n            displayName\\n            username\\n          }\\n        }\\n        ... on Review {\\n          mgmtResponse {\\n            id\\n          }\\n          provider {\\n            isLocalProvider\\n          }\\n        }\\n        ... on Review {\\n          translationType\\n          location {\\n            locationId\\n            parentGeoId\\n          }\\n          provider {\\n            isLocalProvider\\n            isToolsProvider\\n          }\\n          original {\\n            id\\n            url\\n            locationId\\n            userId\\n            language\\n            submissionDomain\\n          }\\n        }\\n        ... on Review {\\n          locationId\\n          mcid\\n          attribution\\n        }\\n        ... on Review {\\n          __typename\\n          locationId\\n          helpfulVotes\\n          photoIds\\n          route {\\n            url\\n          }\\n          socialStatistics {\\n            followCount\\n            isFollowing\\n            isLiked\\n            isReposted\\n            isSaved\\n            likeCount\\n            repostCount\\n            tripCount\\n          }\\n          status\\n          userId\\n          userProfile {\\n            id\\n            displayName\\n            isFollowing\\n          }\\n          location {\\n            __typename\\n            locationId\\n            additionalNames {\\n              normal\\n              long\\n              longOnlyParent\\n              longParentAbbreviated\\n              longOnlyParentAbbreviated\\n              longParentStateAbbreviated\\n              longOnlyParentStateAbbreviated\\n              geo\\n              abbreviated\\n              abbreviatedRaw\\n              abbreviatedStateTerritory\\n              abbreviatedStateTerritoryRaw\\n            }\\n            parent {\\n              locationId\\n              additionalNames {\\n                normal\\n                long\\n                longOnlyParent\\n                longParentAbbreviated\\n                longOnlyParentAbbreviated\\n                longParentStateAbbreviated\\n                longOnlyParentStateAbbreviated\\n                geo\\n                abbreviated\\n                abbreviatedRaw\\n                abbreviatedStateTerritory\\n                abbreviatedStateTerritoryRaw\\n              }\\n            }\\n          }\\n        }\\n        ... on Review {\\n          text\\n          language\\n        }\\n        ... on Review {\\n          locationId\\n          absoluteUrl\\n          mcid\\n          translationType\\n          mtProviderId\\n          originalLanguage\\n          rating\\n        }\\n        ... on Review {\\n          id\\n          locationId\\n          title\\n          labels\\n          rating\\n          absoluteUrl\\n          mcid\\n          translationType\\n          mtProviderId\\n          alertStatus\\n        }\\n      }\\n    }\\n    reviewAggregations {\\n      ratingCounts\\n      languageCounts\\n      alertStatusCount\\n    }\\n  }\\n}\\n","variables":' \
               '{"locationId":' + item_id +',"offset":'+ str(page_size*i) +',"filters":[{"axis":"SEGMENT","selections":["Family"]}],"prefs":null,"initialPrefs":{},"limit":5,"filterCacheKey":null,"prefsCacheKey":"locationReviewPrefs","needKeywords":false,"keywordVariant":"location_keywords_v2_llr_order_30_en"}},{"query":"query IsSubscribed {\\n  isSubscribed: OptimusBenefits_isSubscribedToOptimus\\n}\\n","variables":{}},{"query":"query PageTargetingQuery($pageAdsRequestInput: AdContext_PageAdsRequestInput) {\\n  gptInfo: AdContext_getPageAdsBatch(requests: [$pageAdsRequestInput]) {\\n    adBase\\n    ppid\\n    pageLevelTargeting {\\n      key\\n      value\\n    }\\n  }\\n}\\n","variables":{"pageAdsRequestInput":{"hotelTravelInfo":{"checkInDate":"2021-09-25","checkOutDate":"2021-09-26","defaultDates":true},' \
                '"locationId":' + item_id +',"pageType":"Hotel_Review","browserType":"CHROME","drs":[{"space":"ABC","sliceNum":80},{"space":"AFIL","sliceNum":7},{"space":"ATTPromo","sliceNum":75},{"space":"AUC","sliceNum":11},{"space":"BBML","sliceNum":61},{"space":"BMP","sliceNum":83},{"space":"BRDTTD","sliceNum":87},{"space":"Brand","sliceNum":44},{"space":"CAKE","sliceNum":69},{"space":"CAR","sliceNum":73},{"space":"COM","sliceNum":58},{"space":"CRS","sliceNum":51},{"space":"Community","sliceNum":53},{"space":"Content","sliceNum":71},{"space":"CoreX","sliceNum":4},{"space":"EATPIZZA","sliceNum":24},{"space":"EID","sliceNum":56},{"space":"EXP","sliceNum":88},{"space":"Engage","sliceNum":47},{"space":"FDP","sliceNum":84},{"space":"FDS","sliceNum":27},{"space":"FDU","sliceNum":5},{"space":"FLTMERCH","sliceNum":75},{"space":"FLTREV","sliceNum":1},{"space":"Filters","sliceNum":60},{"space":"Flights","sliceNum":59},{"space":"HRATF","sliceNum":39},{"space":"HSX","sliceNum":85},{"space":"HSXB","sliceNum":42},{"space":"IBEX","sliceNum":88},{"space":"ING","sliceNum":11},{"space":"INT1","sliceNum":98},{"space":"INT2","sliceNum":45},{"space":"ITR","sliceNum":23},{"space":"L10N","sliceNum":75},{"space":"ML","sliceNum":11},{"space":"ML6","sliceNum":72},{"space":"MM","sliceNum":84},{"space":"MOBILEAPP","sliceNum":-1},{"space":"MOF","sliceNum":66},{"space":"MPS","sliceNum":85},{"space":"MTA","sliceNum":68},{"space":"Me2","sliceNum":68},{"space":"Mem","sliceNum":99},{"space":"Mobile","sliceNum":3},{"space":"MobileCore","sliceNum":50},{"space":"Notifications","sliceNum":47},{"space":"Other","sliceNum":85},{"space":"P13N","sliceNum":67},{"space":"PIE","sliceNum":87},{"space":"PLS","sliceNum":64},{"space":"POS","sliceNum":31},{"space":"PRT","sliceNum":74},{"space":"RDS1","sliceNum":63},{"space":"RDS2","sliceNum":90},{"space":"RDS3","sliceNum":82},{"space":"RDS4","sliceNum":76},{"space":"RDS5","sliceNum":18},{"space":"RET","sliceNum":63},{"space":"REV","sliceNum":22},{"space":"REVB","sliceNum":8},{"space":"REVH","sliceNum":36},{"space":"REVM","sliceNum":45},{"space":"REVSD","sliceNum":94},{"space":"REVSP","sliceNum":32},{"space":"REVXS","sliceNum":51},{"space":"RNA","sliceNum":58},{"space":"RSE1","sliceNum":33},{"space":"RSE2","sliceNum":87},{"space":"Rooms","sliceNum":58},{"space":"S3PO","sliceNum":4},{"space":"SD40","sliceNum":44},{"space":"SE2O","sliceNum":60},{"space":"SEM","sliceNum":54},{"space":"SEO","sliceNum":77},{"space":"SORT1","sliceNum":72},{"space":"Sales","sliceNum":52},{"space":"Search","sliceNum":67},{"space":"SiteX","sliceNum":53},{"space":"Surveys","sliceNum":71},{"space":"T4B","sliceNum":33},{"space":"TGT","sliceNum":28},{"space":"TRP","sliceNum":37},{"space":"TTD","sliceNum":16},{"space":"TX","sliceNum":49},{"space":"Timeline","sliceNum":62},{"space":"VP","sliceNum":51},{"space":"VR","sliceNum":37},{"space":"YM","sliceNum":68},{"space":"YMB","sliceNum":40}],' \
               '"globalContextUrlParameters":[{"key":"offset","value":"r5"},{"key":"detailId","value":"' + item_id +'"},{"key":"geoId","value":"' + g_id +'"}],"userAgentCategory":"DESKTOP"}}}]'
        # print data
        body = post_request_json(url, cookie, data, header)

        location = None

        for b in body:
            if 'locations' in b['data']:
                location = b['data']['locations'][0]
                break

        if location:
            reviews = location['reviewListPage']['reviews']
            print hotel_id, i, len(reviews)
            for review in reviews:
                try:
                    create_dt = get_comment_date(review['createdDate'])

                    if int(create_dt.split('/')[-1]) < 2020:
                        terminate = True
                        break

                    displayName = review['userProfile']['displayName']
                    user_url = review['userProfile']['route']['url']
                    hometown = review['userProfile']['hometown']
                    user_location = 'N/A'
                    try:
                        user_location = hometown['location']['additionalNames']['long']
                    except:
                        pass
                    rating = review['rating']
                    title = review['title']
                    text = review['text']

                    one_row = [hotel_id, hotel_name, displayName, user_location, rating, create_dt, user_url, title, text]
                    sheet3_data.append(one_row)
                except Exception as e:
                    print 'review row error---', e

        i += 1


def request_tips(hotel_id, hotel_name, hotel_url, no_tips):
    url = 'https://www.tripadvisor.com.my/data/graphql/batched'

    g_id, item_id = get_id_from_url(hotel_url)
    i = 0
    terminate = False
    page_size = 5
    total_page = no_tips / page_size
    header = {
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'x-requested-by': 'TNI1625!AK1qauweEB/vQdtumi/1GgOSlXgaEaXb6OH52zft8h889v5gcc4zScVn/2ZvhANVw7X9s2SGV02EBpceyoBjG70DHi51390O4JpQV9XNXpqOoydIc2JpzDZQ8jSkipWuRWtGqpwcFO/+9Tcfn/sg6vsklsgZHGx/9sDPqrEeceGS',
    }
    while not terminate and i <= total_page:
        data = '[{"query":"query TipsTabQuery($locationId: Int!, $offset: Int!, $limit: Int!, $loggedIn: Boolean!, $loggedInUserId: String) {\\n  currentMember: memberProfile(userId: {id: $loggedInUserId}) @include(if: $loggedIn) {\\n    ...MemberFieldsTabFragment\\n  }\\n  locations(locationIds: [$locationId]) {\\n    locationId\\n    name\\n    roomTipsCount\\n    roomTips(page: {offset: $offset, limit: $limit}) {\\n      id\\n      text\\n      rating\\n      url\\n      publishedDate\\n      userProfile {\\n        ...MemberFieldsTabFragment\\n      }\\n    }\\n  }\\n}\\n\\nfragment MemberFieldsTabFragment on MemberProfile {\\n  userId: id\\n  isMe\\n  isVerified\\n  isFollowing\\n  displayName\\n  username\\n  avatar {\\n    id\\n    photoSizes {\\n      ...PhotoSizesTabFragment\\n    }\\n  }\\n  hometown {\\n    locationId\\n    fallbackString\\n    location {\\n      locationId\\n      additionalNames {\\n        long\\n      }\\n      name\\n    }\\n  }\\n  contributionCounts {\\n    sumAllUgc\\n    helpfulVote\\n  }\\n  route {\\n    url\\n  }\\n}\\n\\nfragment PhotoSizesTabFragment on PhotoSize {\\n  url\\n  width\\n  height\\n  isHorizontal\\n}\\n","variables":' \
               '{"locationId":' + item_id + ',"offset":' + str(page_size * i) + ',"limit":5,"loggedInUserId":"ABD562818D249697A8AB4E2FFBFCE092","loggedIn":true}}]'

        # print data
        body = post_request_json(url, cookie, data, header)
        location = None

        for b in body:
            if 'locations' in b['data']:
                location = b['data']['locations'][0]
                break

        if location:
            reviews = location['roomTips']
            print hotel_id, i, total_page
            for review in reviews:
                try:
                    create_dt = get_comment_date(review['publishedDate'])

                    if int(create_dt.split('/')[-1]) < 2020:
                        terminate = True
                        break

                    displayName = review['userProfile']['displayName']
                    user_url = review['userProfile']['route']['url']
                    hometown = review['userProfile']['hometown']
                    user_location = 'N/A'
                    try:
                        user_location = hometown['location']['additionalNames']['long']
                    except:
                        pass
                    rating = review['rating']
                    text = review['text']

                    one_row = [hotel_id, hotel_name, displayName, user_location, rating, create_dt, user_url, text]

                    sheet4_data.append(one_row)
                except Exception as e:
                    print 'review row error---', e
        i += 1


def get_id_from_url(url):
    # https://www.tripadvisor.com.my/Hotel_Review-g14134875-d308070-Reviews-Yokohama_Royal_Park_Hotel-Minatomirai_Nishi_Yokohama_Kanagawa_Prefecture_Kanto.html#REVIEWS
    temp = url.split('Review-g')[-1].split('-Reviews-')[0]
    return temp.split('-d')


def get_level_uid(filename, start=1):
    global R_ID, sheet3_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    uid_level = {}

    for i in range(start, table.nrows):
        row = table.row(i)

        url = row[6].value
        one_row = [row[j].value for j in range(0, table.ncols)]

        try:
            if url not in uid_level:
                level = get_level(url)
                print url, level
                uid_level[url] = level
            one_row[6] = uid_level[url]
            sheet3_data.append(one_row)
        except Exception as e:
            print url, e

    write_excel(filename, sheet3_data)
    # write_excel('sheet4.xls', sheet4_data)


def get_level(url):
    userId = url.split('/')[-1]
    badge_url = 'https://www.tripadvisor.com.my/members-badgecollection/' + userId

    html = get_request_html(badge_url, cookie)

    reg = 'data-backbone-name="modules.membercenter.Level"(.*?)</div'
    raw_data = re.compile(reg).findall(html)[0]
    if 'tripcollectiveLevels' in raw_data:
        reg = 'tripcollectiveLevels.*?span>(.*?)<'
        return re.compile(reg).findall(raw_data)[0]
    return 'N/A'


def step_1():
    for item in urls:
        request_sheet1(item)
        write_excel(item[1] + '_1hotel.xls', sheet1_data)
        write_excel(item[1] + '_2hotel.xls', sheet2_data)

reload(sys)
sys.setdefaultencoding('utf-8')
# step_1()
# read_excel('data/Australia_1hotel.xls')
# get_level_uid('data/sheet3.xls')
# get_level_uid('data/sheet4.xls')

# if True:
#     data = xlrd.open_workbook('data/Penang_hotel1.xls', encoding_override="utf-8")
#     table = data.sheets()[0]
#
#     for i in range(1, table.nrows):
#         row = table.row(i)
#         main_url = row[2].value
#
#         try:
#             _, star = get_hotel_details(main_url)
#             print star
#         except Exception as e:
#             print main_url, e

data = xlrd.open_workbook('data/Australia_1hotel.xls', encoding_override="utf-8")
table = data.sheets()[0]
hotel_dict = {}

for i in range(1, table.nrows):
    row = table.row(i)

    url = row[2].value

    try:
        if url not in hotel_dict:
            travel_safe_list, star, rate_list, amenities_list, feature_list, types_list, hotel_style, great_list, Choice, no_tips = get_hotel_details(url)
            hotel_dict[url] = hotel_style
        print hotel_dict[url]
    except Exception as e:
        print url, e