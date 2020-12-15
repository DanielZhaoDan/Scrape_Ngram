# -*- coding: utf-8 -*-
import requests
import re
from selenium import webdriver
import time

cookie = ''
baidu_keywords = [u'维生素', u'益生菌', u'多种维生素', u'维生素和矿物质', u'维生素D', u'补充剂', u'草药补充剂', u'膳食补充剂', u'多种维生素的功效', u'服用多种维生素', u'不要服用多种维生素', u'优于多种维生素', u'天然补品', u'有机食品', u'功能保健食品', u'欧米加3', u'无用的维生素', u'植物营养素', u'糖尿病/糖尿病补充剂', u'胶质维生素', u'维塔糖蜜',]
tw_keywords = [u'維生素', u'益生菌', u'多種維生素', u'維生素和礦物質', u'維生素D', u'補充劑', u'草藥補充劑', u'膳食補充劑', u'多種維生素的功效', u'服用多種維生素', u'不要服用多種維生素', u'優於多種維生素', u'天然補品', u'有機食品', u'功能保健食品', u'歐米加3', u'無用的維生素', u'植物營養素', u'糖尿病/糖尿病補充劑', u'膠質維生素', u'維塔糖蜜']
baidu_baseurl = 'http://www.baidu.com/s?wd='
google_baseurl = 'https://www.google.com.tw/?gws_rd=ssl#q='


def get_request(get_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'connection': 'Keep-Alive',
        'Referer': get_url,
        'Cookie': cookie,
    }
    res_data = requests.get(get_url, headers=headers, timeout=10)
    return res_data.content.replace('\t', '').replace('\r', '').replace('\n', '')


def open_browser_scroll(url):
    global html_name
    driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
    driver.get(url)
    time.sleep(5)
    html_source = driver.page_source
    data = html_source.encode('utf-8').replace('\t', '').replace('\r', '').replace('\n', '')
    driver.close()
    return data


def get_baidu_result_number(keyword):
    url = baidu_baseurl + keyword.encode('utf-8')
    html = get_request(url)
    reg = '百度为您找到相关结果约(.*?)个'

    res = re.compile(reg).findall(html)
    if res:
        return int(res[0].replace(',', ''))
    return -1


def get_google_result_number(keyword):
    reg = 'About (.*?) result'
    url = google_baseurl + keyword.encode('utf-8')
    html = open_browser_scroll(url)

    res = re.compile(reg).findall(html)
    if res:
        return int(res[0].replace(',', ''))
    return -1

