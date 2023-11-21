import os
import sys
import shutil
from random import sample
from collections import OrderedDict


if len(sys.argv) < 2:
    print('input val num')
    # print(sys.argv[0]) 0 --> 檔案名稱 1 --> 參數
    exit()

valNum = int(sys.argv[1])
# print(valNum)

lst = os.listdir('all') # for返回all資料夾，all 也可以以路徑取代
lst.remove('classes.txt')

lst_jpg = [];
lst_png = [];

jpg_format = ""
png_format = ""

for f in lst:
    # f = 01.jpg
    extension = f.split('.')[-1] # 副檔名
    match extension:
        case "png":
            lst_png.append(f)
            png_format = 'png'
        case "jpg":
            lst_jpg.append(f)
            jpg_format = 'jpg'

    # if 'txt' not in f:
    #     extension = f.split('.')[-1] # 保留最後一段
    #     break
    # elif 'jpg' not in f:
    #     extension = f.split('.')[-2]
    #     break
    # elif 'png' not in f:
    #     extension = f.split('.')[-3]
    #     break
    # else:
    #     extension = f.split('.')[-1]
    #     break

lst_jpg = [i.split('.')[0] for i in lst_jpg]
lst_png = [i.split('.')[0] for i in lst_png]

names = [i.split('.')[0] for i in lst] # 01, 02 ,03
names = list(OrderedDict.fromkeys(names))
# OrderedDict.fromkeys(names) 統一賦予names裡的value，但目前沒有
# list()把所有資料放入list裡面

valNames = sorted(sample(names, valNum))
# sample(x, k=len(x))，隨機取樣
names = sorted(list(set(names).difference(set(valNames))))
# 建立包含 names 和 valNames 的集合並取差集，留下新資料並排序
#以上在做隨機分配測試跟訓練的資料


paths = [os.path.join('nutrition_image', 'train'),
         os.path.join('nutrition_image', 'val'),
         os.path.join('nutrition_labels', 'train'),
         os.path.join('nutrition_labels', 'val')]

for p in paths:
    os.makedirs(p)  # 創建目錄，如果已有目錄存在會拋出OSError的錯誤

trainPath = [] # list
for fname in names:
    if fname in lst_jpg:

        orgJpgPath = os.path.join('all', f'{fname}.{jpg_format}')  # all\檔案名.jpg
        newJpgPath = os.path.join(paths[0], f'{fname}.{jpg_format}')  # train\檔案名
        trainPath.append(os.path.abspath(newJpgPath) + '\n')
        shutil.copy(orgJpgPath, newJpgPath)

        # orgImgPath = os.path.join('all', f'{fname}.{jpg_format}')  # all\檔案名.jpg
        # newImgPath = os.path.join(paths[0], f'{fname}.{jpg_format}')  # train\檔案名
        # trainPath.append(os.path.abspath(newImgPath) + '\n')
        # shutil.copy(orgImgPath, newImgPath)
    elif fname in lst_png:

        orgPngPath = os.path.join('all', f'{fname}.{png_format}')  # all\檔案名.jpg
        newPngPath = os.path.join(paths[0], f'{fname}.{png_format}')  # train\檔案名
        trainPath.append(os.path.abspath(newPngPath) + '\n')
        shutil.copy(orgPngPath, newPngPath)

        # orgImgPath = os.path.join('all', f'{fname}.{png_format}')  # all\檔案名.jpg
        # newImgPath = os.path.join(paths[0], f'{fname}.{png_format}')  # train\檔案名
        # trainPath.append(os.path.abspath(newImgPath) + '\n')
        # shutil.copy(orgImgPath, newImgPath)

    # orgImgPath = os.path.join('all', f'{fname}.{extension}')  # all\檔案名.jpg
    # newImgPath = os.path.join(paths[0], f'{fname}.{extension}')  # train\檔案名
    # trainPath.append(os.path.abspath(newImgPath) + '\n')
    else:
        orgTxtPath = os.path.join('all', f'{fname}.txt')
        newTxtPath = os.path.join(paths[2], f'{fname}.txt')


        shutil.copy(orgTxtPath, newTxtPath)

valPath = []
for fname in valNames:

    if fname in lst_jpg:

        orgJpgPath = os.path.join('all',f'{fname}.{jpg_format}')
        newJpgPath = os.path.join(paths[1], f'{fname}.{jpg_format}')
        valPath.append(os.path.abspath(newJpgPath) + '\n')
        shutil.copy(orgJpgPath, newJpgPath)
    elif fname in lst_png:
        orgPngPath = os.path.join('all', f'{fname}.{png_format}')
        newPngPath = os.path.join(paths[1], f'{fname}.{png_format}')
        valPath.append(os.path.abspath(newPngPath) + '\n')
        shutil.copy(orgPngPath, newPngPath)
    else:
        orgTxtPath = os.path.join('all', f'{fname}.txt')
        newTxtPath = os.path.join(paths[3], f'{fname}.txt')
        shutil.copy(orgTxtPath, newTxtPath)


    # orgImgPath = os.path.join('all', f'{fname}.{extension}')
    # newImgPath = os.path.join(paths[1], f'{fname}.{extension}')
    # valPath.append(os.path.abspath(newImgPath) + '\n')


with open('train.txt', 'w') as f:
    f.writelines(trainPath)
    
with open('val.txt', 'w') as f:
    f.writelines(valPath)
    
shutil.copy(os.path.join('all', 'classes.txt'), 'classes.names')