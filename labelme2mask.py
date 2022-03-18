import yaml
import argparse
import base64
import json
import os
import os.path as osp

import PIL.Image

from labelme.logger import logger
from labelme import utils
from math import *

def main():
    list_path = os.listdir(json_dir)      # 这是我的路径，替换成自己的就好
    for i in range(0, len(list_path)):
            #logger.warning('This script is aimed to demonstrate how to convert the'
            #               'JSON file to a single image dataset, and not to handle'
            #               'multiple JSON files to generate a real-use dataset.')

            parser = argparse.ArgumentParser()
            parser.add_argument('--json_file')
            parser.add_argument('-o', '--out', default=None)
            args = parser.parse_args()

            json_file = json_dir + list_path[i]         # 这是我的路径，替换成自己的就好
            print(list_path[i])
            if args.out is None:
                out_name = osp.basename(json_file).replace('.', '_')  # 返回文件名
                out_dir = osp.join(osp.dirname(labelme_dir), out_name)  # 把目录和文件名合成一个路径
            else:
                out_dir = args.out
            if not osp.exists(out_dir):
                os.mkdir(out_dir)  # 用于以数字权限模式创建目录

            data = json.load(open(json_file))
            imageData = data.get('imageData')

            if not imageData:
                imagePath = os.path.join(os.path.dirname(json_file), data['imagePath']) # os.path.dirname返回文件路径
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

            PIL.Image.fromarray(img).save(osp.join(out_dir, 'img.png'))
            utils.lblsave(osp.join(out_dir, 'label.png'), lbl)
            PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, 'label_viz.png'))

            with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
                for lbl_name in label_names:
                    f.write(lbl_name + '\n')

            #logger.warning('info.yaml is being replaced by label_names.txt')
            info = dict(label_names=label_names)
            with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
                yaml.safe_dump(info, f, default_flow_style=False)
            print(str(i) + '/' + str(len(list_path)))

            logger.info('Saved to: {}'.format(out_dir))
            x = out_dir+'\\label.png'

if __name__ == '__main__':
    #label_name_to_value = {'_background_': 0, 'line': 1, 'pole': 2, 'sign': 3, 'diam': 4, 'single_arrow': 5, 'double_arrow': 6, \
    #                        'sidewalk': 7, 'lane_a': 8, 'triangle': 9, 'stopline': 10, 'stopline_a': 11, 'triple_arrow': 12, \
    #                        'stop_marker': 13, 'circle_marker': 14}
    label_name_to_value = {'BG':0, 'white_lane':1, 'yellow_lane':2, 'white_long_lane':3, 'yellow_long_lane':4, 'pole':5, 'rect_sign':6, 'circle_sign':7, \
                'triangle_sign':8, 'diam':9, 'sidewalk':10, 'single_arrow':11, 'double_arrow':12, 'triple_arrow':13, 'triangle':14, 'stopline':15, \
                'dashed_stopline':16, 'yellow_decel_line':17, 'white_decel_line':18, 'guide_line':19, 'stop_marker':20, 'circle_marker':21, \
                'traffic_light':22, 'light_sign':23, 'direction_sign':24, 'fire_window':25, 'tunnel_groove':26, 'curb':27, 'tunnel_light':28}
    json_dir = '/media/uisee/Zexi/labeled_data/rgb/liangxiang/json/'
    labelme_dir = '/media/uisee/Zexi/labeled_data/rgb/liangxiang/labelme/'
    main()
