import numpy as np
import matplotlib.pyplot as plt

# 把数学公式写成python函数
def logistic(x, L=1, k=1, x0=0):
    return L / (1 + np.exp(-k * (x - x0)))

# 生成x轴数据
x = np.linspace(-10, 10, 400)

# 计算y的值
y = logistic(x, L=1, k=1, x0=0)

# 画图
plt.figure(figsize=(8, 5))
plt.plot(x, y, label='L=1, k=1, x0=0')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Standard Logistic Function')
plt.legend()
plt.grid(True)

plt.show()

# 比较L的影响
plt.figure(figsize=(8, 5))

for L in [0.5, 1, 2]:
    y = logistic(x, L=L, k=1, x0=0)
    plt.plot(x, y, label=f'L={L}')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Effect of L (Maximum Value)')
plt.legend()
plt.grid(True)
plt.show()

# 比较k的影响
plt.figure(figsize=(8, 5))

for k in [0.5, 1, 3]:
    y = logistic(x, L=1, k=k, x0=0)
    plt.plot(x, y, label=f'k={k}')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Effect of k (Steepness)')
plt.legend()
plt.grid(True)
plt.show()

# 比较x0的影响
plt.figure(figsize=(8, 5))

for x0 in [-3, 0, 3]:
    y = logistic(x, L=1, k=1, x0=x0)
    plt.plot(x, y, label=f'x0={x0}')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Effect of x0 (Midpoint Shift)')
plt.legend()
plt.grid(True)
plt.show()

