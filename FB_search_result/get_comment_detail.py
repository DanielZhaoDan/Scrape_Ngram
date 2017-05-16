import xlrd
import xlwt
import urllib
import re
import os
import urllib2

url_comment = [['Post url', 'Comment']]
files = []
cookie = 'datr=8Wr0WBPCvG1hAY_GM9Zykf_v; dats=1; sb=5SkIWRQI17-q41aRoiii9GQl; pl=n; lu=ggNbfvL0A2bcBIcVj69LEkkQ; c_user=100006957738125; xs=204%3AUDThmkC8Jv58jw%3A2%3A1494914617%3A20772; fr=0SiWnVrFqp9JSfI4Y.AWWbL_B5xhPZIOPkZHNw8kSnaik.BY4ewn.J-.FkV.0.0.BZGqor.AWUG5QVz; presence=EDvF3EtimeF1494919788EuserFA21B06957738125A2EstateFDutF1494919788712CEchFDp_5f1B06957738125F2CC; act=1494919835511%2F0'


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
        comments = re.compile(comment_list_reg).findall(html)
        if comments:
            comment_list = re.compile(reg).findall(comments[0])
        else:
            comment_list = re.compile('\{\"body\":\{\"text\":\"(.*?)\"').findall(html)
        for obj in comment_list:
            url_comment.append([url, obj])
        if len(comment_list) > 0:
            print(url, len(comment_list))
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
    w = xlwt.Workbook(encoding="UTF-8")
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(data)):
        one_row = data[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)
    print filename + "===========over============"


filenames = walk('data')
for filename in filenames:
    print '======start========='+filename
    read_excel(filename, 1)
    write_excel('result_'+filename.replace('.xlsx', '.xls'), url_comment)
    del url_comment
    url_comment = [['Post url', 'Comment']]