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

cookie = 'sid=ole8idn6qe51hboqse1ggd961ujae3s970uhc7ehjht5eocj5kb19lfpn3p533jisb7a7uh3b37hvpara60p0tj0p20t26pr2s0pid3; retnbb=87; _ga=GA1.2.1894909371.1590766710; _gid=GA1.2.90297511.1590766710; scarab.visitor=%227665BFC879844169%22; AMCVS_FB2F5FCF5C0816830A495E15%40AdobeOrg=1; _dy_csc_ses=t; _dy_c_exps=; s_ecid=MCMID%7C61762727923851601532786708455884256401; s_cc=true; _dycnst=dg; _dyid=1157425994867885709; _dyjsession=c88ec3f3048c92779268817fdb9b8238; _dycst=dk.m.c.ws.; _dy_geo=SG.AS.SG_.SG__Singapore; _dy_df_geo=Singapore..Singapore; CRTOABE=1; __zlcmid=yRjAdJ7ihWZnng; hl_p=c6a9f294-731c-4d4a-b570-fd849fbf6127; _dy_c_att_exps=; _gcl_au=1.1.327860326.1590767527; scarab.profile=%22659468%7C1590767527%22; googtrans=/de/en; googtrans=/de/en; _dyfs=1590769022062; bm_mi=02DDB281397FD3510A065EF9B415E830~seQC9kEIDO5sEuV4Kdi2wBbbNcgrD3lNObkqwnBowuJZypF2CJ26qt8Alevym9cbf9O1+4zxQdOk+bp+Qi4OnIiu1EcV6iatGhMa5dhxdqJO2jvMj1091NnTQSjEBQDPW9BbhrEraEEWe4tUhcV6pGt6K5FJnmBd+C4DoudDI+Sw4UpUDnLar2ubj/tioGOUm7tMD2XJBpMRQW0zejpZdGwdLhRBJMgko+PdF7TBkvxWrlLbEqnTuQW61cbhYhbpQ+Prnzzg1t57eCpVJQJalOW6U76Wdmw2ELMK5S016TnBDZTQV4z16j7MF6DZ9FifGjiTGvae/KO9T2M8PxsO/g==; AMCV_FB2F5FCF5C0816830A495E15%40AdobeOrg=-408604571%7CMCIDTS%7C18412%7CMCMID%7C61762727923851601532786708455884256401%7CMCAAMLH-1591436473%7C3%7CMCAAMB-1591436473%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1590838873s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; ak_bmsc=05F07CFDDC3317C81F0F820261787E861732E09DC31B0000342AD25E84030160~plc/NDDcMHljW5HcifAUvlKlrmnmbuGMGpeS2YB7lTtC9EoAhmW7IhmfVGO+MTMRc2bMOCewxNmEZGPH5JDGUmaZdjuVTklvUm6fFHrd3uoUQuEpMGKJwW9rlW85WF2P8esAhHCEBkl5FzEMaPAbfkY5x1RX5vHKKZEPTEh9YfcRUJ/J/lzSrrZxNzOgp40i67JzZ9mtFPtzaVaCM20uLmfLpBp3DWmxxezY8VE3gN5WyLkCI4WxyJWI4TCRtIUrah; dy_fs_page=www.notebooksbilliger.de%2Fnotebooks%2Fhp%2B250%2Bg7%2B8mh66es%2B631614; s_sq=%5B%5BB%5D%5D; _dy_ses_load_seq=54300%3A1590832165624; _dy_lu_ses=c88ec3f3048c92779268817fdb9b8238%3A1590832166092; _dy_toffset=-1; _dy_soct=472983.859546.1590766713*477263.869354.1590767527*240186.359704.1590832165*425680.745456.1590832165*470145.852771.1590832165*481273.878590.1590832165*485260.889199.1590832165*390233.660130.1590832166*284067.439703.1590832166; bm_sv=C97CC774D4A3D17A32E0CB16EACB7B0D~OGbxE/YDhNXk9bmY0/B/6xi2vgDbmTHfdoAaniIkbvxTORKhB5xow1N2szr3KCxAj5fU1QnO/2ygNxasvWIyzfK0TlJUKGloVW9sDt7KiITZvGwzcrZDTaNuEgF4Cg2dlVFa+pwwtiowOEtd3i4Ji3B9iWk3rzvEKPeSTVKiU+k=; scarab.mayAdd=%5B%7B%22i%22%3A%22659468%22%7D%2C%7B%22i%22%3A%22654478%22%7D%2C%7B%22i%22%3A%22473691%22%7D%2C%7B%22i%22%3A%22423908%22%7D%2C%7B%22i%22%3A%22654240%22%7D%2C%7B%22i%22%3A%22631614%22%7D%2C%7B%22i%22%3A%22647059%22%7D%2C%7B%22i%22%3A%22659633%22%7D%5D'
G_ID = 1
stop = False

base_url = 'https://www.notebooksbilliger.de/extensions/apii/filter.php?filters=on&listing=on&advisor=&box_2256_1_min=&box_2256_1_max=&box_2256_1_slid=&box_433_1_min=&box_433_1_max=&box_433_1_slid=&box_480_1_min=&box_480_1_max=&box_480_1_slid=&box_479_1_min=&box_479_1_max=&box_479_1_slid=&box_1791_1_min=&box_1791_1_max=&box_1791_1_slid=&box_9126_1_min=&box_9126_1_max=&box_9126_1_slid=&box_2441_1=&action=applyFilters&category_id=1&perPage=50&sort=popularity&order=desc&availability=sofort&eqsqid=&page='

prefix = ''


def request_sheet1(page_no):

    global G_ID, driver

    url = base_url + str(page_no)
    print url
    html = utils.get_request_html(url, cookie)


    reg = 'id="mouseover_(.*?)".*?href="(.*?)".*?>(.*?)<.*?src="(.*?)".*?star-rating.*?<span.*?>(.*?)<.*?star-sum">\((.*?)\).*?product-price__regular.*?data-price="(.*?)"'
    data_list = re.compile(reg).findall(html)

    for i in range(len(data_list)):
        id = data_list[i][0]
        item_url = data_list[i][1]
        title = data_list[i][2].strip()
        img_url = "https:" + data_list[i][3]

        no_review = data_list[i][5]

        if '0' in no_review:
            rating = "0"
        else:
            rating = data_list[i][4].split(" ")[1]

        is_sponsored = False
        is_new = False

        price = data_list[i][6]

        # details = request_sheet2(item_url)

        one_row = [prefix + id, item_url, img_url, is_sponsored, is_new, title, rating, no_review, G_ID, price]

        sheet1.append(one_row)
        G_ID += 1
        print one_row


def request_sheet2(sheet1_data):
    global sheet2, stop
    url = sheet1_data[1]
    html = utils.get_request_html(url, cookie)

    if 'if you are not a bot' in html:
        stop = True
        return

    details = ['N/A' for i in range(11)]
    category_dict = {}

    reg = 'product_detail_img.*?src="(.*?)size.*?article_number.*?>(.*?)<'

    if 'nbb-sprite-pds nbb-sprite-pds-title_specification' in html:
        reg += '.*?nbb-sprite-pds nbb-sprite-pds-title_specification(.*?)</table'

    raw_data = re.compile(reg).findall(html)

    if not raw_data:
        return sheet1_data + details

    sheet1_data[2] = "https:" + raw_data[0][0] + 'size=195'

    # brand
    details[2] = sheet1_data[5].split(' ')[0]

    if len(raw_data[0]) <= 2:
        return sheet1_data + details

    reg = 'group_header">(.*?)</div(.*?)group_header_wrapper produktDetails_eigenschaft1'
    td_reg = '<tr .*?>.*?<td.*?>(.*?)</td.*?<td.*?>(.*?)</'

    data_list = re.compile(reg).findall(raw_data[0][2])

    for data in data_list:
        if data[0] == 'Prozessor':
            info = re.compile(td_reg).findall(data[1])
            details[9] = utils.remove_html_tag(info[0][1])
            if len(info) >= 2:
                details[9] = details[9] + ' ' + utils.remove_html_tag(info[1][1])
        elif data[0] == 'Grafik':
            info = re.compile(td_reg).findall(data[1])
            details[8] = utils.remove_html_tag(info[0][1])
            if len(info) >= 2:
                details[8] = details[8] + ' ' + utils.remove_html_tag(info[1][1])
        elif data[0] == 'Arbeitsspeicher': #RAM
            info = re.compile(td_reg).findall(data[1])
            details[7] = utils.remove_html_tag(info[0][1])
        elif data[0] == 'Festplatte': #Hard disk
            info = re.compile(td_reg).findall(data[1])
            for inf in info:
                if inf[0] == 'Typ':
                    details[5] = utils.remove_html_tag(inf[1])
                elif '(Gesamt)' in inf[0]:
                    details[6] = utils.remove_html_tag(inf[1])
        elif data[0] == 'Ausstattung': #color
            info = re.compile(td_reg).findall(data[1])
            for inf in info:
                if inf[0] == 'Farbe':
                    details[2] = utils.remove_html_tag(inf[1])

    return sheet1_data + details


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
            if stop:
                break
            one_row = request_sheet2([table.row(i)[j].value for j in range(table.ncols)])
            print one_row
            sheet2.append(one_row)
        except Exception as e:
            print 'read excel exception--', e, url


# print request_sheet2(['', 'https://www.notebooksbilliger.de/notebooks/medion+akoya+e14301+659633', '', '', '', ''])
# for i in range(1, 24):
#     request_sheet1(i)
# utils.write_excel("sheet1.xls", sheet1)
read_excel('data/sheet1.xls')
utils.write_excel("sheet2.xls", sheet2, encoding='ISO 8859-1')