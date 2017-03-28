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
    index_number = 0

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            one_row = []
            for j in range(0, table.ncols):
                if j == 0 and i != 0:
                    index = int(row[j].value.split('_')[1])
                    if i >= 2 and index < int(table.row(i-1)[j].value.split('_')[1]):
                        index_number += 1
                    new_index = row[j].value.split('_')[0] + '_' + str(30*index_number + index)
                    one_row.append(new_index)
                else:
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


files = walk('data')
# files = ['data/kyoto_2.xls']
for filename in files:
    read_excel(filename, 0)
    write_excel(filename.replace('data', 'new'))
    alldata = []



