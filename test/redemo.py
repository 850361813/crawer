#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup

if __name__ == '__main__':
    text = '''<li>
   <a href="/s-wohnung-mieten/dachgeschosswohnung/bayern/c203l5510+wohnung_mieten.wohnungstyp_s:dachgeschosswohnung">Dachgeschosswohnung</a>&nbsp;<span class="browsebox-facet text-light">(704)</span></li>'''
    text2 = '94469 Bayern - Deggendorf'
    pattern = re.compile(r'<li>([\s\S]*)href="([\s\S]*)">([\s\S]*)<([\s\S]*)a>([\s\S]*)\(([\s\S]*)\)([\s\S]*)li>')
    match = pattern.match(text)
    print match.group(2)
    print match.group(3)
    print match.group(6)


