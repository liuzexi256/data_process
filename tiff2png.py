'''
Author: Zexi Liu
Date: 2021-07-22 16:45:40
LastEditors: Zexi Liu
LastEditTime: 2022-05-26 22:13:04
FilePath: /data_process/tiff2png.py
Description: 

Copyright (c) 2022 by Uisee, All Rights Reserved. 
'''
import os
import cv2

def tiff2png(input_dir, output_dir, format):
            files = os.listdir(input_dir)
            i = 1
            for f in files:
                file_name, file_extend = os.path.splitext(f)
                output_name = os.path.join(output_dir, file_name + format)
                if file_extend != '.tiff':
                    continue
                img = cv2.imread(os.path.join(input_dir, f))

                cv2.imwrite(output_name, img)
                print('{}/{}'.format(i, len(files)))
                i += 1

input_dir = '/home/zexi/Downloads/image_capturer_7'
output_dir = 'L1'
format = '.png'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

tiff2png(input_dir, output_dir, format)