# -*- coding: utf-8 -*-
import os
import urllib
import urllib2

import requests

from common.google_position import get_geo_for_address
from http import http_fetcher

if __name__ == '__main__':

    addr = raw_input('\nAddress or (Lat,Long): ')
    while addr <> '':
        url = ''
        if addr[0] == '(':
            center = addr.replace('(', '').replace(')', '')
            lat, lng = center.split(',')
            url = 'http://maps.google.com/maps?q=%s+%s' % (lat, lng)
        else:
            # Encode query string into URL
            url = 'http://maps.google.com/?q=' + urllib.quote(addr) + '&output=js'
            print '\nQuery: %s' % (url)

            # Get XML location
            xml = urllib.urlopen(url).read()

            if '<error>' in xml:
                print '\nGoogle cannot interpret the address.'
            else:
                # Strip lat/long coordinates from XML
                lat, lng = 0.0, 0.0
                center = xml[xml.find('{center') + 10:xml.find('}', xml.find('{center'))]
                center = center.replace('lat:', '').replace('lng:', '')
                lat, lng = center.split(',')
                url = 'http://maps.google.com/maps?q=%s+%s' % (lat, lng)

        if url <> '':
            print 'Map: %s' % (url)
            os.startfile(url)

        addr = raw_input('\nAddress or (Lat,Long): ')

