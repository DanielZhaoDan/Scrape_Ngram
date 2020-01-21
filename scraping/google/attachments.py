# -*- coding: utf-8 -*-
from scraping.utils import get_attachments, post_request_html, write_excel
import re

cookie = '__utmz=231532751.1576219136.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); GA_XSRF_TOKEN=AO6Y7m8fBLbyYyE0i2Fe-jxrooQY4IOuFg:1579334364471; __utma=231532751.760866652.1575884403.1577851698.1579334507.9; __utmb=231532751.0.10.1579334507; __utmc=231532751; _ga=GA1.3-2.760866652.1575884403; _gid=GA1.3-2.2117924216.1579334366; OGPC=19015603-1:; OGP=-19015603:; SEARCH_SAMESITE=CgQI3Y4B; NID=196=PWwby9151W97ET892nzZvH2soqkDpRi-Xm56Az-76RzCtbVZDGmgno3-CSE5a_m96glYzvmyNTzp0HbB5gV_AcyOAYWKuXaKZX_9NHIY6t9cXH-F3QN-fQPAAgj-6K8f-Hr36__NAGK5Em7qJ7BiO8zoREfzj1ptaaqEMfpyFuEcJBH-ohSoMB1eghgfCsbsfvr3mEvu8l3SNIdLlMmmhQiibzF9zqUx2mURN-DhsmnVpTEsS0KKl8gyk948eWh7XdVkiEERTARy5JiNS4vgO6xhffXDNJ8DBMfcdVYh-5hN; SID=swc33X793ENWLhrhiGP_PPRTFqWWemNExIDv488udw4qo76O5yCYDaa73OBOlKc8B1nbGg.; __Secure-3PSID=swc33X793ENWLhrhiGP_PPRTFqWWemNExIDv488udw4qo76O8IULgIMyU5aXvjAcCk1S1w.; HSID=AIcvYAGoOt_Nx5wep; SSID=Am6qj81m9aDUn5zBr; APISID=d3z5uqrCuUVib7q1/AsShSIjMtN8lDTc-H; SAPISID=k8jlVE1Z_6h_XE2F/AeNNiahCz9G5ZglUw; __Secure-HSID=AIcvYAGoOt_Nx5wep; __Secure-SSID=Am6qj81m9aDUn5zBr; __Secure-APISID=d3z5uqrCuUVib7q1/AsShSIjMtN8lDTc-H; __Secure-3PAPISID=k8jlVE1Z_6h_XE2F/AeNNiahCz9G5ZglUw; _gid=GA1.3.2117924216.1579334366; S=analytics-realtime-frontend=8Wiibfmbsu9tKCj3NteLFHFDAvuutXgQ; 1P_JAR=2020-01-18-08; _ga_X6LMX9VR0Y=GS1.1.1579334370.11.1.1579334907.0; _ga=GA1.3.760866652.1575884403; SIDCC=AN0-TYsIi-tq417hmQnhLB_pmIfooK7U7nfH9kXBh6knR2vH-KcFHn5pE3CJOIsoMDsGGRWxWWrp'

sheet_p = [['Pages', 'Previous Page Path', 'Page Views', '%Page Views']]
sheet_n = [['Pages', 'Next Page Path', 'Page Views', '%Page Views']]

# a116178497w86333592p89585249

def prepare_url():
    return [
        '/ru/about/clears-expertise.html',
        '/ru/about/our-purpose.html',
        '/ru/articles-for-men.html',
        '/ru/articles-for-women.html',
        '/ru/faq.html',
        '/ru/home.html',
        '/ru/location-selector.html',
        '/ru/men.html',
        '/ru/products.html',
        '/ru/products/anti-grease.html',
        '/ru/products/needs/anti-grease.html',
        '/ru/products/needs/anti-itch.html',
        '/ru/products/needs/damage-repair.html',
        '/ru/products/needs/nourishment.html',
        '/ru/products/type/conditioner.html',
        '/ru/products/type/conditioner/clear-color-damaged-conditioner.html',
        '/ru/products/type/conditioner/clear-hairfall-defense-conditioner.html',
        '/ru/products/type/shampoo.html',
        '/ru/products/type/shampoo/clear-anti-hairfall-shampoo.html',
        '/ru/products/type/shampoo/clear-color-damaged-shampoo.html',
        '/ru/products/type/shampoo/clear-complete-care-shampoo.html',
        '/ru/products/type/shampoo/clear-ice-cool-menthol-shampoo.html',
        '/ru/products/type/shampoo/clear-intense-hydration-shampoo.html',
        '/ru/products/type/shampoo/clear-men-anti-hairfall-shampoo.html',
        '/ru/products/type/shampoo/clear-men-ice-fresh-shampoo.html',
        '/ru/products/type/shampoo/clear-men-phytotechnology-shampoo.html',
        '/ru/products/type/shampoo/clear-men-shower-fresh-shampoo.html',
        '/ru/products/type/shampoo/clear-oil-control-balance-shampoo.html',
        '/ru/products/type/shampoo/clear-phytotechnology-shampoo.html',
        '/ru/products/type/shampoo/clear-shampoo-and-conditioner-2in-1-activesport.html',
        '/ru/products/type/shampoo/clear-shampoo-and-conditioner-2in-1-deep-clense.html',
        '/ru/products/type/shampoo/clear-ultimate-control-2in1-shampoo.html',
        '/ru/products/type/shampoo/clear-volume-maxx-shampoo.html',
        '/ru/scalp-care.html',
        '/ru/scalp-care/5-keys-to-head-turning-hair.html',
        '/ru/scalp-care/5-steps-to-get-rid-of-dandruff.html',
        '/ru/scalp-care/dandruff-myths-busted.html',
        '/ru/scalp-care/end-itchy-scalp-for-good.html',
        '/ru/scalp-care/oily-scalp-causes-and-treatments.html',
        '/ru/scalp-care/prichiny-vypadeniya-volos.html',
        '/ru/scalp-care/should-men-and-women-use-the-same-shampoo.html',
        '/ru/scalp-care/soothe-your-itchy-scalp.html',
        '/ru/scalp-care/the-5-most-surprising-male-scalp-secrets.html',
        '/ru/scalp-care/the-dandruff-solution-for-every-scalp.html',
        '/ru/scalp-care/the-mens-guide-to-busting-dandruff-in-style.html',
        '/ru/scalp-care/what-causes-dandruff.html',
        '/ru/scalp-care/what-is-dandruff.html',
        '/ru/search.html?Locale=ru_ru&BrandName=clear&stags=unilever:clear/article/editorial-category/scalp-care/women&noesc=',
        '/ru/search.html?Locale=ru_ru&BrandName=clear&stags=unilever:clear/product/needs/itchy&noesc=',
        '/ru/secure/contactus.html',
        '/ru/women.html',
    ]


def get_data2():

    global sheet_p, sheet_n

    base_url = 'https://analytics.google.com/analytics/web/getPage?_u.date00=20190101&_u.date01=20191231&_r.tabId=navigationsummary&id=content-pages&ds=a116178497w86398311p89642028&cid=navigationsummary%2CreportHeader%2CtabControl%2CtimestampMessage&hl=en_GB&authuser=1&sstPremiumUser=true'
    body = {
        'token': 'AO6Y7m9McQ4Gz6y6AJRe81dnNzdZng8n4A:1579334503685',
    }

    urls = prepare_url()

    reg = 'rowCluster":(.*?)"clusteredRowLabel'
    detail_reg = '"displayKey":"(.*?)".*?dataValue":"(.*?)".*?dataValue":"(.*?)"'

    for url in urls:
        try:
            target_url = base_url + '&_r.drilldown=analytics.pagePath:' + url.replace('/', '%2f')
            print target_url
            html = post_request_html(target_url, cookie, data=body)
            raw = re.compile(reg).findall(html)

            if raw:
                datas = re.compile(detail_reg).findall(raw[0])
                for data in datas:
                    one_row = [url, data[0], data[1], data[2]]
                    print one_row
                    sheet_p.append(one_row)
                datas = re.compile(detail_reg).findall(raw[1])
                for data in datas:
                    one_row = [url, data[0], data[1], data[2]]
                    print one_row
                    sheet_n.append(one_row)
        except Exception as e:
            print 'err--', url, e

    write_excel('data/previous.xls', sheet_p)
    write_excel('data/next.xls', sheet_n)


def get_sheet3():
    urls = prepare_url()
    head = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'origin': 'https://analytics.google.com',
        'referer': 'https://analytics.google.com/analytics/app/?authuser=1',
        'x-client-data': 'CLG1yQEIh7bJAQimtskBCMG2yQEIqZ3KAQioo8oBCLGnygEI4qjKAQjxqcoBCMuuygEI97TKAQ==',
    }

    target_url = 'https://analytics.google.com/analytics/web/exportReport?hl=en_GB&authuser=1&sstPremiumUser=true&ef=XLSX'

    for url in urls[1:]:
        body = {
            '_u.date00': '20190901',
            '_u.date01': '20191201',
            'search_console-table.plotKeys': '[]',
            'search_console-table.rowStart': '0',
            'search_console-table.rowCount': '5000',
            '_r.drilldown': 'analytics.landingPagePath:' + url,
            'id': 'acquisition-sc-landingpages',
            'ds': 'a116178497w103157272p107273512',
            'exportUrl': 'https://analytics.google.com/analytics/web/?authuser=1#/report/acquisition-sc-landingpages/a116178497w103157272p107273512/_u.date00=20190901&_u.date01=20191201&search_console-table.plotKeys=%5B%5D&search_console-table.rowStart=0&search_console-table.rowCount=5000&_r.drilldown=analytics.landingPagePath:' + url.replace('/', '~2F'),
        }

        try:
            get_attachments(target_url, url.replace('/', '_') + '.xlsx', headers=head, data=body)
        except Exception as e:
            print 'err-', target_url, e


get_data2()