'''
Author: Zexi Liu
Date: 2023-03-06 18:12:37
LastEditors: Zexi Liu
LastEditTime: 2023-03-07 16:43:51
FilePath: /data_process/view_res.py
Description:

Copyright (c) 2023 by Uisee, All Rights Reserved.
'''
import cv2
import numpy as np


image = cv2.imread("/data/demo.png")
#image = cv2.resize(image, (384, 384))

f = open('/data/res.txt')

labels = []
scores = []
boxes = []
box = []
flag = 0
for line in open("/data/res.txt"):
    line = line[:-2]
    if line[0] == '*':
        boxes.append(box)
        box = []
        flag = 0
        continue
    if flag == 0:
        labels.append(float(line))
        flag += 1
    elif flag == 1:
        scores.append(float(line))
        flag += 1
    elif flag == 2:
        if float(line) < 0:
            labels.pop()
            labels.append(-1)
        box.append(int(float(line)))

f.close()
for i in range(10):
    if labels[i] == -1:
        continue
    draw_1 = cv2.rectangle(image, (boxes[i][0],boxes[i][1]), (boxes[i][2],boxes[i][3]), (0,255,0), 2)

cv2.imshow("draw_0", draw_1)

cv2.waitKey(0)