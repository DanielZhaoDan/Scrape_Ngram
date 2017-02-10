# -*- coding: utf-8 -*-
import nltk
from collections import Counter
import xlrd, xlwt
import os, gc
import tinysegmenter
from nltk.util import ngrams
from konlpy.tag import Kkma

stop_words = ['%', '``', '$', '$', '*', '\'m', '\'re', '--', '\'s', 'or', '.', '|', '"', '&', 'amp', '&', '{', '}', '\'s', '\'ve', '[', ']', ',', 'it\'s', 'its', 'wont', 'won\'t', '@', '#', '!', '*', '(', ')', '--', '_', '\\', '?', 'nt', 'n\'t']
stop_words += ['\'\'', ':/', "/", "<", ">", '.', '/)', ':', '-']
stop_words += ['wrote']
files = []
NGRAM_RESULT_FOLDER = 'ngram_'


def load_data_from_excel(filename, col_indexs):
    content = ''
    data = xlrd.open_workbook(filename, encoding_override='utf-8')
    table = data.sheets()[0]
    for i in range(1, table.nrows):
        for col_index in col_indexs:
            try:
                if 'N/A' != table.row(i)[col_index].value and '' != table.row(i)[col_index].value:
                    content = content + table.row(i)[col_index].value + '\n'
            except:
                continue
    return content


def load_data_from_txt(filename):
    with open(filename) as f:
        content = f.readlines()
    return ''.join(content)


def get_unigram(token_list, reverse):
    fre_dist = Counter(token_list)
    fre_list = [(key, val) for key, val in fre_dist.items()]
    fre_list.sort(key=getKey, reverse=reverse)
    return fre_list


def get_bigram(tokens_list, reverse):
    bigram = nltk.bigrams(tokens_list)
    fre_dist = nltk.FreqDist(bigram)
    fre_list = [(key, val) for key, val in fre_dist.items()]
    fre_list.sort(key=getKey, reverse=reverse)
    return fre_list


def get_trigram(tokens_list, reverse):
    trigram = nltk.trigrams(tokens_list)
    fre_dist = nltk.FreqDist(trigram)
    fre_list = [(key, val) for key, val in fre_dist.items()]
    fre_list.sort(key=getKey, reverse=reverse)
    return fre_list


def get_fourgram(tokens_list, reverse):
    fourgram = ngrams(tokens_list, 4)
    fre_dist = nltk.FreqDist(fourgram)
    fre_list = [(key, val) for key, val in fre_dist.items()]
    fre_list.sort(key=getKey, reverse=reverse)
    return fre_list


def get_fivegram(tokens_list, reverse):
    fourgram = ngrams(tokens_list, 5)
    fre_dist = nltk.FreqDist(fourgram)
    fre_list = [(key, val) for key, val in fre_dist.items()]
    fre_list.sort(key=getKey, reverse=reverse)
    return fre_list


def getKey(item):
    return item[1]


def remove_stopwords(ori_list, entry_length):
    result = ori_list[:]
    for entry in ori_list:
        if entry_length == 1:
            if entry[0].strip() == '':
                result.remove(entry)
        else:
            for i in range(entry_length):
                if entry[0][1].strip() == 'wrote' or entry[0][1].strip() == '' or entry[0][1].strip() == 'N/A':
                    result.remove(entry)
                    break
    return result


def write_excel(filename, alldata):
    filename = filename.replace('xlsx', 'xls').replace('txt', 'xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    row_length = len(alldata)
    if row_length > 1000:
        row_length = 1000
    for row in range(0,row_length):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col])
            except:
                pass
    w.save(filename)


def map_into_list(results):
    alldata = []
    for result in results:
        entry = result[0]
        one_row_1 = ''
        for i in range(len(entry)):
            one_row_1 += entry[i]
            if i < len(entry) -1 :
                one_row_1 += ', '
        one_row = [one_row_1, result[1]]
        alldata.append(one_row)
    return alldata


def each_ori_file(filename, col_index):
    print '----start loading----'+filename
    content = ''
    if '.txt' in filename:
        content = load_data_from_txt(filename)
        content = content.decode('utf-16')
    else:
        content = load_data_from_excel(filename, col_index)

    print '----start tokenize----'+filename
    words = []

    #eng
    words = nltk.word_tokenize(content)
    #jp
    # words = get_tokenize(content)
    #kr
    # kkma = Kkma()
    # words = kkma.morphs(content)

    # print '----unigram----'+filename
    # li = get_unigram(words, True)
    # result = remove_stopwords(li, 1)
    # write_excel(NGRAM_RESULT_FOLDER+filename.replace('.','-Uni.'), result)

    print '----bigram----'
    li = get_bigram(words, True)
    result = remove_stopwords(li, 2)
    alldata = map_into_list(result)
    write_excel(NGRAM_RESULT_FOLDER+filename.replace('.','-Bi.'), alldata)
    del alldata
    gc.collect()


    print '----trigram----'
    li = get_trigram(words, True)
    result = remove_stopwords(li, 3)
    alldata = map_into_list(result)
    write_excel(NGRAM_RESULT_FOLDER+filename.replace('.','-Tri.'), alldata)
    del alldata
    gc.collect()

    # print '----fourgram----'
    # li = get_fourgram(words, True)
    # result = remove_stopwords(li, 4)
    # alldata = map_into_list(result)
    # write_excel(NGRAM_RESULT_FOLDER+filename.replace('.','-Four.'), alldata)
    # del alldata
    # gc.collect()

    # print '----fivegram----'
    # li = get_fivegram(words, True)
    # result = remove_stopwords(li, 5)
    # alldata = map_into_list(result)
    # write_excel('result1/fivegram_'+filename, alldata)
    # print '-----over------'+filename
    # del alldata
    # gc.collect()


def get_tokenize(content):
    segment = tinysegmenter.TinySegmenter()
    return segment.tokenize(content)


def walk(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if '.xls' in path or 'txt' in path:
            files.append(path)
        if os.path.isdir(path):
            walk(path)
    return files

col_indexs = [[1]]

filenames = walk('data')

for i in range(0, len(filenames)):
    each_ori_file(filenames[i], col_indexs[0])
    # try:
    #     each_ori_file(filenames[i], col_indexs[i])
    # except Exception:
    #     print '-----ERROR'+filenames[i]
