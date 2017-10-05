# -*- coding: utf-8 -*-
import ConfigParser
import os

config_file = 'youtube.conf'


def get_config_dir():
    home_dir = os.path.abspath(os.getcwd() + os.sep + '.')
    return home_dir + os.sep + 'conf' + os.sep


def load_db_config():
    """
    获取DB连接配置信息
    :return:
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read(get_config_dir() + config_file)

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


def load_system_config():
    """
    配置系统信息
    :return:
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read(get_config_dir() + config_file)
    return {
        'home_url': cp.get('system', 'home_url'),
        'daily_fetch_page': cp.get('system', 'daily_fetch_page'),
        'key_words': cp.get('system', 'key_words'),
    }