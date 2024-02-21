import matplotlib.pyplot as plt
import numpy as np
import random
import math
import matplotlib.animation as animation

#グラフ領域のサイズ
x_lim = 10
y_lim = 8

class Bird:
    def __init__(self, id):
        #鳥の識別番号
        self.id = id
        #鳥の座標
        x = random.uniform(0, x_lim)
        y = random.uniform(0, y_lim)
        self.pos = np.array([x, y])
        #鳥の速度
        velocity = random.uniform(0.1, 0.4)
        self.velocity = velocity
        #方向
        theta = random.uniform(0, 6.28)
        self.theta = theta
        self.vector = np.array([np.cos(theta), np.sin(theta)])

def clamp(min, max, val):
    if(val > max):
        val = max
    if(val < min):
        val = min
    return val

def reposition(pos):
    if (pos[0] < 0):
        pos[0] = x_lim
        pos[1] = clamp(0,y_lim,y_lim - pos[1])
    if (pos[1] < 0):
        pos[0] = clamp(0, x_lim, x_lim - pos[0])
        pos[1] = y_lim
    if (pos[0] > x_lim):
        pos[0] = 0
        pos[1] = clamp(0,y_lim,y_lim - pos[1])
    if (pos[1] > y_lim):
        pos[0] = clamp(0, x_lim, x_lim - pos[0])
        pos[1] = 0

#インスタンスリストbirds
birds = []
for i in range(0, 100):
    birds.append(Bird(id=i))

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

def init():
    ax.set_xlim(0,x_lim)
    ax.set_ylim(0,y_lim)

def plot(data): #描画
    ax.cla()
    ax.set_xlim(0,x_lim)
    ax.set_ylim(0,y_lim)
    for bird in birds:
        ax.plot(bird.pos[0], bird.pos[1], marker='.')
        x = bird.velocity * np.cos(bird.theta)
        y = bird.velocity * np.sin(bird.theta)
        bird.pos += np.array([x, y])
        reposition(bird.pos)
        
ani = animation.FuncAnimation(fig, plot, interval=20,cache_frame_data=False,init_func=init)
plt.show()
