import numpy as np

# 原始字串列表
# string_list = [
#     "[[[32.0, 648.0], [155.0, 648.0], [155.0, 713.0], [32.0, 713.0]], ('脂肪', 0.9324982166290283)]",
#     "[[[84.0, 728.0], [313.0, 731.0], [312.0, 791.0], [83.0, 787.0]], ('和脂肪', 0.9711733460426331)]",
#     "[[[86.0, 804.0], [313.0, 809.0], [312.0, 868.0], [84.0, 863.0]], ('反式脂肪', 0.9931995868682861)]"
# ]
#
# # 解析每個字串元素，提取坐標部分，並轉換為 NumPy 陣列
# float_arrays = []
# print("float_arrays = ", float_arrays)

final = "   [32.0, 648.0], [155.0, 648.0], [155.0, 713.0], [32.0, 713.0]"
# 删除字符串中的空格
final = final.replace(' ', '')

# 初始化存储浮点数数组的列表
float_arrays = []

# 初始化一个临时字符串
temp_str = ''

# 初始化计数器和标志
num = 0
sign = 0
count = 0

for char in final:
    if char == '[':
        count += 1
    elif char == ']':
        count += 1
    elif char == ',':
        sign += 1
        if sign == 2:
            sign = 0
            continue
    temp_str += char
    if count == 2:
        # 打印当前的 temp_str
        print("temp_str =", temp_str)

        # 使用 eval 函数将字符串转换为列表
        coords_list = eval(temp_str)

        # 转换坐标列表中的元素为浮点数
        float_coords = [float(coord) for coord in coords_list]

        # 添加到 float_arrays 中
        float_arrays.append(float_coords)

        # 重置 temp_str 和计数器
        temp_str = ''
        count = 0

# 打印最终的浮点数数组
print('float_arrays =', float_arrays)
temp_arr = np.array(float_arrays, dtype=float)
for i in temp_arr:
    print('temp_arr =', type(i))
# for float_coords in float_arrays:
#     print('float_coords types =', type(float_coords))



# ////////////////////
# final = "   [32.0, 648.0], [155.0, 648.0], [155.0, 713.0], [32.0, 713.0]"
# print(final)
# final = final.replace(' ','')
# print(final)
#
# temp_str = ''
# store_list = []
# num = 0
# sign = 0
# count = 0
#
# float_arrays = []
#
# for char in final:
#     print(char)
#     if char == '[':
#         count = count + 1
#     elif char == ']':
#         count = count + 1
#     elif char == ',':
#         sign = sign + 1
#         if sign == 2:
#             sign = 0
#             continue
#     temp_str = temp_str + char
#     if count == 2:
#         print("temp_str = ", temp_str)
#         store_list.append(temp_str)
#         temp_str = ''
#         count = 0
#     num = num + 1
#     for i in store_list:
#         print(i)
#     for string in store_list:
#         # 使用 eval 函数将字符串转换为列表
#         coords_list = eval(string)
#         print('coords_list =', coords_list)
#
#         float_coords = [float(coord) for coord in coords_list]
#         float_arrays.append(float_coords)
#     for float_coords in float_arrays:
#         print('float_coords =', float_coords)

# //////////////////

# for x in final:
#     print(float(x[0]), float(x[1]))


# # for string in string_list:
# #     # 使用 eval 函數提取坐標部分並轉為 Python 列表
# #
# #     s = " ".join('%s' % id for id in string_list)
# #     coords_str = s.split("], [")  # 提取坐標部分
# #     print("coords_str = ", coords_str)
# #
# #     coords_list = eval("[" + coords_str + "]")
# #     print("coords_list = ", coords_list)
# #
# #     # 將 Python 列表轉為 NumPy 陣列
# #     coords_array = np.array(coords_list, dtype=float)
# #     print("coords_array = ", coords_array)
# #
# #     float_arrays.append(coords_array)
# #     print("float_arrays = ", float_arrays)
#
# # 現在 float_arrays 中包含了每個字串元素的坐標部分的浮點數陣列
# # 打印結果
# # for arr in float_arrays:
# #     print(arr)