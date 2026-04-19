import numpy as np
from scipy.optimize import linprog
import math

def solve_elevator_pricing(u, delta_pmin, WTP, C, T=15, households=2):
    """
    解决电梯定价的线性优化问题。
    
    参数：
    - u: 第2到6层的权重数组，形状 (5,)
    - delta_pmin: 相邻层间最小价格差异
    - WTP: 第2到6层的居民意愿补偿上限，形状 (5,)
    - C: 总成本约束
    - T: 年数，默认15
    - households: 户数，默认2
    
    返回：
    - 第2到6层的最优价格 p
    """
    n = 5  # 第2到6层，共5层

    # 目标函数：最大化 ∑ ui*pi，等价于最小化 -∑ ui*pi
    c = -u

    # 约束条件矩阵
    # 1. 层间差异约束：pi+1 - pi >= delta_pmin，转换为 -pi + pi+1 >= delta_pmin
    #    在 linprog 中，A_ub * x <= b_ub，所以 -(-pi + pi+1) <= -delta_pmin
    A_diff = np.zeros((4, n))
    for k in range(4):
        A_diff[k, k] = 1      # pi
        A_diff[k, k + 1] = -1 # pi+1
    b_diff = np.full(4, -delta_pmin)

    # 2. 上限约束：pi <= WTP_i
    A_wtp = np.eye(n)
    b_wtp = WTP

    # 3. 总收益约束：365*T*households * ∑ ui*pi >= C
    #    转换为 -∑ ui*pi <= -C / (365*T*households)
    A_sum = -u.reshape(1, -1)
    b_sum = np.array([-C / (365 * T * households)])
    print(b_sum)
    # 合并所有约束
    A_ub = np.vstack([A_diff, A_wtp, A_sum])
    b_ub = np.hstack([b_diff, b_wtp, b_sum])

    # 变量界限：pi >= 0
    bounds = [(0, None)] * n

    # 求解线性规划
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if res.success:
        return res.x
    else:
        raise ValueError("优化失败")
    
def normalize(arr):
    return (arr - arr.min()) / (arr.max() - arr.min())

def welfare_calc(delta_p):
    compliance_rate = 1-0.3*math.exp(-2*delta_p)
    cost_cover = (p_6-p_2)*usage_6*365*15
    return compliance_rate*cost_cover

if __name__ == "__main__":
    # 定义楼层编号 n
    n = np.arange(2, 7)
    # 根据公式计算 λ_n
    u = -0.661 * n**2 + 6.796 * n -5.100
    u = u.astype(int)
    delta_pmin = 0.2  # 最小价格差异
    C = 450000  # 总成本
    Pmax = 1.4 #理论
    Ni = np.array([0.12, 0.29, 0.53, 0.76,1])  #噪音补偿比
    Li =  np.array([0.44,0.52,0.63,0.77,0.9])   #采光补偿比
    Vi = np.array([0.18,0.25,0.45,0.6,1])  #房价补偿比 
    Nn, Ln, Vn = normalize(Ni), normalize(Li), normalize(Vi)
    weighted_sum = Ni * 0.3 + Li * 0.4 + Vi * 0.3
    WTP = Pmax * weighted_sum
    
    try:
        p_opt = solve_elevator_pricing(u, delta_pmin, WTP, C)
        print("第2到6层的最优价格：", p_opt)
    except ValueError as e:
        print(e)
