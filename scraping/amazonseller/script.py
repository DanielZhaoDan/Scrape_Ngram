# -*- coding: utf-8 -*-
import re
import requests
import xlwt, xlrd
import urllib2
from datetime import datetime
import HTMLParser
import json
import os, sys

best_seller_item_list = [
    ('BSD_%d', 'Desktop', 'All-in-one', 2,
     'https://www.amazon.com/Best-Sellers-Computers-Accessories-All-One/zgbs/pc/13896603011/ref=zg_bs_nav_pc_2_565098'),
    ('BSD_%d', 'Desktop', 'Minis', 2,
     'https://www.amazon.com/Best-Sellers-Computers-Accessories-Mini/zgbs/pc/13896591011/ref=zg_bs_nav_pc_3_13896603011'),
    ('BSD_%d', 'Desktop', 'Towers', 2,
     'https://www.amazon.com/Best-Sellers-Computers-Accessories-Tower/zgbs/pc/13896597011/ref=zg_bs_nav_pc_3_13896591011'),
    ('BSL_%d', 'Laptop', '2 in 1', 2,
     'https://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop/zgbs/pc/13896609011/ref=zg_bs_nav_pc_2_565108'),
    ('BSL_%d', 'Laptop', 'traditional', 2,
     'https://www.amazon.com/Best-Sellers-Computers-Accessories-Traditional-Laptop/zgbs/pc/13896615011/ref=zg_bs_nav_pc_3_13896609011'),
    ('BST_%d', 'Tablets', 'Tablets', 2,
     'https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Tablets/zgbs/pc/1232597011/ref=zg_bs_nav_pc_1_pc'),
]

wish_item_list = [
    ('WLD_%d', 'Desktop', 'All-in-one', 2,
     'https://www.amazon.com/gp/most-wished-for/electronics/13896603011/ref=zg_mw_nav_e_4_565098'),
    ('WLD_%d', 'Desktop', 'Minis', 2,
     'https://www.amazon.com/gp/most-wished-for/electronics/13896591011/ref=zg_mw_nav_e_5_13896603011'),
    ('WLD_%d', 'Desktop', 'Towers', 2,
     'https://www.amazon.com/gp/most-wished-for/electronics/13896597011/ref=zg_mw_nav_e_5_13896591011'),
    ('WLL_%d', 'Laptop', '2 in 1', 2,
     'https://www.amazon.com/gp/most-wished-for/electronics/13896609011/ref=zg_mw_nav_e_4_565108'),
    ('WLL_%d', 'Laptop', 'traditional', 2,
     'https://www.amazon.com/gp/most-wished-for/electronics/13896615011/ref=zg_mw_nav_e_5_13896609011'),
    ('WLT_%d', 'Tablets', 'Tablets', 2,
     'https://www.amazon.com/gp/most-wished-for/electronics/1232597011/ref=zg_mw_nav_e_3_13896617011'),
]

cookie = 'session-id=137-4159431-1628353; session-id-time=2082787201l; ubid-main=130-1305884-1691337; x-wl-uid=1yFGd+4uU+sLw79h9msoSltTflYZ16jVRPgIv7af4+p/Le8risJHzrtM6x3PoQR4IxztKr/Z7HGM=; aws-priv=eyJ2IjoxLCJldSI6MCwic3QiOjB9; aws-target-static-id=1546683908048-583417; aws-target-data=%7B%22support%22%3A%221%22%7D; s_fid=16D9F2FEB6222859-35924A1B801AADBD; s_vn=1578219908429%26vn%3D1; regStatus=pre-register; c_m=undefinedwww.google.comSearch%20Engine; s_cc=true; aws-target-visitor-id=1546683908051-919584.22_31; s_dslv=1546684110083; sp-cdn="L5Z9:SG"; csm-hit=82EH9D6RFS5KREWDZD40+s-TZVDYZ8ERXHZQWYDFSB5|1564371035777; a-ogbcbff=1; session-token="bT1ohlaBP62DcY59pQMYWj6nd98H3A1QV9yY1TMExLVXqXrDO8+batym+RE6lFSKZbQm4EWAEAwbwV2vcMf+aSUi2YanYi4t9qSfR8MLr9q2tkQaa/0zuDkLIEfkDRf6Qtwgjn6d6XUMb4LIb4jLVFGNuBOacSAbjCwFXCvtoaxEC/qA2MUA6aPJD/W+flUEezmdx3Nvt4Ac4eZ7gti05/id/A66Lbh1upj5ZJoWFoo="; x-main="7TEv7R?H5HsjvgPRBI2GrXLWXXPKpidL0VPg6ohi0IXh1hdpP3zE8PslbPcfrgsT"; at-main=Atza|IwEBIB0ZSKPgSHYzKJu3r4dRu4p0sMdl-BhPIz6AGPCO7ybMbCZ5h9EckrSPTp_YQu4KIMuRsOParWdt6-KNUmlgSWi9qmXYfSzsW2nLGCN1rfQ-0N2F22RH53xiz-2U7uSVW4LKSw1yQxVp4kzX3JvC2viZZXq5Ceh3K-SOM_-eU1h53ifatgEFWOfKAp6AbyccHmyJOqFK5KOQOKR128IQY5uwPf5EG7d6SKV9GHyltqaM_je86JjjoWhcnKWaPTb6mdxA6OOubFpNpeZKtQZo86rpHh6W8iHZbw-oU7bd7dy98THsKRP-V9rU77wtRP614uXxtQyroV9gu0QgvBNR8hrSfniLQhGo2R4hOIOrRKuEgo5NC_-TTbhX-h-cHVcJuY5BySSx4QVLx3yyHoO3rXdH; sess-at-main="sYVPVlxbhAJxwu8J35CQqATQZNo4wEaA17Ocbb+KDD8="; sst-main=Sst1|PQHXA4_DQpysTs7VZEu75Ma4C2P7edAaOMOR1x2i6TUHK9iAWmyqWIP1k06UmBzxe20pjdJxDBeTbK9TgHNZbeYEwusgbofUjvdkPR-ZPtg0h6CAnIrzGy00CcpFgmyEAQNg-geSjOLc2R5iUu1HJvT-I74QSnNbeFbSVgQJeZgvui9BP_RnhirVfEsgURfT8WnEbv0ZSh4rnOFuUfXLzxtkktg0_YxSQ43lxDelT4FhOadHkmKBfKT9CJarqnvx4a1RXufph_owHesHn1BEsmEtq3MYh2gXntyOOAbpYpNQee1Ozn9myA-aTYrNJ_B6H131q2E4rEmZiS--3VggEwf1YQ; lc-main=en_US'

G_ID = 1
sheet_seller = [
    ['ID', 'category', 'sub-category', 'rank', 'url', 'title', 'avg rating', 'No. of rating', 'price', 'header',
     'details']]
sheet_wish = [
    ['ID', 'category', 'sub-category', 'rank', 'url', 'title', 'avg rating', 'No. of rating', 'price', 'header',
     'details']]


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print("write over")


def write_excel(filename, alldata, flag=None):
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
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
    print(filename + "===========over============")


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
        'accept': '*/*',
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    res = res_data.content.replace('\n', '').replace('\t', '')
    return res


def request_list(param, sheet):
    global G_ID
    prefix, main_type, sub_type, num, base_url = param
    reg = 'aok-inline-block zg-item.*?href="(.*?)".*?alt="(.*?)"(.*?)</li'
    star_reg = 'a-icon-star.*?span.*?>(.*?) '
    price_reg = 'a-size-base.*?span.*?\$(.*?)<'

    rank = 1
    for i in range(1, num + 1):
        url = base_url + '?pg=%d' % i
        try:
            html = get_request(url)
            item_list = re.compile(reg).findall(html)

            for item in item_list:
                url = 'https://www.amazon.com' + item[0]
                title = item[1]
                star = 'N/A'
                if 'a-icon-star' in item[2]:
                    star = re.compile(star_reg).findall(item[2])[0]

                price = 'N/A'
                if 'a-size-base' in item[2]:
                    price = re.compile(price_reg).findall(item[2])[0]

                review_nums, detail_list = request_detail(url)
                for detail in detail_list:
                    try:
                        one_row = [prefix % G_ID, main_type, sub_type, rank, url, title, star, review_nums, price,
                                   remove_html_tag(detail[0]), remove_html_tag(detail[1])]
                        sheet.append(one_row)
                    except Exception as e:
                        print url, e
                print url, review_nums, len(detail_list)
                G_ID += 1
                rank += 1
        except Exception as e:
            print url, e


def request_detail(url):
    num_reg = 'acrCustomerReviewText.*?>(.*?) '
    html = get_request(url).replace('\n', '')
    review_num = 'N/A'
    if 'acrCustomerReviewText' in html:
        review_num = re.compile(num_reg).findall(html)[0]

    detail_table_reg = 'productDetails_techSpec_section_1(.*?)</table'
    detail_table_reg_2 = 'productDetails_techSpec_section_2(.*?)</table'
    detail_table_reg_3 = 'tech-specs-table-left(.*?)</table'
    detail_table_reg_4 = 'tech-specs-table-right(.*?)</table'
    reg = 'th.*?>(.*?)<.*?td.*?>(.*?)<'
    reg_2 = 'td.*?>(.*?)</td.*?<td.*?>(.*?)</td'

    detail_list = [[]]

    if 'productDetails_techSpec_section_1' in html:
        detail_table = re.compile(detail_table_reg).findall(html)[0]
        detail_list += re.compile(reg).findall(detail_table)
    if 'productDetails_techSpec_section_2' in html:
        detail_table = re.compile(detail_table_reg_2).findall(html)[0]
        detail_list += re.compile(reg).findall(detail_table)

    if 'tech-specs-table-left' in html:
        detail_table = re.compile(detail_table_reg_3).findall(html)[0]
        detail_list += re.compile(reg_2).findall(detail_table)
    if 'tech-specs-table-right' in html:
        detail_table = re.compile(detail_table_reg_4).findall(html)[0]
        detail_list += re.compile(reg_2).findall(detail_table)
    return review_num, [['N/A', 'N/A']] if len(detail_list) == 1 else detail_list[1:]


def best_seller():
    global G_ID, sheet_seller
    G_ID = 1
    for item in best_seller_item_list[0:3]:
        request_list(item, sheet_seller)
    G_ID = 1
    for item in best_seller_item_list[3:5]:
        request_list(item, sheet_seller)
    G_ID = 1
    for item in best_seller_item_list[5:6]:
        request_list(item, sheet_seller)

    write_excel('data/best_seller.xls', sheet_seller)


def wish_list():
    global G_ID, sheet_wish
    G_ID = 1
    for item in wish_item_list[0:3]:
        request_list(item, sheet_wish)
    G_ID = 1
    for item in wish_item_list[3:5]:
        request_list(item, sheet_wish)
    G_ID = 1
    for item in wish_item_list[5:6]:
        request_list(item, sheet_wish)

    write_excel('data/wish_list.xls', sheet_wish)


def redo_scraping(filename):
    data = xlrd.open_workbook(filename, encoding_override="utf-8")
    table = data.sheets()[0]
    new_sheet = [[]]

    for i in range(1, table.nrows):
        row = table.row(i)
        try:
            url = row[4].value
            product = row[9].value
            if 'N/A' == product:
                no_review, details = request_detail(url)
                for detail in details:
                    try:
                        one_row = [row[j].value for j in range(7)] + [no_review, row[8].value, remove_html_tag(detail[0]), remove_html_tag(detail[1])]
                        new_sheet.append(one_row)
                    except Exception as e:
                        print i, url, e
                print i, url, no_review, len(details)
            else:
                one_row = [row[j].value for j in range(table.ncols)]
                new_sheet.append(one_row)
        except Exception as e:
            print(i, e)
    write_excel("data/new_sheet.xls", new_sheet)


# best_seller()
# wish_list()
redo_scraping('data/wish_list.xls')
