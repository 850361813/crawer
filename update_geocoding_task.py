# -*- coding: utf-8 -*-

from dao import house_info_dao
from ebay import config

"""
更新经纬度字段任务
"""


def start(db_config):
    house_info_dao.update_geocoding_info(db_config)

if __name__ == '__main__':
    app_config = config.load_db_config()
    start(app_config)
