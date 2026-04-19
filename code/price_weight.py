import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
import warnings
from pylab import mpl
mpl.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False

# 参数设定
r = 0.0315  # 无风险收益率
T1_T0 = 0.5  # 加装电梯工程完成时间
sigma_O_prime = 0.2  # 假设一个更合理的波动率
O_S_T0 = 19575  # 宣布加装电梯前基准楼层价值
O_S_T1 = 19934  # 宣布加装电梯时基准楼层价值
F_S = 302.13  # 基准楼层加装电梯费用

# 修正IS的计算
IS = O_S_T1 - O_S_T0 - F_S

# 楼层数据
floors = ['1楼', '2楼', '3楼', '4楼', '5楼', '6楼']
prices_T0 = [19183, 19379, 19966, 19575, 18987, 17226]  # 宣布前价格
prices_T1 = [16943, 18139, 19136, 19934, 20133, 20332]  # 宣布时价格
floor_coefficients = [0.97, 0.98, 1.01, 1.00, 0.96, 0.88]  # 楼层价值系数
costs_per_m2 = [0, 107.90, 194.23, 302.13, 410.04, 517.95]  # 每平方米费用

# 计算各楼层补偿金额
def calculate_compensation(IS, floor_coefficients, costs_per_m2):
    compensations = []
    for i in range(len(floor_coefficients)):
        I_i = IS * floor_coefficients[i]
        VC_i = I_i - costs_per_m2[i]
        compensations.append(VC_i)
    return compensations

compensations = calculate_compensation(IS, floor_coefficients, costs_per_m2)
total_compensation = sum(compensations)

# 计算房价增幅系数
increments = [(prices_T1[i] - prices_T0[i]) / prices_T0[i] for i in range(len(floors))]
min_inc = min(increments)
max_inc = max(increments)
price_increase_coeffs = [(inc - min_inc) / (max_inc - min_inc) for inc in increments]

# 创建可视化
fig = plt.figure(figsize=(14, 9), dpi=300)
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1], hspace=0.3, wspace=0.3)

# 子图1：价格变化
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(floors))
width = 0.35
bars1 = ax1.bar(x - width/2, prices_T0, width, label='宣布前价格 (T0)', color='#4C78A8', edgecolor='black', alpha=0.9)
bars2 = ax1.bar(x + width/2, prices_T1, width, label='宣布时价格 (T1)', color='#F58518', edgecolor='black', alpha=0.9)
ax1.set_xlabel('楼层', fontsize=14, labelpad=10)
ax1.set_ylabel('价格 (元/平方米)', fontsize=14, labelpad=10)
ax1.set_title('加装电梯前后各楼层房价变化', fontsize=16, pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(floors, fontsize=12)
ax1.legend(fontsize=12, frameon=True, edgecolor='black', loc='upper left')
ax1.tick_params(axis='both', labelsize=11)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# 子图2：补偿金额（美观度增强）
ax2 = fig.add_subplot(gs[1, 0])
colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0', '#FFB3E6']
x = np.arange(len(floors))
width = 0.6  # 调整柱状图宽度
bars = ax2.bar(x, compensations, width=width, color=colors, edgecolor='black', alpha=0.9)
# 调整阴影效果
shadow_offset = 0.05
ax2.bar(x + shadow_offset, compensations, width=width, color='lightgray', alpha=0.2)
ax2.set_xlabel('楼层', fontsize=14, labelpad=10)
ax2.set_ylabel('补偿金额 (元/平方米)', fontsize=14, labelpad=10)
ax2.set_title('各楼层补偿金额', fontsize=16, pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(floors, fontsize=12)
ax2.tick_params(axis='both', labelsize=11)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
# 调整 y 轴范围
ax2.set_ylim(min(compensations) - 100, max(compensations) + 100)
# 添加数值标签
for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 30 if yval > 0 else yval - 20, 
             f'{yval:.0f}', ha='center', va='bottom' if yval > 0 else 'top', fontsize=9, fontweight='bold')

# 子图3：系数和费用表格（新增房价增幅系数）
ax3 = fig.add_subplot(gs[1, 1])
ax3.axis('off')
table_data = [
    ['楼层'] + floors,
    ['价值系数'] + [f'{c:.2f}' for c in floor_coefficients],
    ['费用 '] + [f'{c:.2f}' for c in costs_per_m2],
    ['房价增幅系数'] + [f'{c:.2f}' for c in price_increase_coeffs]
]
table = ax3.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.2] + [0.13]*6,
                  cellColours=[['#F5F5F5'] + ['#FFFFFF']*6]*4, edges='closed')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.8)
ax3.set_title('楼层价值系数与费用', fontsize=16, pad=15)

# 添加摘要统计信息
summary_text = (
    f'基准楼层价值增加 (IS): {IS:.2f} 元/平方米\n'
    f'总补偿金额: {total_compensation:.2f} 元/平方米\n'
    f'无风险收益率: {r*100:.2f}%\n'
    f'工程完成时间: {T1_T0*12:.0f} 个月'
)
fig.text(0.02, 0.02, summary_text, fontsize=11, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.95))

# 调整布局并保存
plt.savefig('elevator_impact_visualization_chinese_enhanced.png', dpi=300, bbox_inches='tight')
plt.close()
