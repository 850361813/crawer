# -*- coding: utf-8 -*-
import cookielib
import urllib
import urllib2

import requests

from bs4 import BeautifulSoup as bf
from ebay import config

session_requests = requests.session()


def login():
    """
    网站登录
    :return: 
    """
    user_config = config.load_user_config()

    url = user_config['login_url']
    home_url = user_config['home_url']
    email = user_config['email']
    password = user_config['password']
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    h = urllib2.urlopen(home_url)

    postData = {
        'targetUrl': url,
        'loginMail': email,
        'password': password,
        '_csrf': 'b8e1e045-7d4b-4ddf-a448-8111c9749c27'

    }
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,de;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'text/plain',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }

    login_url = 'https://www.ebay-kleinanzeigen.de/m-einloggen.html'
    result = session_requests.get(login_url)
    soup = get_soup_from_html(result.text)
    csrf_raw = soup.find("input", attrs={'name': '_csrf'})
    postData['_csrf'] = csrf_raw.attrs['value'].encode("UTF-8")
    result = session_requests.post(login_url, postData, headers)
    if result.status_code == 200:
        print 'login success for user: ' + email


def get_html(url):
    result = session_requests.get(url)

    return result.text


def get_soup(url):
    return get_soup_from_html(get_html(url))


def get_soup_from_html(html):
    return bf(html, "html.parser")


def download(url, path):
    urllib.urlretrieve(url, path)

if __name__ == '__main__':
    login()
