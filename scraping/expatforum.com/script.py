import re
import sys
from datetime import datetime
import HTMLParser
import xlrd
import json
from scraping.utils import post_request_json, get_request_html_with_status, write_html, write_excel, remove_html_tag, post_request_html

saved_hotel = set()
R_ID = 1
sheet1_data = [['Site', 'Topic', 'Title', 'thread url', 'Replies', 'Views', 'Username', 'Status', 'Date Posted', 'Content', 'No, of reactions']]

cookie = '__cfduid=d04e54399eb7c62ffb23fc3805251077d1606889330; __cf_bm=2542b8cd72e9abe4f39daf61418403b9afc18ba4-1606889330-1800-AQAGi07Op8+0Kz6S9HEe4WFeG0jkGcRO72kXX/ODRsi53JhXfhgs2pp/AW1XDyjl4+nXI7mYZHvsElv0MT7O/h4=; cf_chl_1=f3a27ba68b02324; cf_chl_prog=a19; cf_clearance=44ad96b54a33e46e94d618e2eadd4496fc4082ea-1606889348-0-250; xf_csrf=Pz4tRxjuzZg-3MNc; xf_last_time_visited=1606889349089; lux_uid=160688934918799300; _ga=GA1.2.1689214405.1606889349; _gid=GA1.2.1596749565.1606889349; _gat_threadloomTracker=1; _gat_UA-27401719-47=1'

url = 'https://www.expatforum.com/forums/britain-expat-forum-for-expats-living-in-the-uk.8/?last_days=365&__cf_chl_captcha_tk__=e728a4e8dfa8f4ee471e3e1cfb7e6bfdca5094e2-1606889330-0-AXEk5yhvp3xHgqW-BozEa3ksQVB9zhOKZtMcvoOX5c2WNK7p8XaCJE-zvd5Pulxs_OL0BCgj3CfNiyQ-VFMfZQ-gUHfuKW4uJ7ty4_87TCb-t7ikRfOW1vfcuOYYkEe76DYTBi-8DnmwAPt0stqg5tslQIArt6im-dSNdbDIXthX9ia0zl44sZL552za1NC0iJPsGKLtkaMKIEqfng1ZAJPszzpisrinZ5-cqsHj21-nGmaqZiAcq1EjAVQvL_zkqwsw6h4ieLcPCecjdGnGnDnxk21SOcniQ-3It6t9bJqcxAZdsODejZ-Tnj8QYQKg24pofY5HMk4Rv3PqMDIr5D6R7WXiobAi45dQaI71U_FEDXDI9rIZuxaJY9F4lFJWJ3vUMDy6nFnvhiSGp10V-jnf4nF6Hrm8rMINjiTzOKkIlVOHc_JH7gVL7tjrckcUg6p7kGtf5WyNk7L7qwpcxqGEFbQvDwlR0Q2nXHmMDAZm8cOVPhF1LYKw-nrFfbI7Y0vPhBNoUrPLoBbS-KqFOJzGyzjPjFoKKjrRzc-dJIowNRyMiWVfnnFkTKLLR5cy4GHNY8Z0b2jMp2KcQX20kA3BTcXuyTSx5DylXx1SyV7AUJXkDOUCdcMcb1RhbhkOPCRCmTRYis0RPrrzH0ur22yJJBx5p_wI_lj8SUnxwHyuGnnpwpefNraG9dJxf8Fppg'

uid_level_dict = {}


def request_sheet1(base_url, topic, site):
    global sheet1_data

    base_reg = 'structItem-title.*?href="(.*?)".*?thread-item-title.*?>(.*?)<.*?thread-item-reply-count-icon.*?i>(.*?)<.*?-view-count-icon.*?i>(.*?)<'
    comment_reg = 'message-username.*?class="username.*?>(.*?)<.*?message-user-title.*?>(.*?)<.*?u-concealed.*?datetime="(.*?)".*?bbWrapper">(.*?)</article>.*?post-reaction-bar(.*?)message-actionBar'

    for i in range(26, 44):
        if i > 1:
            url = base_url.replace('?last_days=365', 'page-%d?last_days=365' % i)
            start_index = 0
        else:
            url = base_url
            start_index = 7
        # url = 'https://www.expatforum.com/forums/britain-expat-forum-for-expats-living-in-the-uk.8/?last_days=365'
        print url
        header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://www.expatforum.com/forums/britain-expat-forum-for-expats-living-in-the-uk.8/page-2',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'upgrade-insecure-requests': '1',
            # 'accept-encoding': 'gzip, deflate, br',
            'cache-control': 'max-age=0',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
            'if-modified-since': 'Tue, 01 Dec 2020 05:34:39 GMT',
        }
        html, status = get_request_html_with_status(url, cookie, add_header=header)
        if status != 200:
            break
        threads = re.compile(base_reg).findall(html)

        for thread in threads[start_index:]:
            try:
                title = thread[1].replace('&amp;', '')
                thread_url = 'https://www.expatforum.com' + thread[0]
                # thread_url = 'https://www.expat.com/forum/viewtopic.php?id=745872'
                try:
                    replies = int(thread[2].replace('K', '000').replace('M', '000000'))
                except:
                    replies = 'N/A'
                views = thread[3].replace('K', '000').replace('M', '000000')

                page_no = 1 if replies <= 20 else (replies / 20 + 1)
                page_no = min(20, page_no)
                j = 1
                while j <= page_no:
                    if j > 1:
                        page_url = thread_url + 'page-' + str(j)
                    else:
                        page_url = thread_url
                    # page_url = 'https://www.expatforum.com/threads/post-your-uk-visa-timeline-here-timelines-only-no-questions-or-comments.30135/page-13'
                    print page_url, page_no, j

                    try:
                        html, status = get_request_html_with_status(page_url, cookie)
                        if status != 200:
                            break

                        comments = re.compile(comment_reg).findall(html)

                        one_row = None
                        for comment in comments:
                            status = comment[1]
                            username = comment[0]
                            time = comment[2].split('T')[0]
                            content = remove_html_tag(comment[3]).strip()
                            no_reactions = 0 if 'post-reaction-bar-list' not in comment[4] else get_reactions(comment[4])

                            one_row = [site, topic, title, thread_url, replies, views, username, status, time, content, no_reactions]

                            sheet1_data.append(one_row)
                        print one_row
                        j+=1
                    except Exception as e:
                        print 'ERR--', page_url, e
            except Exception as e:
                print 'ERR--', thread[0], e


def get_reactions(ori):
    count = ori.count('<bdi>')

    if 'others' in ori:
        reg = 'and(.*?)others'
        count += int(re.compile(reg).findall(ori)[0].strip())
    return count


def step_1():
    request_sheet1(url, '', 'expatforum.com')
    write_excel('expat.xls', sheet1_data)


reload(sys)
sys.setdefaultencoding('utf-8')
step_1()