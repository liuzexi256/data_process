import os
from libtiff import TIFF
import imageio

def tiff_to_jpg(src, dst):
            files = os.listdir(src)
            i = 1
            for f in files:
                tif = TIFF.open(os.path.join(src, f), mode = 'r')
                for im in list(tif.iter_images()):
                    file_name, file_extend = os.path.splitext(f)
                    new_path = os.path.join(dst, file_name + '.jpg')
                    imageio.imsave(new_path, im)
                    print('{}/{}'.format(i, len(files)))
                    i += 1
                    print('successfully saved!!!')

src = "doudian_need_label"
dst = "doudian_need_label_jpg"
tiff_to_jpg(src, dst)