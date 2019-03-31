
import numpy as np
from random import random
import matplotlib.pyplot as plt
from matplotlib import collections  as mc


class Line():
    def __init__(self, p0, p1):
        self.p = np.array(p0)
        self.dirn = np.array(p1) - np.array(p0)
        self.dist = np.linalg.norm(self.dirn)
        self.dirn /= self.dist # normalize

    def path(self, t):
        return self.p + t * self.dirn


def Intersection(line, center, radius):
    a = np.dot(line.dirn, line.dirn)
    b = 2 * np.dot(line.dirn, line.p - center)
    c = np.dot(line.p - center, line.p - center) - radius * radius

    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return False

    t1 = (-b + np.sqrt(discriminant)) / (2 * a);
    t2 = (-b - np.sqrt(discriminant)) / (2 * a);

    if (t1 < 0 and t2 < 0) or (t1 > line.dist and t2 > line.dist):
        return False

    return True


# p0 = (0., 0.)
# p1 = (1., 1.)
# center = (1., 0.)
# radius1 = 1. / np.sqrt(2) + 0.01
# radius2 = 1. / np.sqrt(2) - 0.01
#
# line = Line(p0, p1)
# print(Intersection(line, center, radius1)) # True
# print(Intersection(line, center, radius2)) # False
# print(Intersection(line, (0.5, 0.5), radius1)) # True
# print(Intersection(line, (2., 2.), radius1)) # False
# print(Intersection(line, (-1., -1.), radius1)) # False



def distance(x, y):
    return np.linalg.norm(np.array(x) - np.array(y))


def isInObstacle(vex):
    for obs in obstacles:
        if distance(obs, vex) < radius:
            return True
    return False


def isThruObstacle(line, obstacles):
    for obs in obstacles:
        if Intersection(line, obs, radius):
            return True
    return False


def nearest(G, vex):
    Nvex = None
    Nidx = None
    minDist = float("inf")

    for idx, v in enumerate(G.vertices):
        line = Line(v, vex)
        if isThruObstacle(line, obstacles):
            continue

        dist = distance(v, vex)
        if dist < minDist:
            minDist = dist
            Nidx = idx
            Nvex = v

    return Nvex, Nidx



class Graph:

    def __init__(self, startpos, endpos):
        self.startpos = startpos
        self.endpos = endpos
        self.vertices = [startpos]
        self.edges = []

        self.sx = endpos[0] - startpos[0]
        self.sy = endpos[1] - startpos[1]

    def randomPosition(self):
        rx = random()
        ry = random()

        posx = self.startpos[0] - (self.sx / 2.) + rx * self.sx * 2
        posy = self.startpos[1] - (self.sy / 2.) + ry * self.sy * 2
        return posx, posy

# startpos = (0., 0.)
# endpos = (3., 2.)
# G = Graph(startpos, endpos)
# G.randomPosition()


def RRT(startpos, endpos):
    G = Graph(startpos, endpos)

    for _ in range(n_iter):
        newvex = G.randomPosition()
        if isInObstacle(newvex):
            continue

        Nvex, Nidx = nearest(G, newvex)
        if Nvex is None:
            continue

        G.edges.append((Nidx, len(G.vertices)))
        G.vertices.append(newvex)

        if distance(newvex, G.endpos) < radius:
            G.edges.append((len(G.vertices)-1, len(G.vertices)))
            G.vertices.append(G.endpos)
            print('success')
            break
    return G


startpos = (0., 0.)
endpos = (5., 5.)
obstacles = [(1., 1.), (2., 2.)]
n_iter = 100
radius = 0.5

G = RRT(startpos, endpos)


def plot(G):
    px = [x for x, y in G.vertices]
    py = [y for x, y in G.vertices]

#     plt.plot(px, py, 'ro')
#     plt.plot(startpos[0], startpos[1], 'go')
#     plt.plot(endpos[0], endpos[1], 'bo')

    fig, ax = plt.subplots()

    ax.scatter(px, py, c='red')
    ax.scatter(startpos[0], startpos[1], c='black')
    ax.scatter(endpos[0], endpos[1], c='black')

    lines = [(G.vertices[edge[0]], G.vertices[edge[1]]) for edge in G.edges]
    lc = mc.LineCollection(lines, linewidths=2)
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.show()


plot(G)