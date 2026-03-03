import numpy as np

# ========= 1、生成数据 =========
points_A = np.random.randint(0, 101, size=(5, 2))
points_B = np.random.randint(0, 101, size=(8, 2))

print("points_A:\n", points_A)
print("points_B:\n", points_B)

# ========= 2、计算距离矩阵 =========

# Step1: 扩展维度
A_expanded = points_A[:, np.newaxis, :]   # (5, 1, 2)
B_expanded = points_B[np.newaxis, :, :]   # (1, 8, 2)

print("A_expanded:\n", A_expanded)
print("B_expanded:\n", B_expanded)

# Step2: 做差(触发广播)
diff = A_expanded - B_expanded
print("difference:\n", diff)

# Step3: 平方
sq = diff ** 2
print("sq:\n", sq)

# Step4: 沿坐标轴求和
sum_sq = np.sum(sq, axis=2)
print("sum_sq:\n", sum_sq)

# Step5: 开根号
distance_matrix = np.sqrt(sum_sq)

print(distance_matrix)
print(distance_matrix.shape)

# ========= 3、对每个A点，找最近的B点 =========
min_distances = np.min(distance_matrix, axis=1)

print(min_distances)
print(min_distances.shape)

# ========= 4、找出满足距离 < 20 的B点索引 =========

# Step1: 生成布尔矩阵
mask = distance_matrix < 20

# Step2: 找出某列是否有 "True"
valid_B = np.any(mask, axis=0)

# Step3: 提取索引
indices = np.where(valid_B)[0]

print(indices)