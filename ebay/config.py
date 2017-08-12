# -*- coding: utf-8 -*-
import ConfigParser

config_file = '/Users/baidu/PycharmProjects/crawer/conf/app.conf'

"""
配置解析服务
"""


def load_db_config():
    """
    获取DB连接配置信息
    :return: 
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read(config_file)

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


def load_user_config():
    """
    配置网站用户信息
    :return: 
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read(config_file)
    return {
        'email': cp.get('user', 'email'),
        'password': cp.get('user', 'password'),
        'home_url': cp.get('user', 'home_url'),
        'base_url': cp.get('user', 'base_url'),
        'login_url': cp.get('user', 'login_url'),
    }


def load_system_config():
    """
    配置系统信息
    :return: 
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read(config_file)
    return {
        'fetch_num': cp.get('system', 'fetch_num'),
        'min_sleep_seconds': cp.get('system', 'min_sleep_seconds'),
        'max_sleep_seconds': cp.get('system', 'max_sleep_seconds'),
        'begin_index': cp.get('system', 'begin_index'),
        'cache_detail_url_file': cp.get('system', 'cache_detail_url_file'),
    }
