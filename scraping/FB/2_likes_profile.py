# coding: utf-8
import sys, urllib
import urllib2
import re
import HTMLParser
import time, datetime
import xlwt
import os
import httplib

stop = False
urls = [
    ['https://www.facebook.com/AIAHongKong/', 'AIA Hong Kong', '258,782', '252,818', 'AIA_%d'],
    ['https://www.facebook.com/AXAHongKong/', 'AXA Hong Kong', '18,271', '18,610', 'AXA_%d'],
    ['https://www.facebook.com/BupaHongKong/', 'Bupa Hong Kong 保柏', '67,675', '65,603', 'BUP_%d'],
    ['https://www.facebook.com/CignaHK/', 'Cigna Hong Kong 信諾環球保險', '34,264', '34,679', 'CIG_%d'],
]

page_id = ''

alldata = [['Profile ID', 'Name', 'Profile URL', 'Lives in', 'Likes Main Page', 'Profile like Url']]

cookie = 'sb=4vPuWu4_DWNmHEBouS4jeeAI; datr=6vPuWmi5IYVhJZtr0yzaQ4Jl; dpr=2; c_user=100006957738125; xs=90%3A6hEzya-A7h34oA%3A2%3A1532013169%3A20772%3A8703; fr=0NT9QsWhwBGUSDrtW.AWXSW2eZfHL6Hx6-ohqA60peDM0.BazwYT.Bv.AAA.0.0.BbUKpx.AWX5mqSL; pl=n; spin=r.4119144_b.trunk_t.1532013170_s.1_v.2_; act=1532013241147%2F0; presence=EDvF3EtimeF1532013300EuserFA21B06957738125A2EstateFDutF1532013300454Et3F_5b_5dElm3FnullEutc3F0CEchFDp_5f1B06957738125F2CC; wd=1123x310'


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


def save_value(params):
    i = 1
    count = 0
    cursor = 'AbpTsh-CFYj1lO2qB7HFW4DFgz71Z4IX0j_Bw2NEE-Pdp_ffVprsucjicW_2by-F5iKg7tFLbup-rDGpdzzhQeOyBYdeMG_IyHU92-poPps5jK6ecv6P4PJI90Ob4RS8bKtDsfgiZkxg3AZY1ZNCeqKGGjxV6Tl4NBuEJqKBB1fHRKpoVOvrIJ2TENGQK98OMcP14XHFZ_32mfwSqZj8_Qg0RiBpDbQaf5J11UperKdsqaPzWldbUIRyX14jOv1khOU2lYfmHLEfwxntbCS_R6hAbfcQw8upm7z3rXRzEJ6gP0y_qAr9YpIbhJEltU5MbFBMJJ1m8GbM9QV8-i2V3pCa30Jvu0SKCsEKcqXDIjmNJIM_02dRgObw7TtCxW7qQkm6nOET0p3QtWrPUSDNt7ab'
    while count <= 500 and not stop:
        try:
            url = 'https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet?dpr=2&data={"view":"list","encoded_query":"{\\"bqf\\":\\"likers(%s)\\",\\"browse_sid\\":\\"65e1c0e9c991d7c2062d11d6db380364\\",\\"typeahead_sid\\":null,\\"vertical\\":\\"none\\",\\"post_search_vertical\\":null,\\"intent_data\\":null,\\"filters\\":[],\\"has_chrono_sort\\":false,\\"query_analysis\\":null,\\"subrequest_disabled\\":false,\\"token_role\\":\\"NONE\\",\\"preloaded_story_ids\\":[],\\"extra_data\\":null,\\"disable_main_browse_unicorn\\":false,\\"entry_point_scope\\":null,\\"entry_point_surface\\":null,\\"squashed_ent_ids\\":[],\\"source_session_id\\":null,\\"preloaded_entity_ids\\":[],\\"preloaded_entity_type\\":null,\\"high_confidence_argument\\":null,\\"query_source\\":null,\\"logging_unit_id\\":\\"browse_serp:25c540b7-41bb-c28f-4b32-da05a5461885\\",\\"query_title\\":null}","encoded_title":"WyJQZW9wbGUrd2hvK2xpa2UrIix7InRleHQiOiJBZGVzK0luZG9uZXNpYSIsInVpZCI6MzQwOTQ5NzMyNjIyMDEzLCJ0eXBlIjoiYWN0aXZpdHkifV0","ref":"about","logger_source":"www_main","typeahead_sid":"","tl_log":false,"impression_id":"67d3933a","filter_ids":{"100002761197106":100002761197106,"100003479972525":100003479972525},"experience_type":"grammar","exclude_ids":null,"browse_location":"browse_location:browse","trending_source":null,"reaction_surface":null,"reaction_session_id":null,"is_trending":false,"topic_id":null,"place_id":null,"story_id":null,"callsite":"browse_ui:init_result_set","has_top_pagelet":true,"display_params":{"crct":"none"},"cursor":"%s","page_number":%d,"em":false,"tr":null}&__user=100006957738125&__a=1&__dyn=7AgNe-4am2d2u6aJGeFxqewRyWzEy4QjFwxx-6ES2N6wAxu13wHwZx-EK3q2OUuxa3KbwTz8S2S4o5eu58O5U7S4E9ohwoU8u3S7WwaWu0w8fFHxC68nxK1Iwgovy88E6WdzEmx21OzK8xa4oC2bK2i6S3C788U8Kq0QUuw&__req=b&__be=1&__pc=PHASED:DEFAULT&__rev=3899976&__spin_r=3899976&__spin_b=trunk&__spin_t=1526050650' % (page_id, cursor, i)
            html = get_request_of_url(url)
            reg = 'class="_32mo" href="(.*?)".*?<span>(.*?)<.*?class="_glo">.*?href="/search(.*?)">.*?(.*?)<div class="_glp"'
            profile_list = re.compile(reg).findall(html)
            if not profile_list:
                continue
            for profile in profile_list:
                profile_url = profile[0]
                profile_name = remove_html_tag(profile[1])
                profile_like_url = 'https://www.facebook.com/search' + profile[2]
                content = remove_html_tag(profile[3])
                live_reg = 'Lives in Hong Kong'
                location = re.compile(live_reg).findall(content)
                if location:
                    one_row = [params[4] % count, profile_name, profile_url, 'Hong Kong', params[1], profile_like_url]
                    print(one_row)
                    alldata.append(one_row)
                    count += 1
            cursor_reg = '"cursor":"(.*?)"'
            cursors = re.compile(cursor_reg).findall(html)
            for cur in cursors:
                if cur != cursor:
                    cursor = cur
                    break
        except Exception as e:
            print(e)
        i += 1


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
        write_excel('profile_'+filename, alldata)
        del alldata
        stop = False
        alldata = [['Profile ID', 'Name', 'Profile URL', 'Lives in', 'Likes Main Page', 'Profile like Url']]

