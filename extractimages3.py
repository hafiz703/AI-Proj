import os
from shutil import copy

cwd = os.path.dirname(os.path.realpath(__file__))      #path to current file
par_dir = os.path.split(cwd)[0]                        #path to parent directory
train_file =  os.path.join(par_dir,"breakhis_data/train_val_test_60_12_28/non_shuffled/split1/100X_train.txt")
val_file =  os.path.join(par_dir,"breakhis_data/train_val_test_60_12_28/non_shuffled/split1/100X_val.txt")
test_file =  os.path.join(par_dir,"breakhis_data/train_val_test_60_12_28/non_shuffled/split1/100X_test.txt")

os.makedirs("100X")
os.makedirs("100X/benign")
os.makedirs("100X/malignant")


with open(train_file) as f:
    for line in f:
        l = line.rstrip().split(" ")
        imageloc = os.path.join(par_dir,"breakhis_data/",l[0])
        if l[1] == "1":
            basename = os.path.basename(imageloc)
            copy(imageloc, "100X/malignant")
            os.rename("100X/malignant/"+basename, "100X/malignant/"+basename[:-4]+"_train.jpg")
        else:
            basename = os.path.basename(imageloc)
            copy(imageloc, "100X/benign")
            os.rename("100X/benign/"+basename, "100X/benign/"+basename[:-4]+"_train.jpg")


with open(val_file) as f:
    for line in f:
        l = line.rstrip().split(" ")
        imageloc = os.path.join(par_dir,"breakhis_data/",l[0])
        if l[1] == "1":
            basename = os.path.basename(imageloc)
            copy(imageloc, "100X/malignant")
            os.rename("100X/malignant/"+basename, "100X/malignant/"+basename[:-4]+"_val.jpg")
        else:
            basename = os.path.basename(imageloc)
            copy(imageloc, "100X/benign")
            os.rename("100X/benign/"+basename, "100X/benign/"+basename[:-4]+"_val.jpg")

with open(test_file) as f:
    for line in f:
        l = line.rstrip().split(" ")
        imageloc = os.path.join(par_dir,"breakhis_data/",l[0])
        if l[1] == "1":
            basename = os.path.basename(imageloc)
            copy(imageloc, "100X/malignant")
            os.rename("100X/malignant/"+basename, "100X/malignant/"+basename[:-4]+"_test.jpg")
        else:
            basename = os.path.basename(imageloc)
            copy(imageloc, "100X/benign")
            os.rename("100X/benign/"+basename, "100X/benign/"+basename[:-4]+"_test.jpg")
