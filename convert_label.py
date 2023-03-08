'''
Author: Zexi Liu
Date: 2022-07-25 17:51:00
LastEditors: Zexi Liu
LastEditTime: 2023-03-08 11:46:14
FilePath: /data_process/convert_label.py
Description:

Copyright (c) 2022 by Uisee, All Rights Reserved.
'''

import os

from tqdm import tqdm
import numpy as np
from PIL import Image
import cv2

def main():

    pred_list = os.listdir(input_dir)
    pred_list.sort()
    iou_list = []

    for pred in tqdm(pred_list):
        input_path = os.path.join(input_dir, pred)
        output_path = os.path.join(output_dir, pred)
        #pred_path = os.path.join(pt_dir, '1630563633_963148_00000487_0.png')
        converted_img = np.zeros((720, 1280))

        input_img = np.array(Image.open(input_path))
        input_img = input_img.tolist()
        for i in range(len(input_img)):
            for j in range(len(input_img[i])):
                if input_img[i][j] not in old_label:
                    print(input_img[i][j])
                else:
                    label = old_label.index(input_img[i][j])
                    converted_img[i][j] = label
        cv2.imwrite(output_path, converted_img)

    miou = np.mean(iou_list)
    return miou
if __name__ == '__main__':
    input_dir = '/data/xiaoU_test'
    output_dir = '/data/xiaoU_test_2'
    old_label = [[0, 0, 0], [63, 0, 63], [63, 63, 0], [0, 127, 127], [0, 127, 0], [0, 0, 127], [127, 127, 0], [127, 0, 127], [127, 0, 0]]
    main()
