import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from paddleocr import PaddleOCR
import numpy as np

ocr_model = PaddleOCR(lang='ch', use_gpu=True)  # chi_tra 在tesseract 是繁體
img_path = 'C:/Users/User/Desktop/menu2.jpg'
result = ocr_model.ocr(img_path)
s = " ".join('%s' % id for id in result)  # list to string
x = s.split(")],")  # string split to list

all_words = np.array(x)  # list to array

# for i in x:
#     print(i)

# def keyword_processing(store_keyword):
words_list = []

# 去掉後面的('糖', 0.9993472695350647)
for i in range(len(all_words)):
    add_str = ""  # add_str用來存沒有('糖', 0.9993472695350647)的字串
    # print("i = ", i)
    if "], (" in all_words[i]:
        temp = all_words[i]
        start_index = all_words[i].find("], (")  # 找出 "], (" 的索引值
        if start_index != -1:
            # for j in range(all_words[i]):
            #     add_str = add_str + all_words[i][j]
            add_str = temp[(start_index + 4):]
        else:
            print("can not find")
    # add_str = add_str.replace('[[', '')  # 去掉前面的兩個括號
    # print("add_str = ", add_str)
    words_list.append(add_str)

# for i in words_list:
#     print("words_list =", i)

result_list = []

for i in range(len(words_list)):
    add_str = ""  # add_str用來存沒有('糖', 0.9993472695350647)的字串
    # print("i = ", i)
    temp_split = []
    temp_split = words_list[i].split(',')
    add_str = temp_split[0]

    result_list.append(add_str)
    # if "'" in words_list[i]:
    #     temp = words_list[i]
    #     start_index = words_list[i].find("0.")  # 找出 "], (" 的索引值
    #     if start_index != -1:
    #         for j in range(len(words_list[i])):
    #             add_str = add_str + words_list[i][j]
    #     else:
    #         print("can not find")
    # words_list.append(add_str)


for i in result_list:
    print("result_list =", i)

# output字
# for i in x:
#     print(i)
