import xlrd
import xlsxwriter
import sets

alldata = []


def read_excel_into_dict(filename, start, key_index, value_indexes):
    d = {}
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            key = row[key_index].value
            values = []
            for j in range(0, table.ncols):
                if j in value_indexes:
                    values.append(row[j].value)
            d[key] = values
        except:
            print(i)
    return d


def read_excel(filename, start, source_dict, key_index):
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            one_row = []
            key = row[key_index].value.split('/recent-acti')[0]
            values = source_dict.get(key, [])
            for j in range(0, table.ncols):
                one_row.append(row[j].value)
            for t in values:
                one_row.append(t)
            alldata.append(one_row)
        except:
            print(i)


def read_excel_filter(filename, start, key_index):
    print('process -> '+filename)
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    s = set([])

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            key = row[key_index].value
            if s.__contains__(key):
                continue
            s.add(key)
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
                ws.write_string(row, col, one_row[col])
            except:
                try:
                    ws.write(row, col, one_row[col])
                except:
                    raise
    w.close()
    print filename+"===========over============"

d = read_excel_into_dict('1.xlsx', 1, 3, [0])
read_excel('2.xlsx', 1, d, 0)
# read_excel_filter('2.xlsx', 0, 1)
write_excel('result'+'.xlsx')
