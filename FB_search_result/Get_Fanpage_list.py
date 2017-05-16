import xlrd
import xlwt
import urllib
import re
import os
import urllib2

cookie = 'datr=JvOuVyItp7-wt5YrOGKr9V7P; dats=1; sb=PPOuV7-Wg9ncLv3N5qnvF8Iq; pl=n; lu=ggn3eV7wCUY_nKwLaHHKOZuw; c_user=100006957738125; xs=152%3AHbkgPULgfH87Rw%3A2%3A1494575387%3A20772; fr=03NniPbnhahIjspAF.AWUPvHMe0b0jKeIed90jb8A9QLw.BXorjj.xL.FkV.0.0.BZGlqU.AWWBDng2; act=1494900032112%2F2; presence=EDvF3EtimeF1494900206EuserFA21B06957738125A2EstateFDutF1494900206772CEchFDp_5f1B06957738125F7CC'
alldata = []
url_fan_dict = {}


def is_fanpage(url):
    html = get_request(url)
    if 'data-referrer="timeline_light_nav_top" id="u_0_n"' in html:
        return 'N'
    return 'Y'


def get_request(get_url):
    req = urllib2.Request(get_url)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
    req.add_header("connection", "Keep-Alive")
    req.add_header("Referer", get_url)
    req.add_header("Cookie", cookie)
    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    res = res.replace('\t', '').replace('\r', '').replace('\n', '')
    return res


def read_excel(filename, start):
    global alldata
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        if i % 100 == 0:
            print filename + '---' +str(i)
        try:
            url = table.row(i)[4].value.strip().split('?')[0]
            if table.row(i)[3].value.strip() != '':
                url_fan_dict[url] = table.row(i)[3].value
                continue
            if not url_fan_dict.get(url):
                is_fan = is_fanpage(url)
                url_fan_dict[url] = is_fan
            else:
                is_fan = url_fan_dict.get(url)
            print table.row(i)[2].value, is_fan, url
            alldata.append([url, is_fan])
        except:
            print 'ERROR--' + str(i)
            continue


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def write_excel(filename, data):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding="UTF-8")
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(data)):
        one_row = data[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)
    print filename + "===========over============"

read_excel('result_data/data.xlsx', 1)
write_excel('result_data/fanpage.xls', alldata)
# write(get_request('https://www.facebook.com/wilawan.keajung/'), '2.html')


