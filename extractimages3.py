import os, sys
from shutil import copy

cwd = os.path.dirname(os.path.realpath(__file__))      #path to current file
par_dir = os.path.split(cwd)[0]                        #path to parent directory
magnification = sys.argv[1]
split = sys.argv[2]

dir_name=magnification+"_"+split
train_file =  os.path.join(par_dir,"breakhis_data/train_val_test_60_12_28/non_shuffled/"+split+"/"+magnification+"_train.txt")
val_file =  os.path.join(par_dir,"breakhis_data/train_val_test_60_12_28/non_shuffled/"+split+"/"+magnification+"_val.txt")
test_file =  os.path.join(par_dir,"breakhis_data/train_val_test_60_12_28/non_shuffled/"+split+"/"+magnification+"_test.txt")

os.makedirs(dir_name)
os.makedirs(dir_name+"/benign")
os.makedirs(dir_name+"/malignant")


with open(train_file) as f:
    for line in f:
        l = line.rstrip().split(" ")
        imageloc = os.path.join(par_dir,"breakhis_data/",l[0])
        if l[1] == "1":
            basename = os.path.basename(imageloc)
            copy(imageloc, dir_name+"/malignant")
            os.rename(dir_name+"/malignant/"+basename, dir_name+"/malignant/"+basename[:-4]+"_train.jpg")
        else:
            basename = os.path.basename(imageloc)
            copy(imageloc, magnification+"_"+split+"/benign")
            os.rename(dir_name+"/benign/"+basename, dir_name+"/benign/"+basename[:-4]+"_train.jpg")


with open(val_file) as f:
    for line in f:
        l = line.rstrip().split(" ")
        imageloc = os.path.join(par_dir,"breakhis_data/",l[0])
        if l[1] == "1":
            basename = os.path.basename(imageloc)
            copy(imageloc, dir_name+"/malignant")
            os.rename(dir_name+"/malignant/"+basename, dir_name+"/malignant/"+basename[:-4]+"_val.jpg")
        else:
            basename = os.path.basename(imageloc)
            copy(imageloc, dir_name+"/benign")
            os.rename(dir_name+"/benign/"+basename, dir_name+"/benign/"+basename[:-4]+"_val.jpg")

with open(test_file) as f:
    for line in f:
        l = line.rstrip().split(" ")
        imageloc = os.path.join(par_dir,"breakhis_data/",l[0])
        if l[1] == "1":
            basename = os.path.basename(imageloc)
            copy(imageloc, dir_name+"/malignant")
            os.rename(dir_name+"/malignant/"+basename, dir_name+"/malignant/"+basename[:-4]+"_test.jpg")
        else:
            basename = os.path.basename(imageloc)
            copy(imageloc, dir_name+"/benign")
            os.rename(dir_name+"/benign/"+basename, dir_name+"/benign/"+basename[:-4]+"_test.jpg")


# python extractimages3.py 100X split3
