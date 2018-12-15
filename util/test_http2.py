import xlrd
import xlsxwriter
import os
import csv

uid_set = set()
index_uid_dict = {}
duplicated_count = 0
files = []


def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path or 'csv' in path:
            if 'result' not in path:
                files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files


def read_excel(filename, start):
    global duplicated_count
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

def read_file():
    array = []
    with open("exception.txt", "r") as ins:
        for line in ins:
            row = index_uid_dict.get(line.strip(), ['N/A', line.strip()])
            array.append(row)
    return array

def read_csv(filename):
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            index = row[1]
            index_uid_dict[index] = row

def write_list(filename, my_list):
    with open(filename, 'w') as f:
        for item in my_list:
            f.write("%s\n" % ';'.join(item))

files = walk('data')
for i in range(len(files)):
    if '' in files[i]:
        read_csv(files[i])
res = read_file()
write_list('ex.txt', res)
