import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
line, = ax.plot([], [])

def update(frame):
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x + frame / 10)
    line.set_data(x, y)
    return line,

ani = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=50)

plt.show()