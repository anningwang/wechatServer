# -*- coding: utf-8 -*-
#  filename: basic.py

import urllib
import time
import json


class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_access_token(self):
        app_id = "wx7f16d7b8d26a4970"
        app_secret = "cd873d15f0c4ae0d1460269ebfff2f9f"
        post_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % \
                   (app_id, app_secret)
        url_resp = urllib.urlopen(post_url)
        url_resp = json.loads(url_resp.read())
        self.__accessToken = url_resp['access_token']
        self.__leftTime = url_resp['expires_in']

    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
            return self.__accessToken

    def run(self):
        while True:
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()
