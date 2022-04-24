# coding=utf-8
import cv2
from flask import Flask, send_file
from flask import request
import json
import time
import base64
import re
import numpy as np
import getModelResult as getModelResult

app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
    return send_file("static/index.html")


import socket


def check_port_in_use(port, host='127.0.0.1'):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        return True
    except socket.error:
        return False
    finally:
        if s:
            s.close()

@app.route("/initialize", methods=['GET', 'POST'])
def initialize():
    # while check_port_in_use(9001) == False:
    #     print("waiting for http server start")
    #     time.sleep(1)

    return "Initialization successful"

@app.route("/invoke", methods=['GET', 'POST'])
def invoke():
    return "invoke successful"

@app.route("/get_test_image", methods=['GET', 'POST'])
def get_test_image():
    return send_file("static/test.jpg")



def rt_success(msg="", time=0, result=None):
    return {
        "code": 200,
        "msg": msg,
        "time": time,
        "result": result
    }


def rt_error(code, msg="", time=0, result=None):
    return {
        "code": code,
        "msg": msg,
        "time": time,
        "result": result
    }


@app.route("/put_base64", methods=['GET', 'POST'])
def put_base64():
    if request.method == 'GET':
        return rt_error(500, "post")

    src = request.form.get('data')
    threshold = request.values.get('threshold')
    nms_threshold = request.values.get('nms_threshold')

    if (src == None):
        response = request.get_json()
        src = response['data']
        try:
            threshold = response['threshold']
            nms_threshold = response['nms_threshold']
        except:
            pass

    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
    else:
        raise Exception("Do not parse!")
    result = getModelResult.getResult(data, float(threshold), float(nms_threshold))
    return json.dumps(result)


@app.route('/put', methods=['GET', 'POST'])
def put():
    if request.method == 'GET':
        return rt_error(500, "post")

    threshold = request.values.get('threshold')
    nms_threshold = request.values.get('nms_threshold')

    f = request.files['image']
    data = f.read()
    f.close()

    img = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(img, cv2.IMREAD_ANYCOLOR)
    data = base64.b64encode(image.tostring()).decode('utf8')
    result = getModelResult.getResult(data, float(threshold), float(nms_threshold))
    return json.dumps(result)


@app.route('/show', methods=['GET', 'POST'])
def show():
    return send_file("static/index.html")


@app.route('/apidoc', methods=['GET', 'POST'])
def apidoc():
    return send_file("static/api.html")

if __name__ == '__main__':
    app.debug = False
    app.threaded = False
    app.run(port=9000, host='0.0.0.0')
