import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import linprog
import matplotlib as mpl
from matplotlib.patches import Rectangle

# 设置中文显示和美观样式
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体支持中文
mpl.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
#plt.style.use('seaborn-v0_8-whitegrid')  # 白色网格背景，简洁优雅
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['legend.fontsize'] = 12
mpl.rcParams['figure.titlesize'] = 18

# 数据准备
n = np.arange(2, 7)  # 楼层编号
u = (-0.661 * n**2 + 6.796 * n - 5.100).astype(int)  # 单位需求
Ni = np.array([0.12, 0.29, 0.53, 0.76,1])  #噪音补偿比
Li =  np.array([0.44,0.52,0.63,0.77,0.9])   #采光补偿比
Vi = np.array([0.18,0.25,0.45,0.6,1])  #房价补偿比 
WTP = 1.4 * (Ni * 0.3 + Li * 0.4 + Vi * 0.3)  # 支付意愿
delta = 0.2  # 价格差异约束
C = 450000  # 总收入目标
T, households = 15, 2  # 时间周期和住户数

# 线性规划求解
c = -u  # 目标函数：最大化需求
A_diff = np.zeros((4, 5))  # 价格差异约束矩阵
for k in range(4):
    A_diff[k, k] = 1
    A_diff[k, k+1] = -1
b_diff = np.full(4, -delta)
A_wtp = np.eye(5)  # 支付意愿约束
b_wtp = WTP
A_sum = -u.reshape(1, -1)  # 收入约束
b_sum = np.array([-C/(365*T*households)])
A_ub = np.vstack([A_diff, A_wtp, A_sum])
b_ub = np.hstack([b_diff, b_wtp, b_sum])
bounds = [(0, None)] * 5  # 非负约束
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
p_opt = res.x  # 优化价格

# 创建绘图
fig = plt.figure(figsize=(14, 10), dpi=100)
fig.suptitle('电梯定价的线性规划几何过程', fontweight='bold', y=0.98)

# 子图1：三维约束面 (第1行，第1列，索引1)
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
p2 = np.linspace(0, WTP[0], 50)
p3 = np.linspace(0, WTP[1], 50)
P2, P3 = np.meshgrid(p2, p3)
P4_plane1 = P3 + delta  # 约束：p4 >= p3 + delta
P4_plane2 = (C/(365*T*households) - u[0]*P2 - u[1]*P3) / u[2]  # 收入约束面
ax1.plot_surface(P2, P3, P4_plane1, alpha=0.5, color='#87CEEB', edgecolor='none')
ax1.plot_surface(P2, P3, P4_plane2, alpha=0.5, color='#FFA500', edgecolor='none')
ax1.scatter(p_opt[0], p_opt[1], p_opt[2], color='red', s=100, label='最优解', zorder=5)
ax1.set_xlabel('第2层单次乘坐价格')
ax1.set_ylabel('第3层单次乘坐价格')
ax1.set_zlabel('第4层单次乘坐价格')
ax1.set_title('三维约束面与最优解')
ax1.view_init(elev=20, azim=45)  # 优化视角
# 创建代理艺术家用于3D图例
proxy1 = Rectangle((0, 0), 1, 1, facecolor='#87CEEB', alpha=0.5)
proxy2 = Rectangle((0, 0), 1, 1, facecolor='#FFA500', alpha=0.5)
ax1.legend([proxy1, proxy2, ax1.scatter([], [], [], color='red', s=100)],
           ['价格差异约束', '收入约束', '最优解'],
           loc='upper right', frameon=True, shadow=True)

# 子图2：二维约束区域 (第1行，第2列，索引2)
ax2 = fig.add_subplot(2, 2, 2)
p2_vals = np.linspace(0, WTP[0], 300)
rev_line = (C/(365*T*households) - u[0]*p2_vals)/u[1]  # 收入约束线
ax2.plot(p2_vals, p2_vals + delta, label='价格差异约束：p3 ≥ p2 + Δ', color='#4682B4', linewidth=2.5)
ax2.plot(p2_vals, rev_line, label='收入约束', color='#FF8C00', linewidth=2.5)
ax2.fill_between(p2_vals, p2_vals + delta, rev_line, where=(rev_line > p2_vals + delta), 
                 color='lightblue', alpha=0.3, label='可行区域')
ax2.scatter(p_opt[0], p_opt[1], color='red', s=100, zorder=5, label='最优解')
ax2.set_xlabel('第2层单次乘坐价格')
ax2.set_ylabel('第3层单次乘坐价格')
ax2.set_title('二维约束区域与最优解')
# 添加约束方程标注
ax2.annotate('p3 = p2 + Δ', xy=(p2_vals[-1], p2_vals[-1] + delta), xytext=(p2_vals[-1] - 0.2, p2_vals[-1] + delta + 0.1),
             fontsize=10, color='#4682B4', bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.8))
ax2.annotate(f'{u[0]}p2 + {u[1]}p3 + ... ≤ {C/(365*T*households):.2f}', 
             xy=(p2_vals[0], rev_line[0]), xytext=(p2_vals[0] + 0.1, rev_line[0] - 0.2),
             fontsize=10, color='#FF8C00', bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.8))
ax2.legend(loc='upper right', frameon=True, shadow=True)
ax2.grid(True, linestyle='--', alpha=0.7)

# 子图3：优化价格与支付意愿对比 (第2行，第1-2列，索引3-4)
ax3 = fig.add_subplot(2, 2, (3, 4))
ax3.plot(n, WTP, marker='x', linestyle='--', color='gray', label='支付意愿上限', linewidth=2)
ax3.plot(n, p_opt, marker='o', color='#1E90FF', label='优化价格', linewidth=2)
# 添加需求数据（u）作为次坐标轴
ax3_twin = ax3.twinx()
ax3_twin.plot(n, u, marker='s', linestyle=':', color='#228B22', label='需求量', linewidth=2)
ax3_twin.set_ylabel('需求量（单位）', color='#228B22')
ax3_twin.tick_params(axis='y', labelcolor='#228B22')
# 标注价格和需求
for xi, pi, ui in zip(n, p_opt, u):
    ax3.text(xi, pi + 0.1, f'{pi:.2f}', ha='center', fontsize=10, color='#1E90FF')
    ax3.text(xi, WTP[xi-2] + 0.05, f'{WTP[xi-2]:.2f}', ha='center', fontsize=10, color='gray')
    ax3_twin.text(xi, ui + 0.5, f'{ui}', ha='center', fontsize=10, color='#228B22')
ax3.set_xticks(n)
ax3.set_xlabel('楼层')
ax3.set_ylabel('价格（每次乘坐）')
ax3.set_title('支付意愿、优化价格与需求对比')
# 合并图例
lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3_twin.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + lines2, loc='lower right', frameon=True, shadow=True)
ax3.grid(True, linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('linear_programming_visualization.png')  # 保存图像
