#读取文件夹下的文件并将其文件名（无后缀）分成4份保存在保存在一个txt文件中
#作者：阿玉
#时间：2020.5.12
#说明：文件分为训练集、验证集和测试集，tranval为训练集和验证机的合集。
#为了划分数据集写的
#可修改参数：将被划分的文件夹路径，存储txt文件的路径及4个文件的名字，固定随机数的seed，
#训练集和验证集的占比，共8个参数

import os
import random

trainval_percent = 1 #确定用于训练的数据占比
train_percent = 0.8 #确定在用于训练的数据中，训练集的占比
xmlfilepath = '/media/uisee/Zexi/train_data/gray/all_train_data_compress/training/anno_extract' #将被划分的xml文件
txtsavepath = '/media/uisee/Zexi/train_data/gray/all_train_data_compress' #划分后 得到的txt保存的地方

#固定随机数的生成
random.seed(2022)

total_xml = os.listdir(xmlfilepath) #读取文件夹下所有文件的名字
num = len(total_xml) #文件夹下文件的数目
list = range(num)
tv = int(num * trainval_percent) #trainval的数目
tr = int(tv * train_percent) #train的数目
trainval = random.sample(list, tv) #被选中的文件编号
train = random.sample(trainval, tr)

ftrainval = open(os.path.join(txtsavepath,'trainval.txt'), 'w') #打开文件等待写入
ftest = open(os.path.join(txtsavepath,'test.txt'), 'w')
ftrain = open(os.path.join(txtsavepath,'train.txt'), 'w')
fval = open(os.path.join(txtsavepath,'val.txt'), 'w')

for i in list:
    name = total_xml[i][:-4] + '\n' #去后缀，换行
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
