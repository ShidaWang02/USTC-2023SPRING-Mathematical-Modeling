import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 定义SIR模型的微分方程
def SIR(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# 定义模型参数
N = 10000 # 总人口数
beta = 0.2 # 感染率
gamma = 0.1 # 恢复率
I0, R0 = 1, 0 # 初始感染人数和恢复人数
S0 = N - I0 - R0 # 初始易感人数

# 定义时间范围
t = np.linspace(0, 365, 365)

# 解微分方程
y0 = S0, I0, R0
ret = odeint(SIR, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

# 绘制动图
fig = plt.figure(facecolor='w',dpi=150)
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.set_xlabel('Time /days')
ax.set_ylabel(f'Number ({N}s)')
ax.set_xlim(0, 365)
ax.set_ylim(0, 10000)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
line1, = ax.plot([], [], 'b', alpha=0.5, lw=2, label='Susceptible',ls='-.')
line2, = ax.plot([], [], 'r', alpha=0.5, lw=2, label='Infected',ls='-.')
line3, = ax.plot([], [], 'g', alpha=0.5, lw=2, label='Recovered with immunity',ls='-.')
ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.legend(loc='upper right')
plt.title('SIRE Model')
def update(i):
    line1.set_data(t[:i], S[:i])
    line2.set_data(t[:i], I[:i])
    line3.set_data(t[:i], R[:i])
    return line1, line2, line3

ani = FuncAnimation(fig, update, frames=np.arange(0, 365, 3), interval=50)

# 保存动图
# ani.save('SIRE.gif', writer='pillow', fps=1000/50)
plt.show()
