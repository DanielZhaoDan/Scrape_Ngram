import xlrd
import xlsxwriter
import os
import time
import requests

cookie = 'ajs_anonymous_id=%22176919ac-6f17-4c5f-bcdf-20cf3b97d65e%22; _first_pageview=1; _jsuid=3862967262; ajs_user_id=null; ajs_group_id=null; _ga=GA1.2.1216111861.1496139082; _gid=GA1.2.1682312280.1496139207; _drip_client_9331461=vid%253Dffceee50274d013562411277a4eb0864%2526pageViews%253D5%2526sessionPageCount%253D5%2526lastVisitedAt%253D1496139206945%2526weeklySessionCount%253D1%2526lastSessionAt%253D1496139083569; mp_ef8589eff3bf62c9dcac2779564de029_mixpanel=%7B%22distinct_id%22%3A%20%2215c58d6a80f260-034a4d5ef6bfff-3024410f-13c680-15c58d6a81083f%22%2C%22mp_lib%22%3A%20%22Segment%3A%20web%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; mp_mixpanel__c=0; _gat=1; amplitude_iddiffbot.com=eyJkZXZpY2VJZCI6IjNhMjU3NjczLTUzZDUtNDExMi04MjkzLWYyMDg1MTUzNjk0YlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTQ5NjEzOTA4MTYxNSwibGFzdEV2ZW50VGltZSI6MTQ5NjEzOTIwNzAwMSwiZXZlbnRJZCI6NSwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjV9; _hp2_ses_props.2423915105=%7B%22ts%22%3A1496139081984%2C%22d%22%3A%22www.diffbot.com%22%2C%22h%22%3A%22%2F%22%7D; _hp2_id.2423915105=%7B%22userId%22%3A%226606554637446143%22%2C%22pageviewId%22%3A%220515182173179074%22%2C%22sessionId%22%3A%221042976026160454%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%223.0%22%7D; __hstc=66047665.e05766620da0ed36aed902946bd3531d.1496139086082.1496139086082.1496139086082.1; __hssrc=1; __hssc=66047665.5.1496139086083; hubspotutk=e05766620da0ed36aed902946bd3531d; _eventqueue=%7B%22heatmap%22%3A%5B%5D%2C%22events%22%3A%5B%5D%7D; _vwo_uuid_v2=3187BC3B7AC5C456EAC86E5135924194|c286fcc6977e26218c9e1bac9b7199e3'
alldata = []
diff_token='4250a98168a8fc9c3299a73780b74459'

def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    return res_data


def get_cleaned_html(url):
    global alldata
    req_url_base = 'https://api.diffbot.com/v3/analyze?token={token}&url={url}'
    req_url = req_url_base.format(url=url, token=diff_token)

    html = get_request(req_url)
    if 'Rate limit exceeded' in html:
        print [url, html]
        return False
    resp_obj = html.json()
    objects = resp_obj.get('objects', [])
    if objects:
        title = objects[0].get('title', '')
        text = objects[0].get('text', '')
    else:
        title = resp_obj.get('title', '')
        text = ''
    one_row = [url, title, text if text else '']
    print 'SUCC', url, title, len(text)
    alldata.append(one_row)
    return True


def read_excel(filename, start):
    global alldata
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        try:
            if i not in [1, 3, 4, 10, 11, 12, 13, 15, 19, 20, 21, 22, 24, 26, 27, 28, 33, 34, 35, 36, 37, 39, 43, 44, 45]:
                continue
            url = table.row(i)[5].value.strip()
            flag = get_cleaned_html(url)
            if not flag:
                break
            time.sleep(0.5)
        except Exception as e:
            print 'ERROR--' + str(i), e
            time.sleep(1)
            continue
        if i > 10000:
            break


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, data):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    workbook = xlsxwriter.Workbook(filename)
    ws = workbook.add_worksheet()
    for row in range(0, len(data)):
        one_row = data[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    workbook.close()
    print filename + "===========over============"

read_excel('data/sheet1.xls', 1)
write_excel('data/sheet3.xls', alldata)