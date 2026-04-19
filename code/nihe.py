import numpy as np
import matplotlib.pyplot as plt

n = np.array([1, 2, 3, 4, 5, 6])
y = np.array([1, 6, 9, 12 ,12, 12])

# 拟合二次函数
coeffs = np.polyfit(n, y, deg=2)
a, b, c = coeffs
lambda_n = a * n**2 + b * n + c

print(f"拟合函数: λ_n = {a:.3f} n² + {b:.3f} n + {c:.3f}")

# 可视化
plt.scatter(n, y, label="Observed", color='blue')
plt.plot(n, lambda_n, label="Fitted λ_n", color='red')
plt.legend()
plt.title("Poisson Rate λ_n Fitting")
plt.xlabel("n")
plt.ylabel("λ_n")
plt.show()
