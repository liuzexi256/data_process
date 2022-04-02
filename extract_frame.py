import numpy as np
import os
import cv2
import sys
import shutil

input_dir = '/media/uisee/Zexi/20210701/dump_images/image_capturer_7'
output_dir = '/media/uisee/Zexi/L1_need_label'
#img_type = '.png'
frame_gap = 3
start_frame = 0
end_frame = 10000000

def extract(input_dir):
        files = os.listdir(input_dir)
        files = np.sort(files)
        num = 0
        for f in files:
            if os.path.isdir(os.path.join(input_dir, f)):
                continue
            #file_name, file_extend = os.path.splitext(f)

            if num % frame_gap == 1:
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
                    if file_extend != '.tiff':
                        continue
                    img = cv2.imread(os.path.join(input_dir, f))

                    cv2.imwrite(output_name, img)
                    print('{}/{}'.format(i, len(files)))
                i += 1

extract_and_convert(input_dir, output_dir, '.png')