# -*- coding: utf-8 -*-
#  filename: __init__.py

from apscheduler.schedulers.background import BackgroundScheduler
import threading
import basic
import menu


__q = threading.Lock()        # create a lock object
__token = basic.Basic()
scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', id='job_id_wx_token', seconds=2)
def job_function():
    __q.acquire()  # acquire the lock
    __token.run(2)
    __q.release()  # release the lock


scheduler.start()


def get_access_token_for_wx():
    __q.acquire()
    token = __token.get_access_token()
    __q.release()
    return token


menu_json = """
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
                "name": "测试",
                "key": "mp"
            }
          ]
    }
    """
menu.Menu.create(menu_json, get_access_token_for_wx())      # 创建微信公众号菜单
