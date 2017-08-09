# -*- coding: utf-8 -*-

import ConfigParser
import os
import random
import time

import re
import json


import sys
from threading import Timer

from ebay import config
from http import http_fetcher

init_fetch_num = 0


def write_config(demain, key, filepath, value):
    """
    更新配置信息
    :param demain: 域
    :param key: 
    :param filepath: 
    :param value: 
    :return: 
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read(filepath)
    cp.set(demain, key, value)
    cp.write(open(filepath, "w"))


def sleep_random_second():
    """
    随机暂停一段时间（针对网站反爬虫机制）
    :return: 
    """
    print 'sleeping'
    sleep_time = random.randint(int(system_config['min_sleep_seconds']), int(system_config['max_sleep_seconds']))
    time.sleep(sleep_time)
    print 'sleep for second:' + str(sleep_time)


def write_data(file, data):
    """
    写数据到文件
    :param file: 
    :param data: 
    :return: 
    """
    if os.path.exists(file):
        os.remove(file)
    obj = open(file, 'wb')
    obj.write(data)
    obj.close()


def read_data(file):
    """
    从文件读数据
    :param file: 
    :return: 
    """
    f = open(file, "r")
    return f.readlines()


def get_first_class_urls(url):
    """
    获取一级城市所有url模型
    :param url: 
    :return: 
    """
    soup = handle_single_url(url)
    ort_list = soup.find("ul", attrs={'data-overlayheadline': 'Ort'})
    url_model_list = []

    if ort_list is not None:
        a_href_list = ort_list.find_all("li")
        if a_href_list is not None:
            for li in a_href_list:
                pattern = re.compile(r'<li>([\s\S]*)href="([\s\S]*)">([\s\S]*)<([\s\S]*)a>([\s\S]*)li>')
                match = pattern.match(li.encode("utf-8"))
                url_model = dict()
                url_model[url_key] = home_url + match.group(2)
                url_model[city_key] = match.group(3)
                url_model[zip_code_key] = ""
                url_model_list.append(url_model)

    return url_model_list


def get_second_class_urls(url_model_list):
    """
    获取二级城市所有url模型
    :param url_model_list: 
    :return: 
    """
    second_url_models = []
    if url_model_list is None:
        return []
    for url_model in url_model_list:
        soup = handle_single_url(url_model[url_key])
        ort = url_model[city_key]
        ort_list = soup.find("ul", attrs={'data-overlayheadline': ort})
        if ort_list is not None:
            a_href_list = ort_list.find_all("li")
            if a_href_list is not None:
                for li in a_href_list:
                    pattern = re.compile(r'<li>([\s\S]*)href="([\s\S]*)">([\s\S]*)<([\s\S]*)a>([\s\S]*)\(([\s\S]*)\)([\s\S]*)li>')
                    match = pattern.match(li.encode("utf-8"))
                    if match is not None:
                        second_url_model = dict()
                        second_url_model[url_key] = home_url + match.group(2)
                        second_url_model[city_key] = url_model[city_key]
                        second_url_model[region_kay] = match.group(3)
                        second_url_model[zip_code_key] = ""
                        second_url_model[page_key] = match.group(6).replace('.', '') # 页码数据
                        second_url_models.append(second_url_model)

    return second_url_models


def model_pager(url_model):
    dest_urls_models = []
    default_num_per_page = 25
    total_data_num = int(url_model[page_key])
    src_url = url_model[url_key]
    if total_data_num <= default_num_per_page:
        dest_urls_models.append(url_model)
    else:
        total_page = total_data_num/default_num_per_page + 1
        for i in range(1, total_page + 1):
            page_url = src_url[0:src_url.rfind('/') + 1] + 'seite:' + str(i) + src_url[src_url.rfind('/'):len(src_url)]
            url_model_d = url_model.copy()
            url_model_d[url_key] = page_url
            dest_urls_models.append(url_model_d)
    return dest_urls_models


def get_detail_urls(url_model):
    """
    获取详情页面列表url模型信息
    :param url_model: 
    :return: 
    """
    url_model_list = []
    if url_model is not None:
        soup = handle_single_url(url_model[url_key])
        detail_list = soup.find_all("h2", attrs={'class': 'text-module-begin'})
        if detail_list is not None:
            for detail in detail_list:
                pattern = re.compile(r'<h2 class="text-module-begin"><a href="([\s\S]*)">([\s\S]*)<([\s\S]*)a></h2>')
                match = pattern.match(detail.encode("utf-8"))
                if match is not None:
                    second_url_model = dict()
                    second_url_model[url_key] = home_url + match.group(1)
                    second_url_model[city_key] = url_model[city_key]
                    second_url_model[region_kay] = url_model[region_kay]
                    second_url_model[zip_code_key] = ""
                    second_url_model[title_key] = match.group(2)
                    url_model_list.append(second_url_model)
    return url_model_list


def handle_single_url(url):
    """
    单个URL处理
    :param url: 
    :return: BeautifulSoup
    """
    global init_fetch_num
    init_fetch_num = init_fetch_num + 1
    if init_fetch_num % fetch_num == 0:
        sleep_random_second()
    begin = time.time() * 1000
    soup = http_fetcher.get_soup(url)
    now = time.time() * 1000
    print ('time spends: ' + str(now - begin) + 'ms for processing url:' + url)
    return soup


def start_from_web():
    """
    从web抓取信息，进行处理，同时缓存信息到文件
    :return: 
    """
    total_detail_models = []
    first_url_models = get_first_class_urls(base_url)
    second_url_models = get_second_class_urls(first_url_models)
    for second_uel_model in second_url_models:
        models = model_pager(second_uel_model)
        for sub_model in models:
            detail_models = get_detail_urls(sub_model)
            total_detail_models.extend(detail_models)
    print 'total model: ' + str(len(total_detail_models))
    write_data(system_config['cache_detail_url_file'], json.dumps(total_detail_models))


if __name__ == '__main__':

    # 定时任务，自动登录检查
    Timer(300, http_fetcher.login()).start()

    # 程序参数表
    url_key = "url"
    city_key = "city"
    region_kay = "region"
    zip_code_key = "zip_code"
    title_key = "title"
    soup_key = "soup"
    page_key = "page"

    app_config = config.load_db_config()
    system_config = config.load_system_config()
    user_config = config.load_user_config()
    home_url = user_config['home_url']
    base_url = user_config['base_url']

    fetch_num = int(system_config['fetch_num'])

    start_from_web()
    print 'process finish, exit'
    sys.exit(0)
