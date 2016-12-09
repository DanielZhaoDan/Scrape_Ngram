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


def read_excel(filename):
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(0, table.nrows):
        row = table.row(i)
        try:
            name = row[0].value
            email = row[1].value
            url = row[2].value
            if email != 'N/A':
                alldata.append([name, email, url])
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

folder = 'sh'
files = walk(folder)
for fi in files:
    try:
        read_excel(fi)
    except:
        print(fi)
write_excel(folder + '/result.xls')
