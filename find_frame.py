import os
import shutil
import json
from collections import OrderedDict

IMAGE_DIR = '/media/uisee/Zexi/wlmq_images/hx'
FIND_DIR = '/data/20210903_vv6car3_yuantong2/dump_images_2/image_capturer_7/'
SAVE_DIR = '/media/uisee/Zexi/doudian_need_label/'
#img_files = os.listdir(IMAGE_DIR)

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

#with open('/media/uisee/Zexi/all_train_data/val.txt', 'r') as f:
#    img_files = f.readlines()

with open('/media/uisee/Zexi/labeled_data/doudian_need_label/batch_27--semantic.map.rgb_20220216_dd.json', 'r') as f:
    json = json.load(f)

for i in range(len(json)):
    marker = json[i]
    img_file = marker["file_obj"].split('/')[-1]
    target = img_file[:-3] + 'tiff'
    shutil.copy(FIND_DIR + target, SAVE_DIR)
    a = 1

for item in img_files:
    #rgb_item = item[:-3] + 'png'
    rgb_item = item[:-1] + '.png'
    shutil.copy(FIND_DIR + rgb_item, SAVE_DIR)
