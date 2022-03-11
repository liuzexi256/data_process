import os
from PIL import Image
import numpy as np

IMAGE_DIR = '/media/uisee/Zexi/jiashan_modified_v2.0_finished/cv2_mask/'

img_files = os.listdir(IMAGE_DIR)
for image_ in img_files:

    I = Image.open(IMAGE_DIR + image_)
    I = np.array(I)
    if 9 in I or 10 in I:
        for i in range(len(I)):
            for j in range(len(I[0])):
                if I[i][j] == 9:
                    I[i][j] = 10
                elif I[i][j] == 10:
                    I[i][j] = 9
    I = Image.fromarray(I)
    I.save('/media/uisee/Zexi/jiashan_modified_v2.0_finished/cv2_mask_modified/' + image_)