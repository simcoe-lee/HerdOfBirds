import matplotlib.pyplot as plt
import numpy as np
import random
import math
import matplotlib.animation as animation

#グラフ領域のサイズ
x_lim = 10
y_lim = 8
#壁を避け始める境目
margin = 3
#アニメーション間隔[ms]
interval = 20
#1コマあたりの秒数
time = interval / 1000

class Bird:
    def __init__(self, id):
        #鳥の識別番号
        self.id = id
        #鳥の座標
        x = random.uniform(0, x_lim)
        y = random.uniform(0, y_lim)
        self.pos = np.array([x, y])
        #方向
        theta = random.uniform(0, 6.28)
        self.theta = theta
        #鳥の速度(thetaは初期値のためだけに使ってその後はvxvyで)
        velocity = random.uniform(1, 4)
        self.velocity = velocity 
        self.vx = velocity*np.cos(theta)
        self.vy = velocity*np.sin(theta)
        #加速度
        self.dx = 0
        self.dy = 0

def clamp(min, max, val):
    if(val > max):
        val = max
    if(val < min):
        val = min
    return val

def distance(bird1, bird2):
    return np.sqrt(
        (bird1.pos[0] - bird2.pos[0]) * (bird1.pos[0] - bird2.pos[0]) +
        (bird1.pos[1] - bird2.pos[1]) * (bird1.pos[1] - bird2.pos[1])
    )

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
def avoidWall(bird):
    turnFactor = 20
    if(bird.pos[0] < margin):
        bird.dx += (margin-bird.pos[0])*turnFactor
    if(bird.pos[0] > x_lim - margin):
        bird.dx -= (bird.pos[0]-x_lim + margin)*turnFactor
    if(bird.pos[1] < margin):
        bird.dy += (margin-bird.pos[1])*turnFactor
    if(bird.pos[1] > y_lim - margin):
        bird.dy -= (bird.pos[1]-y_lim + margin)*turnFactor


def pos_update(bird):
    bird.vx = bird.vx + bird.dx*time
    bird.vy = bird.vy + bird.dy*time
    bird.pos += np.array([bird.vx*time, bird.vy*time])

def limitspeed(bird):
    limit = 6
    bird.velocity = np.sqrt(bird.vx * bird.vx + bird.vy * bird.vy)
    if (bird.velocity > limit):
        bird.vx = bird.vx * limit / bird.velocity
        bird.vy = bird.vy * limit / bird.velocity

def flyTowardsCenter(bird):
    centeringFactor = 0.5
    centerX = 0
    centerY = 0
    numNeighbors = 0
    #視野内の鳥たちで重心を取る
    visualRange = 1
    for otherbird in birds:
        if(distance(bird, otherbird) < visualRange):
            centerX += otherbird.pos[0]
            centerY += otherbird.pos[1]
            numNeighbors += 1
        if(numNeighbors):
            centerX = centerX / numNeighbors
            centerY = centerY / numNeighbors
            bird.dx += (centerX - bird.pos[0]) * centeringFactor
            bird.dy += (centerY - bird.pos[1]) * centeringFactor


#インスタンスリストbirds
birds = []
for i in range(0, 40):
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
        #flyTowardsCenter(bird)
        avoidWall(bird)
        limitspeed(bird)
        

        pos_update(bird)
        #reposition(bird.pos)
        
ani = animation.FuncAnimation(fig, plot, interval=interval,cache_frame_data=False,init_func=init)
plt.show()
