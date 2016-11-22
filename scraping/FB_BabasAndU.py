#coding: utf-8
import sys, urllib
import urllib2
import re
import HTMLParser
import time,datetime
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
'''

first_four_col = []
second_four_col = {}
third_four_col = []
alldata = []

cookie = 'datr=OYmDV4pQ1woh4694JL3-5EoE; pl=n; lu=ggncrA8_InXU9zQqQIq3HeHA; sb=ZYmDVwozRepnSPcjn8-p-9Ul; c_user=100006957738125; xs=225%3Ak9MlA7_F3uQMrw%3A2%3A1470056820%3A20772; fr=1pJP65hZ44wMFk9by.AWXzN3Yq_NyDAgrv_aKMilOa9Vw.BXg4k5.ss.AAA.1.0.BX9OnZ.AWWMh8zj; csm=2; s=Aa62sIAe4bgGCH6s.BXn0l1; p=-2; presence=EDvF3EtimeF1475668621EuserFA21B06957738125A2EstateFDt2F_5b_5dElm2FnullEuct2F1475667838BEtrFA2loadA2EtwF700850837EatF1475668585022G475668621759CEchFDp_5f1B06957738125F3CC; wd=1234x351'
req_list_ = []
tail = '&surface=www_pages_home&unit_count=8&dpr=1&__user=100006957738125&__a=1&__dyn=5V5yAW8-aFoFxp2u6aOGeFxqeCwKAKGgS8zCC-C26m6oKewWhEnz8nwgUaqwHx24UJi28rxuF8WUOuVWxeUWq58O4GDgdUOum4UpKq4GCzEkxvDAzUO49e5o5S9ADBy8K48hxGbwYDx2r_xLgkBDxu2jzQ&__af=o&__req=k&__be=-1&__pc=PHASED:DEFAULT&__rev=2604134'


def get_ori_html(url):
	page=urllib.urlopen(url)
	html=page.read()
	page.close()
	return html

def write(html,filename):
    fp = open(filename,"w")
    fp.write(html)
    fp.close()
    print "write over"

def get_first_four_column(html, full_time_format, time_format):
    ''' analysis response to get value of first four columns in excel'''

    global first_four_col
    reg = '<a class="_5pcq" href="(.*?)".*?><abbr title="(.*?)".*?</abbr>.*?<div class=".*?userContent".*?>(.*?)</div>'
    postlist = re.compile(reg).findall(html)
    last_date = ''
    for i in postlist:
        '''i[0] message url; i[1] raw date; i[2] raw message'''
        ## Url in the text/post
        text_url = "N/A"
        text_url_reg = '.*?u=(.*?)&.*?'
        text_url_list = re.compile(text_url_reg).findall(i[2])

        if(len(text_url_list) > 0) :
            text_url = urllib.unquote(text_url_list[0]).replace("u00253A",":").replace("u00252F","/")
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub('',i[2])
        ## Message
        message = HTMLParser.HTMLParser().unescape(dd)
        if(message == ""):
            message = "N/A"
        ## Date-----Tuesday, 7 June 2016
        ##date = datetime.datetime.strptime(i[1].split(" at")[0], '%A, %d %B %Y').strftime('%d/%m/%Y')
        ##last_date = time.mktime(time.strptime(i[1],'%A, %d %B %Y at %H:%M'))

        date = datetime.datetime.strptime(i[1].split(" at")[0], time_format).strftime('%d/%m/%Y')
        last_date = time.mktime(time.strptime(i[1], full_time_format))
        message_url = "https://www.facebook.com"+str(i[0])
        message_url = message_url.replace("amp;","")
        one_row = [str(message), message_url.replace("amp;",""), str(date), str(text_url.replace("amp;",""))]
        print one_row[2] + "  " + one_row[0] + "  " + one_row[1] + "  " + one_row[3]
        first_four_col.append(one_row)

    return str(last_date).split('.')[0]

def get_second_four_column(html):
    ''' analysis response to get value of second four columns in excel'''
    global second_four_col
    '''i[0]: comment count; i[1]: like count; i[2]: message URL; i[3]: sharecount; i[4]: comment list'''
    reg = '"canviewerreact":.*?,"commentcount":(.*?),.*?lc":.*?"likecount":(.*?),.*?"permalink":"(.*?)".*?"sharecount":(.*?),.*?,"comments":(.*?),"profiles"'
    likeshare = re.compile(reg).findall(html)
    length = 1
    for i in likeshare:
        one_row = [i[1], i[0], str(get_last_comment_date(i[4])), i[3]]
        if "https://www.facebook.com" in str(i[2]):
            key = str(i[2])
        else:
            key = "https://www.facebook.com"+str(i[2])
        key.replace("amp;","")
        print key + "   " + one_row[0] + "  " + one_row[1] + "  " + one_row[2] + "  " + one_row[3]
        second_four_col[key] = one_row
        length += 1
    return length

def get_third_four_column(ori_url, likes_url):
    global third_four_col
    reg=r'<span id="PagesLikesCountDOMID"><span class="_52id _50f5 _50f7">(.*?)<span class="_50f8 _50f4 _5kx5">.*?</span></span></span>'
    pagelike = re.compile(reg).findall(get_ori_html(ori_url))
    like_reg = '<meta name="description" content=".*? (.*?) likes.*?; (.*?) talking about this'
    html = get_ori_html(likes_url)
    last_three = re.compile(like_reg).findall(html)
    third_four_col.append(str(pagelike[0]).replace(" ",""))
    third_four_col.append(last_three[0][1])
    third_four_col.append(last_three[0][0].split(" ")[-1])

def get_last_comment_date(commentlist):
    if(str(commentlist).endswith("[]")):
        return "N/A"
    reg = '.*?"time":(.*?),.*?'
    commentdatelist = re.compile(reg).findall(str(commentlist))
    latestdate = commentdatelist[0]
    for date in commentdatelist:
        if(date > latestdate):
            latestdate = date
    localtime = time.localtime(long(latestdate))
    timeStr=time.strftime("%d/%m/%Y", localtime)
    return timeStr

def get_req(page_id, time_line, minus8, timestamp):

    '''send response to facebook server to get the return value (6 posts in one time)'''
    '''00000000001446908402:04611686018427387904:09223372036854775800:04611686018427387904'''
    url = "https://www.facebook.com/pages_reaction_units/more/?page_id="

    url += page_id

    data = '&cursor={"timeline_cursor":"timeline_unit:1:0000000000'
    data = data+ str(timestamp)+':'+time_line+':0'+str(minus8)+':'+time_line+'",'

    data += '"timeline_section_cursor":{},"has_next_page":true}'
    # data += '"timeline_section_cursor":{"profile_id":'+page_id+',"start":0,"end":1475669953,"query_type":36,"filter":1},"has_next_page":true}'

    data += tail
    url += data

    req = urllib2.Request(url)
    print(url)
    req.add_header("Cookie",cookie);
    req.add_header("user-agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return unicode(res, 'unicode-escape').replace("\\","").decode("utf-8")

def get_req_first(url):
    req = urllib2.Request(url)
    req.add_header("Cookie",cookie);
    req.add_header("user-agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return unicode(res, 'unicode-escape').replace("\\","").decode("utf-8")

def savevalue(filename, ori_url):
    global third_four_col
    likes_url = "https://www.facebook.com/" + ori_url.split("/")[3].split("?")[0] + "/likes"
    i=0
    length = 6
    '''
    1:00000000001447171200:04611686018427387904:09223372036854775804:04611686018427387904
    time_line = 04611686018427387904
    minus4 = 9223372036854775804
    timestamp = 1447171200
    '''
    time_line = '04611686018427387904'
    minus8 = 9223372036854775801
    ##timestamp = '1420099199' ##2014
    timestamp = '1475294400'
    page_id = "345568205488066"
    full_time_format = '%A, %B %d, %Y at %H:%M'
    time_format = '%A, %B %d, %Y'

    while(i >=0 ):
        if(i < len(req_list_)):
            full_time_format = '%A, %d %B %Y at %H:%M'
            time_format = '%A, %d %B %Y'
            response = get_req_first(req_list_[i])
        else:
            full_time_format = '%A, %d %B %Y at %H:%M'
            time_format = '%A, %d %B %Y'
            response = get_req(page_id, time_line, minus8, timestamp)
            minus8 -= 8
        response = response.replace("\n","").replace("\r","")
        timestamp = get_first_four_column(response, full_time_format, time_format)
        length = get_second_four_column(response)
        i += 1
        if timestamp < '1451577600':
            break
    print "minus8========"+str(minus8)
    third_four_col = ['331481','21941','331481']
    write_excel(filename)

def write_excel(filename):
    global first_four_col, second_four_col, third_four_col

    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('Data', cell_overwrite_ok=True)
    ##column name
    col_name = ['#', 'Message','Message URL','Date','Url in the text/post','Likes Count','Comments Count','Last Comment Date','Shares Count','No. of Page Likes','Ppl Talking','Total pg likes']

    for i in range(0,len(first_four_col)):
        first_four = first_four_col[i]
        ws.write(i+1,0,first_four[0])
        ws.write(i+1,1,first_four[1])
        ws.write(i+1,2,first_four[2])
        ws.write(i+1,3,first_four[3])

        second_four = ['N/A','N/A','N/A','N/A']
        if(second_four_col.has_key(first_four[1])):
            second_four = second_four_col.pop(first_four[1])
        ws.write(i+1,4,second_four[0])
        ws.write(i+1,5,second_four[1])
        ws.write(i+1,6,second_four[2])
        ws.write(i+1,7,second_four[3])

        ws.write(i+1,8,third_four_col[0])
        ws.write(i+1,9,third_four_col[1])
        ws.write(i+1,10,third_four_col[2])
    w.save(filename)
    print "===========over============"


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    ori_url = "https://www.facebook.com/BabasAndU/"

    filename = "" + ori_url.split("/")[3].split("?")[0] + "1.xls"

    savevalue(filename, ori_url)

