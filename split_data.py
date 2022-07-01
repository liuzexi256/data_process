'''
Author: Zexi Liu
Date: 2022-01-19 14:47:39
LastEditors: Zexi Liu
LastEditTime: 2022-06-30 14:48:07
FilePath: /data_process/split_data.py
Description: 

Copyright (c) 2022 by Uisee, All Rights Reserved. 
'''
import os
import random

def main():
    total_file = os.listdir(file_path)
    num = len(total_file)
    list = range(num)
    tv = int(num * trainval_percent) #trainval num
    tr = int(tv * train_percent) #train num
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    ftrainval = open(os.path.join(txt_save_path,'trainval.txt'), 'w')
    ftest = open(os.path.join(txt_save_path,'test.txt'), 'w')
    ftrain = open(os.path.join(txt_save_path,'train.txt'), 'w')
    fval = open(os.path.join(txt_save_path,'val.txt'), 'w')

    for i in list:
        name = total_file[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()

if __name__=='__main__':
    trainval_percent = 1 #train and val data percent
    train_percent = 0.8 #train data percent in train and val data 
    file_path = '/media/zexi/Zexi/train_data/rgb/all_train_data/train/anno' #file path
    txt_save_path = '/media/zexi/Zexi/train_data/rgb/all_train_data' #result save path

    random.seed(2022)
    main()