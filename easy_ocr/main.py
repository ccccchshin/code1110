# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import easyocr
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    reader = easyocr.Reader(['ch_tra', 'en'])

    img_path = os.path.join('C:/Users/shin/410828608/yolov7-main/inference/images/ej9ej9.jpg')


    result = reader.readtext(img_path)

    for i in result:
        print(i)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
