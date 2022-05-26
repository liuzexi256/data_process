'''
Author: Zexi Liu
Date: 2021-07-22 16:45:40
LastEditors: Zexi Liu
LastEditTime: 2022-05-25 15:52:01
FilePath: /data_process/tiff2gray.py
Description: 

Copyright (c) 2022 by Uisee, All Rights Reserved. 
'''

import numpy as np
import os
import sys
import shutil
from PIL import Image

path = '/home/zexi/Downloads/image_capturer_7'
newpath = 'L1'

def turnto8(path):
        files = os.listdir(path)
        files = np.sort(files)
        num = 0
        for f in files:
            if os.path.isdir(os.path.join(path, f)):
                continue
            file_name, file_extend = os.path.splitext(f)
            new_name = file_name + '.png'

            dirpath = newpath

            num_name = str(num)
            #while len(num_name) < 6:
            #    num_name = '0' + num_name
            #num_name = '_' + num_name

            src = os.path.join(os.path.abspath(path), f)
            #dst = os.path.join(os.path.abspath(dirpath), file_name + num_name + '.png')
            dst = os.path.join(os.path.abspath(dirpath), file_name + '.png')
            shutil.copy(src, dst)
            img = Image.open(dst, "r").convert('L')
            #img = Image.open(dst, "r")
            img.save(dst)
            num += 1

turnto8(path)