# -*- coding: utf-8 -*-

from dao import house_info_dao
from ebay import config

"""
更新翻译字段任务
"""


def start(db_config):
    house_info_dao.update_translation_column(db_config)

if __name__ == '__main__':
    app_config = config.load_db_config()
    start(app_config)
