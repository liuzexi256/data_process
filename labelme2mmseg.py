'''
Author: Zexi Liu
Date: 2022-01-13 17:53:46
LastEditors: Zexi Liu
LastEditTime: 2022-06-02 11:36:50
FilePath: /data_process/labelme2mmseg.py
Description: 

Copyright (c) 2022 by Uisee, All Rights Reserved. 
'''

import os
import shutil

main_dir = '/media/zexi/Zexi/labeled_data/lx'
origin_dirs = os.path.join(main_dir, 'labelme')

img_folder = os.path.join(main_dir, 'imgs')
label_folder = os.path.join(main_dir, 'label')
label_viz_folder = os.path.join(main_dir, 'label_viz')

if not os.path.exists(img_folder):
    os.makedirs(img_folder)

if not os.path.exists(label_folder):
    os.makedirs(label_folder)

if not os.path.exists(label_viz_folder):
    os.makedirs(label_viz_folder)

FileNameList = os.listdir(origin_dirs)
for i in range(len(FileNameList)):
    name = FileNameList[i][:-5]
    temp_img_dir = os.path.join(origin_dirs, FileNameList[i], 'img.png')
    temp_label_dir = os.path.join(origin_dirs, FileNameList[i], 'label.png')
    temp_label_viz_dir = os.path.join(origin_dirs, FileNameList[i], 'label_viz.png')
    
    temp_img_save_dir = os.path.join(img_folder, name + '.png')
    temp_label_save_dir = os.path.join(label_folder, name + '.png')
    temp_label_viz_save_dir = os.path.join(label_viz_folder, name + '.png')
    
    shutil.copy(temp_img_dir, temp_img_save_dir)
    shutil.copy(temp_label_dir, temp_label_save_dir)
    shutil.copy(temp_label_viz_dir, temp_label_viz_save_dir)
