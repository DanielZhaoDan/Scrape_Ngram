# -*- coding: utf-8 -*-
import os
import xlrd, xlwt
import gc
import operator

alldata = {}

def write_excel(filename, alldata):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    row_length = len(alldata)
    for row in range(0,row_length):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            ws.write(row, col, one_row[col])
    w.save(filename)

def read_count_into_dict(filename, start):
    global alldata
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        try:
            data = str(table.row(i)[0].value).strip()
            count = alldata.get(data, 0)
            count = count + int(table.row(i)[1].value)
            alldata[data] = count
        except:
            continue

filenames = ['filtered_data22/PC_show_3_1-Tri.xls', 'filtered_data22/PC_show_3_2-Tri.xls', 'filtered_data22/PC_show_3_2-Tri.xls', 'filtered_data22/PC_show_3_4-Tri.xls']
for filename in filenames:
    read_count_into_dict(filename, 1)
sorted_alldata = sorted(alldata.items(), key=operator.itemgetter(1), reverse=True)
write_excel('filtered_data22/PC_show-Tri.xls', sorted_alldata)