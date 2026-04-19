import numpy as np
from scipy.optimize import linprog

# 参数设置
n = np.arange(2, 7)  # 楼层 2-6
u = np.array([6,9,12,12,12])  # 每日使用频率
C = 450000  # 总成本
households = 2  # 每层户数
Pmax = 1.4 #理论
delta_pmin = 0.2
Ni = np.array([0.12, 0.29, 0.53, 0.76,1])  #噪音补偿比
Li =  np.array([0.44,0.52,0.63,0.77,0.9])   #采光补偿比
Vi = np.array([0.18,0.25,0.45,0.6,1]) #房价补偿比 
weighted_sum = Ni * 0.3 + Li * 0.4 + Vi * 0.3
WTP = Pmax * weighted_sum
annual_usage = u * 365  # 年使用次数

# 方案一：优化按年收费
def optimize_annual_fee():
    n = 5
    c = -np.ones(n) * households  # 最大化收入
    # 层间差异约束：y[i+1] - y[i] <= -200
    A_diff = np.zeros((4, n))
    for k in range(4):
        A_diff[k, k] = 1
        A_diff[k, k + 1] = -1
    b_diff = np.full(4, delta_pmin*365)
    A_wtp = np.eye(n)
    b_wtp = WTP * annual_usage*1.15
    A_sum = -u.reshape(1, -1)
    b_sum = np.array([-C / (15 * households)])
    A_ub = np.vstack([A_diff, A_wtp, A_sum])
    b_ub = np.hstack([b_diff, b_wtp, b_sum])
    bounds = [(0, None)] * n
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    if res.success:
        annual_fee = res.x
        total_income = np.sum(annual_fee) * households
        payback_time = C / total_income
        return annual_fee, total_income, payback_time
    else:
        raise ValueError("年费优化失败")

# 方案二：按次计费 + 套餐，计算收入
def calculate_usage_income(x1, x2, x3):
    total_income = 0
    for i in range(5):
        usage = annual_usage[i]
        # 单位成本
        season_cost = x2 / 300 if x2 > 0 else float('inf')
        month_cost = x1 / 100 if x1 > 0 else float('inf')
        single_cost = x3
        
        si, mi, excess = 0, 0, 0
        # 优先季卡
        if season_cost <= min(month_cost, single_cost):
            si = int(usage // 300)
            usage -= si * 300
        # 剩余用月卡或单次
        if usage > 0:
            if month_cost <= single_cost and usage >= 100:
                mi = int(usage // 100)
                excess = usage - mi * 100
            else:
                excess = usage
        # 每层收入
        income = (si * x2 + mi * x1 + excess * x3) * households
        total_income += income
    return total_income

# 方案二：优化套餐价格
def optimize_usage_scheme():
    best_income = 0
    best_payback = float('inf')
    best_x = (0, 0, 0)
    for x1 in np.linspace(20, 200, 19):  # 月卡价格
        for x2 in np.linspace(20, 500, 25):  # 季卡价格
            for x3 in np.linspace(0.5, 2.0, 8):  # 单次价格
                if x1 / 100 <= x2 / 300 <= x3:  # 性价比约束
                    income = calculate_usage_income(x1, x2, x3)
                    if income > best_income:
                        best_income = income
                        best_payback = C / income
                        best_x = (x1, x2, x3)
    return best_x, best_income, best_payback
def compute_income_from_scheme(price_scheme, annual_usage, households):
    total_income = 0
    for i in range(5):
        usage = annual_usage[i]
        single_price, month_price, season_price = price_scheme[i]
        
        season_unit = season_price / 300
        month_unit = month_price / 100
        
        # 优先选择单位成本最低的套餐
        si = mi = excess = 0
        if season_unit <= min(month_unit, single_price):
            si = usage // 300
            usage -= si * 300
        if usage > 0:
            if month_unit <= single_price and usage >= 100:
                mi = usage // 100
                usage -= mi * 100
        excess = usage

        # 层总收入
        layer_income = (si * season_price + mi * month_price + excess * single_price) * households
        total_income += layer_income
    return total_income

# 主程序
if __name__ == "__main__":
    # 方案一：优化按年收费
    annual_fee, annual_income, annual_payback = optimize_annual_fee()
    print("方案一：优化按年收费")
    print(f"每层年费（2-6层）：{np.round(annual_fee, 2)} 元/户")
    print(f"年收入：{annual_income:.2f} 元")
    print(f"回本时间：{annual_payback:.2f} 年")

    per_use_fee = [0.318, 0.518, 0.7644, 1.0024, 1.344]
    price_scheme = []
    print(f"\n方案二：使用层级套餐映射方案")
    print("楼层 | 单次费 | 月卡费 | 季卡费 | 单次>月均>季均")
    for i, fee in enumerate(per_use_fee):
        single = round(fee * 1.5, 3)
        month = round(fee * 100*1.3, 2)
        season = round(fee * 300 * 1.1, 2)
        # 验证单位性价比
        per_month = round(month / 100, 3)
        per_season = round(season / 300, 3)
        valid = single > per_month > per_season
        price_scheme.append((single, month, season))
        print(f"{i+2}层 | {single:.3f} 元 | {month:.2f} 元 | {season:.2f} 元 | {'✓' if valid else '×'}")
    income = compute_income_from_scheme(price_scheme, annual_usage, households)
    payback_years = C / income
    print(f"年收入：{income:.2f} 元")
    print(f"回本时间：{payback_years:.2f} 年")

