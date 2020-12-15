from scraping import utils
import re
import urllib
import xlrd
import time
from selenium import webdriver

sheet1 = [['UID', 'index', 'Logo', 'title', 'url', 'img_url', 'Rank']]
sheet2_title = ['Product Name', 'Brand', 'Color', 'Touch Screen', 'Screen Size', 'Storage Type', 'Total Storage Capacity', 'System Memory (RAM)', 'Graphics', 'Processor Model', 'Battery Life']
sheet2 = []
sheet2.append(sheet2_title)

cookie = 'tfs_upg=true; UID=2a29f8e6-3fc2-4f8e-ae00-d034d7de2e93; bby_rdp=l; CTT=fb7c03a26c68521dd307480b2be25751; SID=880bfb12-3d5a-4df2-8707-cfe80e0cfb02; AMCVS_F6301253512D2BDB0A490D45%40AdobeOrg=1; vt=0fc13314-815e-11ea-9c7b-0af75617aea0; s_ecid=MCMID%7C60939390380952398832848776037620555139; s_cc=true; AMCV_F6301253512D2BDB0A490D45%40AdobeOrg=1585540135%7CMCMID%7C60939390380952398832848776037620555139%7CMCAAMLH-1587809958%7C3%7CMCAAMB-1587809958%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1587212358s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1181920462%7CvVersion%7C4.4.0; aam_uuid=67510623380186900253362623901423547553; 52245=; _gcl_au=1.1.293315184.1587205159; intl_splash=false; ltc=%20; oid=429075881; optimizelyEndUserId=oeu1587205225104r0.4601884882949532; COM_TEST_FIX=2020-04-18T10%3A20%3A25.829Z; bby_basket_lb=p-basket-e; locDestZip=96939; locStoreId=852; pst2=852; sc-location-v2=%7B%22meta%22%3A%7B%22CreatedAt%22%3A%222020-04-18T10%3A21%3A00.704Z%22%2C%22ModifiedAt%22%3A%222020-04-18T10%3A21%3A02.572Z%22%2C%22ExpiresAt%22%3A%222021-04-18T10%3A21%3A02.572Z%22%7D%2C%22value%22%3A%22%7B%5C%22physical%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2296939%5C%22%2C%5C%22source%5C%22%3A%5C%22A%5C%22%2C%5C%22captureTime%5C%22%3A%5C%222020-04-18T10%3A21%3A00.703Z%5C%22%7D%2C%5C%22store%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2296701%5C%22%2C%5C%22storeId%5C%22%3A852%2C%5C%22storeHydratedCaptureTime%5C%22%3A%5C%222020-04-18T10%3A21%3A02.571Z%5C%22%7D%2C%5C%22destination%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2296939%5C%22%7D%7D%22%7D; CTE13=T; lastSearchTerm=amd%20laptop; listFacets=undefined; bby_cbc_lb=p-browse-e; bby_prc_lb=p-prc-w; CRTOABE=1; bby_suggest_lb=p-suggest-e; gvpHeaderFooterTransition=headerFooterGvp; c6db37d7c8add47f1af93cf219c2c682=91f0d58b1dc84232db63e5dc3a3fbb84; basketTimestamp=1587206215399; c2=Search%20Results; CTE14=T; bm_sz=BC0C742EEF9D7CDC6BD5612AC1E32C4F~YAAQWon+pcUgJ3hxAQAAU7jdjAeaUcWO14FMGzl0fMzouAMLwrFwKDQp1TuPY187s54Af6WFFrLOZKuQRLsng9ZKT0dFls6nzdPCNAxy+Wo3Hka+l7Wlae+auJrFhx84ceDsMulIwPOth+MX7Ty6xUpI12E8iCghUMRt4YlDIiyAAC+4FHyZG35pauRij4cHXw==; _abck=A0E7306666E54EE3CDF4E920EDB2BADE~-1~YAAQWon+pcYgJ3hxAQAAU7jdjAPalkdmLvhmj99fpz2rdX/lsRJBI/l6XuzqGhzYRdbvkAE316oXBLQTDDOtVV+noI5vT9ppNk296v8ZK5Qz9ypni14f3agCwdPV1gCe39nOkk86WTofQdkccnUXeN/yBiXLxYoV8G3GqIydqjE1obTKNqJ/D0U1hHW00fSPkScAzqrcrdyyF8siBCCv8EA40vJXGedzgrfJzZErk116C8pmnp8OlfDw0Gdakr2FbiHbuyfFHvQE+SG8w/bICReXTwC4pOKsVS4f2GmIN/+4dA==~-1~-1~-1; s_sq=%5B%5BB%5D%5D'
G_ID = 1

base_url = 'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&intl=nosplash&keys=keys&ks=960&list=n&sc=Global&sp=-bestsellingsort%20skuidsaas&st=laptop&type=page&usc=All%20Categories&cp='


driver = webdriver.Chrome('./chromedriver')
prefix = ''


def request_sheet1(page_no):

    global G_ID, driver

    url = base_url + str(page_no)
    print url
    html = open_browser_scroll(url)

    reg = 'class="list-item lv" data-sku-id="(.*?)".*?class="image-link" href="(.*?)".*?src="(.*?)".*?right-column(.*?)class="sku-header">(.*?)</h4.*?c-ratings-reviews-v2.*?sr-only">(.*?)<.*?Your price for this item.*?>(.*?)<'
    data_list = re.compile(reg).findall(html)

    for i in range(len(data_list)):
        id = data_list[i][0]
        item_url = 'https://www.bestbuy.com' + data_list[i][1]
        img_url = data_list[i][2]

        is_sponsored = 'is-sponsored' in data_list[i][3]
        is_new = 'New!' in data_list[i][4]
        title = utils.remove_html_tag(data_list[i][4])

        rating, no_review = get_review(data_list[i][5])
        price = data_list[i][6]

        # details = request_sheet2(url)

        one_row = [prefix + id, item_url, img_url, is_sponsored, is_new, title, rating, no_review, G_ID, price]

        sheet1.append(one_row)
        G_ID += 1
        print one_row


def get_review(ori):
    if 'Not yet reviewed' in ori:
        return 'N/A', 0
    data = str(ori).split(" ")
    return data[1], data[6]


def open_browser_scroll(url, sleep_time=1):
    try:
        driver.get(url)
        html_source = driver.page_source
        data = html_source.encode('utf-8').replace('\t', '').replace('\r', '').replace('\n', '')
    except Exception as e:
        print "open page error: ", url, e
    return data


def ger_url(ori):
    return 'https://www.amazon.in' + urllib.unquote(ori.split('url=')[-1])


def request_sheet2(url):
    global sheet2
    html = open_browser_scroll(url)

    details = ['N/A' for i in range(11)]
    category_dict = {}

    reg = 'class="row-title">(.*?)</div.*?class="row-value.*?>(.*?)<'

    data_list = re.compile(reg).findall(html)

    for data in data_list:
        category_dict[utils.remove_html_tag(data[0]).strip()] = utils.remove_html_tag(data[1])

    for i in range(len(sheet2_title)):
        details[i] = category_dict.get(sheet2_title[i], category_dict.get(sheet2_title[i]+'Info', 'N/A'))
    return details


def get_spec(ori):

    reg = 'class="a-list-item">(.*?)<'

    data_list = re.compile(reg).findall(ori)
    return data_list[0], ';'.join(data_list[1:])


def read_excel(filename, start=1):
    global sheet2
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        url = table.row(i)[1].value
        try:
            details = request_sheet2(url)
            one_row = [table.row(i)[j].value for j in range(table.ncols)] + details
            print one_row
            sheet2.append(one_row)
        except Exception as e:
            print 'read excel exception--', e, url


# for i in range(1, 39):
#     request_sheet1(i)
# utils.write_excel("sheet1.xls", sheet1)
read_excel('data/sheet1.xls')
utils.write_excel("sheet2.xls", sheet2)
driver.close()