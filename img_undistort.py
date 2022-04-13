'''
Author: Zexi Liu
Date: 2022-04-08 10:21:02
LastEditors: Zexi Liu
LastEditTime: 2022-04-13 16:28:37
FilePath: /data_process/img_undistort.py
Description: image undistort

Copyright (c) 2022 by Uisee, All Rights Reserved. 
'''
import numpy as np
import os
import cv2
 

input_dir = '/media/uisee/Zexi/doudian_need_label'
output_dir = '/media/uisee/Zexi/doudian_need_label_python'
R = np.eye(3)
img_size = (1280, 720)
camera_matrix = np.array( [960.07010948, 0, 670.79225889, 0, 959.49102760, 353.78707256, 0, 0, 1, ]).reshape([3, 3])
distortion_coefficients = np.array( [-0.36911477, 0.12326040, -0.00049742, 0.00018606]).reshape([4, 1])

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

new_K, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, img_size, 0, img_size)
mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, distortion_coefficients, R, new_K, img_size, cv2.CV_16SC2)

files = os.listdir(input_dir)
num = 1
for file in files:
    img_in_dir = os.path.join(input_dir, file)
    img_in = cv2.imread(img_in_dir)
    img_out = cv2.remap(img_in, mapx, mapy, cv2.INTER_LINEAR)
    
    img_out_dir = os.path.join(output_dir, file)
    cv2.imwrite(img_out_dir, img_out)
    print('{}/{}'.format(num, len(files)))
    num += 1
#img_in = cv2.imread('1.png')
#img_out = cv2.undistort(img_in, camera_matrix, distortion_coefficients, None, new_K)
#cv2.imwrite('test.png', img_out)

#mapx, mapy = cv2.fisheye.initUndistortRectifyMap(camera_matrix, distortion_coefficients, R, new_K, img_size, cv2.CV_16SC2)
#srcImg = cv.imread("camera.bmp")
#resultImg = cv2.remap(srcImg, mapx, mapy, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)