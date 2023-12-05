# -*- coding: utf-8 -*-
import os

import jpysocket

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from paddleocr import PaddleOCR
import numpy as np

ocr_model = PaddleOCR(lang='ch', use_gpu=True)  # chi_tra 在tesseract 是繁體
img_path = 'C:/Users/User/410828608/yolov7-main/chat_ocr.JPG'
result = ocr_model.ocr(img_path)
s = " ".join('%s' % id for id in result)  # list to string
x = s.split(")],")  # string split to list

all_words = np.array(x)  # list to array
words_list = []

for i in range(len(all_words)):
    add_str = ""
    # print("i = ", i)
    if "], (" in all_words[i]:
        temp = all_words[i]
        start_index = all_words[i].find("], (")  # 找出 "], (" 的索引值
        if start_index != -1:
            add_str = temp[(start_index + 4):]
        else:
            print("can not find")
    words_list.append(add_str)

result_list = []
for i in range(len(words_list)):
    add_str = ""
    temp_split = [] # '堂', 0.091212
    temp_split = words_list[i].split(',')
    add_str = temp_split[0]
    result_list.append(add_str)

file_path = "C:/Users/User/410828608/yolov7-main/chat_ocr.txt"  # 指定文件的路徑
with open(file_path, "a", encoding="UTF-8") as file:
    for i in result_list:
        new_contents = i
        file.write(new_contents)
        print("result_list =", i)


