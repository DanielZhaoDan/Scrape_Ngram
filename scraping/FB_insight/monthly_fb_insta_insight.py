# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import csv
import os, sys
from scraping.utils import post_request_html, get_request_html, write_html, write_excel, download_response


# yusiang.how@gmail.com
# H0wyusi4ng
# excel: https://docs.google.com/spreadsheets/d/1DUx8_pVsPOZULbzUc48bo4iZWNNzs07mJStIYlZG7rM/edit#gid=1763024187
cookie = 'sb=_tPGYNbkgIw4zTnP_IoqaykH; datr=7cXdYAZroOXZhT3ID1_pTaOa; dpr=2; locale=en_US; c_user=100000028096171; xs=27%3AxgkkCPxf6wtlXg%3A2%3A1625150711%3A-1%3A9564; fr=1OadYiD0x0n9kaUB4.AWWRCLUJ8DBxvnSCjX7ZceAsF1w.BgxtP-.Q1.AAA.0.0.Bg3dT1.AWVo4ae1hxI; spin=r.1004069160_b.trunk_t.1625150712_s.1_v.2_; wd=1388x277'

fb_dtsg = 'AQGwqePchN30PFk:AQGH5_WBMIOgt6E'

headers = {
    'x-fb-friendly-name':'BCMPInsightsTableRelayRoot_ResultsQuery',
    'x-fb-lsd':'FqN0n-vMbsAfqBTiZLfQkO',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}

sheet1_data = [['country', 'platform', 'ID', 'Creator', 'Type', 'Permalink', 'Post Message', 'date', 'Lifetime Post Total Reach', 'Lifetime Post Paid Reach', 'Lifetime Post organic reach', 'Lifetime Post Total Comments', 'Lifetime Post Total Shares', 'Lifetime Post Total Clicks', 'Lifetime Post Total Reactions', 'Lifetime Post Total save']]
urls = [
    ('global', 'Instagram', 'https://www.facebook.com/collabsmanager/brand/insights?page_id=333389816697888&entry_source=page_insights&insights_end_date=1735660800&insights_platforms=Instagram&insights_start_date=1577808000'),
    ('RU', 'Instagram', 'https://www.facebook.com/collabsmanager/brand/insights?page_id=809819392381976&entry_source=page_insights&insights_end_date=1735660800&insights_platforms=Instagram&insights_start_date=1577808000'),
    ('TR', 'Instagram', 'https://www.facebook.com/collabsmanager/brand/insights?page_id=138354229593892&entry_source=page_insights&insights_end_date=1735660800&insights_platforms=Instagram&insights_start_date=1577808000'),
    ('EG', 'Instagram', 'https://www.facebook.com/collabsmanager/brand/insights?page_id=509931205722897&entry_source=page_insights&insights_end_date=1735660800&insights_platforms=Instagram&insights_start_date=1577808000'), #
    ('KZ', 'Instagram', 'https://www.facebook.com/collabsmanager/brand/insights?page_id=221215561376869&entry_source=page_insights&insights_end_date=1735660800&insights_platforms=Instagram&insights_start_date=1577808000'), #
    ('Id', 'Instagram', 'https://business.facebook.com/creatorstudio/?tab=instagram_monetization_branded_content&collection_id=free_form_collection&branded_content=%7B%22page_id%22%3A%2217841401312923496%22%2C%22bc_auto_shown_tagged_post_id%22%3Anull%2C%22active_tab%22%3A%22insights%22%2C%22insights_campaign_types%22%3Anull%2C%22insights_creator_id%22%3Anull%2C%22insights_end_date%22%3A1735660800%2C%22insights_platforms%22%3Anull%2C%22insights_start_date%22%3A1577808000%7D'),

    ('global', 'Facebook', 'https://www.facebook.com/collabsmanager/brand/insights?page_id=333389816697888&entry_source=page_insights&insights_end_date=1735660800&insights_platforms=Facebook&insights_start_date=1577808000'),
    ('PH', 'Facebook', 'https://www.facebook.com/collabsmanager/brand/insights?page_id=146131338887530&entry_source=page_insights&insights_end_date=1735660800&insights_platforms=Facebook&insights_start_date=1577808000'),
    ('TH', 'Facebook', 'https://www.facebook.com/collabsmanager/brand/insights?page_id=138354229593892&entry_source=page_insights&insights_end_date=1735660800&insights_platforms=Facebook&insights_start_date=1577808000'), #
    ('TR', 'Facebook', 'https://www.facebook.com/collabsmanager/brand/insights?page_id=138354229593892&entry_source=page_insights&insights_end_date=1735660800&insights_platforms=Facebook&insights_start_date=1577808000'), #
    ('BR', 'Facebook', 'https://business.facebook.com/creatorstudio/?tab=monetization_branded_content&collection_id=free_form_collection&branded_content=%7B%22page_id%22%3A%22166866083481130%22%2C%22bc_auto_shown_tagged_post_id%22%3Anull%2C%22active_tab%22%3A%22insights%22%2C%22insights_campaign_types%22%3Anull%2C%22insights_creator_id%22%3Anull%2C%22insights_end_date%22%3A1735660800%2C%22insights_platforms%22%3A[%22Facebook%22]%2C%22insights_start_date%22%3A1577808000%7D'), #
    ('ID', 'Facebook', 'https://business.facebook.com/creatorstudio/?tab=monetization_branded_content&collection_id=free_form_collection&branded_content=%7B%22page_id%22%3A%22174889372570036%22%2C%22bc_auto_shown_tagged_post_id%22%3Anull%2C%22active_tab%22%3A%22insights%22%2C%22insights_campaign_types%22%3Anull%2C%22insights_creator_id%22%3Anull%2C%22insights_end_date%22%3A1735660800%2C%22insights_platforms%22%3A[%22Facebook%22]%2C%22insights_start_date%22%3A1577808000%7D'), #
    ('VN', 'Facebook', 'https://business.facebook.com/creatorstudio/?tab=monetization_branded_content&collection_id=free_form_collection&branded_content=%7B%22page_id%22%3A%22359149557454798%22%2C%22bc_auto_shown_tagged_post_id%22%3Anull%2C%22active_tab%22%3A%22insights%22%2C%22insights_campaign_types%22%3Anull%2C%22insights_creator_id%22%3Anull%2C%22insights_end_date%22%3A1735660800%2C%22insights_platforms%22%3A[%22Facebook%22]%2C%22insights_start_date%22%3A1577808000%7D'),

]


def request_sheet1(item):
    country, platform, url = item

    print item

    if 'collabsmanager' in url:
        assetID = url.split("page_id=")[1].split('&')[0]
    elif 'creatorstudio' in url:
        assetID = url.split('page_id%22%3A%22')[1].split('%22')[0]

    realurl = url.split('.com')[0] + '.com/api/graphql/'

    body = {
        'av': '100000028096171',
        '__user': '100000028096171',
        '__a': '1',
        '__dyn': '7xeUmBz8fXgydwn8K2abBWqxK5E9EeFU99oWFGxK7oHoO366UjyUW3qiidBxa7GzU72czES2SfUCaBzogwSxS0x8C8yEqx62G7A1kxa4o8e14DyU9E7G2qq1eCBBwLghUcd5xS2du68K5EKU9oiAwu8sxF0Vxm3G4UOi3K2x0g8lUScwTwmElwtbyUtwAKi8xW3mawnHxC2611DxSbg942Cu9zE8U984678TwkE5abxZxK12x6i8wxK68GfxW4U4S3G3G1nBwZAw_zo5G4EqxinwwwywnFUqwGwJwEyEkx27oaU5G1tx64EK4oOEdEGdw',
        '__csr': '',
        '__req': 'z',
        '__beoa': '0',
        '__pc': 'PHASED:media_manager_pkg',
        'dpr': '1',
        '__ccg': 'EXCELLENT',
        '__rev': '1003908050',
        '__s': 'hfhc6e:9w5kk6:py2qc7',
        '__hsi': '6969940909180662243-0',
        'lsd': 'FqN0n-vMbsAfqBTiZLfQkO',
        '__spin_r':' 1003908050',
        '__spin_b':'trunk',
        '__spin_t':'1622814748',
        '__comet_req': '0',
        'fb_dtsg': fb_dtsg,
        'jazoest': '21889',
        '__jssesw': '1',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'BCMPInsightsTableRelayRoot_ResultsQuery',
        'variables': '{"assetID":"'+ assetID +'","filters":{"partner":null,"end_date":1735660800,"platform":["' + platform + '"],"post_type":null,"start_date":1577808000,"post_IDs":null,"campaign_types":null},"isTaggedView":true,"actorType":"creator"}',
        'server_timestamps': 'true',
        'doc_id': '4164068033626157',
    }

    html = post_request_html(realurl, cookie, add_header=headers, data=body)

    if 'Rate limit exceeded' in html:
        print 'Rate limit exceeded sheet1'
        return

    json_obj = json.loads(html)

    bc_posts_insights = json_obj.get('data', {}).get('bcmp_creator', {}).get('bc_posts_insights', {})

    end_cursor = process_response(bc_posts_insights, realurl, assetID, country, platform)

    if end_cursor:
        request_loop(end_cursor, realurl, assetID, country, platform)


def process_response(bc_posts_insights, realurl, assetID, country, platform):

    edges = bc_posts_insights.get('edges', [])

    print len(edges),

    for post in edges:
        node = post['node']
        post_id = node['post_id']
        fb_post = node['fb_post']
        ig_post = node['ig_post']

        try :
            if fb_post:
                author, media_type, content, create_time = get_fb_basic(fb_post)
                _, details = get_details(realurl, assetID, post_id)
            elif ig_post:
                author = node.get('additional_ig_post_metadata', {}).get('owner_username', 'N/A')
                content, create_time = get_ig_basic(ig_post)
                media_type, details = get_details(realurl, assetID, post_id)
        except Exception as e:
            print 'EXCEPTION---', realurl, assetID, post_id, e
            continue

        Permalink = 'https://facebook.com/collabsmanager/creator/insights/?page_id=' + assetID + '&bc_auto_shown_tagged_post_id=' + post_id

        one_row = [country, platform, post_id, author, media_type, Permalink, content, get_date(create_time)] + details

        # print one_row
        sheet1_data.append(one_row)

    end_cursor = bc_posts_insights.get('page_info', {}).get('end_cursor')

    return end_cursor


def get_details(realurl, pageId, post_id):
    body = {
        'av': '100000028096171',
        '__user': '100000028096171',
        '__a': '1',
        '__dyn': '7xe6FoO3-Q5E5ObG5V8WnFwRwCwgE98nyUdU6C7QdwSAAzoObxW4E6S7ES2S4oeodEeE6u3y4o4O11wlE1upE4W0LEK0KEswv8ao88hwKwEwDxC5o-0jG12Ki8wl8G1uw_wsU9k2C2218wIwNxK16wnEfogw9KfxW18wkU3mwkE9od8e85m1uws8cU-mmU',
        '__csr': '',
        '__req': 'm',
        '__beoa': '0',
        '__pc': 'PHASED:DEFAULT',
        'dpr': '1',
        '__ccg': 'EXCELLENT',
        '__rev': '1002842064',
        '__s': 'y3zifk:plhj15:18horo',
        '__hsi': '6884867916017957847-0',
        '__comet_req': '0',
        'fb_dtsg': fb_dtsg,
        'jazoest': '22104',
        '__spin_r': '1002842064',
        '__spin_b': 'trunk',
        '__spin_t': '1602949428',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'BCMPInsightsMetricsCard_ResultsQuery',
        'variables': '{"postIDs":["'+ post_id +'"],"pageID":"'+ pageId +'"}',
        'server_timestamps': 'true',
        'doc_id': '3622051797846943',
    }

    media_type = None

    # return 'N/A', ['N/A' for i in range(8)]

    html = post_request_html(realurl, cookie, add_header=headers, data=body)

    if 'Rate limit exceeded' in html:
        return 'N/A', ['N/A' for i in range(8)]

    json_obj = json.loads(html)['data']
    aggregated_bc_posts_with_insights = json_obj.get('aggregated_bc_posts_with_insights', {})
    posts_with_insights = aggregated_bc_posts_with_insights['posts_with_insights'][0]
    aggregated_post_insights = aggregated_bc_posts_with_insights['aggregated_post_insights']
    total_reach = exist_no_na(aggregated_post_insights['reach']['total'], '0')
    total_paid = exist_no_na(aggregated_post_insights['reach']['paid'], '0')
    total_organic = exist_no_na(aggregated_post_insights['reach']['organic'], '0')

    post_insights = posts_with_insights.get('post_insights')
    reactions = exist_no_na(post_insights['reactions']['total'])
    comments = exist_no_na(post_insights['comments']['total'])
    saves = exist_no_na(post_insights['saves']['total'])
    shares = exist_no_na(post_insights['shares']['total'])
    clicks = exist_no_na(post_insights['clicks']['total'])

    if posts_with_insights.get('ig_post'):
        video_view_count = posts_with_insights['ig_post']['video_view_count']
        media_type = 'Photo' if not video_view_count else 'Video'

    return media_type, [total_reach, total_paid, total_organic, comments, shares, clicks, reactions, saves]


def exist_no_na(ori, default='0'):
    return ori if ori else default


def get_fb_basic(obj):
    author = obj['actors'][0]['name']
    media_type = obj['attachments'][0]['media']['__typename']
    content = obj['message']['text']
    create_time = obj['creation_time']

    return author, media_type, content, create_time


def get_ig_basic(obj):

    content = obj['caption_text']
    create_time = obj['creation_time']
    return content, create_time


def get_date(ori):
    dt = datetime.fromtimestamp(ori)
    return dt.strftime('%d/%m/%Y')


def request_loop(end_cursor, realurl, assetID, country, platform):

    while end_cursor:
        body = {
            'av': '100000028096171',
            '__user': '100000028096171',
            '__a': '1',
            '__dyn': '7xe6FoO3-Q5E5ObG5V8WnFwRwCwgE98nyUdU6C7QdwSAAzoObxW4E6S7ES2S4oeodEeE6u3y4o4O11wlE1upE4W0LEK0KEswv8ao88hwKwEwDxC5o-0jG12Ki8wl8G1uw_wsU9k2C2218wIwNxK16wnEfogw9KfxW18wkU3mwkE9od8e85m1uws8cU-mmU',
            '__csr': '',
            '__req': '1b',
            '__beoa': '0',
            '__pc': 'PHASED:DEFAULT',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1002842064',
            '__s': 'z2moug:plhj15:3bxmwl',
            '__hsi': '6884867916017957847-0',
            '__comet_req': '0',
            'fb_dtsg': fb_dtsg,
            'jazoest': '22004',
            '__spin_r': '1002842064',
            '__spin_b': 'trunk',
            '__spin_t': '1602949428',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'BCMPInsightsTablePaginationContainerQuery',
            'variables': '{"count":20,"cursor":"' + end_cursor.replace('"', '\\"') + '","filters":{"end_date":1735660800,"platform":["' + platform + '"],"post_IDs":null,"post_type":null,"start_date":1577808000},"actor_type":"brand","is_tagged_view":true,"pageID":"' + assetID + '"}',
            'server_timestamps': 'true',
            'doc_id': '3719409521508201',
        }

        html = post_request_html(realurl, cookie, add_header=headers, data=body)

        json_obj = json.loads(html)

        bc_posts_insights = json_obj.get('data', {}).get('page', {}).get('bc_posts_insights', {})

        end_cursor = process_response(bc_posts_insights, realurl, assetID, country, platform)


def walk(rootDir):
    files = []
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.csv' in path:
            files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files


def one_sheet1_():
    for item in urls:
        request_sheet1(item)

    write_excel('sheet1.xls', sheet1_data)


def two_export_details(filename):
    asset_postIds = {}

    page_size = 92

    sheet = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = sheet.sheets()[0]

    for i in range(1, table.nrows):
        row = table.row(i)
        post_id = row[2].value
        post_url = row[5].value
        assetID = post_url.split("page_id=")[1].split('&')[0]
        # if assetID != '111693948918341':
        #     continue
        if assetID not in asset_postIds:
            asset_postIds[assetID] = []
        asset_postIds.get(assetID).append(post_id)

    for k, v in asset_postIds.items():
        length = len(v)
        t = 0
        while length > 0:
            url = 'https://www.facebook.com/branded_content/brand/' + k + '/export_insights/?actor_type=brand&selected_metrics[0]=post_impressions_unique&selected_metrics[1]=post_impressions_paid_unique&selected_metrics[2]=post_impressions_organic_unique&selected_metrics[3]=fb_post_reaction_breakdown&selected_metrics[4]=fb_post_comment_viral_breakdown&selected_metrics[5]=fb_post_share_viral_breakdown&selected_metrics[6]=fb_post_click_breakdown&selected_metrics[7]=ig_post_save_breakdown'
            print k,  length
            for i in range(min(length, page_size)):
                url += '&post_ids[%d]=%s' % (i, v[i])
            print url
            download_response(url, cookie, 'data/%s_%d.csv' % (k, t))

            length -= page_size
            t += 1
            v = v[t*page_size:]


def three_assemble(basic_filename):

    post_details = {}

    filenames = walk('data/')

    for filename in filenames:
        with open(filename) as fp:
            reader = csv.reader((line.replace('\r', '') for line in fp), delimiter=",", quotechar='"')
            data_read = [row for row in reader]
            for data in data_read[2:]:
                if not data:
                    continue
                try:
                    k = filename.split('data/')[1].split('_')[0] + '_' + data[0].replace('\'', '')
                except Exception as e:
                    print filename, data, e
                v = data
                post_details[k] = v

    print len(post_details)

    sheet = xlrd.open_workbook(basic_filename, encoding_override="utf-8")
    table = sheet.sheets()[0]

    for i in range(1, table.nrows):
        row = table.row(i)
        post_id = row[2].value
        post_url = row[5].value
        assetID = post_url.split("page_id=")[1].split('&')[0]

        details = post_details.get(assetID+'_'+post_id)

        one_row = [row[j].value for j in range(table.ncols)]

        try:
            if not details:
                print 'no cache---', assetID, post_id
                media_type, details = get_details('https://business.facebook.com/api/graphql/', assetID, post_id)
                one_row = one_row[:7] + details
                if media_type:
                    one_row[4] = media_type
            else:
                one_row[4] = details[2] # type
                one_row[8] = details[5]  # total reach
                one_row[9] = details[6]  # paid reach
                one_row[10] = details[7]  # organic reach
                one_row[11] = details[9]  # comments
                one_row[12] = details[10]  # shares
                one_row[13] = details[11]  # click
                one_row[14] = details[8]  # reaction
                one_row[15] = details[12]  # save
        except Exception as e:
            print 'EXCEPTION--assemble', one_row, e
            media_type, details = get_details('https://business.facebook.com/api/graphql/', assetID, post_id)
            one_row = one_row[:7] + details
            if media_type:
                one_row[4] = media_type
        sheet1_data.append(one_row)

    write_excel('final.xls', sheet1_data)

one_sheet1_()
two_export_details('data/sheet1.xls')
three_assemble('data/sheet1.xls')