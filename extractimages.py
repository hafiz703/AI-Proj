import os
from shutil import copy

cwd = os.path.dirname(os.path.realpath(__file__))      #path to current file
par_dir = os.path.split(cwd)[0]                        #path to parent directory
train_file =  os.path.join(par_dir,"breakhis_data/train_val_test_60_12_28/non_shuffled/split1/100X_train.txt")
val_file =  os.path.join(par_dir,"breakhis_data/train_val_test_60_12_28/non_shuffled/split1/100X_val.txt")
test_file =  os.path.join(par_dir,"breakhis_data/train_val_test_60_12_28/non_shuffled/split1/100X_test.txt")

# os.makedirs("100X_train")
# os.makedirs("100X_train/benign")
# os.makedirs("100X_train/malignant")
os.makedirs("100X_val")
os.makedirs("100X_val/benign")
os.makedirs("100X_val/malignant")
os.makedirs("100X_test")
os.makedirs("100X_test/benign")
os.makedirs("100X_test/malignant")

# with open(train_file) as f:
#     for line in f:
#         l = line.rstrip().split(" ")
#         imageloc = os.path.join(par_dir,"breakhis_data/",l[0])
#         if l[1] == "1":
#             copy(imageloc, "100X_train/malignant")
#         else:
#             copy(imageloc, "100X_train/benign")

with open(val_file) as f:
    for line in f:
        l = line.rstrip().split(" ")
        imageloc = os.path.join(par_dir,"breakhis_data/",l[0])
        if l[1] == "1":
            copy(imageloc, "100X_val/malignant")
        else:
            copy(imageloc, "100X_val/benign")

with open(test_file) as f:
    for line in f:
        l = line.rstrip().split(" ")
        imageloc = os.path.join(par_dir,"breakhis_data/",l[0])
        if l[1] == "1":
            copy(imageloc, "100X_test/malignant")
        else:
            copy(imageloc, "100X_test/benign")
