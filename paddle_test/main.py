# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from imageio.plugins import opencv
from paddleocr import PaddleOCR, draw_ocr
from matplotlib import pyplot as plt
import cv2
import os_two


# def split_list(l, n):
#     # 將list分割 (l:list, n:每個matrix裡面有n個元素)
#     for idx in range(0, len(l), n):
#         yield l[idx:idx + n]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ocr_model = PaddleOCR(lang='ch', use_gpu=False) # chi_tra 在tesseract 是繁體

    img_path = os_two.path.join('C:/Users/shin/410828608/yolov7-main/inference/images/S__74694868.jpg')

    # img_path = os.path.join(C:\Users\shin\410828608\yolov7 - main\inference\images, '88621')

    # Run the ocr method on the ocr model

    result = ocr_model.ocr(img_path)
    # result = ocr_model.ocr(img_path)

    # result_sp = list(split_list(result, 1))  # 將list分割成每份中有3個元素

    s = " ".join('%s' %id for id in result) # list to string

    x = s.split(")],") # string split to list

    # print(x, end = "\n")

    for i in x:
        print(i)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
