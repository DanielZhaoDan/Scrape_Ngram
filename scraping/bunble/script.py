# -*- coding: utf-8 -*-

import re
import urllib2
import xlwt
import sys
from datetime import datetime
from selenium import webdriver
import HTMLParser
import os
import xlrd
import requests
import time

sheet1_data = [['ID', 'Name', 'Location', 'Overall rating', 'Rank all Bali', 'Number of reviews', 'Cuisine', 'Reserve Online', 'Excellent', 'Very good', 'Average', 'Poor', 'Terrible', 'Families', 'Couples', 'Solo', 'Business', 'Friends', 'Mar-May', 'Jun-Aug', 'Sep-Nov', 'Dec-Feb']]
sheet2_data = [['ID', 'Contributor Name', 'Contributor Location', 'Contributor country', 'Contributor level', 'Review headline', 'rating', 'Review date', 'Review text', 'Reviewer Value', 'Reviewer Service', 'Reviewer Food']]

base_url = 'https://www.burpple.com/search/sg?distance_to=0.0&offset=%s&open_now=false&price_from=0&price_to=90&q=sentosa&type=places'

url_follower_dict = {}
cookie = '__cfduid=dc774e622983a98a8351252891d0d02b31533813304; _ga=GA1.2.804335954.1533813307; _gid=GA1.2.1895045947.1533813307; _dlAppPopped=true; current_city_id=1; _Burpple_session=cGVMQVZrNkhTYXdvRHJVMW5sdWpsaWZRV1AzZ1hhdmdDTW5mM2J1eDVNZWtRTmx6b3laVUIrZDFJL2diRWpTTzNiS21GNFZTM3BWSHRVcEUzUm1sOFpKazhKem1nbmphVmZGaUlMaFp2cUFnVkJqbXJLVndFWWF1VWJKOVlMeFlZNVZ0T3M2NnEvZXFBcWNySEFQaU5oVjUya3FrOFNybEE3ekVoWlpOYVA4NmVhaktqQ3FjcmVCUVVLazlEb3lYWFJBdmFqTjVFTEFVRVl1cjJWL0NsemgzRkZQc1EzNDFPQSs5RlczcElsWTFDS09mVW9NbGl5SEZtR1B0ZlBUeVhxT1N2NE9mL01Oc1N0LzZxZ1REVHc9PS0tUTEwTG5ENXhaSmtsNmZwYmNaYzlBQT09--5e3247efbd48b5874bbebf2247732ca07dec0532; amplitude_id_7d6212a836a2f52ed783dbb6006589ecburpple.com=eyJkZXZpY2VJZCI6IjI4NWE3N2I3LTAwMjUtNDYwNC04NzlhLTY5ODJhYmY4NWFmMVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTUzMzgxOTkwMDMzNCwibGFzdEV2ZW50VGltZSI6MTUzMzgyMTYzNTMwOSwiZXZlbnRJZCI6NjMsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjo2M30=; _gat=1; _gali=load-more-reviews'


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_'+str(flag)+'.xls')
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
                    print '===Write excel ERROR==='+str(one_row[col])
    w.save(filename)
    print filename+"===========over============"


def request_sheet1(url):
    global sheet1_data
    html = get_request(url)
    reg = 'data-index="(.*?)".*?href="(.*?)".*?searchVenue-header-name-name.*?">(.*?)<(.*?)searchVenue-header-reviews">(.*?) .*?searchVenue-header-locationDistancePrice">(.*?)searchVenue-header-categories">(.*?)<'
    item_list = re.compile(reg).findall(html)

    for item in item_list:
        try:
            id = 'BP_%s' % item[0]
            item_url = 'https://www.burpple.com' + item[1]
            name = remove_html_tag(item[2])
            can_reserve = get_reserve(item[3])
            no_reviews = int(item[4])
            pricing = get_pricing(item[5])
            all_feature = remove_html_tag(item[6])
            
            one_row = [id, item_url, name, can_reserve, no_reviews, pricing, all_feature]
            print(one_row)
            sheet1_data.append(one_row)
            # if no_reviews > 0:
            #     request_sheet2(id, item_url, name, no_reviews)
        except:
            print 'ERR---level 1---' + url

def get_reserve(ori):
    return 'Yes' if 'earchVenue-header-name-icons-icon-reservation' in ori else 'No'           

def get_pricing(ori):
    if 'searchVenue-header-locationDistancePrice-price">' in ori:
        reg = '\$(.*?)<'
        return re.compile(reg).findall(ori)[0]
    return 'N/A'

def request_one(url):
    driver.get(url)
    layer = driver.find_element_by_class_name('modal-closeBtn')

    for i in range(0, 10):
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            if layer:
                layer.click()
        except:
            pass
        try:
            button = driver.find_element_by_class_name('btn-see-more')
            if not button:
                break
            button.click()
        except:
            pass
    html_source = driver.page_source
    data = html_source.encode('utf-8')
    write(data.replace('\n', '').replace('\r', ''), '1.html')
    return data.replace('\r', '').replace('\r', '')

def request_sheet2(hotel_id, hotel_url, hotel_name, no_reviews):
    total_length = 3
    html = get_request(hotel_url)
    venue_id = re.compile('venue_id=(.*?)"').findall(html)[0]
    
    reg = 'card-body.*?class="food-description">(.*?)<div class="food-activity".*?class="card-item-set--link-title".*?href="(.*?)">(.*?)<.*?class="card-item-set--link-main">.*?Level (.*?) .*?</a> .*? (.*?) '
    comment_list = re.compile(reg).findall(html)
    get_comment_from_list(hotel_id, hotel_url, hotel_name, comment_list, total_length)

    for i in range(10):
        url = 'https://www.burpple.com/foods/load_more?offset=%s&venue_id=%s' % (str(3+i*6), venue_id)
        html = get_request(url)
        html = html.replace("\\/", '/').replace('\\"', '"').replace('\\n','')
        reg = 'class="food-description">(.*?)<div class="food-activity">.*?class="card-item-set--link-title".*?href="(.*?)">(.*?)<.*?class="card-item-set--link-main">.*?Level (.*?) .*?</a> .*? (.*?) '    
        comment_list = re.compile(reg).findall(html)
        total_length += 6
        get_comment_from_list(hotel_id, hotel_url, hotel_name, comment_list, total_length)
        if total_length > no_reviews:
            break

def get_comment_from_list(hotel_id, hotel_url, hotel_name, commment_list, total_length):
    global sheet2_data
    for comment in commment_list:
        try:
            text = remove_html_tag(comment[0])
            reviewer_url = 'https://www.burpple.com' + comment[1]
            reviewer_name = comment[2]
            level = comment[3]
            no_review = comment[4]
            # no_follower, location = get_follower_location(reviewer_url)
            no_follower, location = 0, 'N/A'
            one_row = [hotel_id, hotel_url, hotel_name, reviewer_name, reviewer_url, text, level, no_review, no_follower, location]
            print('sheet2--', total_length, one_row)
            sheet2_data.append(one_row)
        except:
            print('EXP-sheet2--', hotel_url)

def get_follower_location(url):
    if url_follower_dict.get(url):
        return url_follower_dict.get(url)
    html = get_pure_request(url).replace('\t', '').replace('\r', '').replace('\n', '')
    reg = 'class="profile-page-details"(.*?)collectionFeed collectionFeed--boxes'
    data = re.compile(reg).findall(html)[0]

    if 'profile-page-details__main' in data:
        real_reg = 'class="profile-page-details__main".*?</a>.*? (.*?)<.*?Wishlists</a.*?<span>(.*?)<'
        follower = re.compile(real_reg).findall(data)
        res = (remove_html_tag(follower[0][0]), follower[0][1])
    else:
        real_reg = '.*?Wishlists</a.*?<span>(.*?)<'
        follower = re.compile(real_reg).findall(data)
        res = (follower[0], 'N/A')
    url_follower_dict[url] = res
    return res


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def get_date(ori):
    d = datetime.strptime(ori, '%a %b %d, %Y %I:%M %p')
    date = d.strftime('%d/%m/%Y')
    return date, d.weekday() + 1


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header('accept', '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript')
    req.add_header('cookie', '__cfduid=d9a36588c99556450e79264562a844bbf1533812207; current_city_id=1; _ga=GA1.2.1333025509.1533812210; _gid=GA1.2.1508434489.1533812210; _dlAppPopped=true; _Burpple_session=MS9WNzE5bGcybUNsYzl2bTZKT0Z5WndnQnlRZmpTYUtwck9oQlJuK255QVNNVnREYkM0WEUzaHc4YWpBL0xwMUU2N09hdVhKSXlnejNkYUxaaWtGRjlISnUvMDhyZDJPdSsyaitBb296dzdYZUdrZXRtc1h3WU51cnhHL1YyTmU3TEswdnRuNW5SbXBhVFc4aklqQzVBNlBIL2FBNGNMWkYxWDJQWHdmV3lNWXFSa0RyaUdKVmR3UHlKRUNxZThGRW1Vd2p2ZWxnWk1vQ0JKUVpjZ2JMS3hQczNiQ01VWVlpVWdQZCtNZXZ6dFdRNXNCaGZlWjQ2d2JlQ1c0NHlqVEliMmJnWlVibEpMWmpDaWx4L3paNEN6dGZIUjE4MHFXVDBVWnNLUWZ3Yms9LS1iQ25yVEw3cHdTSlNFNmd1aDRlNXJBPT0%3D--74d27ec18bb609e6156134d0932fd26bec5590ab; _gat=1; amplitude_id_7d6212a836a2f52ed783dbb6006589ecburpple.com=eyJkZXZpY2VJZCI6IjJjZTRhYzVlLTJmZTMtNGYxMS1iMTU2LWQ3OTExOWFjNTVjMVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTUzMzg0MjkzNDgwNCwibGFzdEV2ZW50VGltZSI6MTUzMzg0MzIxMzkxNiwiZXZlbnRJZCI6MjE4LCJpZGVudGlmeUlkIjoxLCJzZXF1ZW5jZU51bWJlciI6MjE5fQ==; _gali=load-more-reviews')
    # req.add_header('if-none-match', 'W/"60583b2fe8576f1e6e3a796b17b095b1"')
    req.add_header('referer', 'https://www.burpple.com/woobar')
    req.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36 OPR/56.0.3037.0 (Edition developer)')
    # req.add_header('x-csrf-token', '5713Xpu4+lFbKUZFgc/25oY4ZaOPwG3Rz2L8t972I1GOdYhyKOhosyI1bDGjKkVgwed8CZ8G+WTUAkY11uHYxA==')
    # req.add_header('x-newrelic-id', 'XQUDWVdACgICVQ==')
    # req.add_header('x-requested-with', 'XMLHttpRequest')
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res

def get_pure_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", 'https://www.tripadvisor.com.sg/Restaurants-g294226-Bali.html')
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    return res

def read_excel(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            hotel_id = row[0].value
            hotel_url = row[1].value
            hotel_name = row[2].value
            no_reviews = int(row[4].value)
            request_sheet2(hotel_id, hotel_url, hotel_name, no_reviews)
        except Exception as e:
            print(i, e)

def read_excel_for_food(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            url = row[4].value
            res = get_follower_location(url)
            print(res)
            sheet2_data.append(res)
        except Exception as e:
            print(i, e)


reload(sys)
sys.setdefaultencoding('utf-8')

read_excel_for_food('/Users/zhaodan/Documents/personal/code/Scrape_Ngram/scraping/bunble/data/sheet2.xls')
write_excel('data/sheet3.xls', sheet2_data)