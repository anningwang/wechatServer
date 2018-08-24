# -*- coding: utf-8 -*-
#  filename: basic.py

import urllib
import urllib2
import json
from tools.getip import is_windows_os

APP_ID = u"wx7f16d7b8d26a4970"
APP_SECRET = u"cd873d15f0c4ae0d1460269ebfff2f9f"


class Basic:
    """
    获取公众号的 access token
    """
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
        self.__REFRESH_SECONDS = 60 * 30

    def __real_get_access_token(self):
        if is_windows_os():
            post_url = "http://47.106.172.59/api/wx/token"
            values = {'appid': APP_ID, 'secret': APP_SECRET}
            # data = json.dumps(values)
            data = urllib.urlencode(values)
            req = urllib2.Request(url=post_url, data=data)
            url_resp = urllib2.urlopen(req)
        else:
            post_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % \
                       (APP_ID, APP_SECRET)
            url_resp = urllib.urlopen(post_url)
        url_resp = json.loads(url_resp.read())
        print url_resp
        self.__accessToken = url_resp['access_token']
        self.__leftTime = url_resp['expires_in']

    def get_access_token(self):
        if self.__leftTime < self.__REFRESH_SECONDS:
            self.__real_get_access_token()
        return self.__accessToken, self.__leftTime

    def run(self, inc=2):
        if self.__leftTime > self.__REFRESH_SECONDS:
            self.__leftTime -= inc
        else:
            self.__real_get_access_token()
