import os
import sys
import shutil
from random import sample
from collections import OrderedDict


if len(sys.argv) < 2:
    print('input val num')
    # print(sys.argv[0])
    exit()

valNum = int(sys.argv[1])

lst = os.listdir('all')
lst.remove('classes.txt')

for f in lst:
    if 'txt' not in f:
        extension = f.split('.')[-1]
        break
    elif 'jpg' not in f:
        extension = f.split('.')[-2]
        break

names = [i.split('.')[0] for i in lst]
names = list(OrderedDict.fromkeys(names))

valNames = sorted(sample(names, valNum))
names = sorted(list(set(names).difference(set(valNames))))

paths = [os.path.join('nutrition_image', 'train'),
         os.path.join('nutrition_image', 'val'),
         os.path.join('nutrition_labels', 'train'),
         os.path.join('nutrition_labels', 'val')]

for p in paths:
    os.makedirs(p)

trainPath = []
for fname in names:
    orgImgPath = os.path.join('all', f'{fname}.{extension}')
    newImgPath = os.path.join(paths[0], f'{fname}.{extension}')
    trainPath.append(os.path.abspath(newImgPath) + '\n')
    
    orgTxtPath = os.path.join('all', f'{fname}.txt')
    newTxtPath = os.path.join(paths[2], f'{fname}.txt')
    
    shutil.copy(orgImgPath, newImgPath)
    shutil.copy(orgTxtPath, newTxtPath)

valPath = []
for fname in valNames:
    orgImgPath = os.path.join('all', f'{fname}.{extension}')
    newImgPath = os.path.join(paths[1], f'{fname}.{extension}')
    valPath.append(os.path.abspath(newImgPath) + '\n')
    
    orgTxtPath = os.path.join('all', f'{fname}.txt')
    newTxtPath = os.path.join(paths[3], f'{fname}.txt')
    
    shutil.copy(orgImgPath, newImgPath)
    shutil.copy(orgTxtPath, newTxtPath)

with open('train.txt', 'w') as f:
    f.writelines(trainPath)
    
with open('val.txt', 'w') as f:
    f.writelines(valPath)
    
shutil.copy(os.path.join('all', 'classes.txt'), 'classes.names')
