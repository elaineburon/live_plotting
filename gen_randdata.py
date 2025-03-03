"""
Created on Sat Feb 15 17:24:35 2025

@author: ejrbu

Generates its own data and uses FuncAnimation to d
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from time import sleep

# Initialize the figure and axis for plotting
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.grid()

# Initialization function for the animation
def init():
    line.set_data([], [])
    sleep(0.5)
    return line,

# Animation function which updates line for each frame
def animate(i):
    x = np.linspace(0, 100, 100)
    y = np.random.rand(100) * 100  # Generate random y values between 0 and 100
    line.set_data(x, y)
    sleep(0.5)
    return line,

# Create the animation

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=True)

# Show the plot
plt.show()