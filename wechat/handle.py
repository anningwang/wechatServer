# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import urllib
import json
from . import reply, receive, get_access_token_for_wx


class WxHandle(object):
    @staticmethod
    def process_request(method, args, xml=None):
        obj = args
        print 'args=', obj

        signature = obj.get('signature')
        timestamp = obj.get('timestamp')
        nonce = obj.get('nonce')
        if method == 'GET':
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
                open_id = obj.get('openid')
                print 'openid=', open_id
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
                elif isinstance(rec_msg, receive.EventMsg):
                    to_user = rec_msg.FromUserName
                    from_user = rec_msg.ToUserName
                    if rec_msg.Event == 'CLICK' and isinstance(rec_msg, receive.Click):
                        if rec_msg.EventKey == 'mpGuide':
                            content = u"编写中，尚未完成".encode('utf-8')
                            reply_msg = reply.TextMsg(to_user, from_user, content)
                            WxHandle.get_union_id(open_id, get_access_token_for_wx)
                            return reply_msg.send()

                print "暂且不处理"
                return reply.Msg().send()
            except Exception, a:
                print 'args', a
                return a

    @staticmethod
    def get_union_id(open_id, access_token):
        """
        接口调用请求说明
        http请求方式: GET
        https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
        :param open_id:
        :param access_token:
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % \
              (access_token, open_id)
        resp = urllib.urlopen(url)
        print resp
        resp = json.loads(resp.read())
        print resp
