import os
cwd = os.path.dirname(os.path.realpath(__file__))
magnification = "100X"
train_file = magnification+"_train.txt"
val_file = magnification+"_val.txt"
test_file = magnification+"_test.txt"
hi = os.path.join(cwd,"train_val_test_60_12_28","non_shuffled","split1",train_file)

for root, dirs, files in os.walk(r'train_val_test_60_12_28'):
    print(root)
print (hi)
if "train" in train_file:
    print("YASIA")

with open(hi, 'r') as f:
  for line in f:
      print(line)
      break
