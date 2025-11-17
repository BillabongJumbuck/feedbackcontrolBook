import random

class Buffer:
    def __init__(self, max_wip, max_flow):
        self.queued = 0
        self.wip = 0  # work-in-progress ("ready pool")

        self.max_wip = max_wip
        self.max_flow = max_flow  # avg outflow is max_flow / 2

    def work(self, u: float) -> int:
        # u: 加入ready pool的units的数量
        # Add to ready pool
        u = max(0, int(round(u)))  # u四舍五入并转换为int, u为负数的时候，截断为0
        u = min(u, self.max_wip)  # 避免超过设定的加入最大值
        self.wip += u

        # Transfer from ready pool to queue
        r = int(round(random.uniform(0, self.wip)))  # 从ready pool到queue的数量是随机的
        self.wip -= r
        self.queued += r

        # Release from queue to downstream process
        r = int(round(random.uniform(0, self.max_flow)))  # 从queue到下游步骤的数量也是随机的
        r = min(r, self.queued)
        self.queued -= r
        
        return self.queued  # 返回队列的长度
    

class Controller:
    def __init__(self, kp, ki):
        self.kp = kp
        self.ki = ki
        self.i = 0  # Cumulative error ("integral")

    def work(self, e):
        self.i += e

        return self.kp * e + self.ki*self.i
    
def open_loop(p: Buffer, tm=5000):
    def target(t):
        return 5.0  # 5.1
    
    data = []

    for t in range(tm):
        u = target(t)
        y = p.work(u)

        data.append((t, u, y))
    
    return data

def closed_loop(c: Controller, p: Buffer, tm=5000):
    def setpoint(t):
        if t < 100: return 0
        if t < 300: return 50
        return 10
    
    data = []
    y = 0
    for t in range(tm):
        r = setpoint(t)
        e = r - y
        u = c.work(e)
        y = p.work(u)

        data.append((t, r, e, u, y))

    return data

c = Controller(1.25, 0.01)
p = Buffer(50, 10)
tm_run = 1000

# open_loop(p, 1000)
# closed_loop( c, p, 1000 )

# -------------- 绘图部分代码--------------

import matplotlib.pyplot as plt
import numpy as np

running_flag = False  # 为true执行闭环

if running_flag:
    # 🌟 执行闭环仿真并接收返回的数据
    results = closed_loop( c, p, tm_run )

    # 使用 NumPy 数组解包数据 (方便绘图)
    # t: 时间, r: 设定值, e: 误差, u: 控制量, y: 输出/队列长度
    t, r, e, u, y = np.array(results).T 

    # --- 绘图 ---

    plt.figure(figsize=(12, 8))

    # 子图 1: 设定值 (r) 与 队列长度 (y) 对比
    plt.subplot(2, 1, 1)
    plt.plot(t, r, label='Setpoint (r)', linestyle='--', color='blue')
    plt.plot(t, y, label='Queue Length (y, System Output)', color='red')
    plt.title('Closed-Loop Control Simulation (r vs y)')
    plt.xlabel('Time Step (t)')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)

    # 子图 2: 控制量 (u)
    plt.subplot(2, 1, 2)
    plt.plot(t, u, label='Control Signal (u)', color='green')
    plt.title('Controller Output (u)')
    plt.xlabel('Time Step (t)')
    plt.ylabel('Control Signal')
    plt.legend()
    plt.grid(True)

    plt.tight_layout() # 自动调整子图参数，使之填充整个图像区域
    plt.show()

else:
    # 🌟 执行闭环仿真并接收返回的数据
    results = open_loop(p, tm_run)

    # t: 时间, u: 输入, y: 输出/队列长度

    t, u, y = np.array(results).T 

    plt.figure(figsize=(12, 4))
    
    plt.plot(t, u, label='Input Signal (u)', linestyle='--', color='blue')
    plt.plot(t, y, label='Queue Length (y, System Output)', color='red')
    
    plt.title(f'Open-Loop Simulation (Time Steps: {tm_run})')
    plt.xlabel('Time Step (t)')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)

    plt.tight_layout() # 自动调整子图参数，使之填充整个图像区域
    plt.show()
