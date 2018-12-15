# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import sys
from datetime import datetime
import HTMLParser
import os
import pytz
import urllib2
from urlparse import urlparse
import time
import random
from apscheduler.schedulers.blocking import BlockingScheduler

ins_cookie = 'mid=W-u__gAEAAEhh26m31QbTG97OUH0; mcd=3; fbm_124024574287414=base_domain=.instagram.com; csrftoken=vLvc98valMtFcrDjjbpmSYswRBylfaRN; shbid=12530; shbts=1542176792.8468142; ds_user_id=1106215210; sessionid=1106215210%3ABjJTyJ885ruv4T%3A14; rur=ASH; ig_lang=en; fbsr_124024574287414=rDRleU5f8Kp6kvEApKEM07KatPaU9A0SEXuuIGTPMDM.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUJtaVBKX0Y0V3lnVDBDZWx6ZDN6RmJ4VTQ2WHJBTUpIY1hJZUtwdVhEaHMzd1ZFZG5vcTJWVWMxd1Fza2YyQVdQNUFPQkFpOXE0Z1BEVHMxOXE2X2Vla0pxVG11VHdOeDRiemgzYmgzclpaSDN1V1ZhRVFScWp2RXpySjdlMWd4Y3M4YmJRYmtULWhjbGd1Vm9XbFVuOWJvaFVGSHVuM0t4ZnVVLUV6LTVFbFM4LU14dGVtRVQxQ0ZwOWh0ajdIVGxKcU1fNE1CNzFiZFBnaU5fWkQ3YWVDejhGV25KREhaRHktYkVlMmtTWDJLZVBCVmJELVprdXk2aGlLM2ZhWXY4THZvbmJMVk84cmZRRzdSYmk0Uy1UOTQ2cXBwSjdqUDd6R2pma0pwbXZJQ2FadFRRZDhqU2IyZHZOQnM1V2RFWGNiSm1CVU9fNGZmYU54NG9XVC0xcCIsImlzc3VlZF9hdCI6MTU0MjE3OTgxMCwidXNlcl9pZCI6IjEwMDAwNjk1NzczODEyNSJ9; urlgen="{\"45.62.52.59\": 32181\054 \"45.62.52.15\": 32181}:1gMpPv:Ov96EjqhnGA3B7_Z746jB4XRiPk"'
tw_cookie = 'personalization_id="v1_x2BKuuvBAdUk7NxqynJGZQ=="; guest_id=v1%3A154217930211516786; ct0=31234449d197cfe8ab5d35997c62bf74; _ga=GA1.2.209209783.1542179306; _gid=GA1.2.782708477.1542179306; gt=1062603149062488064; _gat=1; ads_prefs="HBERAAA="; kdt=M4wYA82MYA6p12Tkylt3UOnechyIMIv3cgbZLIrM; remember_checked_on=1; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCOaqDBFnAToMY3NyZl9p%250AZCIlZjNkZTBmZTMzMzg2YmJhZDE5YjhjNTY1MGM5OGFhZGI6B2lkIiVkYWNl%250AY2VjMWU5NmMyNDNkMGYzODU4ZWYyYTlkZjZlMDoJdXNlcmwrB2IP058%253D--549b6ff0906cf6cc2b2719d2b01f28742422b8cd; twid="u=2681409378"; auth_token=5df30733a4009c721b5a142eab5c085cea4430e3; csrf_same_site_set=1; csrf_same_site=1; lang=en-gb'
fb_cookie = 'datr=RKzWW_1NuhIxB9RG7RUemqv0; sb=ovjqW-tww_Qe7OR39cZQ91wp; locale=en_GB; c_user=100006957738125; xs=145%3Ay4f_mOf19tmvnQ%3A2%3A1542430919%3A20772%3A8703; pl=n; dpr=2; spin=r.4548695_b.trunk_t.1542638053_s.1_v.2_; act=1542639874786%2F1; fr=0mVSQPNFOoV7LvCYc.AWVWZvgfIqiR2Np4qN_AxVfgztw.Bb0aQ1.Cv.AAA.0.0.Bb806Q.AWUsIh6L; wd=1385x340; presence=EDvF3EtimeF1542672484EuserFA21B06957738125A2EstateFDt3F_5b_5dG542672484687CEchFDp_5f1B06957738125F2CC; pnl_data2=eyJhIjoiQmlnUGlwZS9pbml0IiwiYyI6IlhWaWRlb1Blcm1hbGlua0NvbnRyb2xsZXIiLCJiIjpmYWxzZSwiZCI6Ii9yZWFsdGFycmFidWRpbWFuL3ZpZGVvcy8zMjA1ODc4NTU0Mzg1ODUvIiwiZSI6W119'

cur_date = None
sheet_data = [['Date (GMT+7)', 'Time (GMT+7)', 'Category', 'Post', 'URL', 'Likes', 'Views', 'Comments', 'Share/Retweet', 'Interested', 'Going']]
# sheet_data = [['Date (GMT+7)', 'Time (GMT+7)', 'View', 'Comment', 'Share', 'reaction_count']]
FB_video_urls = [
    ('https://www.facebook.com/realtarrabudiman/videos/320587855438585/', 'FB_FAN_PAGE', 'Teaser', 'https://www.facebook.com/video/tahoe/async/320587855438585/?originalmediaid=320587855438585&playerorigin=permalink&playersuborigin=tahoe&ispermalink=true&numcopyrightmatchedvideoplayedconsecutively=0&storyidentifier=UzpfSTEwMTMzMzAxMDE5ODUzMjpWSzozMjA1ODc4NTU0Mzg1ODU&payloadtype=secondary&dpr=2'),
    ('https://www.facebook.com/tarra.budiman.31/videos/10217614393048698/', 'FB_PROFILE', 'Teaser', 'https://www.facebook.com/video/tahoe/async/10217614393048698/?originalmediaid=10217614393048698&playerorigin=permalink&playersuborigin=tahoe&ispermalink=true&numcopyrightmatchedvideoplayedconsecutively=0&storyidentifier=UzpfSTExNDQ2MjU5MzM6Vks6MTAyMTc2MTQzOTMwNDg2OTg&payloadtype=secondary&dpr=2'),
    ('https://www.facebook.com/MasterCardID/videos/1052908328202996/', 'MC IND Page FB', 'Teaser Boosted', 'https://www.facebook.com/video/tahoe/async/1052908328202996/?originalmediaid=1052908328202996&playerorigin=permalink&playersuborigin=tahoe&ispermalink=true&numcopyrightmatchedvideoplayedconsecutively=0&storyidentifier=UzpfSTkwNjg5NjkyOTM5ODY1OTpWSzoxMDUyOTA4MzI4MjAyOTk2&payloadtype=secondary&dpr=2')
]
FB_posts_multi = [
    ('https://www.facebook.com/MasterCardID/photos/a.947467582008260/1951841041570904/', '1951842181570790', 'MC IND Page FB', '360'),
]
FB_personal = [
    ('https://www.facebook.com/tarra.budiman.31?lst=100006957738125%3A1144625933%3A1542462305', 'FB_PROFILE', 'Invite', '/tarra.budiman.31/posts/10217629723471949')
]
FB_posts = [
    ('https://www.facebook.com/photo.php?fbid=10217621812114170&set=a.10203809864424110&type=3&theater', 'FB_PROFILE', '360')
]
event_urls = [
    'https://www.facebook.com/events/291842851666556/',
    'https://www.facebook.com/events/291842848333223/',
    'https://www.facebook.com/events/291842858333222/',
]


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
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
                    print('===Write excel ERROR===' + str(one_row[col]))
    w.save(filename)
    print(filename + "===========over============")


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_date():
    global cur_date
    cur_date = datetime.now(pytz.timezone('Etc/GMT-7')).strftime('%H:%M %d/%m/%Y')


def get_request_of_url(url, cookie):
    print url
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
    req.add_header("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    res = HTMLParser.HTMLParser().unescape(res).decode('unicode-escape').replace('\\', '')
    return res


def get_request(get_url, cookie):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
        'x-csrf-token': '31234449d197cfe8ab5d35997c62bf74',
        'x-twitter-auth-type': 'OAuth2Session',
        'refer': get_url,
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAPYXBAAAAAAACLXUNDekMxqa8h%2F40K4moUkGsoc%3DTYfbDKbT3jJPCEVnMYqilB28NHfOPqkca3qaAxGfsyKCs0wRbw'
    }
    res_data = requests.get(get_url, headers=headers, timeout=12)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


def post_request(get_url, cookie):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Referer': 'https://www.facebook.com/realtarrabudiman/videos/320587855438585/',
        'Cookie': cookie,
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
    }
    data = {
        '__user': '100006957738125',
        '__a': '1',
        '__dyn': '7AgNe-4amaxx2u6Xolg9odoKEW74jFwxx-6EeAq2i5U4e2C3-7WyUrxuEbbxWU4GawhoS2S4o5K58O0BoiwBx61zwzU5K0IpU2_CxS326U6O11x-2K1KxO5Egw9-4oC2bwEwlUOEOm19w8OEG1zwxKdwl8G5EcUjzbxi6o984Wexp2Utwww',
        '__req': '3',
        '__be': '1',
        '__pc': 'PHASED:DEFAULT',
        '__rev': '4548695',
        'fb_dtsg': 'AQFUs5zysSlm:AQFMl2WMljlf',
        'jazoest': '26581708511553122121115831081095865817077108508777108106108102',
        '__spin_r': '4548695',
        '__spin_b': 'trunk',
        '__spin_t': '1542638053',
    }
    res_data = requests.post(get_url, headers=headers, timeout=10, data=data)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


def for_inst():
    url = 'https://www.instagram.com/p/BqJjd9pB8be/'
    html = get_request(url, ins_cookie)
    reg = '<meta content="(.*?) Likes, (.*?) Comments.*?video_view_count":(.*?),'
    data = re.compile(reg).findall(html)
    # like, comment, view
    one_row = [cur_date.split(' ')[1], cur_date.split(' ')[0], 'IG', 'Teaser', url, data[0][0], data[0][2], data[0][1], '0', '0', '0']
    sheet_data.append(one_row)


def for_fb_video():
    for url in FB_video_urls:
        html = post_request(url[3], fb_cookie)
        reg = 'postViewCount":(.*?),.*?commentCount":(.*?)}.*?sharecount":(.*?),.*?reactioncount":(.*?),.*?'

        data = re.compile(reg).findall(html)
        sheet_data.append([cur_date.split(' ')[1], cur_date.split(' ')[0], url[1], url[2], url[0], data[0][3], data[0][0], data[0][1], data[0][2], '0', '0'])


def for_FB_post_with_multi():
    for url in FB_posts_multi:
        html = get_request(url[0], fb_cookie)
        reg = 'postViewCount.*?:(.*?),.*?commentcount.*?:(.*?),.*?"post_fbid":(.*?)}.*?sharecount.*?:(.*?),.*?reactioncount.*?:(.*?),'

        data_list = re.compile(reg).findall(html)

        for data in data_list:
            if data[2] == url[1]:
                sheet_data.append([cur_date.split(' ')[1], cur_date.split(' ')[0], url[2], url[3], url[0], data[4], data[0], data[1], data[3], '0', '0'])


def for_FB_post():
    for url in FB_posts:
        html = get_request(url[0], fb_cookie)
        reg = 'postViewCount.*?:(.*?),.*?commentcount.*?:(.*?),.*?sharecount.*?:(.*?),.*?reactioncount.*?:(.*?),'

        data_list = re.compile(reg).findall(html)

        data = data_list[0]
        sheet_data.append(
            [cur_date.split(' ')[1], cur_date.split(' ')[0], url[1], url[2], url[0], data[3], '0', data[1], data[2], '0', '0'])


def for_FB_personal():
    for url in FB_personal:
        reg = 'permalink:"(.*?)".*?commentcount:(.*?),.*?harecount.*?:(.*?),.*?reactioncount.*?:(.*?),'
        html = get_request(url[0], fb_cookie)
        data_list = re.compile(reg).findall(html)

        for data in data_list:
            if data[0] == url[3]:
                sheet_data.append([cur_date.split(' ')[1], cur_date.split(' ')[0], url[1], url[2], url[0], data[3], '0', data[1], data[2], '0', '0'])


def for_tweet():
    urls = [
        # ('https://twitter.com/TarraBudiman/status/1062590045968719872', 'Teaser'),
        # ('https://twitter.com/TarraBudiman/status/1063309912795725829', 'TWITTER1'),
    ]
    for url in urls:
        html = get_request(url[0], tw_cookie)
        reg = 'data-tweet-stat-count="(.*?)"'
        data_list = re.compile(reg).findall(html)

        view_url = 'https://api.twitter.com/1.1/videos/tweet/config/%s.json' % url[0].split('/')[-1]
        view_json = get_request(view_url, tw_cookie)
        reg = 'viewCount":"(.*?)"'
        view_data = re.compile(reg).findall(view_json)

        if view_data:
            sheet_data.append([cur_date.split(' ')[1], cur_date.split(' ')[0], 'TWITTER', url[1], url[0], data_list[1], view_data[0], data_list[2], data_list[0], '0', '0'])
        else:
            sheet_data.append([cur_date.split(' ')[1], cur_date.split(' ')[0], 'TWITTER', url[1], url[0], data_list[1], '0', data_list[2], data_list[0], '0', '0'])


def for_tweet_live():
    urls = [
        ('https://twitter.com/TarraBudiman/status/1065225930451279873', 'TWITTER'),
    ]
    for url in urls:
        html = get_request(url[0], tw_cookie)
        reg = 'data-tweet-stat-count="(.*?)"'
        data_list = re.compile(reg).findall(html)

        view_url = 'https://api.twitter.com/1.1/broadcasts/show.json?ids=1DXxyaPQyWZxM&include_events=true'
        view_json = get_request(view_url, tw_cookie)
        reg = '"total_watching":"(.*?)"'
        view_data = re.compile(reg).findall(view_json)

        if view_data:
            sheet_data.append([cur_date.split(' ')[1], cur_date.split(' ')[0], 'TWITTER', url[1], url[0], data_list[1], view_data[0], data_list[2], data_list[0], '0', '0'])
        else:
            sheet_data.append([cur_date.split(' ')[1], cur_date.split(' ')[0], 'TWITTER', url[1], url[0], data_list[1], '0', data_list[2], data_list[0], '0', '0'])


def for_FB_live(live_id):
    global sheet_data
    total_url = 'https://www.facebook.com/video/tahoe/async/%s/?originalmediaid=%s&playerorigin=permalink&playersuborigin=tahoe&ispermalink=true&numcopyrightmatchedvideoplayedconsecutively=0&storyidentifier=UzpfSTE5MDAyMjU4NjY5MDUyMzk6Vks6MjEwODI3Njg0NjE2OTE5MQ&payloadtype=secondary&dpr=2' % (live_id, live_id)
    sub_url = 'https://www.facebook.com/ufi/reaction/profile/dialog/?ft_ent_identifier=' + live_id + '&av=100006957738125&dpr=2&fb_dtsg_ag=AdyhXByjwAdm-uQET_4p2ypMu-iQ_s57QCWgoqDUtByVzg%3AAdwqm8M_j0nXclQ6_GtSqTXcaKGf9xymdt238XqHG1ke6w&__asyncDialog=1&__user=100006957738125&__a=1&__dyn=7AgNe-4amaxx2u6aJGeFxqewRyWzEpF4Wo8ovxGdwIhE98nwgUaofUvGbxK5WwIK7HzEeWDwUyKdwJx64e2u5Ku58O5UlwQwOxa2m4o6e2fwmWxW5o7Cu1uwobG7ooxu6Uao4a11x-2KdUcUaEszXG48fE9EO48y4Ehyo8J1W8BUjU8Vo-cGECmUpzUiVE2cGFUaUaVpoizHAy8aEaoGqbK3e4UOUkxC2i3ufCUO5AbxS22&__req=1d&__be=1&__pc=PHASED%3ADEFAULT&__rev=4548695&__spin_r=4548695&__spin_b=trunk&__spin_t=1542638053'
    live_view_url = 'https://www.facebook.com/video/liveviewcount/?video_id=' + live_id + '&source=tahoe&player_origin=permalink&unmuted=true&dpr=2&fb_dtsg_ag=AdxvB6Upi4JwXAVqiQifWBC9MfkOAfm1Pj9VW1ZgEJHl0A%3AAdxmZvCTMg-iuJL-vu0nuvWPKkEM2XYGedfXUigj1oTOeQ&__user=100006957738125&__a=1&__dyn=7AgNe-4amaUmgDxyHqzGomzFEbEyGzEy4aheC267Uqzob4q2i5U4e2C3-7RyUrxuEnxiUuKewXGu3yaUS2SaCx3wCgmVV8-cxu5od8tyEC4E9ohwj8mwzU5KEuxm1VDwnE4G5rG7ooxu6Uao4a11x-2KaHwPwGUkBz_G486mcx28xa4oC2bhEny9u4-2emfzaG9BK6o-4Kq7o6WGDz8uxC4ppoizHAy8aEaoGqbK3e4UOUkxC2i3ufCUO5AbxS6Fo&__req=16&__be=1&__pc=PHASED%3ADEFAULT&__rev=4554898&__spin_r=4554898&__spin_b=trunk&__spin_t=1542801358'

    html = post_request(total_url, fb_cookie)
    total_reg = 'commentcount":(.*?),.*?sharecount":(.*?),.*?reactioncount":(.*?),'
    total_data = re.compile(total_reg).findall(html)
    comment_count, share_count, reaction_count = total_data[0]

    html = get_request(sub_url, fb_cookie)
    body_reg = 'ScrollableAreaGripper(.*?)FriendListFlyoutLoading'
    data_wrapper = re.compile(body_reg).findall(html)[0]

    sub_reg = 'aria-label=\\\\"(.*?) .*?with (.*?)\\\\'
    sub_list = re.compile(sub_reg).findall(data_wrapper)

    html = get_request(live_view_url, fb_cookie)
    view_reg = 'viewerCount.*?:(.*?),'
    view_data = re.compile(view_reg).findall(html)

    one_row = [cur_date.split(' ')[1], cur_date.split(' ')[0], view_data[0], comment_count, share_count, reaction_count] + [i[0] for i in sub_list]
    sheet_data.append(one_row)


def for_event():
    going_count = 0
    for url in event_urls:
        reg = '"_5z74">(.*?) going'
        html = get_request(url, fb_cookie)
        data = re.compile(reg).findall(html)

        if not data:
            reg = '"dialog" role="button">(.*?) going'
            data = re.compile(reg).findall(html)
        going_count += int(data[0].split('role="button">')[-1])

    reg = 'class="_5z74".*?role="button">(.*?) interested'
    html = get_request('https://www.facebook.com/events/291842844999890/?active_tab=about', fb_cookie)
    data = re.compile(reg).findall(html)
    interest_count = data[0]
    sheet_data.append([cur_date.split(' ')[1], cur_date.split(' ')[0], 'FB', 'Invite', url, '0', '0', '0', '0', interest_count, going_count])


def one_batch():
    get_date()
    print("scraping: ", cur_date)
    for_inst() # 1

    for_fb_video()

    for_FB_post() # 1

    for_FB_post_with_multi() # 1

    for_FB_personal() # 1

    for_event() # 1
    for_tweet() # 2
    write_excel('data/%s.xls' % cur_date.replace(' ', '_').replace('/', '').replace(':', '-'), sheet_data)


def batch_two():
    get_date()
    print("scraping: ", cur_date)

    # for_FB_live('1353618718108708')
    for_tweet_live()
    write_excel('data/%s_tweet.xls' % cur_date.replace(' ', '_').replace('/', '').replace(':', '-'), sheet_data)


# one_batch()
batch_two()
scheduler = BlockingScheduler()
scheduler.add_job(batch_two, 'interval', minutes=1)
scheduler.start()