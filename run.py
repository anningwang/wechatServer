# -*- coding:utf-8 -*-

from flask import Flask, request
from wechat import handle
import platform
import socket

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Flask!'


@app.route('/api/wx',  methods=['GET', 'POST'])
def api_wx():
    handle.WxHandle.process_request(request.method, request.args, request.data)


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
