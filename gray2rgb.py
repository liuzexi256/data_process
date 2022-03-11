import numpy as np
import cv2
import os

path = '/data'
save_path = '/data'
#colors = [(0,0.5,0.5), (0.5,0,0.5), (0.5,0.5,0), (0,1,1), (0,1,0), (0,0,1), (1,1,0), (1,0,1), (1,0,0)]
colors = [[255,255,255], [153,51,250], [0,255,127], [255,215,0], [0,199,140], [0,0,255], [0,255,0], [255,0,255], [255,127,80], [255,97,0], [128,42,42], [255,0,0]]

files = os.listdir(path)
files = np.sort(files)

for f in files:

    #src = cv2.imread(path + f, 0)
    src = cv2.imread('/data/1642561761.340967_00026467_0.png', 0)
    src = np.reshape(src, -1)

    final_RGB = np.zeros([720, 1280, 3])
    src_RGB = np.zeros([720, 1280, 3])
    final_RGB = np.reshape(final_RGB, (-1, 3))
    src_RGB = np.reshape(src_RGB, (-1, 3))
    for i in range(1, len(colors)):
        idxes = (src == i)
        src_RGB[:,0] = colors[i][2] * idxes
        src_RGB[:,1] = colors[i][1] * idxes
        src_RGB[:,2] = colors[i][0] * idxes
        final_RGB += src_RGB
    final_RGB = final_RGB.astype(np.uint8)
    final_RGB = np.reshape(final_RGB, (720,1280,3))

   #cv2.imwrite(save_path + f, final_RGB)
    cv2.imwrite('/data/1642561761.340967_00026467_0_rgb.png', final_RGB)
