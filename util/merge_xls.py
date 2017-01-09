import xlwt, xlrd
import os

alldata = []
files = []


def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path or 'txt' in path:
            if 'result' not in path:
                files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files


def read_excel(filename, start):
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            one_row = []
            for j in range(0, table.ncols):
                one_row.append(row[j].value)
            alldata.append(one_row)
        except:
            print(i)


def write_excel(filename):
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)
    print filename+"===========over============"

prefix = 'vacation'
# read_excel('data/'+prefix+'-2016.xls', 0)
# read_excel('data/'+prefix+'-2015.xls', 1)
read_excel('data/'+prefix+'-2014.xls', 1)
read_excel('data/'+prefix+'-2013.xls', 1)
write_excel(prefix+'.xls')
