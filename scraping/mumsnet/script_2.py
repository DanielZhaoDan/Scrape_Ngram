import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
import json
from scraping.utils import post_request_json, get_request_html_with_status, write_html, write_excel, remove_html_tag, \
    post_request_html

R_ID = 1
sheet1_data = [['Topic URL', 'Topic', 'Subject', 'Subject url', 'No. replies', 'Posts', 'Status', 'Date']]

cookie = '__cfduid=d55fe160144625242409ce78fa78e4c611607244606; mnshow=c1607244606775-202012060; mnax=1607244606775; rootsess=3FDDA11850C5947EE09DCE6F48B06BA1-n1; mnpop=c1607244606776-20201206x0; _ga=GA1.2.1019555004.1607244609; _gid=GA1.2.1609638681.1607244609; __utma=210627209.1019555004.1607244609.1607244609.1607244609.1; __utmc=210627209; __utmz=210627209.1607244609.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _sp_ses.1970=*; sp=a463581f-e462-4501-9c37-3ec4a0dfb25e; mpref=jp-haf~100_pt~8eaca573-0fd9-44dc-8fce-78a886b77426_sa~0_; mnft=QURHLTAxOjI5LE5PVC0wMTo4OCxTQ0gtMDE6MzgsQVNILTAxOjIyLENDTC0wMjo0MixBRFQtMTA6NSxBRFQtMDI6NjEsTFNILTAxOjI1LEFEVC0wMzo0NixKV1YtMDQ6MjAsUFBPLTAxOjg3LE5BRC0wMTo2LEJPTy0wMTo3OSxBRFQtMDk6OCxUQUctMDE6NTA=; __utmt_UA-410043-1=1; FCCDCF=[["AKsRol9ySQHrVu4dTOEQJb2ZegBVB1FhyATOHoif_Vu8he9N2vIJFOVodRgWYxnF60ONw5H7qJhjhlruXm--LSMEosZBBlNNVsdEZGENSemTPe10k3Ra_f-CHnceERG2twuYuVwFh1p66TOaePp-g-UhqojRmaWAVA=="],null,["[[],[],[],[],null,null,true]",1607245254628],null]; __utmb=210627209.7.10.1607244609; _sp_id.1970=a03766e6-390d-4b7e-8fa7-76329e847d22.1607244609.1.1607245545.1607244609.0cc2aa13-a849-4831-8ecb-3c4a5fc1cf6c'
topic_count = {}


def request_sheet2(no_row, base_url, topic, title, thread_url, replies):
    global sheet1_data
    comment_reg = 'data-post=.*?post_time">(.*?)<.*?message">(.*?)</p>'

    page_no = 1
    topic_count[topic] = topic_count.get(topic, 0)+1
    if topic_count[topic] > 2500:
        return
    i = 1
    isMain = True
    if i <= page_no:
        url = thread_url + '?pg=%d' % i
        print no_row, page_no, url
        try:
            html, _ = get_request_html_with_status(url, cookie)
            threads = re.compile(comment_reg).findall(html)

            for thread in threads:
                commment_date = get_date(thread[0].split(' ')[1])
                content = remove_html_tag(thread[1])
                one_row = [base_url, topic, title, thread_url, replies, content, 'Main' if isMain else 'Reply',
                           commment_date]
                sheet1_data.append(one_row)
                isMain = False
            i += 1
        except Exception as e:
            print 'ERR--', url, e
            i += 1


def get_date(ori):
    try:
        d = datetime.strptime(ori, '%d-%b-%y')
        date = d.strftime('%d/%m/%Y')
        return date
    except:
        return ori


def read_excel(filename, start=1):
    global sheet1_data
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]

    i = start
    while i < table.nrows:
        row = table.row(i)
        try:
            request_sheet2(i, row[0].value, row[1].value, row[2].value, row[3].value, row[4].value)
            i += 1
        except Exception as e:
            print i, e
        if i % 5000 == 0:
            write_excel('sheet2_%d.xls' % i, sheet1_data)
            del sheet1_data
            sheet1_data = []


reload(sys)
sys.setdefaultencoding('utf-8')
read_excel('data/mumset.xlsx', start=65001)
