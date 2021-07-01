# -*- coding: utf-8 -*-

import time
import re
import urllib2
import xlwt
import sys
import HTMLParser
import gc

alldata = [['link','product_title','price','genre','avg rating','rating count','rating headline','rating','rating content','rating date']]
cookie = 'npic=86Ziis71UF5OoAByOqjBsZnu9xDawFDZ/k2PkFDPDYFCq+y6xPV1xNwas7GZTQD9CA==; NNB=3MDNY6SQWSSFO; page_uid=SIgs3spl8T0ssu/F5cVssssssul-428974'
rating_temp = 'http://shopping.naver.com/detail/section_user_review.nhn?nv_mid={product_id}&page={rating_page}&sort=0&mall_id=all&score=all&imgYN=all&briefYN=Y&topicCode=&reviewSeq='
detail_reg = r'class="not_thmb">.*?class="subjcet" title="(.*?)".*?class="curr_avg"><strong>(.*?)<.*?class="atc">(.*?)<.*?class="regdate">(.*?)<'
genre_reg = r'a href=.*?>(.*?)</a'

def write(html,filename):
    fp = open(filename,"w")
    fp.write(html)
    fp.close()
    print "write over"

def write_excel(filename):
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    ##column name.*?<td>(.*?)<
    for row in range(0,len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            ws.write(row,col,one_row[col])
    w.save(filename)
    print filename+"===========over============"

def request_html(url):
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    req.add_header('Referer', 'http://steamcommunity.com/discussions/forum/1/?fp=2')
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t','').replace('\r','').replace('\n','')
    return res

def save_date(url, filename, start, max):
    global alldata
    i = start
    while i<=max:
        one_url = url.replace('{pagingIndex}', str(i)).replace('{paging_size}', str(i*40))
        try:
            print str(i)+'--'+str(max)+'  '+filename+'  '+one_url
            html = request_html(one_url)
            parse_html(html)
        except BaseException:
            print "ERROR===="+one_url
            time.sleep(3)
        i += 1
    write_excel(str(i)+'_'+filename)

def parse_html(html):
    global alldata
    reg = 'model_list".*?product_id="(.*?)".*?class="info".*?<a href="(.*?)".*?title="(.*?)".*?class="num _price_reload".*?>(.*?)<.*?span class="depth">(.*?)</span.*?span class="etc">(.*?)"info_mall"'
    data_list = re.compile(reg).findall(html)
    for data in data_list:
        product_id = str(data[0])
        link = 'http://shopping.naver.com/' + str(data[1]).replace('amp;', '')
        title = remove_html_tag(data[2]).strip()
        price = str(data[3])

        raw_genre = (data[4]).strip()
        genre = re.compile(genre_reg).findall(raw_genre)[-1]

        raw_rating = data[5]
        rating_reg = r''
        if 'class="star_graph"' in raw_rating:
            rating_reg = 'class="star_graph".*?width:(.*?)%'
        if '<em>' in raw_rating:
            rating_reg += '.*?<em>(.*?)<'
        rating_list = re.compile(rating_reg).findall(raw_rating)[0]
        avg_rating = '0'
        rating_count = '0'
        if 'class="star_graph"' in raw_rating:
            avg_rating = float(rating_list[0])/10/2
        if '<em>' in raw_rating:
            rating_count = int(rating_list[-1])

        if avg_rating == '0':
            one_row = [link, title, price, genre, avg_rating, rating_count] + ['N/A','N/A','N/A','N/A']
            alldata.append(one_row)
        else:
            rating_page = rating_count / 20
            if rating_page > 4:
                rating_page = 4

            rating_details = rating_detail(product_id, rating_page)
            for rating in rating_details:
                one_row = [link, title, price, genre, avg_rating, rating_count] + rating
                alldata.append(one_row)


def rating_detail(product_id, rating_page):
    returnVal = []
    for i in range(1, rating_page+2):
        url = rating_temp.replace("{product_id}", product_id).replace('{rating_page}', str(i))
        html = request_html(url)
        details_list = re.compile(detail_reg).findall(html)
        for detail in details_list:
            title = remove_html_tag(detail[0])
            rating = detail[1]
            content = remove_html_tag(detail[2])
            date = str(detail[3])
            one_row = [title, rating, content, date]
            returnVal.append(one_row)

    return returnVal


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))

reload(sys)
sys.setdefaultencoding('utf-8')

url_template = 'http://shopping.naver.com/search/all_search.nhn?query=pc%EA%B2%8C%EC%9E%84&productSet=total&viewType=list&sort=rel&frm=NVSHPAG&sps=N&pagingIndex={pagingIndex}&pagingSize={paging_size}'
save_date(url_template, 'shopping_naver.xls', 51, 100)
# html = request_html('http://shopping.naver.com/search/all_search.nhn?query=pc%EA%B2%8C%EC%9E%84&productSet=total&viewType=list&sort=rel&frm=NVSHPAG&sps=N&pagingIndex=5&pagingSize=200')
# write(html,'0.html')
# parse_html(html)
