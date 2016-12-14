import xlrd, xlwt
import urllib
import re

alldata = [['Date', 'Location', 'Profile Name', 'Profile URL', 'Post Link', 'Content', 'Links in Content', 'Media Type',
         'Headline', 'Body', 'Website', 'emotion count', 'Comment count', 'Share count', 'View count', 'Total Engagement', 'Engagement Ratio', 'Year', 'Keyword']]

def read_count_into_dict(filename, start):
    global alldata
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        if i % 100 == 0:
            print i
        try:
            post_link = str(table.row(i)[4].value).strip().replace('&amp;', '&')
            comment, share = get_share_comment(post_link)
            data = []
            for j in range(table.ncols+2):
                if j == 4:
                    data.append(post_link)
                elif j == 11 or j == 14:
                    data.append(int(table.row(i)[j].value))
                elif j == 12:
                    data.append(int(comment))
                elif j == 13:
                    data.append(int(share))
                elif j == 15:
                    total = data[11] + data[12] + data[13] + data[14]
                    data.append(total)
                elif j == 16:
                    try:
                        ratio = (data[13] + 0.0) / data[15]
                    except:
                        ratio = 0
                    data.append(ratio)
                elif j == 17:
                    data.append(int(table.row(i)[j-2].value))
                elif j > 17:
                    data.append(table.row(i)[j-2].value)
                else:
                    data.append(table.row(i)[j].value)
            alldata.append(data)
        except:
            continue
    print i

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

def get_share_comment(link):
    try:
        html = get_ori_html(link)
        reg = 'commentcount:(.*?),.*?sharecount:(.*?),'
        comment_share = re.compile(reg).findall(html)
        return comment_share[0][0], comment_share[0][1]
    except:
        print 'ERROR==='+link
        return 0, 0

def write_excel(filename, data):
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(data)):
        one_row = data[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)
    print filename + "===========over============"

read_count_into_dict('exp-Consolidated Report.xlsx', 1)
write_excel('result.xls', alldata)
# print(get_share_comment('https://www.facebook.com/fatclaychua/posts/469206499935530?match=YWlyYm5i'))