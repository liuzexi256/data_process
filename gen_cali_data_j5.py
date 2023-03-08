'''
Author: Zexi Liu
Date: 2022-12-16 10:57:59
LastEditors: Zexi Liu
LastEditTime: 2023-02-28 16:46:55
FilePath: /data_process/gen_cali_data.py
Description:

Copyright (c) 2022 by Uisee, All Rights Reserved.
'''

import os

import numpy as np
from tqdm import tqdm
import cv2
from PIL import Image
import matplotlib.pyplot as plt

def letterbox(im, new_shape=(2176, 3840), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border

    return im, r, (dw, dh)

def data_read(filename):
    img = cv2.imread(filename)
    image = img.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image, ratio, dwdh = letterbox(image, auto=False)

    image = image.transpose((2, 0, 1))
    image = np.expand_dims(image, 0)
    image = np.ascontiguousarray(image)
    image = image.astype(np.float32)
    #image = image / 255
    return image

def data_read_centermask(filename):
    pixel_mean = np.array([103.53, 116.28, 123.675])
    pixel_mean = pixel_mean.reshape((3, 1, 1))
    pixel_std = np.array([1.0, 1.0, 1.0])
    pixel_std = pixel_std.reshape((3, 1, 1))
    img = cv2.imread(filename)


    pil_image = Image.fromarray(img)
    pil_image = pil_image.resize((384, 384), 2)
    image = np.asarray(pil_image)
    image = image.transpose((2, 0, 1))
    image = (image - pixel_mean) / pixel_std

    image = np.expand_dims(image, 0)
    image = np.ascontiguousarray(image)
    image = image.astype(np.float32)

    return image

def data_read_dlo(filename):
    img = cv2.imread(filename)
    image = img.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = image.astype(np.float32)
    image = image * (1 / 57.5331) + (-117.0376 / 57.5331)
    image = cv2.resize(image, (368, 208), interpolation=cv2.INTER_LINEAR)

    #image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    #image = image.transpose((2, 0, 1))
    #image = np.expand_dims(image, 0)
    image = np.ascontiguousarray(image)

    #image = image / 255
    return image

def main():
    files_list = os.listdir(data_path)
    files_list.sort()
    num = 0
    a = np.fromfile('/data/J5/horizon_j5_open_explorer_v1.1.37-py38_20230106/calib_centermask_j5_nomean/0.bin', dtype='float32')
    a = a.reshape((3, 384, 384))
    # a = a.tolist()
    # b = cv2.imread('/data/J5/horizon_j5_open_explorer_v1.1.19_20220801/images/1663323503.628924.jpg')

    for i in tqdm(range(len(files_list))):
        temp_file = os.path.join(data_path, files_list[i])
        save_file = os.path.join(cali_save_path, str(num) + '.bin')
        img = data_read_centermask(temp_file)
        #img = data_read_dlo(temp_file)
        #cv2.imwrite(save_file, img)
        img.tofile(save_file)

        num += 1

if __name__ == '__main__':
    data_path = '/data/J5/horizon_j5_open_explorer_v1.1.37-py38_20230106/calib_jixi_0103/'
    cali_save_path = '/data/J5/horizon_j5_open_explorer_v1.1.37-py38_20230106/calib_centermask_j5'
    if not os.path.exists(cali_save_path):
        os.makedirs(cali_save_path)
    main()