# -*- coding: utf-8 -*-
import nltk
from collections import Counter
import xlrd, xlwt
import os, gc
import tinysegmenter
from nltk.util import ngrams
from konlpy.tag import Kkma

stop_word = ['you', 'my', 'do', '#', '<', '>', '|', '.', '。', '~' 'the', 'and', 'we', 'to', 'of', '!', 'I', ':', 'in', ')', 'for', 'with', '...', '(', 'is', '-', '?', 'an', 'a', 'the', 'be', 'as', 'of', 'in', 'on', 'it', 'off', 'to', 'too', 'he', 'she', 'is', 'and', 'because', 'but', 'are', 'were', 'was', 'there', 'their', '$', 'at', 'all', 'did', 'had', 'no', 'you', 'i', 'can', 'if', '$', 'so', '*', '\'m', '\'re', 'not' 'and', '--', 'it', '\'s', 'or', '.', '|', '"', 'this', 'that', 'have', 'has', 'for', '&', 'amp', '&', '{', '}', '\'s', '\'ve', '[', ']', ',', 'it\'s', 'its', 'wont', 'won\'t', '@', '#', '!', '*', '(', ')', '--', '_', '\\', '?', 'nt', 'n\'t']
stop_word += ["a", "able", "about", "above", "abroad", "according", "accordingly", "across", "actually", "adj", "after", "afterwards", "again", "against", "ago", "ahead", "ain't", "all", "allow", "allows", "almost", "alone", "along", "alongside", "already", "also", "although", "always", "am", "amid", "amidst", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway", "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate", "are", "aren't", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "b", "back", "backward", "backwards", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by", "c", "came", "can", "cannot", "cant", "can't", "caption", "cause", "causes", "certain", "certainly", "changes", "clearly", "c'mon", "co", "co.", "com", "come", "comes", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn't", "course", "c's", "currently", "d", "dare", "daren't", "definitely", "described", "despite", "did", "didn't", "different", "directly", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "during", "e", "each", "edu", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "entirely", "especially", "et", "etc", "even", "ever", "evermore", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "f", "fairly", "far", "farther", "few", "fewer", "fifth", "first", "five", "followed", "following", "follows", "for", "forever", "former", "formerly", "forth", "forward", "found", "four", "from", "further", "furthermore", "g", "get", "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "greetings", "h", "had", "hadn't", "half", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "here's", "hereupon", "hers", "herself", "he's", "hi", "him", "himself", "his", "hither", "hopefully", "how", "howbeit", "however", "hundred", "i", "i'd", "ie", "if", "ignored", "i'll", "i'm", "immediate", "in", "inasmuch", "inc", "inc.", "indeed", "indicate", "indicated", "indicates", "inner", "inside", "insofar", "instead", "into", "inward", "is", "isn't", "it", "it'd", "it'll", "its", "it's", "itself", "i've", "j", "just", "k", "keep", "keeps", "kept", "know", "known", "knows", "l", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "let's", "like", "liked", "likely", "likewise", "little", "look", "looking", "looks", "low", "lower", "ltd", "m", "made", "mainly", "make", "makes", "many", "may", "maybe", "mayn't", "me", "mean", "meantime", "meanwhile", "merely", "might", "mightn't", "mine", "minus", "miss", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "must", "mustn't", "my", "myself", "n", "name", "namely", "nd", "near", "nearly", "necessary", "need", "needn't", "needs", "neither", "never", "neverf", "neverless", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "no-one", "nor", "normally", "not", "nothing", "notwithstanding", "novel", "now", "nowhere", "o", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "one's", "only", "onto", "opposite", "or", "other", "others", "otherwise", "ought", "oughtn't", "our", "ours", "ourselves", "out", "outside", "over", "overall", "own", "p", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", "provided", "provides", "q", "que", "quite", "qv", "r", "rather", "rd", "re", "really", "reasonably", "recent", "recently", "regarding", "regardless", "regards", "relatively", "respectively", "right", "round", "s", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "since", "six", "so", "some", "somebody", "someday", "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "t", "take", "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "there'd", "therefore", "therein", "there'll", "there're", "theres", "there's", "thereupon", "there've", "these", "they", "they'd", "they'll", "they're", "they've", "thing", "things", "think", "third", "thirty", "this", "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "till", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "t's", "twice", "two", "u", "un", "under", "underneath", "undoing", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "upwards", "us", "use", "used", "useful", "uses", "using", "usually", "v", "value", "various", "versus", "very", "via", "viz", "vs", "w", "want", "wants", "was", "wasn't", "way", "we", "we'd", "welcome", "well", "we'll", "went", "were", "we're", "weren't", "we've", "what", "whatever", "what'll", "what's", "what've", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "where's", "whereupon", "wherever", "whether", "which", "whichever", "while", "whilst", "whither", "who", "who'd", "whoever", "whole", "who'll", "whom", "whomever", "who's", "whose", "why", "will", "willing", "wish", "with", "within", "without", "wonder", "won't", "would", "wouldn't", "x", "y", "yes", "yet", "you", "you'd", "you'll", "your", "you're", "yours", "yourself", "yourselves", "you've", "z", "zero"]
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
            if entry[0].lower().strip() in stop_word or entry[0].strip() == '':
                result.remove(entry)
        else:
            for i in range(entry_length):
                if entry[0][1].lower().strip() in stop_word or entry[0][1].strip() == '' or entry[0][1].strip() == 'N/A':
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
    # write_excel('result/fourgram_'+filename, alldata)
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
