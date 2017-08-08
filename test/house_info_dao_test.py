#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser

from dao import house_info_dao
from ebay.HouseInfo import HouseInfo, BaseInfo, ContactInfo, WebInfo, AdditionalInfo

if __name__ == '__main__':

    cp = ConfigParser.SafeConfigParser()
    cp.read('/Users/baidu/PycharmProjects/crawer/conf/app.conf')

    config = {
        'host': cp.get('db', 'host'),
        'port': cp.get('db', 'port'),
        'database': cp.get('db', 'database'),
        'user': cp.get('db', 'user'),
        'password': cp.get('db', 'pass'),
        'charset': cp.get('db', 'charset'),
        'use_unicode': True,
        'get_warnings': True,
    }

    baseInfo = BaseInfo('10', '2', '3', '4', '5')
    contactInfo = ContactInfo('1', '2', '3')
    webInfo = WebInfo('3', '5', '5')
    additionalInfo = AdditionalInfo()
    house_info = HouseInfo(baseInfo, contactInfo, webInfo, additionalInfo)

    house_info_dao.insert(house_info, config)