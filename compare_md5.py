'''
Author: Zexi Liu
Date: 2022-07-12 16:22:31
LastEditors: Zexi Liu
LastEditTime: 2022-07-13 15:54:01
FilePath: /data_process/compare_md5.py
Description: 

Copyright (c) 2022 by Uisee, All Rights Reserved. 
'''

import os
import subprocess

from tqdm import tqdm

def main():
    files_list_1 = os.listdir(data_path_1)
    files_list_2 = os.listdir(data_path_2)
    files_list_1.sort()
    files_list_2.sort()
    md5_list_1 = []
    md5_list_2 = []
    with open('md5_list_1.txt', 'w') as f:
        for i in tqdm(range(len(files_list_1))):
            temp_file = os.path.join(data_path_1, files_list_1[i])
            out_bytes = subprocess.check_output(['md5sum', temp_file])
            out_text = out_bytes.decode('utf-8')
            out_text = out_text.split(' ')
            assert len(out_text[0]) == 32, 'Split Error!'
            md5_list_1.append(out_text[0])
            f.writelines(out_text[0] + '\n')
    with open('labeled_bin.txt', 'w') as lf:

        with open('md5_list_2.txt', 'w') as f:
            for i in tqdm(range(len(files_list_2))):
                temp_file = os.path.join(data_path_2, files_list_2[i])
                out_bytes = subprocess.check_output(['md5sum', temp_file])
                out_text = out_bytes.decode('utf-8')
                out_text = out_text.split(' ')
                assert len(out_text[0]) == 32, 'Split Error!'
                if out_text[0] in md5_list_1:
                    print('Find labeled bin!')
                    print(md5_list_1.index(out_text[0]))
                    lf.writelines(str(md5_list_1.index(out_text[0])) + '\n')
                md5_list_2.append(out_text[0])
                f.writelines(out_text[0] + '\n')

if __name__ == '__main__':
    data_path_1 = '/data/dataset/pcd_data_0721/bin'
    data_path_2 = '/data/ceph/UCLF_robotaxi_MSIF/20210721_vv6car3_sence_liangxiang/bins'

    main()
