# -*- coding: utf-8 -*-
import ConfigParser
import os
import random
import time

import re
import json

import datetime

import sys
from threading import Timer

from dao import house_info_dao
from http import http_fetcher
from ebay.HouseInfo import HouseInfo, BaseInfo, ContactInfo, WebInfo, AdditionalInfo


def load_db_config(filepath):
    """
    获取DB连接配置信息
    :param filepath: 
    :return: 
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read(filepath)

    return {
        'host': cp.get('db', 'host'),
        'port': cp.get('db', 'port'),
        'database': cp.get('db', 'database'),
        'user': cp.get('db', 'user'),
        'password': cp.get('db', 'pass'),
        'charset': cp.get('db', 'charset'),
        'use_unicode': True,
        'get_warnings': True,
    }


def load_user_config(filepath):
    """
    配置网站用户信息
    :param filepath: 
    :return: 
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read(filepath)
    return {
        'email': cp.get('user', 'email'),
        'password': cp.get('user', 'password'),
        'home_url': cp.get('user', 'home_url'),
        'base_url': cp.get('user', 'base_url'),
    }


def load_system_config(filepath):
    """
    配置系统信息
    :param filepath: 
    :return: 
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read(filepath)
    return {
        'fetch_num': cp.get('system', 'fetch_num'),
        'min_sleep_seconds': cp.get('system', 'min_sleep_seconds'),
        'max_sleep_seconds': cp.get('system', 'max_sleep_seconds'),
        'is_from_web': cp.get('system', 'is_from_web'),
        'begin_index': cp.get('system', 'begin_index'),
        'cache_detail_url_file': cp.get('system', 'cache_detail_url_file'),
    }


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
                    pattern = re.compile(r'<li>([\s\S]*)href="([\s\S]*)">([\s\S]*)<([\s\S]*)a>([\s\S]*)li>')
                    match = pattern.match(li.encode("utf-8"))
                    if match is not None:
                        second_url_model = dict()
                        second_url_model[url_key] = home_url + match.group(2)
                        second_url_model[city_key] = url_model[city_key]
                        second_url_model[region_kay] = match.group(3)
                        second_url_model[zip_code_key] = ""
                        second_url_models.append(second_url_model)

    return second_url_models


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
    begin = time.time() * 1000
    soup = http_fetcher.get_soup(url)
    now = time.time() * 1000
    print ('time spends: ' + str(now - begin) + 'ms for processing url:' + url)
    return soup


def resolve_base_info(soup):
    """
    获取基础信息
    :param soup: 
    :return: 
    """
    baseInfo = BaseInfo('', '', '')

    title = soup.find("h1", id="viewad-title").string
    if title is not None:
        baseInfo.title = str(title.encode("UTF-8"))

    images_list_parent = soup.find("ul", id="viewad-lightbox-thumbnail-list")
    if images_list_parent is not None:
        images_list = images_list_parent.find_all("li")
        image_url_str = []
        if len(images_list) > 0:
            for image in images_list:
                image_url_str.append(image.div.img['data-imgsrc'])
            baseInfo.image_list = ','.join(image_url_str)

    description = soup.find("section", id="viewad-description").section.p.get_text()
    if description is not None:
        baseInfo.description = description.encode("utf-8").strip()

    return baseInfo


def resolve_web_info(url):
    """
    获取网址信息
    :param url: 
    :return: 
    """
    web_info = WebInfo('0', '')
    web_info.source_link = url

    return web_info


def resolve_contact_info(soup):
    """
    获取联系信息
    :param soup: 
    :return: 
    """
    contact_info = ContactInfo('', '', '')
    profile_box = soup.find("div", id="viewad-profile-box").span
    contact_phone = soup.find("span", id="viewad-contact-phone")

    if contact_phone is not None:
        contact_info.publisher_contact = contact_phone.string.encode("UTF-8")

    pattern = re.compile(
        r'<span([\s\S]*)<a([\s\S]*)>([\s\S]*)</a>([\s\S]*)<span([\s\S]*)>([\s\S]*)<br>([\s\S]*)</span>')
    match = pattern.match(profile_box.encode("UTF-8"))
    if match is not None:
        contact_info.publisher_name = match.group(3).replace('\n', '').strip()
        contact_info.publisher_type = match.group(6).replace('\n', '').strip()

    return contact_info


def resolve_additional_info(soup):
    """
    获取附加详细信息
    :param soup: 
    :return: AdditionalInfo
    """
    additional_info = AdditionalInfo()
    map_data_value = dict()
    attribute_list = soup.find("dl", attrs={'class': 'attributelist-striped'}).get_text().encode("UTF-8")
    data_list = attribute_list.split(":")
    new_data_list = []
    final_data_list = []
    for data in data_list:
        if "\n" in data:
            new_data = data[0:data.rindex("\n")].replace("\n", '') + "\n" + data[data.rindex("\n") + 1:len(data)]
            new_data_list.append(new_data)
        else:
            new_data_list.append(data)

    new_data_list[0] = new_data_list[0].replace("\n", '')
    for new_data in new_data_list:
        final_data = new_data.split("\n")
        final_data_list.extend(final_data)

    for i in xrange(0, len(final_data_list) - 1, 2):
        map_data_value[final_data_list[i]] = final_data_list[i + 1].strip()
    if map_data_value.has_key(Wohnflxa4che_key):
        additional_info.usable_area = map_data_value[Wohnflxa4che_key]
    if map_data_value.has_key(Zimmer_key):
        additional_info.room_amount = map_data_value[Zimmer_key]
    if map_data_value.has_key(erstellungsdatum_key):
        # 时间格式转换 '05.08.2017' 转 int
        time_array = time.strptime(map_data_value[erstellungsdatum_key], "%d.%m.%Y")
        additional_info.source_publish_time = int(time.mktime(time_array))
    if map_data_value.has_key(Nebenkosten_key):
        additional_info.rent_fee_addon = map_data_value[Nebenkosten_key]
    if map_data_value.has_key(Genossenschaftsanteile_key):
        additional_info.rent_fee_deposit = map_data_value[Genossenschaftsanteile_key]
    if map_data_value.has_key(Heizungsart_key):
        additional_info.attribute_heating = '1'
    if map_data_value.has_key(warmmiete_in_euro_key):
        additional_info.rent_fee_hot = map_data_value[warmmiete_in_euro_key]
    if map_data_value.has_key(heizkosten_key):
        additional_info.rent_fee_other = map_data_value[heizkosten_key]

    # 设备
    if map_data_value.has_key(Ausstattung_key):
        for value in map_data_value[Ausstattung_key].split(","):
            if attribute_map.has_key(value.strip()):
                attribute_map[value.strip()] = '1'
        additional_info.attribute_furniture = attribute_map[attribute_furniture_key]
        additional_info.attribute_balcony = attribute_map[attribute_balcony_key]
        additional_info.attribute_terrace = attribute_map[attribute_terrace_key]
        additional_info.layout_kitchen = attribute_map[layout_kitchen_key]
        additional_info.attribute_bathtub = attribute_map[attribute_bathtub_key]
        additional_info.attribute_bathroom = attribute_map[attribute_bathroom_key]
        additional_info.layout_lavatory = attribute_map[layout_lavatory_key]
        additional_info.attribute_disability = attribute_map[attribute_disability_key]
        additional_info.other_new_building = attribute_map[other_new_building_key]
        additional_info.other_old_building = attribute_map[other_old_building_key]
        additional_info.feature_elevator = attribute_map[feature_elevator_key]
        additional_info.feature_basement = attribute_map[feature_basement_key]
        additional_info.feature_loft = attribute_map[feature_loft_key]
        additional_info.attention_welfare_in = attribute_map[attention_welfare_in]
        additional_info.feature_parking_space = attribute_map[feature_parking_space]
        additional_info.feature_garden = attribute_map[feature_garden_key]
        additional_info.attention_allow_pet = attribute_map[attention_allow_pet]
        additional_info.attention_joint_rent = attribute_map[attention_joint_rent]
    if map_data_value.has_key(ort_key):
        ort_data = map_data_value[ort_key]
        # 城市 邮编
        ort_data = ort_data.replace(",", "")
        pattern = re.compile(r'([\s\S]*)([\d]{5})([\s\S]*)')
        match = pattern.match(ort_data)
        if match is not None:
            zip_code = match.group(2)
            city = match.group(3)
        else:
            city = ort_data
        additional_info.zip_code = zip_code
        additional_info.city = city


    # 租金
    price_data = soup.find("h2", attrs={'class': 'articleheader--price'}).get_text().encode("UTF-8")
    if price_data is not None and '€' in price_data:
        additional_info.rent_fee_cold = price_data.split(":")[1]\
            .replace("VB", "").replace(" ", "").replace('€', '').replace(".", '')  # 去除空格和单位

    # 时间
    current = time.mktime(datetime.datetime.now().timetuple())
    additional_info.time_insert = current
    additional_info.time_update = current

    additional_info.subtitle = additional_info.room_amount + '室' + \
    additional_info.layout_kitchen + '厨' + additional_info.layout_lavatory + '卫'
    additional_info.subtitle_de = additional_info.room_amount + ' Zimmer,' + \
                               additional_info.layout_kitchen + ' Küche,' + additional_info.layout_lavatory + ' Baden'
    additional_info.subtitle_en = additional_info.room_amount + ' Room,' + \
                               additional_info.layout_kitchen + ' Kitchen,' + additional_info.layout_lavatory + ' Bath'

    return additional_info


def resolve(url_model):
    """
    解析url，组装houseInfo对象
    :param url_model: 
    :return: 
    """
    soup = handle_single_url(url_model[url_key])

    if soup.find("h1", id="viewad-title") is None: # 标题为空不抓取
        return None
    base_info = resolve_base_info(soup)
    web_info = resolve_web_info(url_model[url_key])
    contact_info = resolve_contact_info(soup)
    additional_info = resolve_additional_info(soup)
    house_info = HouseInfo(base_info, contact_info, web_info, additional_info)
    return house_info


def handle_detail_models(detail_models, begin_index, fetch_num):
    """
    处理URL模型
    :param detail_models: url模型列表
    :param begin_index: 处理开始位置
    :param fetch_num: 每批个数（随机休眠）
    :return: 
    """
    print 'model size : ' + str(len(detail_models))
    print 'start process model, begin at :' + str(begin_index)
    if detail_models is not None:
        for i in range(0, len(detail_models) - 1):
            if i <= begin_index:
                continue
            house_info = resolve(detail_models[i])
            if i % fetch_num == 0:
                sleep_random_second()
            print house_info
            if house_info is None:
                print 'no house info find'
            if house_info is not None:
                house_info_dao.insert(house_info, app_config)
            write_config('system', 'begin_index', config_file, str(i))


def start_from_file(begin_index, fetch_num):
    """
    直接读取缓存文件，处理url
    :param begin_index: 
    :param fetch_num: 
    :return: 
    """
    detail_models = json.load(open(system_config['cache_detail_url_file'], "r"))
    handle_detail_models(detail_models, begin_index, fetch_num)


def start_from_web(fetch_num, begin_index=0):
    """
    从望着你抓取信息，进行处理，同时缓存信息到文件
    :param fetch_num: 
    :param begin_index: 
    :return: 
    """
    total_detail_models = []
    first_url_models = get_first_class_urls(base_url)
    write_data("/Users/baidu/data/first_class_urls.json", json.dumps(first_url_models))
    second_url_models = get_second_class_urls(first_url_models)
    write_data("/Users/baidu/data/second_class_urls.json", json.dumps(second_url_models))
    for second_uel_model in second_url_models:
        detail_models = get_detail_urls(second_uel_model)
        total_detail_models.extend(detail_models)
        handle_detail_models(detail_models, begin_index, fetch_num)
    write_data(app_config['cache_detail_url_file'], json.dumps(total_detail_models))


def start():
    """
    程序开始核心方法
    :return: 
    """
    is_from_web = system_config['is_from_web']
    begin_index = int(system_config['begin_index'])
    fetch_num = int(system_config['fetch_num'])
    # 开始处理
    if is_from_web == '1':
        start_from_web(fetch_num)
    elif is_from_web == '0':
        start_from_file(begin_index, fetch_num)

    # 更新库信息（翻译信息）
    house_info_dao.update_column(app_config)


def test_single_url_model_insert(url):
    """
    单个url处理测试方法
    :param url: 
    :return: 
    """
    url_model = dict()
    url_model[url_key] = url
    url_model[city_key] = "test"
    url_model[zip_code_key] = "00000"
    url_model[region_kay] = "test"
    house_info_dao.insert(resolve(url_model), app_config)


if __name__ == '__main__':

    config_file = '/Users/baidu/PycharmProjects/crawer/conf/app.conf'

    # 定时任务，自动登录检查
    Timer(300, http_fetcher.login(config_file)).start()

    # 程序参数表
    url_key = "url"
    city_key = "city"
    region_kay = "region"
    zip_code_key = "zip_code"
    title_key = "title"
    soup_key = "soup"
    erstellungsdatum_key = 'Erstellungsdatum'  # 发布时间
    Anzeigennummer_key = 'Anzeigennummer'
    Zimmer_key = 'Zimmer'  # 出租类型
    Wohnflxa4che_key = 'Wohnfl\xc3\xa4che (qm)'  # 可用面积
    Nebenkosten_key = 'Nebenkosten (in Euro)'  # 附加费用
    Genossenschaftsanteile_key = 'Kaution / Genossenschaftsanteile (in Euro)'  # 押金
    Wohnungstyp_key = 'Wohnungstyp'  #
    Heizungsart_key = 'Heizungsart'  # 暖气
    Verf_ab_monat_key = 'Verf\xc3\xbcgbar ab Monat'
    Verf_ab_monat_Jahr_key = 'Verf\xc3\xbcgbar ab Jahr'
    Ausstattung_key = 'Ausstattung'  # 设备
    warmmiete_in_euro_key = 'Warmmiete (in Euro)'  # 暖月租金
    heizkosten_key = 'Heizkosten (in Euro)'  # 其他费用

    # 设备列表字典，默认取值为0，key值和网页展示保持一致
    attribute_furniture_key = 'Möbliert/Teilmöbliert'
    attribute_balcony_key = 'Balkon'
    attribute_terrace_key = 'Terrasse'
    layout_kitchen_key = 'Einbauküche'
    attribute_bathtub_key = 'Badewanne'
    attribute_bathroom_key = 'Dusche'
    layout_lavatory_key = 'GästeWC'
    attribute_disability_key = 'Barrierefrei'
    other_old_building_key = 'Altbau'
    other_new_building_key = 'Neubau'
    feature_elevator_key = 'Aufzug'
    feature_basement_key = 'Keller'
    feature_loft_key = 'Dachboden'
    attention_welfare_in = 'Wohnberechtigungsscheinbenötigt'
    feature_parking_space = 'Garage/Stellplatz'
    feature_garden_key = 'Garten/-mitnutzung'
    attention_allow_pet = 'Haustiereerlaubt'
    attention_joint_rent = 'WG-geeignet'
    attribute_map = dict()
    attribute_map[attribute_furniture_key] = '0' # 带家具
    attribute_map[attribute_balcony_key] = '0' # 阳台
    attribute_map[attribute_terrace_key] = '0' # 露台
    attribute_map[layout_kitchen_key] = '0' # 户型-厨房
    attribute_map[attribute_bathtub_key] = '0' # 浴缸
    attribute_map[attribute_bathroom_key] = '0' # 沐浴室
    attribute_map[layout_lavatory_key] = '0' # 户型-厕所
    attribute_map[attribute_disability_key] = '0' # 残疾人
    attribute_map[other_old_building_key] = '0' # 旧建筑
    attribute_map[other_new_building_key] = '0' # 新建筑
    attribute_map[feature_elevator_key] = '0' # 电梯
    attribute_map[feature_basement_key] = '0' # 地下室
    attribute_map[feature_loft_key] = '0' # 阁楼
    attribute_map[attention_welfare_in] = '0' # 需福利准入证
    attribute_map[feature_parking_space] = '0' # 停车位
    attribute_map[feature_garden_key] = '0' # 花园
    attribute_map[attention_allow_pet] = '0' # 允许养宠物
    attribute_map[attention_joint_rent] = '0' # 允许合租
    ort_key = "Ort"  # 地名，邮编，城市

    # 加载app.conf配置文件
    app_config = load_db_config(config_file)
    system_config = load_system_config(config_file)
    user_config = load_user_config(config_file)
    home_url = user_config['home_url']
    base_url = user_config['base_url']

    start()
    print 'process finish, exit'
    sys.exit(0)

