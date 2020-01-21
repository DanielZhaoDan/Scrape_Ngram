import xlrd
import os
import xlwt

alldata = [['Landing page', 'Search Query', 'Impressions', 'Clicks', 'CTR', 'Ave position']]
files = []
uid_set = set()
P_ID = 0
duplicated_count = 0
xlrd.biffh.unicode=lambda s, e: s.decode(e, errors="ignore")
xlrd.book.unicode=lambda s, e: s.decode(e, errors="ignore")


def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xlsx' in path or 'txt' in path:
            if 'result' not in path:
                files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files


def read_excel(filename, start):
    global duplicated_count, P_ID
    print('process -> '+filename)
    try:
        data = xlrd.open_workbook(filename)
        table = data.sheets()[1]

        for i in range(start, table.nrows):
            row = table.row(i)
            try:
                url = filename.replace('_', '/').replace('data/', '')
                one_row = [url]
                for j in range(0, table.ncols):
                    one_row.append(row[j].value)
                P_ID += 1
                alldata.append(one_row)
            except:
                print(i)
    except Exception as e:
        print 'EXP--'+filename, e


def write_excel(filename, alldata, flag=None):
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
        w = xlwt.Workbook(encoding='utf-8')
        ws = w.add_sheet('old', cell_overwrite_ok=True)
        for row in range(0, len(data)):
            one_row = data[row]
            for col in range(0, len(one_row)):
                try:
                    ws.write(row, col, one_row[col][:32766])
                except:
                    try:
                        ws.write(row, col, one_row[col])
                    except:
                        print('===Write excel ERROR===' + str(one_row[col]))
        w.save(_filename)
        print("%s===========over============%d" % (_filename, len(data)))
        i += 1
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
                    print('===Write excel ERROR===' + str(one_row[col]))
    w.save(filename)
    print("%s===========over============%d" % (filename, len(alldata)))


files = walk('data')
for i in range(len(files)):
    read_excel(files[i], 1)

write_excel('dataset2'+'.xls', alldata)
print(duplicated_count)
