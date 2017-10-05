# -*- coding: utf-8 -*-
import os
import re
import time
import urllib2
import hashlib

import datetime

import sys
from selenium import webdriver

from dao import youtube_info_dao
from http import http_fetcher
from youtube import config
from youtube.youtube_info import web_info


def get_next_page_website(soup):
    '''
    获取下一页
    :param soup:
    :return: next page url
    '''
    page_info = soup.find("div", attrs={'class': 'branded-page-box search-pager spf-link '})
    if page_info is not None:
        pattern = re.compile( r'([\s\S]*)<a([\s\S]*)href="([\s\S]*)"><([\s\S]*)>Next([\s\S]*)a>')
        match = pattern.match(page_info.encode("utf-8"))
        if match is not None:
            print home_url + match.group(3)
            return home_url + match.group(3)
        else:
            return ''


def calc_info_hash(key_word, page_num):
    md5 = hashlib.md5()
    md5.update(key_word + str(page_num))
    return md5.hexdigest()


def get_detail_website(info, soup):
    '''
    获取列表中视频链接地址
    :param info: YoutubeInfo.WebInfo
    :return:
    '''
    self_soup = soup
    if self_soup is None:
        self_soup = handle_single_url(info.url)
    detail_list = self_soup.find_all("h3", attrs={'class': 'yt-lockup-title '})
    if detail_list is not None:
        video_links = []
        for detail in detail_list:
            pattern = re.compile(
                r'<h3([\s\S]*)data-sessionlink([\s\S]*)href="([\s\S]*)" rel="spf-prefetch"([\s\S]*)</h3>')
            match = pattern.match(detail.encode("utf-8"))
            if match is not None:
                video_links.append(home_url + match.group(3))
        info.video_links=",".join(video_links)


def handle_single_url(url):
    """
    单个URL处理
    :param url:
    :return: BeautifulSoup
    """
    begin = time.time() * 1000
    soup = http_fetcher.get_soup(url)
    now = time.time() * 1000
    print ('time spends: ' + str(now - begin) + 'ms for processing url:' + url)
    return soup

if __name__ == '__main__':
    reload(sys)
    db_config = config.load_db_config()
    system_config = config.load_system_config()
    daily_fetch_page=int(system_config.get('daily_fetch_page'))
    home_url=system_config.get('home_url')
    key_words = system_config.get('key_words')
    fetch_progress_info = youtube_info_dao.select_progress_info(key_words, db_config)
    start_page = fetch_progress_info.page_num

    now = datetime.datetime.now()

    # 已经爬取过的页面不重复爬取
    soup = None
    if start_page == 1:
        quoto_key_words = urllib2.quote(key_words, ':?=/')
        query_url = home_url + '/results?search_query=' + quoto_key_words
        soup = handle_single_url(query_url)
    else:
        soup = handle_single_url(fetch_progress_info.page_url)

    for i in range(start_page-1, daily_fetch_page + start_page):
        print 'begin craw page : ' + str(i)
        request_url=get_next_page_website(soup)
        if request_url=='':
            print '关键字：' + key_words + '抓取完成'
            fetch_progress_info = youtube_info_dao.select_progress_info(key_words, db_config)
            fetch_progress_info.page_num = i
            fetch_progress_info.status=1
            youtube_info_dao.update_progress_info(fetch_progress_info, db_config)
            sys.exit(0)
        soup = handle_single_url(request_url)
        info = web_info()
        info.key_word = key_words
        info.url=request_url
        info.page_num=i+1
        info.soup=soup
        info.create_time=now
        info.update_time=now
        info.info_hash=calc_info_hash(key_words, i+1)
        get_detail_website(info, soup)
        youtube_info_dao.insert_base_info(info, db_config)
        fetch_progress_info = youtube_info_dao.select_progress_info(key_words, db_config)
        fetch_progress_info.page_num=i+1
        fetch_progress_info.page_url=request_url
        youtube_info_dao.update_progress_info(fetch_progress_info, db_config)

