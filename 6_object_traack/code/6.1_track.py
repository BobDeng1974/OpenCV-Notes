#-*- coding: utf-8 -*-

import cv2
import numpy as np

'''
    帧差法实现目标追踪
    @author 2019-1-22  19:56
    
    第一帧设为背景--> frame灰度化+高斯模糊 -->计算差异-->寻找轮廓 设定阈值 -->绘框并显示

'''
camera = cv2.VideoCapture(0)

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,4))
kernel = np.ones((5,5), np.uint8)
background = None

while(True):
    ret, frame = camera.read()
    if background is  None:
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background, (21,21), 0)
        continue


    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    diff = cv2.absdiff(background, gray_frame)
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.dilate(diff, es, iterations=2)

    image, cnts, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < 1500:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)

    cv2.imshow("contours", frame)
    cv2.imshow("diff", diff)
    if cv2.waitKey(50) & 0xff == ord("q"):
        break

    cv2.destroyAllWindows()
    camera.release()




























