import os
from PIL import Image
import numpy as np

IMAGE_DIR = '/home/uisee/Desktop/test_data/results_MultiLoop_New/'

img_files = os.listdir(IMAGE_DIR)
for image_ in img_files:

    I = Image.open(IMAGE_DIR + image_) 
    box = (176,93,1135,633)
    a = np.array(I)
    I = I.crop(box)
    img_deal = I.resize((1280, 720),Image.ANTIALIAS)
    #img_deal.show()
    #I.show()
    img_deal.save('L1data_MultiLoop_mask_black_new/' + image_)
a = 1