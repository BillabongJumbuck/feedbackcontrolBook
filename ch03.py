import sys
import matplotlib.pyplot as plt

r = float(sys.argv[1])  # Reference or "setpoint"
k = float(sys.argv[2])  # Controller gain

times = []
outputs = []
setpoint_line = []

u = 0  # Previous output
TIME_STEPS = 200  # 迭代次数
for i in range(TIME_STEPS):
    y = u  # one-step delay: previous output

    e = r - y  # tracking error
    u = k*e  # Controller output

    times.append(i)
    outputs.append(y)
    setpoint_line.append(r)


# ----------------------------------------------------
# 添加绘图逻辑
# ----------------------------------------------------
plt.figure(figsize=(10, 6))

# 绘制设定值 r 和系统输出 y
plt.plot(times, setpoint_line, 'k--', label=f'Setpoint r={r}')
plt.plot(times, outputs, 'r-', label=f'Output y (k={k})')

plt.title(f'P-Controller Response (r={r}, k={k})')
plt.xlabel('Time Step (i)')
plt.ylabel('Output Value')
plt.legend()
plt.grid(True, linestyle=':')
# 生成文件名，将 r 和 k 值包含在文件名中
filename = f'ch03_response_r{r:.2f}_k{k:.2f}.png'
# 将图表保存为 PNG 文件
plt.savefig(filename)
print(f"Plot saved to {filename}")