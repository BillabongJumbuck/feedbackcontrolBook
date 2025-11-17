import numpy as np

def cache(size):
    # 1. 初始化结果数组为线性关系 size / 100.0
    hitrate = size / 100.0

    # 2. 应用下限饱和条件: 如果 size < 0，设置 hitrate = 0
    # np.where(condition, value_if_true, value_if_false)
    hitrate = np.where(size < 0, 0, hitrate)
    
    # 3. 应用上限饱和条件: 如果 size > 100，设置 hitrate = 1
    hitrate = np.where(size > 100, 1, hitrate)
    
    return hitrate

def run_simulation(k, tm=20):
    r = 0.6  # setpoint
    y = 0.0  # actual hit rate
    c = 0.0  # cumulative tracking error 
    u = 0.0  # control action (cache size)

    # 存储数据: (t, r, e, c, u, y)
    data = [] 

    for i in range(tm):
        e = r - y  # traking error
        c += e  # cumulative error
        u = k * c  # control action: cache size
        
        # 记录控制量 u
        u_actual = u 

        y = cache(u)  # process output: hitrate

        data.append((i, r, e, c, u_actual, y))
        
    return data



# -------------- 绘图部分代码--------------
import matplotlib.pyplot as plt

# --- 图 1: 迭代过程 (Top Panel) ---
plt.figure(figsize=(8, 6))

# 1. 绘制过程模型 (Actual Hit Rate)
u_vals = np.linspace(0, 100, 100)
y_vals = cache(u_vals)
plt.plot(u_vals, y_vals, color='black', label='Actual Hit Rate')

# 2. 设定值 (Setpoint)
plt.axhline(0.6, color='green', linestyle='-', label='Setpoint')
plt.axvline(0, color='gray', linestyle=':')

# 3. 初始误差和迭代路径
# 假设初始状态 (u=40, y=0.4)
u0, y0 = 40, 0.4
r = 0.6
e = r - y0 # 0.2

# 绘制初始点
plt.plot(u0, y0, 'ro', markersize=5)
plt.text(u0 + 2, y0 + 0.02, f'({u0}, {y0:.1f})', color='r')

# 绘制误差 e
plt.plot([u0, u0], [y0, r], color='r', linestyle='-')
plt.text(u0 + 1, (y0 + r) / 2, r'$\epsilon$', color='r', fontsize=12)

# 绘制迭代（k=50 和 k=175）
k_small = 50
k_large = 175

# k=50
u1_small = u0 + k_small * e
plt.plot([u0, u1_small, u1_small], [r, r, cache(u1_small)], 
            color='blue', linestyle='-')
plt.text((u0 + u1_small)/2, r - 0.05, r'$50\epsilon$', color='blue', fontsize=10)

# k=175
u1_large = u0 + k_large * e
plt.plot([u0, u1_large, u1_large], [r, r, cache(u1_large)], 
            color='cyan', linestyle='-')
plt.text((u0 + u1_large)/2, r + 0.05, r'$175\epsilon$', color='cyan', fontsize=10)


plt.xlim(0, 105)
plt.ylim(0, 1.05)
plt.xlabel('Buffer Size')
plt.ylabel('Hit Rate')
plt.title('Figure 2-3 Top Panel: Controller Iteration Process')
plt.grid(True, linestyle=':')
plt.show()

# --- 图 2: 时域响应 (Bottom Panel) ---
plt.figure(figsize=(8, 6))

gains = {10: 'magenta', 50: 'blue', 175: 'cyan'}

for k, color in gains.items():
    results = run_simulation(k, tm=20)
    t, _, _, _, _, y = np.array(results).T
    plt.plot(t, y, label=f'k = {k}', color=color, marker='.')

# 设定值
plt.axhline(0.6, color='gray', linestyle='--')

plt.xlim(0, 20)
plt.ylim(0, 1.05)
plt.xlabel('Time Steps')
plt.ylabel('Hit Rate')
plt.title('Figure 2-3 Bottom Panel: Time Evolution of Hit Rate')
plt.legend()
plt.grid(True, linestyle=':')
plt.show()