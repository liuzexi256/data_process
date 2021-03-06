import os
import json
import math
import argparse
import base64

import numpy as np
from collections import OrderedDict
import cv2
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--orig_img_path', nargs='?', default='./', help='the path of orig img path')
parser.add_argument('--orig_json_file', nargs='?', default='./*.json', help='the marker json on new label tools online')
#parser.add_argument('--save_path', nargs='?', default='./labelme_marker', help='the path to save labelme type marker result')
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

def transform_to_label_type(orig_img_path, orig_json_file, save_path):
    with open(orig_json_file, 'r') as f:
        orig_json = json.load(f, object_pairs_hook = OrderedDict)

    marker_nums = len(orig_json)
    for i in tqdm(range(marker_nums)):
        marker = orig_json[i]

        img_file = marker["file_obj"].split('/')[-1]
        img_path = os.path.join(orig_img_path, img_file)
        src = cv2.imread(img_path[:-3] + 'png')
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

if __name__ == '__main__':
    orig_img_path = args.orig_img_path
    orig_json_file = args.orig_json_file
    #save_path = args.save_path

    json_save_path = os.path.join(os.path.dirname(os.path.abspath(orig_img_path)), 'json')
    if not os.path.exists(json_save_path):
        os.makedirs(json_save_path)
    #orig_img_path = '/media/zexi/Zexi/labeled_data/lx_sz_cargo_need_label_new'
    #orig_json_file = '/media/zexi/Zexi/labeled_data/batch_22--semantic.map.rgb_20220116_lx.sz.cargo.json'
    #save_path = '/media/zexi/Zexi/labeled_data/lx/json'
    transform_to_label_type(orig_img_path, orig_json_file, json_save_path)
