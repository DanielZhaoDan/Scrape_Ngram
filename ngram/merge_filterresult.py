# -*- coding: utf-8 -*-
import os
import xlrd, xlwt
import gc
import operator

alldata = {}
files = []

def write_excel(filename, alldata):
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    row_length = len(alldata)
    ws.write(0, 0, 'Words')
    ws.write(0, 1, 'Fequency')
    for row in range(0,row_length):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            ws.write(row+1, col, one_row[col])
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

def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path and '_2016' in path:
            files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files

walk('merge')

for filename in files:
    print '---'+filename+'---'
    filename_2 = filename.replace('_2016', '_2015')
    read_count_into_dict(filename, 1)
    read_count_into_dict(filename_2, 1)
    sorted_alldata = sorted(alldata.items(), key=operator.itemgetter(1), reverse=True)
    write_excel(filename.replace('_2016', ''), sorted_alldata)
    alldata = {}