import numpy as np

# 原始字串列表
string_list = [
    "[[[32.0, 648.0], [155.0, 648.0], [155.0, 713.0], [32.0, 713.0]], ('脂肪', 0.9324982166290283)]",
    "[[[84.0, 728.0], [313.0, 731.0], [312.0, 791.0], [83.0, 787.0]], ('和脂肪', 0.9711733460426331)]",
    "[[[86.0, 804.0], [313.0, 809.0], [312.0, 868.0], [84.0, 863.0]], ('反式脂肪', 0.9931995868682861)]"
]

# 解析每個字串元素，提取坐標部分，並轉換為 NumPy 陣列
float_arrays = []
print("float_arrays = ", float_arrays)
for string in string_list:
    # 使用 eval 函數提取坐標部分並轉為 Python 列表

    s = " ".join('%s' % id for id in string_list)
    coords_str = s.split("], [")  # 提取坐標部分
    print("coords_str = ", coords_str)

    coords_list = eval("[" + coords_str + "]")
    print("coords_list = ", coords_list)

    # 將 Python 列表轉為 NumPy 陣列
    coords_array = np.array(coords_list, dtype=float)
    print("coords_array = ", coords_array)

    float_arrays.append(coords_array)
    print("float_arrays = ", float_arrays)

# 現在 float_arrays 中包含了每個字串元素的坐標部分的浮點數陣列
# 打印結果
for arr in float_arrays:
    print(arr)