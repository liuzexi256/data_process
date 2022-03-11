import os
import shutil

IMAGE_DIR = '/media/uisee/Zexi/wlmq_images/hx'
FIND_DIR = '/media/uisee/Zexi/all_train_data/training/imgs/'
SAVE_DIR = '/media/uisee/Zexi/all_train_data/val/'
#img_files = os.listdir(IMAGE_DIR)

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

with open('/media/uisee/Zexi/all_train_data/val.txt', 'r') as f:
    img_files = f.readlines()


for item in img_files:
    #rgb_item = item[:-3] + 'png'
    rgb_item = item[:-1] + '.png'
    shutil.copy(FIND_DIR + rgb_item, SAVE_DIR)
