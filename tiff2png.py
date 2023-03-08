'''
Author: Zexi Liu
Date: 2021-07-22 16:45:40
LastEditors: Zexi Liu
LastEditTime: 2023-03-08 11:45:18
FilePath: /data_process/tiff2png.py
Description:

Copyright (c) 2022 by Uisee, All Rights Reserved.
'''
import os
from tqdm import tqdm
import cv2

def tiff2png(input_dir, output_dir, format):
    files = os.listdir(input_dir)
    files.sort()
    i = 1
    for f in tqdm(files):
        file_name, file_extend = os.path.splitext(f)
        output_name = os.path.join(output_dir, file_name + format)
        if file_extend != '.tiff':
            continue
        img = cv2.imread(os.path.join(input_dir, f))

        cv2.imwrite(output_name, img)
        #print('{}/{}'.format(i, len(files)))
        i += 1


if __name__ == '__main__':
    input_dir = '/home/zexi/ceph/gy/20210723_liangxiang_zaochen/dump_images_0723/image_capturer_7'
    output_dir = '/data/20210723_liangxiang_zaochen/dump_images_0723'
    format = '.png'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tiff2png(input_dir, output_dir, format)