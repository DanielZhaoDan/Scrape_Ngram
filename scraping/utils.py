import re
import requests
import xlwt, xlrd
import HTMLParser
import os
from functools import wraps
from selenium import webdriver
import errno
import os
import signal
import time

cookie = '__utmz=231532751.1576219136.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=231532751; GA_XSRF_TOKEN=AO6Y7m8Up0G1PuGh2qIWQ_keK2zT0RVU6A:1576489731389; __utma=231532751.760866652.1575884403.1576487154.1576489741.4; __utmb=231532751.0.10.1576489741; _ga=GA1.3-2.760866652.1575884403; _gid=GA1.3-2.1548239716.1576486976; SID=rgc33ZPGn35d-9-JT3xlfZKbWLWHLBqxscXpMo7UusJg8YsK1Xm5zmqdwX06ZQRi9hzjNw.; __Secure-3PSID=rgc33ZPGn35d-9-JT3xlfZKbWLWHLBqxscXpMo7UusJg8YsKVOsMD5ptSK0xm8op5xk-Zg.; HSID=AfYRkOGYiSvbQArRa; SSID=AFy3hjCGqjKOm7mwr; APISID=_BvfqyTu7nnB9_kw/AtKjekBw8UaxVP4qy; SAPISID=cGOet470hpGsWQEV/ATpbBTKsxu5vxPDaL; __Secure-HSID=AfYRkOGYiSvbQArRa; __Secure-SSID=AFy3hjCGqjKOm7mwr; __Secure-APISID=_BvfqyTu7nnB9_kw/AtKjekBw8UaxVP4qy; __Secure-3PAPISID=cGOet470hpGsWQEV/ATpbBTKsxu5vxPDaL; SEARCH_SAMESITE=CgQIxo4B; 1P_JAR=2019-12-16-9; NID=193=HKrRZUHs3jR2X6FIWchUPTfwSSuP0b0eHMMKSztXkVMgAPu8RaQpaFucfiet9Sb3cd-UeZojsZh16_YFQ90uCgWWRMmF4VgIC9njAPgwEpSXUg3YH0u123ogI7ieqKJeDkOgOFtoxPNlNzIAMY4DKIkdbyi2n23Z0Z2lsTpuq7jyNGJLM0GFBD1PPe4enxSmKmLD-Mcc-sWYu6DILoIcLkTASglzv5pO_isRHXgAs9qfbapiCfC9CVINnvSLAwuwH9ohbBlHnOzAuBEJfSkPisb8VOZVzXg; _gid=GA1.3.1548239716.1576486976; S=analytics-realtime-frontend=EVnXGHnmR77CR0CzbT1X3ZLWpXlmKOyR; _gat=1; _gat_ta=1; _gat_tw=1; _gat_UA-60390233-3=1; _ga=GA1.1.760866652.1575884403; _ga_X6LMX9VR0Y=GS1.1.1576487089.5.1.1576489801.0; SIDCC=AN0-TYtyYXkjWKvNrjpBudVmiqoF5aF5MI088UaIyILTqoRHwNyrkLX8gVjzcrI2qyLP57FIumY'


def remove_html_tag(ori):
    try:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', ori)
        return str(HTMLParser.HTMLParser().unescape(dd))
    except Exception as e:
        return ori


def write_excel(filename, alldata, flag=None, encoding='utf-8'):
    filename = 'data/' + filename
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)

    i = 0
    while len(alldata) > 65500:
        _filename = filename.replace('.xls', '_%s.xls' % i)
        start_index = 0
        end_index = 65500
        data = alldata[start_index:end_index]
        alldata = alldata[end_index:]
        w = xlwt.Workbook(encoding=encoding)
        ws = w.add_sheet('old', cell_overwrite_ok=True)
        for row in range(0, len(data)):
            one_row = data[row]
            for col in range(0, len(one_row)):
                try:
                    ws.write(row, col, one_row[col][:32766])
                except Exception as e:
                    try:
                        ws.write(row, col, one_row[col])
                    except:
                        print('===Write excel ERROR===', e, str(one_row[col]))
        w.save(_filename)
        print("%s===========over============%d" % (_filename, len(data)))
        i += 1
    w = xlwt.Workbook(encoding=encoding)
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col][:32766])
            except Exception as e:
                try:
                    ws.write(row, col, one_row[col])
                except:
                    print('===Write excel ERROR===', e,  str(one_row[col]))
    w.save(filename)
    print("%s===========over============%d" % (filename, len(alldata)))


def write_html(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def get_request_html(get_url, cookie, pure=False, add_header={}):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'accept': '*/*',
        'cookie': cookie,
    }
    for k, v in add_header.items():
        headers[k] = v
    res_data = requests.get(get_url, headers=headers, timeout=20)

    res = res_data.content
    if not pure:
        res = res.replace('\t', '').replace('\r', '').replace('\n', '').replace("&quot;", '"').replace("&#92;", '')

    return res


def get_request_html_with_status(get_url, cookie, pure=False, add_header={}):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'accept': '*/*',
        'cookie': cookie,
    }
    for k, v in add_header.items():
        headers[k] = v
    res_data = requests.get(get_url, headers=headers, timeout=20)

    if res_data.status_code != 200:
        print res_data.status_code

    res = res_data.content
    if not pure:
        res = res.replace('\t', '').replace('\r', '').replace('\n', '').replace("&quot;", '"').replace("&#92;", '')

    return res, res_data.status_code


def download_response(url, cookie, filename, pure=False, add_header={}):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': url,
        'accept': '*/*',
        'Cookie': cookie,
    }
    for k, v in add_header.items():
        headers[k] = v
    res_data = requests.get(url, headers=headers, timeout=20)
    open(filename, 'wb').write(res_data.content)


def get_request_json(get_url, cookie):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
        'x-csrftoken': 'jhmwjduVDHhuwLoGd6gN3FKUqywwcBQL',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR0R2OWhvU4GxrOhjPvsyujuBfI94KcCvSV2Confwyu6QXvI',
        'x-requested-with': 'XMLHttpRequest'
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)

    return res_data.json()


def post_request_html(get_url, cookie, data={}, add_header={}):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'referer': get_url,
        'cookie': cookie,
    }
    for k, v in add_header.items():
        headers[k] = v
    res_data = requests.post(get_url, headers=headers, timeout=10, data=data)
    res = res_data.content
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')

    return res


def post_request_json(get_url, cookie, data={}, add_header={}):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'referer': get_url,
        'cookie': cookie,
    }
    for k, v in add_header.items():
        headers[k] = v
    res_data = requests.post(get_url, headers=headers, timeout=5, data=data)
    res = res_data.json()

    return res


class TimeoutError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL,seconds) #used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator


def get_attachments(url, filename, timeout=5, headers={}, data={}):
    print "Getting url", url
    response = requests.post(url, timeout=timeout, stream=True, headers=headers, data=data)
    if response.status_code == 200:
        if response.headers.get('Content-Disposition'):
            print "Writing file to", filename
            open(filename, 'wb').write(response.content)


def open_browser_scroll(url, sleep_time=1):
    try:
        # options = Options()
        # options.add_argument('--proxy-server=%s', random.choice(proxy))
        driver.get(url)
        time.sleep(sleep_time)
        html_source = driver.page_source
        data = html_source.encode('utf-8').replace('\t', '').replace('\r', '').replace('\n', '')
    except Exception as e:
        raise e
    return data
