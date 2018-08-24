# -*- coding:utf-8 -*-

from flask import Flask, request
import reply
import receive
import hashlib
import platform
import socket
import basic
import menu

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Flask!'


@app.route('/api/wx',  methods=['GET', 'POST'])
def api_wx():
    if request.method == 'GET':
        obj = request.args
        print obj
        signature = obj.get('signature')
        timestamp = obj.get('timestamp')
        nonce = obj.get('nonce')
        echo_str = obj.get('echostr')
        token = "hzwugjToken"  # 请按照公众平台官网\基本配置中信息填写

        list_4_signature = [token, timestamp, nonce]
        list_4_signature.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list_4_signature)
        hashcode = sha1.hexdigest()
        print "api_wx/GET func: hashcode, signature: "
        print hashcode
        print signature
        if hashcode == signature:
            print 'success!'
            return echo_str
        else:
            print 'fail!'
            return ''
    else:
        try:
            # print 'request', request
            web_data = request.data
            print 'web_data', web_data

            rec_msg = receive.parse_xml(web_data)
            if isinstance(rec_msg, receive.Msg):
                to_user = rec_msg.FromUserName
                from_user = rec_msg.ToUserName
                if isinstance(rec_msg, receive.TextMsg):
                    content = "功能待开发，你说的是: " + rec_msg.Content
                    reply_msg = reply.TextMsg(to_user, from_user, content)
                    return reply_msg.send()
                elif isinstance(rec_msg, receive.ImageMsg):
                    media_id = rec_msg.MediaId
                    reply_msg = reply.ImageMsg(to_user, from_user, media_id)
                    return reply_msg.send()
                else:
                    return reply.Msg().send()
            elif isinstance(rec_msg, receive.EventMsg):
                to_user = rec_msg.FromUserName
                from_user = rec_msg.ToUserName
                if rec_msg.Event == 'CLICK' and isinstance(rec_msg, receive.Click):
                    if rec_msg.EventKey == 'mpGuide':
                        content = u"编写中，尚未完成".encode('utf-8')
                        reply_msg = reply.TextMsg(to_user, from_user, content)
                        return reply_msg.send()
                return reply.Msg().send()
            else:
                print "暂且不处理"
                return reply.Msg().send()
        except Exception, args:
            print 'args', args
            return args


def get_ip():
    if is_windows_os():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    else:
        ip_address = '0.0.0.0'
    return ip_address


def is_windows_os():
    return 'Windows' in platform.system()


if __name__ == '__main__':
    my_token = basic.Basic()
    # token.run()

    mm = menu.Menu()
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
                "type": "media_id",
                "name": "旅行",
                "media_id": "z2zOokJvlzCXXNhSjF46gdx6rSghwX2xOD5GUV9nbX4"
            }
          ]
    }
    """
    access_token = my_token.get_access_token()
    mm.create(postJson, access_token)

    ip = get_ip()
    app.run(host=ip, port=80)
