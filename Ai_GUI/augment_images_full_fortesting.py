from PIL import Image
import numpy as np
import math
import os
from colorsys import rgb_to_hsv, hsv_to_rgb


def resize_image(img_name):
    shorterside = 460
    pilimg = Image.open(img_name+".jpg")
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
    return flipped
    # save_image(flipped, img_name+"_horizontal_flip.jpg")


def vertical_flip(img, img_name):
    flipped = np.zeros_like(img)
    h = len(img)
    w = len(img[0])
    for i in range(len(img)):
        flipped[h-i-1] = img[i]
    return flipped
    # save_image(flipped, img_name+"_vertical_flip.jpg")


def rotate(img):
    h = len(img)
    w = len(img[0])
    rotated = np.zeros((w, h, 3))
    for i in range(w):
        for j in range(h):
            rotated[i][j] = img[h-j-1][i]
    return rotated


def rotate_full(img, img_name):
    rotated1 = rotate(img)
    # save_image(rotated, img_name+"_rotated_90.jpg")
    rotated2 = rotate(rotated1)
    # save_image(rotated, img_name+"_rotated_180.jpg")
    rotated3 = rotate(rotated2)
    # save_image(rotated, img_name+"_rotated_270.jpg")
    return rotated1, rotated2, rotated3


def random_brightness(img, img_name):
    rounds = 5
    images = []
    for r in range(rounds):
        brightness_multiplier = np.random.uniform() + 0.5
        brightened = np.zeros_like(img)
        for i in range(len(img)):
            for j in range(len(img[i])):
                (h,s,v) = rgb_to_hsv(img[i][j][0], img[i][j][1], img[i][j][2])
                v *= brightness_multiplier
                v = min(255, v)
                brightened[i][j] = hsv_to_rgb(h,s,v)
        images.append(brightened)
    return images
        # save_image(brightened, img_name+"_brightened_"+str(r)+".jpg")


def augment_image(img_name):
    img = resize_image(img_name)
    # crops
    stride_length = 3
    stride_pixels = 350

    h = len(img)
    w = len(img[0])

    if w > h:
      w_stride = np.int32(math.floor(float(stride_pixels)*w/float(h)))
      h_stride = stride_pixels
    elif h > w:
      h_stride = np.int32(math.floor(float(stride_pixels)*h/float(w)))
      w_stride = stride_pixels
    else:
      h_stride = stride_pixels
      w_stride = stride_pixels

    h_step = (h-h_stride)/(stride_length-1)
    w_step = (w-w_stride)/(stride_length-1)
    images = []
    for i in range(stride_length):
        for j in range(stride_length):
            cropped = img[int(i*h_step):int(i*h_step+h_stride), int(j*w_step):int(j*w_step+w_stride)]
            images.append(cropped)
            h,v,r1,r2,r3,b = transform_image(cropped, img_name+"_"+str(i)+"_"+str(j))
            images.append(h)
            images.append(v)
            images.append(r1)
            images.append(r2)
            images.append(r3)
            images.extend(b)
    return images


def transform_image(img, img_name):
    # transforms
    # save_image(img, img_name+".jpg")

    h = horizontal_flip(img, img_name)
    v = vertical_flip(img, img_name)
    r1, r2, r3 = rotate_full(img, img_name)
    b = random_brightness(img, img_name)
    return h,v,r1,r2,r3,b


# if __name__=='__main__':
    # directories = ["images"]
    # directories = ["benign", "malignant"]
    # directories = ["malignant"]
    # for img_dir in directories:
    #     files = os.listdir(img_dir)
    #     for filename in files:
    #         if filename.endswith("_train.jpg"):
    #             img_name = os.path.splitext(filename)[0]
    #             augment_image(os.path.join(img_dir, img_name))
