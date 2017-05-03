import xlrd
import xlsxwriter
import sets

alldata = []


def read_excel(filename, start=1):
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="cp1252")
    table = data.sheets()[0]

    for i in range(start, table.nrows-1):
        row = table.row(i)
        try:
            url = row[1].value
            if 'recent-activity' in url:
                continue
            one_row = [row[i].value for i in range(7)]
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
                ws.write_string(row, col, one_row[col])
            except:
                try:
                    ws.write(row, col, one_row[col])
                except:
                    raise
    w.close()
    print filename+"===========over============"

read_excel('res.xls', start=0)
write_excel('result'+'.xls')
