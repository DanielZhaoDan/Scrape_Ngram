# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
import json
from scraping.utils import post_request_json, get_request_html, write_html, write_excel

saved_hotel = set()
R_ID = 1
sheet1_data = [['ID', 'SKU des', 'Rank', 'Price', 'Brand', 'Product Url', 'Display Size', 'Seller', 'Shipping location',
                'Condition']]

cookie = '_zap=e9f9ab3a-014f-45a1-b9db-bee9f1508413; d_c0="ABBVnRBqwRGPTh7obeupBOLwtzpsYkjVSyA=|1597817591"; _ga=GA1.2.293440759.1597817592; z_c0="2|1:0|10:1599545922|4:z_c0|92:Mi4xelZSSEFBQUFBQUFBRUZXZEVHckJFU1lBQUFCZ0FsVk5RbkJFWUFBcXNWNG9QdGNMYUpvQU5BMVkxb2c4RFc3cFpR|8f84bf9017436ef78a87333a9f8e8d7a5e221ae1eab7295ab9f120f11ec3317c"; q_c1=c8c9d72c43024b20848e706280796d8d|1599545934000|1599545934000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1599545893,1599545895,1599728615,1601800257; _xsrf=2db1e585-0323-47b8-b4f6-a5bc02c50327; KLBRSID=81978cf28cf03c58e07f705c156aa833|1603376495|1603376491'

urls = [
    # ('Rich districts in Shenzhen', 'https://zhuanlan.zhihu.com/p/68574122'),
    # ('House buying for children education', 'https://zhuanlan.zhihu.com/p/164986378'),
    # ('Property', 'https://zhuanlan.zhihu.com/p/59075902'),
    # ('Shopping habits', 'https://zhuanlan.zhihu.com/p/25553397'),
    # ('Servants', 'https://zhuanlan.zhihu.com/p/144642784'),
    # ('Time management', 'https://zhuanlan.zhihu.com/p/36509123'),
    # ('Eating habits', 'https://zhuanlan.zhihu.com/p/103879591'), #
    # ('Resources', 'https://zhuanlan.zhihu.com/p/25268193'),
    ('益生菌', 'https://www.zhihu.com/topic/19671113/hot'),
]


def request_topic(item, uid):
    global sheet1_data
    topic, url = item

    question_id = url.split('/')[-2]
    url_base = 'https://www.zhihu.com/api/v4/topics/' + question_id + '/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id='

    i = 0
    while i < 30:
        url = url_base + str(i*10) + '.00000'
        html = get_request_html(url, cookie)
        json_obj = json.loads(html)

        data_list = json_obj.get('data', [])
        for data in data_list:
            id = data['target'].get('id', 'N/A')
            entry_url = data['target'].get('url', 'N/A')
            title = data['target'].get('title', 'N/A')
            # content = data['target']['content']
            if data['target'].get('created_time'):
                time = get_date(data['target'].get('created_time'))
            else:
                time = get_date(data['target'].get('created', 'N/A'))
            agree = data['target'].get('voteup_count', 'N/A')
            comment = data['target'].get('comment_count', 'N/A')

            one_row = [id, entry_url, title, agree, comment, time]
            sheet1_data.append(one_row)
            print one_row

        i += 1


def get_date(ts):
    try:
        return datetime.fromtimestamp(ts).strftime('%d/%m/%Y')
    except:
        return s


def request_zhuanlan(item, uid):
    global sheet1_data
    topic, url = item
    html = get_request_html(url, cookie)

    question_id = url.split('/')[-1]

    base_reg = 'class="RichText ztext Post-RichText">(.*?)</div.*?aria-label="赞同 (.*?)".*?CommentBtn.*?</span>(.*?) '

    data = re.compile(base_reg).findall(html)

    if not data:
        return
    comments = remove_html_tag(data[0][0])[:32766]
    no_agree = data[0][1]
    no_answer = data[0][2]

    one_row = ['CN_ZH_%s' % question_id, topic, url, no_answer, no_agree, no_answer, comments]
    sheet1_data.append(one_row)

    page_no = int(no_answer.replace(',','')) / 20 + 1

    i = 0

    while i < page_no:
        try:
            comment_url = 'https://www.zhihu.com/api/v4/articles/' + question_id + '/root_comments?order=normal&limit=20&status=open&offset=' + str(i*20)
            html = get_request_html(comment_url, cookie)
            json_obj = json.loads(html)

            print i * 5, no_answer, question_id, len(json_obj.get('data', []))
            if len(json_obj.get('data', [])) == 0:
                break
            i += 1

            for item in json_obj.get('data', []):
                comments = remove_html_tag(item['content'])[:32766]
                no_agree = item['vote_count']
                no_comment = item['child_comment_count']

                one_row = ['CN_ZH_%s' % question_id, topic, url, no_answer, no_agree, no_comment, comments]
                print one_row
                sheet1_data.append(one_row)
        except Exception as e:
            i += 1
            print 'ERR---', url, i, e


def request_sheet1(item, uid):
    global sheet1_data

    topic, url = item

    question_id = url.split('/')[-1]

    api_url = 'https://www.zhihu.com/api/v4/questions/' + question_id + '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&platform=desktop&sort_by=default'

    no_answer = None

    i = 0

    while True:
        try:
            if no_answer and i * 5 > no_answer:
                break

            html = get_request_html(api_url + '&offset=%d' % (i*5), cookie)
            json_obj = json.loads(html)

            if not no_answer:
                no_answer = json_obj.get('paging', {}).get('totals', 0)

            print i * 5, no_answer, question_id, len(json_obj.get('data', []))
            if len(json_obj.get('data', [])) == 0:
                break
            i += 1

            for item in json_obj.get('data', []):
                comments = remove_html_tag(item['content'])[:32766]
                no_agree = item['voteup_count']
                no_comment = item['comment_count']

                one_row = ['CN_ZH_%s' % question_id, topic, url, no_answer, no_agree, no_comment, comments]
                # print one_row
                sheet1_data.append(one_row)
        except Exception as e:
            i += 1
            print 'ERR---', url, i, e


def get_comments(ori):
    escape_words = ['的帖子', '</blockquote>', '編輯', '编辑']

    for word in escape_words:
        if word in ori:
            ori = remove_html_tag(ori.split(word)[-1])
    return remove_html_tag(ori)


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd))


def step_1():
    uid = 1
    for item in urls:
        topic, url = item
        if 'zhuanlan' in url:
            request_zhuanlan(item, 'CN_ZH_%d' % uid)
        elif 'topic' in url:
            request_topic(item, 'CN_ZH_%d' % uid)
        else:
            request_sheet1(item, 'CN_ZH_%d' % uid)
        uid += 1
    write_excel('CN_zhihu.xls', sheet1_data)


def read_excel(filename, start):
    id_content = {}
    alldata = []
    try:
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]

        for i in range(start, table.nrows):
            row = table.row(i)
            try:
                ID = row[0].value
                if ID in id_content:
                    one_row = []
                    for j in range(0, table.ncols):
                        one_row.append(row[j].value)
                    one_row.append(id_content[ID])
                    alldata.append(one_row)
                else:
                    id_content[ID] = row[6].value

            except:
                print(i)
    except Exception as e:
        print 'EXP--'+filename, e
    write_excel('CN_zhihu_v2.xls', alldata)


reload(sys)
sys.setdefaultencoding('utf-8')
step_1()
# read_excel('data/CN_zhihu.xls', start=1)