# encoding=utf8
import time
from selenium import webdriver
import re
import string
import HTMLParser
import urllib2, urllib
import xlwt
import sys
import os

data = [['Date', 'Location', 'Profile Name', 'Profile URL', 'Post Link', 'Content', 'Links in Content', 'Media Type',
         'Headline', 'Body', 'Website', 'emotion count', 'Comment count', 'Share count', 'View count']]
cookie = 'datr=OYmDV4pQ1woh4694JL3-5EoE; _ga=GA1.2.905364245.1476499425; sb=ZYmDVwozRepnSPcjn8-p-9Ul; pl=n; lu=gg-TFkXk6ygDB3WFT8S3NQgw; c_user=100006957738125; xs=196%3AZqliNb7ajY5nOw%3A2%3A1477666718%3A20772; fr=1pJP65hZ44wMFk9by.AWXV81oG5OtMrmzCBT6OAm2WBrQ.BXg4k5.ss.FhF.0.0.BYRsee.AWUYFGvt; csm=2; s=Aa5x7GMcTBJohGaj.BYE2ef; p=-2; presence=EDvF3EtimeF1481033634EuserFA21B06957738125A2EstateFDutF1481033634206Et2F_5b_5dElm2FnullEuct2F148095286B0EtrFA2loadA2EtwF3261839300EatF1481033633696CEchFDp_5f1B06957738125F2CC'
url = 'https://www.facebook.com/search/top/?q=shopping&filters_rp_location=105565836144069&filters_rp_creation_time=%7B%22start_year%22%3A%222016%22%2C%22end_year%22%3A%222016%22%7D'
file_prefix = "Shopping_2015"
save_img = False


def write(html, filename):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    ##column name.*?<td>(.*?)<
    for row in range(0, len(data)):
        one_row = data[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)
    print filename + "===========over============"


def request_html(url):
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res


def open_browser_scroll(url, filename):
    global html_name
    driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
    driver.get(url)

    username = driver.find_element_by_name("email")
    password = driver.find_element_by_name("pass")

    username.send_keys("mymicro@live.com")  ##your username, need to be replaced
    password.send_keys("54zcy54ZCY252729")  ##your password, need to be replaced

    driver.find_element_by_id("u_0_0").click()

    for i in range(1, 2000):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(i)
        time.sleep(3)
        if (i % 50 == 0):
            html_source = driver.page_source
            data = html_source.encode('utf-8')
            write(data, filename + ".html")
            if '<div class="phm _64f">End of results</div>' in data:
                break


def parse_html(html, flag):
    if (html == ""):
        return
    html = html.replace("&quot;", "")
    reg = 'class="_6a _5u5j _6b".*?href="(.*?)".*?>(.*?)</a.*?<a class="_5pcq" href="(.*?)".*?data-utime="(.*?)"(.*?)data-hover="tooltip".*?_5pbx userContent".*?>(.*?)</div>.*?class="_3x-2"(.*?)<form rel="async".*?class="_ipn.*?"(.*?)class="_3399 _a7s clearfix"'
    params_list = re.compile(reg).findall(html)
    print("ALL LIST: " + str(len(params_list)))

    i = 1
    for params in params_list:
        post_link = str(params[2])
        if 'https://www.facebook.com' not in post_link:
            post_link = 'https://www.facebook.com' + post_link
        profile_link = str(params[0])
        profile_name = str(params[1])

        date = format_date(str(params[3]))
        location = get_location(str(params[4]))
        content = cleanup(remove_html_tag(params[5]))
        url_in_content = get_url_from_content(params[6])
        media_params = get_post_media(str(params[6]))
        likes_paramas = get_likes(str(params[7]))

        one_row = [date, location, profile_name, profile_link, post_link, content,
                   url_in_content] + media_params + likes_paramas
        data.append(one_row)
        i += 1


def get_profile_name(q):
    return ''


def get_likes(ori):
    emotion = 0
    comment = 0
    share = 0
    view = 0
    if 'Comments' in ori or 'Comment' in ori:
        try:
            comment = ori.split("Comment")[0][-7:-1].split('>')[1]
        except:
            comment = 0
    if 'Shares' in ori or 'Share' in ori:
        try:
            share = ori.split("Share")[0][-7:-1].split('>')[1]
        except:
            share = 0
    if 'Views' in ori or 'View' in ori:
        try:
            view = ori.split('View')[0][-7:-1].split('>')[1]
        except:
            view = 0
    reg = 'class="_4arz"><span.*?>(.*?)</span>'
    emotion_list = re.compile(reg).findall(ori)
    if len(emotion_list) > 0:
        emotion = emotion_list[0]
    return [emotion, comment, share, view]


def save_image(url):
    url = remove_html_tag(url)
    urllib.urlretrieve(url, file_prefix + '_image/' + str(time.time()) + '.jpg')


def get_post_media(ori):
    media_type = 'unknown'
    if save_img and 'uiScaledImageContainer' in ori:
        media_type = "Image"
        img_reg = 'uiScaledImageContainer.*?src="(.*?)"'
        url = re.compile(img_reg).findall(ori)[0]
        save_image(url)
    if '</video>' in ori or 'aria-label="Loading..."' in ori:
        media_type = "Video"
    returnVal = [media_type]
    a = 'N/A'
    b = 'N/A'
    c = 'N/A'
    if 'class="_6m3 _--6"' in ori:
        reg = ''
        if 'class="mbs _6m6 _2cnj _5s6c"' in ori:
            reg += 'class="mbs _6m6 _2cnj _5s6c".*?><.*?>(.*?)<'
            a = ''
        if 'class="_6m7 _3bt9"' in ori:
            reg += '.*?class="_6m7 _3bt9".*?>(.*?)<'
            b = ''
        if 'class="_59tj _2iau"' in ori:
            reg += '.*?class="_59tj _2iau".*?>(.*?)<a class="_52c6"'
            c = ''
        list = re.compile(reg).findall(ori)

        if (len(list) > 0):
            if a == '':
                a = remove_html_tag(list[0][0])
            if b == '':
                b = remove_html_tag(list[0][1])
            if c == '':
                c = remove_html_tag(list[0][-1])

    returnVal += [a, b, c]
    return returnVal


def format_date(timestamp):
    ltime = time.localtime(long(timestamp))
    timeStr = time.strftime("%d/%m/%Y", ltime)
    return timeStr


def get_location(ori):
    location = 'unknown'
    if "class=\"_5pcq\"" in ori:
        reg = 'class=\"_5pcq\".*?>(.*?)<'
        location = re.compile(reg).findall(ori)[0]
    return str(location)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def cleanup(s, remove=('\n', '\t')):
    newString = ''
    for c in s:
        # Remove special characters defined above.
        # Then we remove anything that is not printable (for instance \xe2)
        # Finally we remove duplicates within the string matching certain characters.
        if c in remove:
            continue
        elif not c in string.printable:
            continue
        elif len(newString) > 0 and c == newString[-1] and c in ('\n', ' ', ',', '.'):
            continue
        newString += c
    return newString


def get_url_from_content(ori):
    reg = 'onmouseover="LinkshimAsyncLink.swap\(this,(.*?)\)'
    url_list = re.compile(reg).findall(ori)
    returnVal = ''
    for url in url_list:
        if returnVal != '':
            returnVal += "|"
        returnVal += str(url).replace("\\", "")
    return returnVal


def get_fan_param(ori):
    ori = unicode(ori, 'unicode-escape').replace("\\", "").replace("&quot;", "").replace("&#039;", "'")
    reg = '"_2kcr _42ef".*?onmouseover="LinkshimAsyncLink.swap\(this, (.*?)\)'
    if '"_2kcr _42ef"' in ori:
        res = re.compile(reg).findall(ori)
        if (len(res) > 0):
            return str(res[0])
    return "N/A"


def read_file(filename):
    file = open(filename)
    try:
        content = file.read()
    finally:
        file.close()
    return content


def write_list_into_file(a, filename):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    f = file(filename, "w+")
    for data in a:
        f.writelines(data[0] + " " + data[1] + '\n')
    print filename + '===========over============'


reload(sys)
sys.setdefaultencoding('utf8')
open_browser_scroll(url, 'html/' + file_prefix)

parse_html(read_file('html/' + file_prefix + ".html"), "close")
write_excel('data/' + file_prefix + '.xls')
