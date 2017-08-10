#!/usr/bin/python
# coding: UTF-8
import json
import urllib2

import requests


def get_geo_for_address(address):
    headers = {
        'Upgrade-Insecure-Requests':'1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    }
    position_dict = dict()
    quoto_address = urllib2.quote(address, ':?=/')
    address_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+quoto_address
    print address_url
    result = urllib2.urlopen(address_url).read().decode('utf-8')

    print result
    # 中文url需要转码才能识别
    # response = result.decode('utf-8')
    response_json = json.loads(result)
    lat = '0'
    lng = '0'
    if response_json.get('status') == 'OK':
        lat = response_json.get('results')[0]['geometry']['location']['lat']
        lng = response_json.get('results')[0]['geometry']['location']['lng']
        print(address + '的经纬度是: %f, %f' % (lat, lng))
    position_dict['lng'] = lng
    position_dict['lat'] = lat
    return position_dict
