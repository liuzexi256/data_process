'''
Author: Zexi Liu
Date: 2023-01-12 13:58:32
LastEditors: Zexi Liu
LastEditTime: 2023-01-12 14:06:23
FilePath: /data_process/img_resize.py
Description:

Copyright (c) 2023 by Uisee, All Rights Reserved.
'''
import os
import cv2
from tqdm import tqdm

def main():
    img_files = os.listdir(IMAGE_READ_DIR)
    img_files.sort()
    for image_ in tqdm(img_files):

        img = cv2.imread(IMAGE_READ_DIR + image_)
        cut_img = cv2.resize(img, (3840, 2160))
        cv2.imwrite(IMAGE_SAVE_DIR + image_, cut_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

if __name__ == '__main__':
    IMAGE_READ_DIR = '/data/uos_cv/install/data/light_ori/'
    IMAGE_SAVE_DIR = '/data/uos_cv/install/data/light_2160p/'
    if not os.path.exists(IMAGE_SAVE_DIR):
        os.makedirs(IMAGE_SAVE_DIR)
    main()