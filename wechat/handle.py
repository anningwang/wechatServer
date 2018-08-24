# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
from . import reply, receive


class WxHandle(object):
    @staticmethod
    def process_request(method, args, xml=None):
        obj = args
        print 'args=', obj
        if method == 'GET':
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
                web_data = xml
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
            except Exception, a:
                print 'args', a
                return a
