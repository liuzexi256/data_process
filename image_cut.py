'''
Author: Zexi Liu
Date: 2021-07-22 16:45:40
LastEditors: Zexi Liu
LastEditTime: 2022-12-26 18:09:37
FilePath: /data_process/image_cut.py
Description:

Copyright (c) 2022 by Uisee, All Rights Reserved.
'''
import os
import cv2
from tqdm import tqdm

def main():
    img_files = os.listdir(IMAGE_READ_DIR)
    img_files.sort()
    for image_ in tqdm(img_files):

        img = cv2.imread(IMAGE_READ_DIR + image_)
        cut_img = img[720:1440, 1280:2560]
        cv2.imwrite(IMAGE_SAVE_DIR + image_, cut_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

if __name__ == '__main__':
    IMAGE_READ_DIR = '/media/zexi/Zexi/j5/light_need_label_dd_2160p/light_need_label_dd_2160p_2/'
    IMAGE_SAVE_DIR = '/media/zexi/Zexi/j5/light_need_label_dd_2160p/light_need_label_dd_720p_2/'
    if not os.path.exists(IMAGE_SAVE_DIR):
        os.makedirs(IMAGE_SAVE_DIR)
    main()