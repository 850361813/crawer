# -*- coding: utf-8 -*-
import mysql.connector
from common import google_service


"""
数据交互服务
"""


def update_translation_column(config):
    """
    更新翻译字段
    :param config: 
    :return: 
    """
    sql = 'select id, title_ge, description_ge from dcs_dorm'
    update_sql = 'update dcs_dorm set title = %s , title_en = %s , description = %s, description_en = %s where id = %s;'
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()

    cur.execute(sql)
    result = cur.fetchall()
    if result is None:
        return
    for data in result:
        title_ge = data[1]
        description_ge = data[2]
        id = data[0]

        # 翻译信息
        title = google_service.google_translate_DtoC(title_ge.encode("UTF-8").replace('&', ''))
        print title
        title_en = google_service.google_translate_DtoE(title_ge.encode("UTF-8").replace('&', ''))
        print title_en
        description = google_service.google_translate_DtoC(description_ge.encode("UTF-8").replace('&', ''))
        print description
        description_en = google_service.google_translate_DtoE(description_ge.encode("UTF-8").replace('&', ''))
        print description_en
        param = (title, title_en, description, description_en, id)
        cur.execute(update_sql, param)
        cnx.commit()
        print 'update data for id : ' + str(id)


def update_geocoding_info(config):
    """
    更新经纬度信息
    :param config: 
    :return: 
    """
    sql = 'select id, city from dcs_dorm'
    update_sql = 'update dcs_dorm set location_longitude = %s,location_latitude = %s where id = %s;'
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()

    cur.execute(sql)
    result = cur.fetchall()
    if result is None:
        return
    for data in result:
        city = data[1]
        id = data[0]
        # 经纬度信息
        position = google_service.get_geo_for_address(city.encode('utf-8'))
        location_longitude = position['lng']
        location_latitude = position['lat']
        param = (location_longitude, location_latitude, id)
        cur.execute(update_sql, param)
        cnx.commit()
        print 'update geocoding data for id : ' + str(id)


def insert(house_info, config):
    default_int = '0'
    default_str = ''
    sql = '''INSERT INTO dcs_dorm 
           (title, title_ge, title_en, subtitle, subtitle_ge,
           subtitle_en,image_list, rent_method, room_amount,usable_area, 
           floor_current,floor_all, rent_fee_hot,rent_fee_cold, rent_fee_addon, 
           rent_fee_other, rent_fee_deposit, rent_fee_undertaking, publisher_type, publisher_name, 
           publisher_contact, source_view_count, source_link, source_publish_time, attribute_furniture, 
           attribute_tv,attribute_heating, attribute_refrigerator, attribute_washer, attribute_wired, 
           attribute_wifi,attribute_bathroom, attribute_bathtub, attribute_bed, attribute_balcony, 
           attribute_terrace, attribute_disability, feature_elevator, feature_entrance_guard, feature_garden, 
           feature_basement,feature_parking_space, feature_bike_parking, feature_subway, feature_bus, 
           feature_hospital,feature_supermarket, feature_loft, attention_allow_pet, attention_allow_cooking,
           attention_can_be_settled, attention_welfare_in, attention_joint_rent, layout_kitchen, layout_lavatory, 
           other_new_building, attention_checkin_any_time, description, description_ge, description_en, 
           time_rent_begin, time_rent_end, rent_shortest_days, view_count, location_name, 
           zip_code, city, location_longitude, location_latitude, state, 
           rank, time_insert, time_update,status) 
           VALUES (
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
           %s, %s, %s, %s)'''
    param = (default_str,
             house_info.baseInfo.title,
             default_str,
             house_info.additionalInfo.subtitle,
             house_info.additionalInfo.subtitle_de,
             house_info.additionalInfo.subtitle_en,
             house_info.baseInfo.image_list,
             house_info.additionalInfo.rent_method,
             house_info.additionalInfo.room_amount,
             house_info.additionalInfo.usable_area,
             house_info.additionalInfo.floor_current,
             default_int,
             house_info.additionalInfo.rent_fee_hot,
             house_info.additionalInfo.rent_fee_cold,
             house_info.additionalInfo.rent_fee_addon,
             house_info.additionalInfo.rent_fee_other,
             house_info.additionalInfo.rent_fee_deposit,
             default_int,
             house_info.contactInfo.publisher_type,
             house_info.contactInfo.publisher_name,
             house_info.contactInfo.publisher_contact,
             house_info.webInfo.source_view_count,
             house_info.webInfo.source_link,
             house_info.additionalInfo.source_publish_time,
             house_info.additionalInfo.attribute_furniture,
             default_int,
             house_info.additionalInfo.attribute_heating,
             default_int,
             default_int,
             default_int,
             default_int,
             house_info.additionalInfo.attribute_bathroom,
             house_info.additionalInfo.attribute_bathtub,
             default_int,
             house_info.additionalInfo.attribute_balcony,
             house_info.additionalInfo.attribute_terrace,
             house_info.additionalInfo.attribute_disability,
             house_info.additionalInfo.feature_elevator,
             default_int,
             house_info.additionalInfo.feature_garden,
             house_info.additionalInfo.feature_basement,
             house_info.additionalInfo.feature_parking_space,
             default_int,
             default_int,
             default_int,
             default_int,
             default_int,
             house_info.additionalInfo.feature_loft,
             house_info.additionalInfo.attention_allow_pet,
             default_int,
             default_int,
             house_info.additionalInfo.attention_welfare_in,
             house_info.additionalInfo.attention_joint_rent,
             house_info.additionalInfo.layout_kitchen,
             house_info.additionalInfo.layout_lavatory,
             house_info.additionalInfo.other_new_building,
             default_int,
             default_str,
             house_info.baseInfo.description,
             default_str,
             default_int,
             default_int,
             default_int,
             house_info.webInfo.source_view_count,
             house_info.additionalInfo.location_name,
             house_info.additionalInfo.zip_code,
             house_info.additionalInfo.city,
             default_int,
             default_int,
             house_info.additionalInfo.state,
             default_int,
             house_info.additionalInfo.time_insert,
             house_info.additionalInfo.time_update,
             house_info.additionalInfo.status)

    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()

    # Insert
    cur.execute(sql, param)
    cnx.commit()
    print ('insert data success, title:' + house_info.baseInfo.title)
