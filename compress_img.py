'''
Author: Zexi Liu
Date: 2022-03-31 10:46:46
LastEditors: Zexi Liu
LastEditTime: 2022-04-14 18:16:57
Description: rename and compress png images to mp4 video

Copyright (c) 2022 by Uisee, All Rights Reserved. 
'''

import os
import shutil
import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('input_dir', help='input images dir path')
args = parser.parse_args()

def rename(input_dir, output_dir, parent_dir, format):
    files = os.listdir(input_dir)
    files.sort()
    i = 1
    with open(parent_dir + '/timestamp.txt', 'w') as tf:
        for f in files:
            file_name, file_extend = os.path.splitext(f)
            output_name = '{:0=6}'.format(i) + format
            if file_extend != format:
                continue
            tf.writelines(file_name + '\n')
            input_img = os.path.join(os.path.abspath(input_dir), f)
            output_img = os.path.join(
                os.path.abspath(output_dir),  output_name)
            shutil.copy(input_img, output_img)
            print('{}/{}'.format(i, len(files)))
            i += 1

input_dir = args.input_dir
parent_dir = os.path.abspath(os.path.join(input_dir, os.pardir))
rename_dir = os.path.join(parent_dir, 'rename_imgs')
format = '.png'

if not os.path.exists(rename_dir):
    os.makedirs(rename_dir)

rename(input_dir, rename_dir, parent_dir, format)
subprocess.run(['ffmpeg', '-f', 'image2', '-i', rename_dir + '/%06d' + format,
               '-vcodec', 'libx264', parent_dir + '/imgs_compress.mp4'])
subprocess.run(['rm', '-rf', rename_dir])