import os
import cv2

def tiff2png(input_dir, output_dir, format):
            files = os.listdir(input_dir)
            i = 1
            for f in files:
                file_name, file_extend = os.path.splitext(f)
                output_name = os.path.join(output_dir, file_name + format)
                if file_extend != '.tiff':
                    continue
                img = cv2.imread(os.path.join(input_dir, f))

                cv2.imwrite(output_name, img)
                print('{}/{}'.format(i, len(files)))
                i += 1

input_dir = '/media/uisee/Zexi/L1_new/dump_images/image_capturer_7'
output_dir = '/media/uisee/Zexi/L1_new/imgs'
format = '.png'
tiff2png(input_dir, output_dir, format)