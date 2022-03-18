import numpy as np
import os
import sys
import shutil
from PIL import Image

path = '/media/uisee/Zexi/Video/5/video5-12350'
newpath = '/media/uisee/Zexi/Video/dongfeng_need_label_1'
img_type = '.png'
frame_gap = 90
start_frame = 0
end_frame = 10000000

def turnto8(path):
        files = os.listdir(path)
        files = np.sort(files)
        num = 0
        for f in files:
            if os.path.isdir(os.path.join(path, f)):
                continue
            file_name, file_extend = os.path.splitext(f)
            new_name = file_name + img_type

            dirpath = newpath

            if num % frame_gap == 1:
                src = os.path.join(os.path.abspath(path), f)
                dst = os.path.join(os.path.abspath(dirpath), file_name + img_type)
                shutil.copy(src, dst)
                #img = Image.open(dst, "r").convert('L')
                #img = Image.open(dst, "r")
                #img.save(dst)
            num += 1
turnto8(path)