#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib
import urllib2
from multiprocessing import Process
from collections import defaultdict


def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))


if __name__ == '__main__':
    urllib.urlretrieve('http://www.chinamoney.com.cn/fe/CMS5_G20306002Resource?info=18105219;res=1460995568251290423926;download=', '/Users/baidu/text.pdf')
