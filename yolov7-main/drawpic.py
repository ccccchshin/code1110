import operator
import string

import cv2
import numpy as np

### https://www.youtube.com/watch?v=vkxv-lsBv38&list=PLHtEtvCzwJzoBCXLalJ620139M4iM-dMB&index=3


list1 = [[[[96.0, 971.0], [195.0, 971.0], [195.0, 1061.0], [96.0, 1061.0]], ('糖', 0.9981556534767151)],
         [[[437.0, 977.0], [703.0, 965.0], [707.0, 1044.0], [441.0, 1056.0]], ('7.3公克', 0.9396489262580872)]]

keyword_XY = []
keyword_info = ''

s = input()

i = 0
while i < len(list1):
    j = 0
    while j < 2:
        if s == list1[i][j][0]:
            keyword_XY = list1[i][0]
            keyword_XY.append(list1[i+1][0])
            keyword_info = list1[i+1][j][0]
            break
        j = j + 1

    i = i + 1

print(keyword_XY)
print(keyword_info)
x = 0
x2 = 0
try:
    x = int(min(min(min(keyword_XY[0][0], keyword_XY[1][0]), keyword_XY[2][0]), keyword_XY[3][0]))
    x2 = int(max(max(max(keyword_XY[0][1], keyword_XY[1][1]), keyword_XY[2][1]), keyword_XY[3][1]))

    print(x)
    print(x2)

    img = cv2.imread("image.jpg")

    # cv2.rectangle(img, (arr[], x), (y, y), (255, 0, 255), 3)
    cv2.line(img, (x, x), (x2, x), (0, 0, 255), 3)
    cv2.imshow('ch_img', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

except:
    print('keyword error')


