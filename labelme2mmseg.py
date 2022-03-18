import os
import shutil

origin_dirs = "/media/uisee/Zexi/labeled_data/rgb/liangxiang/labelme/"

img_folder = "/media/uisee/Zexi/labeled_data/rgb/liangxiang/imgs/"
label_folder = "/media/uisee/Zexi/labeled_data/rgb/liangxiang/label/"
label_viz_folder = "/media/uisee/Zexi/labeled_data/rgb/liangxiang/label_viz/"

if not os.path.exists(img_folder):
    os.makedirs(img_folder)

if not os.path.exists(label_folder):
    os.makedirs(label_folder)

if not os.path.exists(label_viz_folder):
    os.makedirs(label_viz_folder)

FileNameList = os.listdir(origin_dirs)
for i in range(len(FileNameList)):
    name = FileNameList[i][:-5]
    shutil.copy(origin_dirs + FileNameList[i] + '/img.png', img_folder + name + '.png')
    shutil.copy(origin_dirs + FileNameList[i] + '/label.png', label_folder + name + '.png')
    shutil.copy(origin_dirs + FileNameList[i] + '/label_viz.png', label_viz_folder + name + '.png')
