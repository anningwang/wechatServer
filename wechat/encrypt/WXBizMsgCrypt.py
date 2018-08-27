#!/usr/bin/env python
# -*- encoding:utf-8 -*-

""" 对公众平台发送给公众账号的消息加解密示例代码.
@copyright: Copyright (c) 1998-2014 Tencent Inc.

"""
# ------------------------------------------------------------------------

import base64
import string
import random
import hashlib
import time
import struct
from Crypto.Cipher import AES
import xml.etree.cElementTree as cElementTree
import socket
import error


"""
关于Crypto.Cipher模块，ImportError: No module named 'Crypto'解决方案
请到官方网站 https://www.dlitz.net/software/pycrypto/ 下载 pycrypto。
下载后，按照README中的“Installation”小节的提示进行 pycrypto 安装。

or
pip install pycrypto
"""


class FormatException(Exception):
    pass


def throw_exception(message, exception_class=FormatException):
    """my define raise exception function"""
    raise exception_class(message)


class SHA1:
    """计算公众平台的消息签名接口"""
    def __init__(self):
        pass

    def get_sha1(self, token, timestamp, nonce, encrypt):
        """用SHA1算法生成安全签名
        @param token:  票据
        @param timestamp: 时间戳
        @param encrypt: 密文
        @param nonce: 随机字符串
        @return: 安全签名
        """
        try:
            sort_list = [token, timestamp, nonce, encrypt]
            sort_list.sort()
            sha = hashlib.sha1()
            sha.update("".join(sort_list))
            return error.WXBizMsgCrypt_OK, sha.hexdigest()
        except Exception, e:
            print e
            return error.WXBizMsgCrypt_ComputeSignature_Error, None


class XMLParse:
    """提供提取消息格式中的密文及生成回复消息格式的接口"""
    def __init__(self):
        pass

    # xml消息模板
    AES_TEXT_RESPONSE_TEMPLATE = """<xml>
    <Encrypt><![CDATA[%(msg_encrypt)s]]></Encrypt>
    <MsgSignature><![CDATA[%(msg_signature)s]]></MsgSignature>
    <TimeStamp>%(timestamp)s</TimeStamp>
    <Nonce><![CDATA[%(nonce)s]]></Nonce>
    </xml>
    """

    def extract(self, xml_text):
        """提取出xml数据包中的加密消息
        @param xml_text: 待提取的xml字符串
        @return: 提取出的加密消息字符串
        """
        try:
            xml_tree = cElementTree.fromstring(xml_text)
            encrypt = xml_tree.find("Encrypt")
            to_user_name = xml_tree.find("ToUserName")
            return error.WXBizMsgCrypt_OK, encrypt.text, to_user_name.text
        except Exception, e:
            print e
            return error.WXBizMsgCrypt_ParseXml_Error, None, None

    def generate(self, encrypt, signature, timestamp, nonce):
        """生成xml消息
        @param encrypt: 加密后的消息密文
        @param signature: 安全签名
        @param timestamp: 时间戳
        @param nonce: 随机字符串
        @return: 生成的xml字符串
        """
        resp_dict = {
                    'msg_encrypt': encrypt,
                    'msg_signature': signature,
                    'timestamp': timestamp,
                    'nonce': nonce,
                     }
        resp_xml = self.AES_TEXT_RESPONSE_TEMPLATE % resp_dict
        return resp_xml


class PKCS7Encoder:
    """提供基于 PKCS7 算法的加解密接口"""
    block_size = 32

    def __init__(self):
        pass

    def encode(self, text):
        """ 对需要加密的明文进行填充补位
        @param text: 需要进行填充补位操作的明文
        @return: 补齐明文字符串
        """
        text_length = len(text)
        # 计算需要填充的位数
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        # 获得补位所用的字符
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, decrypted):
        """删除解密后明文的补位字符
        @param decrypted: 解密后的明文
        @return: 删除补位字符后的明文
        """
        pad = ord(decrypted[-1])
        if pad < 1 or pad > 32:
            pad = 0
        return decrypted[:-pad]


class Prpcrypt(object):
    """提供接收和推送给公众平台消息的加解密接口"""

    def __init__(self, key):
        # self.key = base64.b64decode(key+"=")
        self.key = key
        # 设置加解密模式为AES的CBC模式
        self.mode = AES.MODE_CBC

    def encrypt(self, text, appid):
        """对明文进行加密
        @param text: 需要加密的明文
        @param appid:
        @return: 加密得到的字符串
        """
        # 16位随机字符串添加到明文开头
        text = self.get_random_str() + struct.pack("I", socket.htonl(len(text))) + text + appid
        # 使用自定义的填充方式对明文进行补位填充
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)
        # 加密
        encryption = AES.new(self.key, self.mode, self.key[:16])
        try:
            cipher_text = encryption.encrypt(text)
            # 使用BASE64对加密后的字符串进行编码
            return error.WXBizMsgCrypt_OK, base64.b64encode(cipher_text)
        except Exception, e:
            print e
            return error.WXBizMsgCrypt_EncryptAES_Error, None

    def decrypt(self, text, appid):
        """对解密后的明文进行补位删除
        @param text: 密文
        @param appid:
        @return: 删除填充补位后的明文
        """
        try:
            encryption = AES.new(self.key, self.mode, self.key[:16])
            # 使用BASE64对密文进行解码，然后AES-CBC解密
            plain_text = encryption.decrypt(base64.b64decode(text))
        except Exception, e:
            print e
            return error.WXBizMsgCrypt_DecryptAES_Error, None
        try:
            pad = ord(plain_text[-1])
            # 去掉补位字符串
            # pkcs7 = PKCS7Encoder()
            # plain_text = pkcs7.encode(plain_text)
            # 去除16位随机字符串
            content = plain_text[16:-pad]
            xml_len = socket.ntohl(struct.unpack("I", content[: 4])[0])
            xml_content = content[4: xml_len+4]
            from_appid = content[xml_len+4:]
        except Exception, e:
            print e
            return error.WXBizMsgCrypt_IllegalBuffer, None
        if from_appid != appid:
            return error.WXBizMsgCrypt_ValidateAppid_Error, None
        return 0, xml_content

    def get_random_str(self):
        """ 随机生成16位字符串
        @return: 16位字符串
        """
        rule = string.letters + string.digits
        str_ret = random.sample(rule, 16)
        return "".join(str_ret)


class WXBizMsgCrypt(object):
    # 构造函数
    # @param token: 公众平台上，开发者设置的Token
    # @param encoding_aes_key: 公众平台上，开发者设置的EncodingAESKey
    # @param appid: 企业号的AppId
    def __init__(self, token, encoding_aes_key, appid):
        try:
            self.key = base64.b64decode(encoding_aes_key+"=")
            assert len(self.key) == 32
        except Exception, e:
            print e
            throw_exception("[error]: EncodingAESKey invalid !", FormatException)
            # return error.WXBizMsgCrypt_IllegalAesKey)
        self.token = token
        self.appid = appid

    def encrypt_msg(self, reply_msg, nonce, timestamp=None):
        # 将公众号回复用户的消息加密打包
        # @param reply_msg: 企业号待回复用户的消息，xml格式的字符串
        # @param nonce: 随机串，可以自己生成，也可以用URL参数的nonce
        # @param timestamp: 时间戳，可以自己生成，也可以用URL参数的timestamp,如为None则自动用当前时间
        # encrypt_msg: 加密后的可以直接回复用户的密文，包括msg_signature, timestamp, nonce, encrypt的xml格式的字符串,
        # return：成功0，encrypt_msg,失败返回对应的错误码None
        pc = Prpcrypt(self.key)
        ret, encrypt = pc.encrypt(reply_msg, self.appid)
        if ret != 0:
            return ret, None
        if timestamp is None:
            timestamp = str(int(time.time()))
        # 生成安全签名
        sha1 = SHA1()
        ret, signature = sha1.get_sha1(self.token, timestamp, nonce, encrypt)
        if ret != 0:
            return ret, None
        xml_parse = XMLParse()
        return ret, xml_parse.generate(encrypt, signature, timestamp, nonce)

    def decrypt_msg(self, post_data, msg_signature, timestamp, nonce):
        # 检验消息的真实性，并且获取解密后的明文
        # @param post_data: 密文，对应POST请求的数据
        # @param msg_signature: 签名串，对应URL参数的msg_signature
        # @param timestamp: 时间戳，对应URL参数的timestamp
        # @param nonce: 随机串，对应URL参数的nonce
        # @return: 成功0，失败返回对应的错误码
        # xml_content: 解密后的原文，当return返回0时有效
        # 验证安全签名
        xml_parse = XMLParse()
        ret, encrypt, to_user_name = xml_parse.extract(post_data)
        if ret != 0:
            return ret, None
        sha1 = SHA1()
        ret, signature = sha1.get_sha1(self.token, timestamp, nonce, encrypt)
        if ret != 0:
            return ret, None
        if not signature == msg_signature:
            return error.WXBizMsgCrypt_ValidateSignature_Error, None
        pc = Prpcrypt(self.key)
        ret, xml_content = pc.decrypt(encrypt, self.appid)
        return ret, xml_content
