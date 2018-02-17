import xlrd
import xlsxwriter
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
    data = xlrd.open_workbook(filename, encoding_override='utf-16-be')
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
    w = xlsxwriter.Workbook(filename)
    ws = w.add_worksheet()
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write_string(row, col, (one_row[col]))
            except:
                ws.write(row, col, (one_row[col]))
    w.close()
    print filename+"===========over============"

files = walk('data')
for i in range(len(files)):
    if '' in files[i]:
        read_excel(files[i], 0 if i == 0 else 1)
write_excel('Employed'+'.xlsx')
