#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup

if __name__ == '__main__':
    text = 'Forstweg, 57258 Nordrhein-Westfalen - Freudenberg'
    text2 = '94469 Bayern - Deggendorf'
    pattern = re.compile(r'([\s\S]*)([\d]{5})([\s\S]*)')
    match = pattern.match(text2.encode("utf-8"))
    print match.group(1)
    print match.group(2)
    print match.group(3)


