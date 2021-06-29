# !/usr/bin/python
# --coding:utf-8--
# Data: 2021/4/28

import os
import numpy as np
import cv2
import json
from PIL import Image
from tqdm import tqdm

def getCornerPoint(org_img):
    greyPic = cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)
    # 二值化
    # threshold(src, thresh, maxval, type, dst=None)
    # src是输入数组，thresh是阈值的具体值，maxval是type取THRESH_BINARY或者THRESH_BINARY_INV时的最大值
    # type有5种类型,这里取0：THRESH_BINARY ，当前点值大于阈值时，取maxval，也就是前一个参数，否则设为0
    # 该函数第一个返回值是阈值的值，第二个是阈值化后的图像
    ret, binPic = cv2.threshold(greyPic, greyPic.mean(), 255, cv2.THRESH_BINARY)
    # print('ret is:', ret)
    # cv2.imshow("binPic", binPic)  #

    # 中值滤波
    median = cv2.medianBlur(binPic, 5)

    # 找轮廓
    # findContours()有三个参数：输入图像，层次类型和轮廓逼近方法
    # 该函数会修改原图像，建议使用img.copy()作为输入
    # 由函数返回的层次树很重要，cv2.RETR_TREE会得到图像中轮廓的整体层次结构，以此来建立轮廓之间的‘关系'。
    # 如果只想得到最外面的轮廓，可以使用cv2.RETE_EXTERNAL。这样可以消除轮廓中其他的轮廓，也就是最大的集合
    # 该函数有三个返回值：修改后的图像，图像的轮廓，它们的层次
    contours, hierarchy = cv2.findContours(median, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(org_img_copy, contours, -1, (0, 255, 0), 2)
    # cv2.imshow("org_img_copy", org_img_copy)        #

    # 获取最小外接矩形
    maxArea = 0
    # 挨个检查看那个轮廓面积最大
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > cv2.contourArea(contours[maxArea]):
            maxArea = i
    hull = cv2.convexHull(contours[maxArea])
    hull = np.squeeze(hull)
    # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
    rect = cv2.minAreaRect(hull)
    # 通过box绘出矩形框
    box = np.int0(cv2.boxPoints(rect))
    # draw_img = cv2.drawContours(org_img_copy, [box], -1, (0, 0, 255), 2)
    # cv2.imshow("org_img_box", draw_img)        #

    # 调整图片角度
    center = rect[0]
    angle = rect[2]
    if angle > 45:
        angle = angle - 90
    elif angle < -45:
        angle = 90 + angle
    # print('rect[2] is:', rect[2])
    # print('angle is:', angle)
    # 旋转矩阵
    M = cv2.getRotationMatrix2D(center, angle, 1)
    h, w, c = org_img.shape
    # 旋转图片
    dst = cv2.warpAffine(org_img, M, (w, h))
    # cv2.imshow("dst", dst)  #
    # 坐标变换
    poly_r = np.asarray([(M[0][0] * x + M[0][1] * y + M[0][2],
                          M[1][0] * x + M[1][1] * y + M[1][2]) for (x, y) in box])

    # 裁剪图片
    x_s, y_s = np.int0(poly_r.min(axis=0))
    x_e, y_e = np.int0(poly_r.max(axis=0))
    # 设置预留边框
    border = 10
    x_s = int(max((x_s - border), 0))
    y_s = int(max((y_s - border), 0))
    x_e = int(min((x_e + border), w))
    y_e = int(min((y_e + border), h))

    # 剪裁
    cut_img = dst[y_s:y_e, x_s:x_e, :]
    # cv2.imshow("cut_img", cut_img)  #

    return cut_img


if __name__ == "__main__":
    BASE_DIR = "C:\\Work\\project\\U01\\Wei_U01_Package\\0507\\撞边，脏污，异物\\"
    OUT_SLICE = "C:\\Work\\project\\U01\\Wei_U01_Package\\image_0507_output\\"

    img_list = os.listdir(BASE_DIR)
    # print(img_list)
    for img_file in tqdm(img_list):
        org_img = Image.open(BASE_DIR + img_file)
        org_img = cv2.cvtColor(np.asarray(org_img), cv2.COLOR_RGB2BGR)

        cut_img = getCornerPoint(org_img)
        new_img_file = img_file[:-4] + '.jpg'
        # cv2.imshow("cut_img", cut_img)
        cv2.imwrite(OUT_SLICE + new_img_file, cut_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
