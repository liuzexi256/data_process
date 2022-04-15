'''
Author: Zexi Liu
Date: 2022-04-02 11:35:32
LastEditors: Zexi Liu
LastEditTime: 2022-04-14 18:16:46
Description: decompress and rename imgs from imgs_compress.mp4 and timestamp.txt

Copyright (c) 2022 by Uisee, All Rights Reserved. 
'''

import os
import shutil
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_dir', help='input mp4 video path')
args = parser.parse_args()

def resume(input_dir, parent_dir, format):
    output_dir = os.path.join(parent_dir, 'resume_imgs')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = os.listdir(input_dir)
    files.sort()
    i = 1
    with open(parent_dir + '/timestamp.txt', 'r') as tf:
        for f in files:
            file_name = tf.readline()[:-1]

            output_name = file_name + format

            input_img = os.path.join(os.path.abspath(input_dir), f)
            output_img = os.path.join(os.path.abspath(output_dir),  output_name)
            shutil.copy(input_img, output_img)
            print('{}/{}'.format(i, len(files)))
            i += 1

input_dir = args.input_dir
parent_dir = os.path.abspath(os.path.join(input_dir, os.pardir))
decompress_dir = os.path.join(parent_dir, 'decompress_imgs')
format = '.png'

if not os.path.exists(decompress_dir):
    os.makedirs(decompress_dir)

subprocess.run(['ffmpeg', '-i', input_dir, decompress_dir + '/%06d' + format])
resume(decompress_dir, parent_dir, format)
subprocess.run(['rm', '-rf', decompress_dir])