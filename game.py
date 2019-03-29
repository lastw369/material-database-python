import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(-np.pi, np.pi, 256, endpoint=True)
c, s = np.sin(x), np.cos(x)

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_xlabel('v data')
ax.set_ylabel('i data')

plt.plot(x, c, color="green", linestyle="-", linewidth=2)
plt.plot(x, s, color="red", linestyle="--")
plt.xticks(np.linspace(-4, 4, 9, endpoint=True))
plt.show()


ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))