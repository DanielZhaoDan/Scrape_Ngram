# coding: utf-8
import sys, urllib
import urllib2
import re
import HTMLParser
import time, datetime
from selenium import webdriver
import xlwt
import os
import httplib
import xlrd

stored_url = set()
remaining_urls = set()


def read_stored_url(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    print 'total size: ', table.nrows

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            profile_url = row[0].value
            stored_url.add(profile_url)
        except Exception as e:
            print(i, e[:20])


def filter_unstored_url(filename, start=1):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    print 'total size: ', table.nrows

    for i in range(start, table.nrows):
        row = table.row(i)
        try:
            profile_url = row[0].value
            if profile_url not in stored_url:
                remaining_urls.add(profile_url)
        except Exception as e:
            print(i, e[:20])


def write_excel(filename, alldata, flag=None):
    filename = 'data/' + filename
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)

    i = 0
    while len(alldata) > 65500:
        _filename = filename.replace('.xls', '_%s.xls' % i)
        start_index = 0
        end_index = 65500
        data = alldata[start_index:end_index]
        alldata = alldata[end_index:]
        w = xlwt.Workbook()
        ws = w.add_sheet('old', cell_overwrite_ok=True)
        for row in range(0, len(data)):
            one_row = data[row]
            for col in range(0, len(one_row)):
                try:
                    ws.write(row, col, one_row[col][:32766])
                except:
                    try:
                        ws.write(row, col, one_row[col])
                    except:
                        print('===Write excel ERROR===' + str(one_row[col]))
        w.save(_filename)
        print("%s===========over============%d" % (_filename, len(data)))
        i += 1
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
                except:
                    print('===Write excel ERROR===' + str(one_row[col]))
    w.save(filename)
    print("%s===========over============%d" % (filename, len(alldata)))


read_stored_url('data/like_follower_pre.xlsx')
filter_unstored_url('data/also_likes.xlsx')
print 'remaining: ', len(remaining_urls)
out_f = open("out.txt", 'w+')
for url in remaining_urls:
    try:
        print >> out_f, url
    except:
        print url
