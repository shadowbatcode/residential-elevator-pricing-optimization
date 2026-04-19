import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from pylab import mpl

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False

# 电梯使用频率与累积噪音函数
def lambda_n(n):
    return -0.661 * n**2 + 6.796 * n -5.100+ np.sin(n) * 0.5

N = 6
floors = np.arange(1, N + 1)
lambda_vals = lambda_n(floors)
cum_vals = [np.sum(lambda_vals[k:]) for k in range(N)]

# 平滑计算
ys = np.linspace(floors.min(), floors.max(), 500)
spl_cum = make_interp_spline(floors, cum_vals, k=3)
cum_smooth = spl_cum(ys)
spl_lambda = make_interp_spline(floors, lambda_vals, k=3)
lambda_smooth = spl_lambda(ys)

# 绘制
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor('#f9f9f9')
ax.grid(True, linestyle='--', alpha=0.5)

ax.plot(cum_smooth, ys, linewidth=2, label='累积噪音影响')
ax.plot(lambda_smooth, ys, linewidth=2, linestyle='--', label='电梯使用频率 λn')
ax.fill_betweenx(ys, cum_smooth, alpha=0.1)
ax.fill_betweenx(ys, lambda_smooth, alpha=0.1)

# 箭头注释
for floor in floors:
    ax.annotate('', xy=(cum_vals[floor-1], floor),
                xytext=(lambda_vals[floor-1], floor),
                arrowprops=dict(arrowstyle='->', alpha=0.6))

# 轴与样式
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

ax.set_title('电梯噪音影响与使用频率', fontsize=16, fontweight='bold')
ax.set_xlabel('数值', fontsize=14)
ax.set_ylabel('楼层', fontsize=14)
ax.legend(loc='lower right', fontsize=12)

plt.tight_layout()
plt.show()

# Filter points within the target payback period (11–15 years)
mask = (Y_vals >= 11) & (Y_vals <= 15)
alpha_target = alpha_s[mask]
beta_target = beta_s[mask]
gamma_target = gamma_s[mask]
Y_target = Y_vals[mask]

# Create 3D scatter plot
fig = go.Figure()

# Plot all points (in grey, semi-transparent)
fig.add_trace(go.Scatter3d(
    x=alpha_s, y=beta_s, z=gamma_s,
    mode='markers',
    marker=dict(size=5, color='grey', opacity=0.3),
    name='All Combinations'
))

# Highlight points in the 11–15 year range (in red)
fig.add_trace(go.Scatter3d(
    x=alpha_target, y=beta_target, z=gamma_target,
    mode='markers',
    marker=dict(size=7, color='red', opacity=0.8),
    name='Payback 11–15 Years'
))

# Customize layout
fig.update_layout(
    title='3D Parameter Space for Payback Period',
    scene=dict(
        xaxis_title='α (Single Use Coefficient)',
        yaxis_title='β (Monthly Coefficient)',
        zaxis_title='γ (Seasonal Coefficient)',
        xaxis=dict(range=[1.2, 1.8]),
        yaxis=dict(range=[1.1, 1.6]),
        zaxis=dict(range=[0.9, 1.5])
    ),
    showlegend=True,
    width=800,
    height=600
)

fig.show()

# Print sample parameter combinations for reference
print("Sample parameter combinations with payback period 11–15 years:")
for a, b, g, y in zip(alpha_target[:5], beta_target[:5], gamma_target[:5], Y_target[:5]):
    print(f"α={a:.2f}, β={b:.2f}, γ={g:.2f} → Payback={y:.1f} years")
