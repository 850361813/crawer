# -*- coding: utf-8 -*-
import re

from http import http_fetcher


def get_visit_num(url):
    last_num_str = url[url.rfind('/') + 1:len(url)]
    adid = last_num_str[0:last_num_str.find('-')]
    visit_url = 'https://www.ebay-kleinanzeigen.de/s-vac-inc-get.json?adId=' + adid
    result = http_fetcher.get_html(visit_url)
    pattern = re.compile(r'{"numVisits":([\d]*),"numVisitsStr":"([\d]*)"')
    match = pattern.match(result.encode("UTF-8"))
    if match is not None:
        return match.group(1)
    else:
        return '0'

if __name__ == '__main__':

    url = 'https://www.ebay-kleinanzeigen.de/s-anzeige/suche-mitbewohner-in-fuer-3-monaten-moeblierte-wohnung-mit-balkon/696196809-203-6450'

    print get_visit_num(url)
