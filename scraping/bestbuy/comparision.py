import xlrd
import difflib
from scraping.utils import write_excel
from io import BytesIO
import requests
from scraping.utils import get_request_html

aml_dict = {}
intel_dict = {}
done = set()

cookie = ''

sheet3 = [[]]

from PIL import Image
from numpy import average, dot, linalg


def get_thum(image, size=(64, 64), greyscale=False):
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        image = image.convert('L')
    return image


def image_similarity_vectors_via_numpy(image1, image2):
    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    res = dot(a / a_norm, b / b_norm)
    return res


def read_excel(filename, start=1, sheet_index=0):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[sheet_index]
    for i in range(start, table.nrows):
        gid = table.row(i)[2].value
        if sheet_index == 5 and '618980' not in str(gid):
            continue
        try:
            if i % 100 == 0:
                print 'processing-', str(sheet_index), '-' , str(i)
            img = table.row(i)[4].value
            if 'http' not in img:
                img = 'https://www.bestbuy.com/' + img
            desp = table.row(i)[5].value
            if sheet_index % 2 == 0:
                if gid in aml_dict:
                    print 'duplicated--', gid
                aml_dict[gid] = (process_img(img), desp)
            else:
                if gid in intel_dict:
                    print 'duplicated--', gid
                intel_dict[gid] = (process_img(img), desp)
        except Exception as e:
            print 'read excel exception--', e, gid


def read_existed(filename, start=1, sheet_index=0):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[sheet_index]
    for i in range(start, table.nrows):
        aml = table.row(i)[0].value
        intel = table.row(i)[1].value
        done.add(str(aml) + '_' + str(intel))
    print 'Done---', len(done)


def process_img(url):
    url += '?size=195'
    image = Image.open(BytesIO(get_request_html(url, cookie=cookie, pure=True)))
    return get_thum(image)


def load_data():
    global sheet
    read_excel('data/Laptop_Source_Data_V6.xlsx', sheet_index=5)
    read_excel('data/Laptop_Source_Data_V6.xlsx', sheet_index=6)

    print 'start comparing', len(aml_dict), len(intel_dict)

    i = 0

    for aml, aml_value in aml_dict.items():
        for intel, intel_value in intel_dict.items():
            if str(aml) + '_' + str(intel) in done:
                continue
            try:
                one_row = [aml, intel,
                           image_similarity_vectors_via_numpy(aml_value[0], intel_value[0]),
                           difflib.SequenceMatcher(None, aml_value[1], intel_value[1]).quick_ratio()]
                sheet3.append(one_row)
                if i % 100 == 0:
                    print i
                i += 1
            except Exception as e:
                print aml, intel, e

load_data()
write_excel('sheet3.xls', sheet3)
