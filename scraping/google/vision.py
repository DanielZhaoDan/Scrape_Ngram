import os
from scraping.utils import *
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"

from google.cloud import vision
client = vision.ImageAnnotatorClient()

urk_dict = {}
alldata = []


def detect_text_uri(uri, targets):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """

    if uri in urk_dict:
        return urk_dict[uri]

    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        for target in targets:
            if target in text.description.strip().lower():
                urk_dict[uri] = True
                return True

    urk_dict[uri] = False
    return False


def read_excel(filename, start=1):
    global alldata
    alldata = []
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    length = table.ncols
    for i in range(start, table.nrows):
        ori_value = [table.row(i)[j].value for j in range(0, table.ncols)]
        g_id = table.row(i)[0].value
        img_url = table.row(i)[length-1].value

        try:
            exist = detect_text_uri(img_url, ['intel'])
            ori_value[2] = 1 if exist else 0
            print g_id, exist
        except Exception as e:
            print 'read excel exception--', e, g_id
        alldata.append(ori_value)


# read_excel('data/asheet1.xls')
# write_excel('ares1.xls', alldata)
#
# read_excel('data/asheet2.xls')
# write_excel('ares2.xls', alldata)
#
# read_excel('data/psheet1.xls')
# write_excel('pres1.xls', alldata)

read_excel('data/psheet2.xls')
write_excel('pres2.xls', alldata)