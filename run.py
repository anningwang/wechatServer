# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify
from wechat import handle
from tools.getip import get_ip

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Flask!'


@app.route('/api/wx',  methods=['GET', 'POST'])
def api_wx():
    return handle.WxHandle.process_request(request.method, request.args, request.data)


@app.route('/api/wx/token',  methods=['GET', 'POST'])
def api_wx_token():
    param = request.form if request.json is None else request.json
    print 'request.form=', request.form, 'request.json=', request.json, 'param=', param
    return jsonify(handle.WxHandle.get_token(param))


if __name__ == '__main__':
    ip = get_ip()
    app.run(host=ip, port=80)
