'''
Author: Zexi Liu
Date: 2022-06-28 11:49:13
LastEditors: Zexi Liu
LastEditTime: 2022-06-28 18:38:13
FilePath: /data_process/ori2mmseg.py
Description: 

Copyright (c) 2022 by Uisee, All Rights Reserved. 
'''
import os
import json
import yaml
import math
import argparse
import base64
import shutil

import numpy as np
from collections import OrderedDict
import cv2
import PIL.Image
from tqdm import tqdm
from labelme.logger import logger
from labelme import utils

parser = argparse.ArgumentParser()
parser.add_argument('--orig_img_path', nargs='?', default='./', help='the path of orig img path')
parser.add_argument('--orig_json_file', nargs='?', default='./*.json', help='the marker json on new label tools online')
parser.add_argument('--main_dir_path', nargs='?', default='./', help='the path to save labelme type marker result')
args = parser.parse_args()

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

def origin2labelme(orig_img_path, orig_json_file, save_path):
    with open(orig_json_file, 'r') as f:
        orig_json = json.load(f, object_pairs_hook = OrderedDict)

    marker_nums = len(orig_json)
    for i in tqdm(range(marker_nums)):
        marker = orig_json[i]
        img_file = marker["file_obj"].split('/')[-1]
        img_path = os.path.join(orig_img_path, img_file)
        src = cv2.imread(img_path[:-3] + 'png')
        #assert src != None, 'Please check img path or img extension!'
        base64_data = base64.b64encode(cv2.imencode('.png', src)[1]).decode()
        img_name, _ = os.path.splitext(img_file)
        #print(str(i) + '/' + str(marker_nums))
        # no marker
        if marker["label_count"] == 0 or marker['status'] != 'FINISHED':
            continue
        # the path to save each img json result
        json_path = os.path.join(save_path, img_name + '.json')

        content_ext = OrderedDict()
        with open(json_path, 'w') as json_file:
            content_ext["version"] = "3.14.1"
            content_ext["flags"] = OrderedDict()

            shapes = []
            label_cnt = marker["label_count"]

            for i in range(label_cnt):
                result = marker["result"][i]
                content = OrderedDict()
                content["label"] = result["tagtype"]

                content["line_color"] = ''
                content["fill_color"] = ''
                points = []

                p1 = result["data"].split(',')
                length = len(p1)
                pt_cnt = int(math.floor(length / 3))
                for i in range(pt_cnt):
                    if p1[3 * i] == "[\"Z\"]":
                        break
                    pt = []
                    pt.append(float(p1[3 * i + 1]))
                    pt.append(float(p1[3 * i + 2].split(']')[0]))
                    points.append(pt)
                points.append(pt)

                if len(points) < 3:
                    continue

                content["points"] = points

                content["shape_type"] = "polygon"

                content["flags"] = OrderedDict()
                shapes.append(content)
            content_ext["shapes"] = shapes
            content_ext["lineColor"] = [0, 255, 0, 128]
            content_ext["fillColor"] = [255, 0, 0, 128]
            content_ext["imagePath"] = marker["file_obj"]
            content_ext["imageData"] = base64_data
            content_ext["imageHeight"] = 720
            content_ext["imageWidth"] = 1280
            #print(content_ext)
            json.dump(content_ext, json_file, sort_keys = False, indent = 4, cls=MyEncoder)

def labelme2mask(json_read_path, labelme_dir):
    list_path = os.listdir(json_read_path)
    for i in tqdm(range(len(list_path))):
        json_file = os.path.join(json_read_path, list_path[i])
        #print(list_path[i])

        out_name = os.path.basename(json_file).replace('.', '_')
        out_dir = os.path.join(labelme_dir, out_name)

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        data = json.load(open(json_file))
        imageData = data.get('imageData')

        if not imageData:
            imagePath = os.path.join(os.path.dirname(json_file), data['imagePath'])
            with open(imagePath, 'rb') as f:
                imageData = f.read()
                imageData = base64.b64encode(imageData).decode('utf-8')
        img = utils.img_b64_to_arr(imageData)

        
        for shape in sorted(data['shapes'], key=lambda x: x['label']):
            label_name = shape['label']
            if label_name in label_name_to_value:
                label_value = label_name_to_value[label_name]
            else:
                label_value = len(label_name_to_value)
                label_name_to_value[label_name] = label_value
        lbl = utils.shapes_to_label(
            img.shape, data['shapes'], label_name_to_value
        )

        label_names = [None] * (max(label_name_to_value.values()) + 1)
        for name, value in label_name_to_value.items():
            label_names[value] = name

        lbl_viz = utils.draw_label(lbl, img, label_names)

        PIL.Image.fromarray(img).save(os.path.join(out_dir, 'img.png'))
        utils.lblsave(os.path.join(out_dir, 'label.png'), lbl)
        PIL.Image.fromarray(lbl_viz).save(os.path.join(out_dir, 'label_viz.png'))

        with open(os.path.join(out_dir, 'label_names.txt'), 'w') as f:
            for lbl_name in label_names:
                f.write(lbl_name + '\n')

        #logger.warning('info.yaml is being replaced by label_names.txt')
        info = dict(label_names=label_names)
        with open(os.path.join(out_dir, 'info.yaml'), 'w') as f:
            yaml.safe_dump(info, f, default_flow_style=False)
        #print(str(i) + '/' + str(len(list_path)))

        #logger.info('Saved to: {}'.format(out_dir))

def labelme2mmseg(main_dir):

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
    for i in tqdm(range(len(FileNameList))):
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

if __name__ == '__main__':
    #label_name_to_value = {'_background_': 0, 'line': 1, 'pole': 2, 'sign': 3, 'diam': 4, 'single_arrow': 5, 'double_arrow': 6, \
    #                        'sidewalk': 7, 'lane_a': 8, 'triangle': 9, 'stopline': 10, 'stopline_a': 11, 'triple_arrow': 12, \
    #                        'stop_marker': 13, 'circle_marker': 14}
    label_name_to_value = {'BG':0, 'white_lane':1, 'yellow_lane':2, 'white_long_lane':3, 'yellow_long_lane':4, 'pole':5, 'rect_sign':6, 'circle_sign':7, \
                'triangle_sign':8, 'diam':9, 'sidewalk':10, 'single_arrow':11, 'double_arrow':12, 'triple_arrow':13, 'triangle':14, 'stopline':15, \
                'dashed_stopline':16, 'yellow_decel_line':17, 'white_decel_line':18, 'guide_line':19, 'stop_marker':20, 'circle_marker':21, \
                'traffic_light':22, 'light_sign':23, 'direction_sign':24, 'fire_window':25, 'tunnel_groove':26, 'curb':27, 'tunnel_light':28}

    img_read_path = args.orig_img_path
    json_read_path = args.orig_json_file
    main_dir = args.main_dir_path
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)

    #img_read_path = '/media/zexi/Zexi/labeled_data/rgb/lx/all_need_label/all_data'
    #json_read_path = '/media/zexi/Zexi/labeled_data/rgb/lx/batch_22--semantic.map.rgb_20220116_lx.sz.cargo.json'
    #main_dir = '/media/zexi/Zexi/labeled_data/lx'

    json_save_path = os.path.join(main_dir, 'json')
    labelme_save_path = os.path.join(main_dir, 'labelme')
    if not os.path.exists(json_save_path):
        os.makedirs(json_save_path)
    if not os.path.exists(labelme_save_path):
        os.makedirs(labelme_save_path)
    origin2labelme(img_read_path, json_read_path, json_save_path)
    labelme2mask(json_save_path, labelme_save_path)
    labelme2mmseg(main_dir)