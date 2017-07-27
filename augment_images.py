from PIL import Image
import numpy as np
import math
import os
from colorsys import rgb_to_hsv, hsv_to_rgb


def resize_image(img_name):
    shorterside = 500
    pilimg = Image.open(img_name+".png")
    w,h=pilimg.size

    if w > h:
      longerside= np.int32(math.floor(float(shorterside)*w/float(h)))
      neww=longerside
      newh=shorterside
    elif h > w:
      longerside= np.int32(math.floor(float(shorterside)*h/float(w)))
      newh=longerside
      neww=shorterside
    else:
      newh=shorterside
      neww=shorterside
    resimg=pilimg.resize((neww,newh))
    im = np.array(resimg,dtype=np.float32)

    if(im.ndim<3):
      im=np.expand_dims(im,2)
      im=np.concatenate((im,im,im),2)

    if(im.shape[2]>3):
      im=im[:,:,0:3]

    return im


def save_image(img, img_name):
    result = Image.fromarray(img.astype('uint8'))
    result.save(img_name)


def horizontal_flip(img, img_name):
    flipped = np.zeros_like(img)
    h = len(img)
    w = len(img[0])
    for i in range(len(img)):
        for j in range(len(img[i])):
            flipped[i][w-j-1] = img[i][j]
    save_image(flipped, img_name+"_horizontal_flip.jpg")


def vertical_flip(img, img_name):
    flipped = np.zeros_like(img)
    h = len(img)
    w = len(img[0])
    for i in range(len(img)):
        for j in range(len(img[i])):
            flipped[h-i-1][j] = img[i][j]
    save_image(flipped, img_name+"_vertical_flip.jpg")


def rotate(img):
    h = len(img)
    w = len(img[0])
    rotated = np.zeros((w, h, 3))
    for i in range(w):
        for j in range(h):
            rotated[i][j] = img[h-j-1][i]
    return rotated


def rotate_full(img, img_name):
    rotated = rotate(img)
    save_image(rotated, img_name+"_rotated_90.jpg")
    rotated = rotate(rotated)
    save_image(rotated, img_name+"_rotated_180.jpg")
    rotated = rotate(rotated)
    save_image(rotated, img_name+"_rotated_270.jpg")


def random_brightness(img, img_name):
    rounds = 10
    for r in range(rounds):
        brightness_multiplier = np.random.uniform() + 0.5
        brightened = np.zeros_like(img)
        for i in range(len(img)):
            for j in range(len(img[i])):
                (h,s,v) = rgb_to_hsv(img[i][j][0], img[i][j][1], img[i][j][2])
                v *= brightness_multiplier
                v = min(255, v)
                brightened[i][j] = hsv_to_rgb(h,s,v)
        save_image(brightened, img_name+"_brightened_"+str(r)+".jpg")


def augment_image(img_name):
    img = resize_image(img_name)

    # augmentation
    horizontal_flip(img, img_name)
    vertical_flip(img, img_name)
    rotate_full(img, img_name)
    random_brightness(img, img_name)


if __name__=='__main__':
    directories = ["benign", "malignant"]
    for img_dir in directories:
        for filename in os.listdir(img_dir):
            if filename.endswith(".png"):
                img_name = os.path.splitext(filename)[0]
                augment_image(os.path.join(img_dir, img_name))
