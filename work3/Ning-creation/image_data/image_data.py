import numpy as np
import matplotlib.pyplot as plt

# ========= 1、创建灰度图并转换为 RGB =========

# Step1: 创建二维灰度图 (200, 300)
grayscale_image = np.random.randint(0, 256, size=(200, 300), dtype=np.uint8)

print(grayscale_image.shape)

# Step2: 转换为 RGB 图像 (200, 300, 3)
color_image = np.stack([grayscale_image]*3, axis=-1)

print(color_image.shape)

# ========= 2、矩阵乘法实现 Sepia 滤镜 =========

# Step1: 矩阵乘法实现 Sepia 滤镜
sepia_matrix = np.array([
    [0.393, 0.769, 0.189],
    [0.349, 0.686, 0.168],
    [0.272, 0.534, 0.131]
])

# Step2: 使用矩阵乘法
sepia_image = color_image @ sepia_matrix.T

# Step3: 截断到 [0, 255]
sepia_image = np.clip(sepia_image, 0, 255)
sepia_image = sepia_image.astype(np.uint8)

# ========= 3、实现过饱和效果 =========

# Step1: 计算亮度 L
L = (
    0.299 * color_image[:, :, 0] +
    0.587 * color_image[:, :, 1] +
    0.114 * color_image[:, :, 2]
)

# Step2: 扩展维度方便广播
L = L[:, :, np.newaxis]

# Step3: 应用过饱和公式
alpha = 1.5

saturated_image = L + alpha * (color_image - L)

# Step4: 截断到 [0, 255]
saturated_image = np.clip(saturated_image, 0, 255)
saturated_image = saturated_image.astype(np.uint8)

# ========= 4、添加左右渐变边框 =========

# Step1: 创建渐变序列
gradient = np.linspace(0, 1, 20)

# Step2: 左边：黑 → 原图
left_border = color_image[:, :20, :] * gradient[np.newaxis, :, np.newaxis]

# Step3: 右边：原图 → 白色
right_gradient = gradient[::-1]
right_border = color_image[:, -20:, :] * right_gradient[np.newaxis, :, np.newaxis] + \
               255 * (1 - right_gradient[np.newaxis, :, np.newaxis])

# Step4: 拼接回去
border_image = color_image.copy()
border_image[:, :20, :] = left_border
border_image[:, -20:, :] = right_border

# ========= 5、显示结果 =========
plt.figure(figsize=(12, 8))

plt.subplot(2,2,1)
plt.title("Original")
plt.imshow(color_image)
plt.axis("off")

plt.subplot(2,2,2)
plt.title("Sepia")
plt.imshow(sepia_image)
plt.axis("off")

plt.subplot(2,2,3)
plt.title("Saturated")
plt.imshow(saturated_image)
plt.axis("off")

plt.subplot(2,2,4)
plt.title("Gradient Border")
plt.imshow(border_image)
plt.axis("off")

plt.tight_layout()
plt.show()

