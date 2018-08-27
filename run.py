# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify, render_template
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


@app.route('/api/wx/qrcode',  methods=['GET', 'POST'])
def api_wx_qrcode():
    return render_template('qrcode.html')


@app.route('/api/wx/weui',  methods=['GET', 'POST'])
def api_wx_weui():
    return render_template('weui.html')


if __name__ == '__main__':
    ip = get_ip()
    app.run(host=ip, port=80)
