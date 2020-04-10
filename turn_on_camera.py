#!/usr/bin/env python
#coding=utf-8

import numpy as np
import cv2
import time
import datetime
from json import JSONDecoder
from PIL import Image
import requests
import base64

cap = cv2.VideoCapture(0)

''' 人脸识别 '''

def christmas(img,x,y,w,h):
    im = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    # 你的贴纸地址
    mark1=Image.open("/home/dong/catkin_ws/src/rc-home-edu-learn-ros/rchomeedu_speech/scripts/hat.png")
    mark2=Image.open("/home/dong/catkin_ws/src/rc-home-edu-learn-ros/rchomeedu_speech/scripts/123.png")
    height = int(w *300/649)
    height0 = int(height*12/10)
    height1 = int(height*8/10)
    rh = int(height*4/3)
    rh2 = int(height*1/6)
    rw2 = int(height)
    w1 = int(w*6/10)
    mark1 = mark1.resize((w, rh))
    mark2 = mark2.resize((rw2, rh2))
    layer=Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark1, (x, y-height0))
    layer.paste(mark2, (x, y+height1))
    layer.paste(mark2,(x+w1, y+height1))
    out=Image.composite(layer, im, layer)
    img = cv2.cvtColor(np.asarray(out), cv2.COLOR_RGB2BGR)
    return img

#videoWriter = cv2.VideoWriter('testwrite.avi', cv2.VideoWriter_fourcc(*'MJPG'), 15, (1000,563))

def detect_face(img):
    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    # 你要调用API的URL
    key = "PWJdVEHsvYVJnUHv4ZUAiLO6O-SAKYA7"
    secret = "Tf8KG-YQizdS81TEhBeHpnftPFf8mES8"
    # face++提供的一对密钥
    filepath1 = "zhaopian.jpg"
    # 图片文件的绝对路径
    frame = cv2.imread('zhaopian.jpg')  # 使用opencv打开照片为了下面标框
    data = {"api_key": key, "api_secret": secret, "return_attributes": "gender,age,smiling,beauty"}
    # 必需的参数，注意key、secret、"gender,age,smiling,beauty"均为字符串，与官网要求一致
    files = {"image_file": open(filepath1, "rb")}
    '''以二进制读入图像，这个字典中open(filepath1, "rb")返回的是二进制的图像文件，所以"image_file"是二进制文件，符合官网要求'''
    response = requests.post(http_url, data=data, files=files)
    # POTS上传
    req_con = response.content.decode('utf-8')
    # response的内容是JSON格式
    req_dict = JSONDecoder().decode(req_con)
    # 对其解码成字典格式
    face_rectangles = []
    #print(req_dict)
    # 输出
    for face in req_dict['faces']:  # 使用循环遍历 reqdict里面的faces部分  把里面提取到的脸的定位给获取出来
        if 'face_rectangle' in face.keys():
            face_rectangles.append(face['face_rectangle'])
    #print(face_rectangles)
    #frame = beautify_face(frame)
    for i in face_rectangles:
        w = i['width']
        t = i['top']
        l = i['left']
        h = i['height']
        cv2.rectangle(frame, (l, t), (w + l, h + t), (0, 0, 255), 2)  # opencv的标框函数
        img = christmas(img,l,t,w,h)
        cv2.imshow("tiezhi",img)
        cv2.imwrite('tiezhi.jpg',img)
        cv2.waitKey(0)
    return img


def beautify_face(img):
    key = "5Ut_EUtu3dG8Q60UBQdj8_LICgc4KByR"
    secret = "cWXtsKOMx62m8zHUx810MG-0oGoOnhSO"
    filepath = "zhaopian.jpg"
    http_url = "https://api-cn.faceplusplus.com/facepp/v1/beautify"
    files = {"image_file": open(filepath, "rb")}
    data = {"api_key": key, "api_secret": secret}
    response = requests.post(http_url, data=data, files=files)
    req_dict = response.json()
    #print(req_dict)
    src = req_dict['result']
    data = src.split(',')[0]
    image_data = base64.b64decode(data)

    with open('meiyan.jpg', 'wb') as f:
        f.write(image_data)
    img1 = cv2.imread('meiyan.jpg')
    cv2.imshow("meiyan.jpg",img1)
    cv2.waitKey(0)
    return img1;


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # 重新定义图片大小
        img = cv2.resize(frame,(800,563))
        cv2.imshow('frame',img)
        if cv2.waitKey(10) & 0xFF == ord('s'):
            print("保存图片")
            cv2.imwrite('zhaopian.jpg',img)
            detect_face(img)
            beautify_face(img)
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
