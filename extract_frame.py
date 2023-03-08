'''
Author: Zexi Liu
Date: 2022-05-31 12:01:32
LastEditors: Zexi Liu
LastEditTime: 2023-01-19 13:47:02
FilePath: /data_process/extract_frame.py
Description:

Copyright (c) 2022 by Uisee, All Rights Reserved.
'''
import numpy as np
import os
import cv2
import sys
import shutil
from tqdm import tqdm

def extract(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    files = os.listdir(input_dir)
    files = np.sort(files)
    num = 0
    for f in tqdm(files):
        if os.path.isdir(os.path.join(input_dir, f)):
            continue
        #file_name, file_extend = os.path.splitext(f)

        if num % frame_gap == 0:
            src = os.path.join(os.path.abspath(input_dir), f)
            dst = os.path.join(os.path.abspath(output_dir), f)
            shutil.copy(src, dst)

        num += 1

def extract_and_convert(input_dir, output_dir, format):
    files = os.listdir(input_dir)
    i = 1
    for f in files:
        if i % frame_gap == 1:
            file_name, file_extend = os.path.splitext(f)
            output_name = os.path.join(output_dir, file_name + format)
            if file_extend != '.png':
                continue
            img = cv2.imread(os.path.join(input_dir, f))

            cv2.imwrite(output_name, img)
            print('{}/{}'.format(i, len(files)))
        i += 1

if __name__ == '__main__':
    input_dir = '/data/light_need_label_lx_night'
    output_dir = '/data/light_need_label_lx_night_less'
    #img_type = '.png'
    frame_gap = 2
    start_frame = 0
    end_frame = 10000000
    #extract_and_convert(input_dir, output_dir, '.png')
    extract(input_dir, output_dir)