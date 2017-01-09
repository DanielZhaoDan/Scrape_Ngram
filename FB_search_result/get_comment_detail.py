import xlrd
import xlwt
import urllib
import re
import os
import urllib2

url_comment = [['Post url', 'Comment']]
files = []
cookie = 'datr=JvOuVyItp7-wt5YrOGKr9V7P; sb=PPOuV7-Wg9ncLv3N5qnvF8Iq; pl=n; lu=ggXBrbDSWNraGSW_RDaCMmoQ; act=1483866890604%2F12; c_user=100006957738125; xs=93%3AA003Pi-A4eHQ4A%3A2%3A1483866643%3A20772; fr=03NniPbnhahIjspAF.AWWaZXtEQQHPvSyxn0zJRQ0GBrM.BXorjj.xL.Fhs.0.0.BYcyAt.AWWKTneu; csm=2; s=Aa5XdK0l3reLVT9K.BYcgIT; p=-2; presence=EDvF3EtimeF1483943444EuserFA21B06957738125A2EstateFDutF1483943444673CEchFDp_5f1B06957738125F2CC; wd=1769x717'


def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path or 'txt' in path:
            files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files


def request_html(url):
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res


def comment_detail(url):
    global url_comment
    comment_list_reg = '\{comments:\[(.*?)\],pinnedcomments'
    reg = 'body:{text:"(.*?)"'
    try:
        html = request_html(url)
        comments = re.compile(comment_list_reg).findall(html)[0]
        comment_list = re.compile(reg).findall(comments)
        for obj in comment_list:
            url_comment.append([url, obj])
    except:
        pass


def read_excel(filename, start):
    global alldata
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        if i % 100 == 0:
            print filename + '---' +str(i)
        try:
            url = str(table.row(i)[4].value).strip().replace('&amp;', '&')
            comment_count = int(table.row(i)[12].value)
            if comment_count > 0:
                comment_detail(url)
        except:
            continue


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def get_ori_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    page.close()
    return html


def write_excel(filename, data):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(data)):
        one_row = data[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)
    print filename + "===========over============"


filenames = walk('data')
for filename in filenames:
    read_excel(filename, 1)
    write_excel('result_'+filename, url_comment)
    del url_comment
    url_comment = [['Post url', 'Comment']]