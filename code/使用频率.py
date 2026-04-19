import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
n = np.array([1, 2, 3, 4, 5, 6])
y = np.array([1, 3 ,4, 6, 5, 4])

# 拟合二次函数
coeffs = np.polyfit(n, y, deg=2)
a, b, c = coeffs
lambda_n = a * n**2 + b * n + c

print(f"拟合函数: λ_n = {a:.3f} n² + {b:.3f} n + {c:.3f}")

# 可视化
plt.scatter(n, y, label="Observed", color='blue')
plt.plot(n, lambda_n, label="Fitted λ_n", color='red')
plt.legend()
plt.title("各楼层电梯使用频率拟合")
plt.xlabel("楼层数")
plt.ylabel("频次")
plt.show()
