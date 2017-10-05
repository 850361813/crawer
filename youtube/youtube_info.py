# -*- coding: utf-8 -*-
class web_info:

    def __init__(self, key_word, page_num, url, video_links,
                 valid, publish_status, collect_time, publish_time, create_time, update_time, info_hash):
        self.key_word = key_word
        self.page_num = page_num
        self.soup=None
        self.video_links = video_links
        self.valid = valid
        self.publish_status = publish_status
        self.collect_time = collect_time
        self.publish_time = publish_time
        self.create_time = create_time
        self.update_time = update_time
        self.url = url
        self.info_hash=info_hash

    def __init__(self):
        self.key_word = ''
        self.page_num = 0
        self.soup = None
        self.video_links = ''
        self.valid = 1 #默认有效
        self.publish_status = 0
        self.collect_time = '1990-01-01 00:000:00'
        self.publish_time = '1990-01-01 00:000:00'
        self.create_time = '1990-01-01 00:000:00'
        self.update_time = '1990-01-01 00:000:00'
        self.url = ''
        self.info_hash=''

    def gatherAttrs(self):
        return ",".join("{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())

class progress_info:
    def __init__(self, key_word, page_num, status, page_url):
        self.key_word = key_word
        self.page_num = page_num
        self.status=status
        self.page_url=page_url

    def __init__(self):
        self.key_word = ''.encode("utf-8")
        self.page_num = 1
        self.status = 0
        self.page_url = ''.encode("utf-8")

    def gatherAttrs(self):
        return ",".join("{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())