import os
import sys
import shutil
from random import sample
from collections import OrderedDict

if len(sys.argv) < 2:
    print('input val num')
    exit()

valNum = int(sys.argv[1])
# print(sys.argv[0]) 0 --> 檔案名稱 1 --> 參數

lst = os.listdir('C:/Users/shin/410828608/yolov7-main/mydataset/all')  # for返回all資料夾，all 也可以以路徑取代
lst.remove('classes.txt')

lst_jpg = []
lst_png = []

jpg_format = ""
png_format = ""

for f in lst:
    # f = 01.jpg
    extension = f.split('.')[-1]  # 副檔名
    if extension == "jpg":
        lst_jpg.append(f)
        jpg_format = 'jpg'
    elif extension == "png":
        lst_png.append(f)
        png_format = 'png'
    # elif len(extension.split()) != 2:
    #     print(extension)

# match extension:
#     case "png":
#         lst_png.append(f)
#         png_format = 'png'
#     case "jpg":
#         lst_jpg.append(f)
#         jpg_format = 'jpg'


lst_jpg = [i.split('.')[0] for i in lst_jpg]
lst_png = [i.split('.')[0] for i in lst_png]

names = [i.split('.')[0] for i in lst]  # 01, 02 ,03
names = list(OrderedDict.fromkeys(names))
# OrderedDict.fromkeys(names) 統一賦予names裡的value，但目前沒有
# list()把所有資料放入list裡面

valNames = sorted(sample(names, valNum))
# sample(x, k=len(x))，隨機取樣
names = sorted(list(set(names).difference(set(valNames))))
# 建立包含 names 和 valNames 的集合並取差集，留下新資料並排序
# 以上在做隨機分配測試跟訓練的資料


paths = [os.path.join('images', 'train'),
         os.path.join('images', 'val'),
         os.path.join('labels', 'train'),
         os.path.join('labels', 'val')]

for p in paths:
    os.makedirs(p)  # 創建目錄，如果已有目錄存在會拋出OSError的錯誤

trainPath = []  # list

for fname in names:

    if fname in lst_jpg:
        orgJpgPath = os.path.join('all', f'{fname}.{jpg_format}')  # all\檔案名.jpg
        newJpgPath = os.path.join(paths[0], f'{fname}.{jpg_format}')  # train\檔案名
        trainPath.append(os.path.abspath(newJpgPath) + '\n')
        shutil.copy(orgJpgPath, newJpgPath)

        orgTxtPath = os.path.join('all', f'{fname}.txt')  # f-string
        newTxtPath = os.path.join(paths[2], f'{fname}.txt')
        shutil.copy(orgTxtPath, newTxtPath)

    elif fname in lst_png:
        orgPngPath = os.path.join('all', f'{fname}.{png_format}')  # all\檔案名.jpg
        newPngPath = os.path.join(paths[0], f'{fname}.{png_format}')  # train\檔案名
        trainPath.append(os.path.abspath(newPngPath) + '\n')
        shutil.copy(orgPngPath, newPngPath)

        orgTxtPath = os.path.join('all', f'{fname}.txt')  # f-string
        newTxtPath = os.path.join(paths[2], f'{fname}.txt')
        shutil.copy(orgTxtPath, newTxtPath)

    # else:
    #     orgTxtPath = os.path.join('all', f'{fname}.txt')  # f-string
    #     newTxtPath = os.path.join(paths[2], f'{fname}.txt')
    #     shutil.copy(orgTxtPath, newTxtPath)

valPath = []

for fname in valNames:

    if fname in lst_jpg:
        orgJpgPath = os.path.join('all', f'{fname}.{jpg_format}')
        newJpgPath = os.path.join(paths[1], f'{fname}.{jpg_format}')
        valPath.append(os.path.abspath(newJpgPath) + '\n')
        shutil.copy(orgJpgPath, newJpgPath)

        orgTxtPath = os.path.join('all', f'{fname}.txt')  # f-string
        newTxtPath = os.path.join(paths[3], f'{fname}.txt')
        shutil.copy(orgTxtPath, newTxtPath)

    elif fname in lst_png:
        orgPngPath = os.path.join('all', f'{fname}.{png_format}')
        newPngPath = os.path.join(paths[1], f'{fname}.{png_format}')
        valPath.append(os.path.abspath(newPngPath) + '\n')
        shutil.copy(orgPngPath, newPngPath)

        orgTxtPath = os.path.join('all', f'{fname}.txt')  # f-string
        newTxtPath = os.path.join(paths[3], f'{fname}.txt')
        shutil.copy(orgTxtPath, newTxtPath)

    # else:
    #     orgTxtPath = os.path.join('all', f'{fname}.txt')
    #     newTxtPath = os.path.join(paths[3], f'{fname}.txt')
    #     shutil.copy(orgTxtPath, newTxtPath)

with open('train.txt', 'w') as f:
    f.writelines(trainPath)

with open('val.txt', 'w') as f:
    f.writelines(valPath)

shutil.copy(os.path.join('all', 'classes.txt'), 'classes.names')
