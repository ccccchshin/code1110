import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from paddleocr import PaddleOCR

ocr_model = PaddleOCR(lang='ch', use_gpu=True)  # chi_tra 在tesseract 是繁體
img_path = 'C:/Users/User/Desktop/menu.jpg'
result = ocr_model.ocr(img_path)
s = " ".join('%s' % id for id in result)  # list to string
# output字
x = s.split(")],")  # string split to list
for i in x:
    print(i)

# import re
# import numpy as np
# import cv2
#
# list1 = ["[[[96.0, 971.0], [195.0, 971.0], [195.0, 1061.0], [96.0, 1061.0]], ('脂肪', 0.9981556534767151)]",
#          "[[[437.0, 977.0], [703.0, 965.0], [707.0, 1044.0], [441.0, 1056.0]], ('反式脂肪', 0.9396489262580872)]"]
#
# arr = []
# for i in range(len(list1)):
#     ret = re.findall(r"-?\d+\.?\d*", list1[i])
#     arr.append(ret)
#
# arr_int = [[int(float(value)) for value in sub_list] for sub_list in arr]
#
# print(len(arr_int))
# print(arr_int)
# print(arr_int[0][0],type(arr_int[0][0]))
#
# # img = cv2.imread("cat.jpg")
# img = np.zeros((1200, 1200, 3), dtype='uint8')
#
# for i in range(2):
#     coordinates = [[arr_int[i][j], arr_int[i][j + 1]]for j in range(0, 7, 2)]
#     pts = np.array(coordinates)
#     cv2.polylines(img, [pts], True, (0, 0, 255), 3)
#     print(coordinates)
#     print(pts)
#
# cv2.namedWindow("cat2", 0)
# cv2.imshow("cat2", img)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()