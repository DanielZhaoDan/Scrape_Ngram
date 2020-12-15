import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
import json
from scraping.utils import post_request_json, get_request_html_with_status, write_html, write_excel, remove_html_tag, post_request_html

saved_hotel = set()
R_ID = 1
sheet1_data = [['Topic URL', 'Topic', 'Subject', 'Subject url', 'No. replies', 'Posts', 'Status', 'Date']]


cookie = '__cfduid=d55fe160144625242409ce78fa78e4c611607244606; mnshow=c1607244606775-202012060; mnax=1607244606775; rootsess=3FDDA11850C5947EE09DCE6F48B06BA1-n1; mnpop=c1607244606776-20201206x0; _ga=GA1.2.1019555004.1607244609; _gid=GA1.2.1609638681.1607244609; __utma=210627209.1019555004.1607244609.1607244609.1607244609.1; __utmc=210627209; __utmz=210627209.1607244609.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _sp_ses.1970=*; sp=a463581f-e462-4501-9c37-3ec4a0dfb25e; mpref=jp-haf~100_pt~8eaca573-0fd9-44dc-8fce-78a886b77426_sa~0_; mnft=QURHLTAxOjI5LE5PVC0wMTo4OCxTQ0gtMDE6MzgsQVNILTAxOjIyLENDTC0wMjo0MixBRFQtMTA6NSxBRFQtMDI6NjEsTFNILTAxOjI1LEFEVC0wMzo0NixKV1YtMDQ6MjAsUFBPLTAxOjg3LE5BRC0wMTo2LEJPTy0wMTo3OSxBRFQtMDk6OCxUQUctMDE6NTA=; __utmt_UA-410043-1=1; FCCDCF=[["AKsRol9ySQHrVu4dTOEQJb2ZegBVB1FhyATOHoif_Vu8he9N2vIJFOVodRgWYxnF60ONw5H7qJhjhlruXm--LSMEosZBBlNNVsdEZGENSemTPe10k3Ra_f-CHnceERG2twuYuVwFh1p66TOaePp-g-UhqojRmaWAVA=="],null,["[[],[],[],[],null,null,true]",1607245254628],null]; __utmb=210627209.7.10.1607244609; _sp_id.1970=a03766e6-390d-4b7e-8fa7-76329e847d22.1607244609.1.1607245545.1607244609.0cc2aa13-a849-4831-8ecb-3c4a5fc1cf6c'

urls = [
    # ('Back to work', 'https://www.mumsnet.com/Talk/going_back_to_work'),
    # ('Business founders/entrepreneurs', 'https://www.mumsnet.com/Talk/small_business'),
    # ('Child mental health', 'https://www.mumsnet.com/Talk/child_adolescent_mental_health'),
    # ('Childcare options', 'https://www.mumsnet.com/Talk/childcare_options'),
    # ('Childminders', 'https://www.mumsnet.com/Talk/childminders_nannies_au_pairs_etc'),
    ('Children\'s health', 'https://www.mumsnet.com/Talk/childrens_health'),
    ('Climate Change', 'https://www.mumsnet.com/Talk/climate_change'),
    ('Dadsnet', 'https://www.mumsnet.com/Talk/dadsnet'),
    ('Divorce/separation', 'https://www.mumsnet.com/Talk/divorce_separation'),
    ('Education', 'https://www.mumsnet.com/Talk/education'),
    ('Elderly parents', 'https://www.mumsnet.com/Talk/elderly_parents'),
    ('Ethical dilemmas', 'https://www.mumsnet.com/Talk/ethical_dilemmas'),
    ('Exercise', 'https://www.mumsnet.com/Talk/exercise'),
    ('Extra-curricular activities', 'https://www.mumsnet.com/Talk/extra_curricular_activities'),
    ('Family planning', 'https://www.mumsnet.com/Talk/family_planning'),
    ('Further education', 'https://www.mumsnet.com/Talk/further_education'),
    ('Gaming', 'https://www.mumsnet.com/Talk/video_games_chat'),
    ('General health', 'https://www.mumsnet.com/Talk/general_health'),
    ('Gifted and talented', 'https://www.mumsnet.com/Talk/gifted_and_talented'),
    ('Home ed', 'https://www.mumsnet.com/Talk/home_ed'),
    ('Investments', 'https://www.mumsnet.com/Talk/investments'),
    ('Living overseas', 'https://www.mumsnet.com/Talk/living_overseas'),
    ('Lockdown learning', 'https://www.mumsnet.com/Talk/lockdown_learning'),
    ('Money matters', 'https://www.mumsnet.com/Talk/legal_money_matters'),
    ('Multicultural families', 'https://www.mumsnet.com/Talk/multicultural_families'),
    ('Parenting', 'https://www.mumsnet.com/Talk/parenting'),
    # ('Preschool education', 'https://www.mumsnet.com/Talk/preschool'),
    # ('Preteens', 'https://www.mumsnet.com/Talk/preteens'),
    # ('Primary education', 'https://www.mumsnet.com/Talk/primary'),
    # ('Step-parenting', 'https://www.mumsnet.com/Talk/stepparenting'),
    # ('Travel advice', 'https://www.mumsnet.com/Talk/general_advice_tips'),
    # ('Volunteering and charitable giving', 'https://www.mumsnet.com/Talk/volunteering_and_charitable_giving'),
    # ('Work', 'https://www.mumsnet.com/Talk/work'),
]

uid_level_dict = {}


def request_sheet1(topic, base_url):
    global sheet1_data

    base_reg = 'standard-thread-title.*?href="(.*?)">(.*?)<.*?post_count">(.*?)<.*?'
    number = None
    page_reg = 'topic-navigate-pages-top.*?of (.*?)<'

    i = 1
    while not number or i <= number:
        url = base_url + '?pg=%d' % i
        html, status = get_request_html_with_status(base_url, cookie)
        if not number:
            number = min(100, int(re.compile(page_reg).findall(html)[0]))

        print topic, number, url

        header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': base_url,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'upgrade-insecure-requests': '1',
            # 'accept-encoding': 'gzip, deflate, br',
            'cache-control': 'max-age=0',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
        }
        html, status = get_request_html_with_status(url, cookie, add_header=header)
        if status != 200:
            break
        threads = re.compile(base_reg).findall(html)
        one_row = None
        for thread in threads:
            try:
                title = thread[1]
                thread_url = 'https://www.mumsnet.com/Talk/' + thread[0]
                # thread_url = 'https://www.expat.com/forum/viewtopic.php?id=745872'
                try:
                    replies = int(thread[2])
                except:
                    replies = 0
                one_row = [base_url, topic, title, thread_url, replies]
                sheet1_data.append(one_row)

            except Exception as e:
                print 'ERR--', thread[0], e
        print one_row
        i += 1


def step_1():
    for url in urls:
        request_sheet1(url[0], url[1])
    write_excel('mumset.xls', sheet1_data)


reload(sys)
sys.setdefaultencoding('utf-8')
step_1()