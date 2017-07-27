from PIL import Image
import numpy as np
import math
import os
from colorsys import rgb_to_hsv, hsv_to_rgb


if __name__=='__main__':
    directories = ["benign", "malignant"]
    for img_dir in directories:
        for filename in os.listdir(img_dir):
            if filename.endswith(".png"):
                img_name = os.path.splitext(filename)[0]
                augment_image(os.path.join(img_dir, img_name))
