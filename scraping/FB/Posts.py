# coding: utf-8
import sys, urllib
import urllib2
import re
import HTMLParser
import time, datetime
import xlwt
import os
import httplib

'''
data format:
https://www.facebook.com/pages_reaction_units/more/
?page_id=119197964825456
&cursor={"timeline_cursor":
    "timeline_unit:1:00000000001465461907:04611686018427387904:09223372036854775800:04611686018427387904",
    "timeline_section_cursor":{},
    "has_next_page":true
}
&surface=www_pages_home&unit_count=8&dpr=2
&__user=0&__a=1&__dyn=7xeXxaER0gbgmwCwRAKGzEy4--C11xG3Kq5Qbxu13wmeexZ3orxuE98KaxeUdUlDixa2qnDBxe6o8fypUlxq2K2S1typ9Uqx24o&__req=5&__be=0&__pc=PHASED:DEFAULT&__rev=2385596
https://www.facebook.com/pages_reaction_units/more/
?page_id=123614990983436
&cursor={"timeline_cursor":
    "timeline_unit:1:00000000001523851389:04611686018427387904:09223372036854775800:04611686018427387904",
    "timeline_section_cursor":{},
    "has_next_page":true}
&surface=www_pages_home&unit_count=8&dpr=2
&__user=100006957738125&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzFEbEyGgS8VpQAjFGA6EvxuES2N6xvyEybGqK6qxeqaxu9wwz8KFUKbnyogyEnGi4FpeuUuF3e2e5WDokzUhyKdyU8rh4jUXVubx11rDAyF8O49ElwQUlByECQi8yFUix6cw_xrUtVe49888vGfCCgWrxjyoG69Q4UlDBgS6p8szoGqfxmfCx6WLBx6695UCUZqBxeybaWzQQ25iK8wDAyXCAzUx39rgCdUcUpx3yUymf-KeAKqUS4oCiEWbAzecUyma-KaDU8fl4yFppbhe4S2eh4yESQ9BK4pUV1bCxe9yEgxO5oggSGDz8uz8JyV8&__req=18&__be=1&__pc=PHASED:DEFAULT&__rev=3882616&__spin_r=3882616&__spin_b=trunk&__spin_t=1525609587
'''

stop = False
urls = [
    ['https://www.facebook.com/SehatAQUA/', 'Sehat AQUA', '2,377,325', '2,360,870'],
    ['https://www.facebook.com/minumvit/', 'Minum VIT', '232,714', '232,596'],
    ['https://www.facebook.com/LeMinerale', 'Le Minerale', '394,864', '394,879'],
    ['https://www.facebook.com/AdesIndonesia', 'Ades Indonesia', '147,516', '147,145'],
]

alldata = [['Page Url', 'Page Name', 'No. likes', 'No. follows', 'Post Url', 'Date', 'Main Text', 'No. reactions', 'No. Comment', 'No. Shares', 'No. Views']]

cookie = 'sb=4vPuWu4_DWNmHEBouS4jeeAI; dpr=2; c_user=100006957738125; xs=243%3AC-TV1OHPqIWwWA%3A2%3A1525609449%3A20772%3A8703; pl=n; datr=6vPuWmi5IYVhJZtr0yzaQ4Jl; fr=0NT9QsWhwBGUSDrtW.AWWHlqXnck2-1LOo2c_8ngXjPRc.BazwYT.Bv.Fru.0.0.Ba7vPt.AWWBu1mc; act=1525609467323%2F2; presence=EDvF3EtimeF1525609595EuserFA21B06957738125A2EstateFDutF1525609595652CEchFDp_5f1B06957738125F2CC; wd=1234x419'
tail = '&surface=www_pages_home&unit_count=8&dpr=1&__user=100006957738125&__a=1&__dyn=5V5yAW8-aFoFxp2u6aOGeFxqeCwKAKGgS8zCC-C26m6oKewWhEnz8nwgUaqwHx24UJi28rxuF8WUOuVWxeUW6UO4GDgdUHDBxe6rCxaLGqu58nVV8-cx2jxm3i2y9ADBy8K48hxGbwYDx2r_xLgkBx-26KiaggzE-49pp8CcVUO&__af=m&__req=m&__be=-1&__pc=PHASED:DEFAULT&__rev=2706175'


def get_ori_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    page.close()
    return html


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_first_four_column(html):
    ''' analysis response to get value of first four columns in excel'''

    global first_four_col, stop
    general_reg = 'class="_5pcr userContentWrapper"(.*?)<form'
    post_list = re.compile(general_reg).findall(html)
    res_photos, res_videos = [], []
    date = ''
    for post in post_list:
        if 'photos' in post and 'videos' not in post:
            reg = 'class="_5pcq" href="/(.*?)".*?><abbr title="(.*?)".*?</abbr>.*?<div class=".*?userContent.*?>(.*?)</div>.*?href=.*?a\.(.*?)\.'
            post_detail = re.compile(reg).findall(post)
            if not post_detail:
                continue
            '''i[0] message url; i[1] raw date; i[2] raw message'''
            i = post_detail[0]
            message = remove_html_tag(i[2])
            date = i[1].split(' ')[0]
            message_url = "https://www.facebook.com/" + i[0]
            res_photos.append([message_url, date, message])
        else :
            reg = 'href="/(.*?)".*?abbr title="(.*?)".*?userContent.*?>(.*?)</div>'
            post_detail = re.compile(reg).findall(post)
            '''i[0] message url; i[1] raw date; i[2] raw message'''
            if not post_detail:
                continue
            i = post_detail[0]
            message = remove_html_tag(i[2])
            date = i[1].split(' ')[0]
            message_url = "https://www.facebook.com/" + i[0]
            res_videos.append([message_url, date, message])
    if not post_list:
        stop = True
        return [], [], 0
    last_time = int(time.mktime(datetime.datetime.strptime(i[1], "%d/%m/%Y %H:%M").timetuple()))
    return res_photos, res_videos, last_time


def get_second_four_column(html):
    ''' analysis response to get value of second four columns in excel'''
    second_four_dict = {}
    '''i[0]: post_id, i[1]: comment count; i[2]: like count; i[3]: message URL; i[4]: sharecount'''
    reg = '"canviewerreact":.*?,.*?"commentcount":(.*?),.*?"entidentifier":"(.*?)".*?lc":.*?"likecount":(.*?),.*?"permalink":"(.*?)".*?"sharecount":(.*?),.*?'
    likeshare = re.compile(reg).findall(html)
    for i in likeshare:
        if 'posts' in i[3]:
            photo_link = get_photo_link_of_posts('http://www.facebook.com' + i[3])
            if photo_link:
                key = photo_link.split('/')[-2]
                second_four_dict[key] = [i[2], i[0], i[4]]
        second_four_dict[i[1]] = [i[2], i[0], i[4]]
    return second_four_dict


def get_photo_link_of_posts(url):
    html = get_request(url)
    reg = 'class="_5pcq" href="(.*?)"'
    res = re.compile(reg).findall(html)
    return res[0] if res else ''


def get_second_four_without_video(html):
    return get_second_four_column(html)


def get_video_view_count(html):
    ''' analysis response to get value of second four columns in excel'''
    second_four_dict = {}
    reg = 'fluentContentToken":"(.*?)".*?"viewCount":"(.*?)"'
    lists = re.compile(reg).findall(html)
    for i in lists:
        second_four_dict[i[0]] = i[1]
    return second_four_dict


def get_req(page_id, time_line, minus8, timestamp):
    '''send response to facebook server to get the return value (6 posts in one time)'''
    '''00000000001446908402:04611686018427387904:09223372036854775800:04611686018427387904'''
    url = "https://www.facebook.com/pages_reaction_units/more/?page_id="

    url += page_id

    data = '&cursor={"timeline_cursor":"timeline_unit:1:0000000000'
    data = data + str(timestamp) + ':' + time_line + ':0' + str(minus8) + ':' + time_line + '",'

    data += '"timeline_section_cursor":{},"has_next_page":true}'
    # data += '"timeline_section_cursor":{"profile_id":'+page_id+',"start":0,"end":1475669953,"query_type":36,"filter":1},"has_next_page":true}'
    data += tail
    url += data

    return get_request_of_url(url)


def get_request_of_url(url):
    print url
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    res = HTMLParser.HTMLParser().unescape(res).decode('unicode-escape').replace('\\', '')
    return res


def get_request(url):
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res


def save_value(params):
    '''
    1:00000000001447171200:04611686018427387904:09223372036854775804:04611686018427387904
    time_line = 04611686018427387904
    minus4 = 9223372036854775804
    timestamp = 1447171200
    '''
    time_line = '04611686018427387904'
    minus8 = 9223372036854775800
    timestamp = str(int(time.time()))
    count = 0

    while count <= 200 and not stop:
        try:
            response = get_req(page_id, time_line, minus8, timestamp)
            # response = get_request_of_url('https://www.facebook.com/pages_reaction_units/more/?page_id=123614990983436&cursor={"timeline_cursor":"timeline_unit:1:00000000001455025200:04611686018427387904:09223372036854775584:04611686018427387904","timeline_section_cursor":{},"has_next_page":true}&surface=www_pages_home&unit_count=8&dpr=1&__user=100006957738125&__a=1&__dyn=5V5yAW8-aFoFxp2u6aOGeFxqeCwKAKGgS8zCC-C26m6oKewWhEnz8nwgUaqwHx24UJi28rxuF8WUOuVWxeUW6UO4GDgdUHDBxe6rCxaLGqu58nVV8-cx2jxm3i2y9ADBy8K48hxGbwYDx2r_xLgkBx-26KiaggzE-49pp8CcVUO&__af=m&__req=m&__be=-1&__pc=PHASED:DEFAULT&__rev=2706175')
            response = response.replace("\n", "").replace("\r", "")
            # write(response, '1.html')
            photo_list, video_list, timestamp = get_first_four_column(response)
            second_four_dict = get_second_four_without_video(response)

            if video_list:
                view_count_dict = get_video_view_count(response)
            else:
                view_count_dict = {}

            for post in photo_list:
                if 'posts' in post[0]:
                    key = post[0].split('/')[-1]
                else:
                    key = post[0].split('/')[-2]
                details = second_four_dict.get(key)
                if details:
                    one_row = params + post[:3] + details + ['N/A']
                    print one_row
                    alldata.append(one_row)
            for post in video_list:
                if 'posts' in post[0]:
                    key = post[0].split('/')[-1]
                else:
                    key = post[0].split('/')[-2]
                details = second_four_dict.get(key)
                if details:
                    one_row = params + post + details + [view_count_dict.get(key, 0)]
                    print one_row
                    alldata.append(one_row)
            minus8 -= 8
            count += len(photo_list) + len(video_list)
        except Exception as e:
            print(e)
            minus8 -= 8


def write_excel(filename, alldata, flag=None):
    filename = 'data/' + filename
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
                    print '===Write excel ERROR===' + str(one_row[col])
    w.save(filename)
    print filename + "===========over============"


def set_page_id(url):
    global page_id
    reg = 'page_id=(\d*)'
    html = get_ori_html(url)
    page_id = str(re.compile(reg).findall(html)[0])


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    for url in urls:
        print '=======start '+url[0]+' ========='
        filename = "" + url[0].split("/")[3].split("?")[0] + ".xls"
        set_page_id(url[0])
        save_value(url)
        write_excel(filename, alldata)
        del alldata
        stop = False
        alldata = [['Page Url', 'Page Name', 'No. likes', 'No. follows', 'Post Url', 'Date', 'Main Text', 'No. reactions', 'No. Comment', 'No. Shares', 'No. Views']]
