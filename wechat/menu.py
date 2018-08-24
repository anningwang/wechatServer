# -*- coding: utf-8 -*-
# filename: menu.py
import urllib
from . import get_access_token_for_wx


class Menu(object):
    def __init__(self):
        pass

    def create(self, post_data, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
        if isinstance(post_data, unicode):
            post_data = post_data.encode('utf-8')
        url_resp = urllib.urlopen(url=post_url, data=post_data)
        print url_resp.read()

    def query(self, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % access_token
        url_resp = urllib.urlopen(url=post_url)
        print url_resp.read()

    def delete(self, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % access_token
        url_resp = urllib.urlopen(url=post_url)
        print url_resp.read()

    # 获取自定义菜单配置接口
    def get_current_selfmenu_info(self, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % access_token
        url_resp = urllib.urlopen(url=post_url)
        print url_resp.read()


if __name__ == '__main__':
    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "type": "click",
                "name": "开发指引",
                "key":  "mpGuide"
            },
            {
                "name": "公众平台",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "更新公告",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "接口权限说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "返回码说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                    }
                ]
            },
            {
                "type": "click",
                "name": "旅行",
                "key": "mp"
            }
          ]
    }
    """
    my_access_token = get_access_token_for_wx()
    myMenu.create(postJson, my_access_token)
