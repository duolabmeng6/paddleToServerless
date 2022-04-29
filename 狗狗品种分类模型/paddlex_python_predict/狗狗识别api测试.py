import requests
import json
import cv2
import os
import base64
import numpy as np
import colorsys
import matplotlib.pyplot as plt

def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tostring()).decode('utf8')

if __name__ == '__main__':
    # 获取图片的base64编码格式
    img1 = cv2_to_base64(cv2.imread("Alaskan_malamute_00346.jpg"))
    img2 = cv2_to_base64(cv2.imread(r"C:\2022dl\guibing.jpg"))
    data = {'images': [img1,img2]}
    # 指定content-type
    headers = {"Content-type": "application/json"}
    # 发送HTTP请求
    url = "http://127.0.0.1:9000/predict/gougoupinzhongshibie"
    r = requests.post(url=url, headers=headers, data=json.dumps(data))

    # 打印预测结果
    print(r.json()["results"])
