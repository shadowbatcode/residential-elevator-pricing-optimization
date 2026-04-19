import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False

# --- 基础参数与函数定义 ---
u = np.array([6, 9, 12, 12, 12])
annual_usage = u * 365
C = 450000
households = 2
per_use_fee = [0.318, 0.518, 0.7644, 1.0024, 1.344]

def compute_income_from_scheme(price_scheme):
    total_income = 0
    for i, usage in enumerate(annual_usage):
        single_price, month_price, season_price = price_scheme[i]
        season_unit = season_price / 300
        month_unit = month_price / 100

        si = mi = 0
        if season_unit <= min(month_unit, single_price):
            si = usage // 300
            usage -= si * 300
        if usage > 0 and month_unit <= single_price and usage >= 100:
            mi = usage // 100
            usage -= mi * 100

        layer_income = (si * season_price + mi * month_price + usage * single_price) * households
        total_income += layer_income
    return total_income

def payback_years(alpha, beta, gamma):
    scheme = [
        (round(f * alpha, 3),
         round(f * 100 * beta, 2),
         round(f * 300 * gamma, 2))
        for f in per_use_fee
    ]
    income = compute_income_from_scheme(scheme)
    return C / income

# --- 1. Monte Carlo 数据 ---
N = 500
alpha_s = np.random.uniform(1.2, 1.8, N)
beta_s  = np.random.uniform(1.1, 1.6, N)
gamma_s = np.random.uniform(0.9, 1.5, N)
Y_vals  = np.array([payback_years(a, b, g) for a, b, g in zip(alpha_s, beta_s, gamma_s)])

# 计算相关系数
corr_alpha = np.corrcoef(alpha_s, Y_vals)[0, 1]
corr_beta  = np.corrcoef(beta_s, Y_vals)[0, 1]
corr_gamma = np.corrcoef(gamma_s, Y_vals)[0, 1]

# --- 2. 响应面等高线数据 ---
# 拟合二次响应面模型
M = 300
a_reg = np.random.uniform(1.2, 1.8, M)
b_reg = np.random.uniform(1.1, 1.6, M)
g_reg = np.random.uniform(0.9, 1.5, M)
Y_reg = np.array([payback_years(a, b, g) for a, b, g in zip(a_reg, b_reg, g_reg)])

# 构建设计矩阵（二次项 + 交互项）
X = np.vstack([
    np.ones(M),
    a_reg, b_reg, g_reg,
    a_reg * b_reg, a_reg * g_reg, b_reg * g_reg,
    a_reg**2, b_reg**2, g_reg**2
]).T
coefs, *_ = np.linalg.lstsq(X, Y_reg, rcond=None)

# 生成 α-β 网格
alpha_grid = np.linspace(1.2, 1.8, 60)
beta_grid  = np.linspace(1.1, 1.6, 60)
A, B = np.meshgrid(alpha_grid, beta_grid)

# --- 3. 绘制组合图 ---
# 图 1: Monte Carlo 散点图 + 响应面等高线
fig1, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左侧：增强散点图
scatter = axes[0].scatter(alpha_s, Y_vals, c=gamma_s, s=beta_s*50, alpha=0.6, cmap='viridis')
fig1.colorbar(scatter, ax=axes[0], label='γ (季卡系数)')
axes[0].set_xlabel('α (单次系数)')
axes[0].set_ylabel('回本年限 (年)')
axes[0].set_title(f'Monte Carlo 散点 (rα={corr_alpha:.2f}, rβ={corr_beta:.2f}, rγ={corr_gamma:.2f})')
axes[0].grid(True)

# 右侧：响应面等高线 (γ=1.1)
baseline_gamma = 1.1
Z = (
    coefs[0]
    + coefs[1]*A + coefs[2]*B + coefs[3]*baseline_gamma
    + coefs[4]*A*B + coefs[5]*A*baseline_gamma + coefs[6]*B*baseline_gamma
    + coefs[7]*A**2 + coefs[8]*B**2 + coefs[9]*baseline_gamma**2
)
cs = axes[1].contourf(A, B, Z, levels=20, cmap='viridis')
axes[1].contour(A, B, Z, levels=[3], colors='red', linestyles='--', label='3年回本线')
fig1.colorbar(cs, ax=axes[1], label='回本年限 (年)')
axes[1].set_xlabel('α (单次系数)')
axes[1].set_ylabel('β (月卡系数)')
axes[1].set_title(f'响应面等高线 (γ={baseline_gamma:.1f})')

plt.suptitle('定价系数对回本年限的 Monte Carlo vs. 响应面分析', fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('monte_carlo_contour.png')
# Generate Monte Carlo data (same as your code)
N = 500
alpha_s = np.random.uniform(1.2, 1.8, N)
beta_s = np.random.uniform(1.1, 1.6, N)
gamma_s = np.random.uniform(0.9, 1.5, N)
Y_vals = np.array([payback_years(a, b, g) for a, b, g in zip(alpha_s, beta_s, gamma_s)])

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
