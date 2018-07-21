import xlrd
import xlwt
import os

C_IDs = [53, 43, 54, 23, 30, 50, 21, 18, 49, 15, 41, 32, 42, 35, 39, 48, 37, 36, 6, 100, 13, 68, 22, 28, 26, 9, 64, 10, 19, 70, 12, 29, 44, 47, 33, 78, 4, 45, 51, 93, 98, 16, 25, 57, 69, 27, 20, 14]


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_'+str(flag)+'.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
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
                except Exception as e:
                    print '===Write excel ERROR==='+str(one_row[col])
                    print(e)
    w.save(filename)
    print filename+"===========over============"


def read_excel(filename, sheet_index, start=1):
    sheet2_data = []
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[sheet_index]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            cid = row[0].value
            if cid != 'Category ID':
                cid = int(cid)
            if cid not in C_IDs:
                one_row = []
                for j in range(0, table.ncols):
                    one_row.append(row[j].value)
                sheet2_data.append(one_row)
        except Exception as e:
            print(i)
            print(e)

    write_excel('data/res1_%d.xls' % sheet_index, sheet2_data[0:65530])
    write_excel('data/res2_%d.xls' % sheet_index, sheet2_data[65531:])


read_excel('data.xlsx', 2, start=0)