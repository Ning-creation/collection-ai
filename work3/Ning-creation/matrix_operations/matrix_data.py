import numpy as np

# ========= 1、创建 10 * 10 数组 =========
data_matrix = np.arange(100) # 创建 0-99 的一维数组
data_matrix = data_matrix.reshape(10, 10) # 变成 10x10
print(data_matrix)

# ========= 2、提取中心 4 * 4 子矩阵 =========
center_submatrix = data_matrix[3:7, 3:7]
print(center_submatrix)

# ========= 3、找到所有 > 75 的元素并设为 0 =========
data_matrix[data_matrix > 75] = 0
print(data_matrix)

# ========= 4、整体缩放 * 0.8 =========
data_matrix = data_matrix.astype(float)  # 先转成 float
data_matrix *= 0.8  # 原地修改，是NumPy推荐的向量化写法
print(data_matrix)

# ========= 5、找到最大值及其位置 =========
max_value = np.max(data_matrix)
print("最大值:", max_value)

max_index = np.argmax(data_matrix)
row, col = np.unravel_index(max_index, data_matrix.shape)
print("最大值位置:", (row, col))