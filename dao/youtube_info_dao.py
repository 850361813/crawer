# -*- coding: utf-8 -*-
import mysql.connector
from youtube import config

from youtube.youtube_info import web_info, progress_info


def insert_base_info(web_info, config):
    info_hash = web_info.info_hash
    data_size = select_base_info(info_hash, config)
    if data_size > 0:
        delete_base_info(info_hash, config)
    default_int = '0'
    default_str = ''
    sql = '''INSERT INTO BASE_INFO 
           (KEY_WORD, PAGE_NUM, URL, VIDEO_LINKS, PUBLISH_STATUS,
           COLLECT_TIME,PUBLISH_TIME, CREATE_TIME, UPDATE_TIME,INFO_HASH) 
           VALUES (
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    param = (web_info.key_word,
             web_info.page_num,
             web_info.url,
             web_info.video_links,
             web_info.publish_status,
             web_info.collect_time,
             web_info.publish_time,
             web_info.create_time,
             web_info.update_time,
             web_info.info_hash
             )
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()

    # Insert
    cur.execute(sql, param)
    cnx.commit()
    print ('insert data success, title:' + web_info.key_word +'--'+ str(web_info.page_num))


def delete_base_info(info_hash, config):
    sql = "DELETE FROM BASE_INFO where INFO_HASH='%s'" % (info_hash)
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    cur.execute(sql)
    cnx.commit()
    print ('delete data success, info_hash:' + info_hash)


def select_base_info(info_hash, config):
    sql = "SELECT KEY_WORD, PAGE_NUM, URL, VIDEO_LINKS, " \
          "PUBLISH_STATUS,COLLECT_TIME,PUBLISH_TIME, CREATE_TIME, UPDATE_TIME,INFO_HASH FROM BASE_INFO where INFO_HASH= '%s'" % (info_hash)
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    cur.execute(sql)
    data_size = len(cur.fetchall())
    cnx.commit()
    return data_size


def select_progress_info(key_word, config):
    fetch_progress_info = progress_info()
    sql = "SELECT KEY_WORD, PAGE_NUM, STATUS, PAGE_URL FROM PROGESS_INFO where KEY_WORD= '%s'" % (key_word)
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    cnx.commit()
    if result is None:
        fetch_progress_info.key_word = key_word
        insert_progress_info(fetch_progress_info, config)
    else:
        data = list(result)
        fetch_progress_info.key_word = data[0].encode("UTF-8")
        fetch_progress_info.page_num = data[1]
        fetch_progress_info.status = data[2]
        fetch_progress_info.page_url = data[3].encode("UTF-8")
    return fetch_progress_info


def update_progress_info(progress_info, config):
    sql = "UPDATE PROGESS_INFO SET PAGE_NUM=%s , STATUS=%s, PAGE_URL='%s' WHERE KEY_WORD='%s'"\
          % (progress_info.page_num, progress_info.status, progress_info.page_url, progress_info.key_word)
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    cur.execute(sql)
    cnx.commit()

def insert_progress_info(progress_info, config):
    sql = "INSERT INTO PROGESS_INFO (KEY_WORD, PAGE_NUM, STATUS) VALUES (%s, %s, %s)"
    param = (progress_info.key_word,
             progress_info.page_num,
             progress_info.status
             )
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()

    # Insert
    cur.execute(sql, param)
    cnx.commit()
    print ('insert data success, PROGRESS_INFO:' + progress_info.key_word + '--' + str(progress_info.page_num))

