# -*- coding: utf-8 -*-


def pager(src_url, total_data_num):
    dest_urls = []
    default_num_per_page = 25
    if total_data_num <= default_num_per_page:
        dest_urls.extend(src_url)
    else:
        total_page = total_data_num/default_num_per_page + 1
        for i in range(1, total_page + 1):
            page_url = src_url[0:src_url.rfind('/') + 1] + 'seite:' + str(i) + src_url[src_url.rfind('/'):len(src_url)]
            dest_urls.append(page_url)
    return dest_urls

if __name__ == '__main__':
    src_url = 'https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/heidelberg/c203l9166'
    print pager(src_url, 28)