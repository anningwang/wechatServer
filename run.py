# -*- coding:utf-8 -*-

from flask import Flask, request
import reply
import receive
import hashlib
import platform
import socket

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
                if rec_msg.MsgType == 'text':
                    content = "功能待开发，你说的是: " + rec_msg.Content
                    reply_msg = reply.TextMsg(to_user, from_user, content)
                    return reply_msg.send()
                if rec_msg.MsgType == 'image':
                    media_id = rec_msg.MediaId
                    reply_msg = reply.ImageMsg(to_user, from_user, media_id)
                    return reply_msg.send()
                else:
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
    ip = get_ip()
    app.run(host=ip, port=80)
