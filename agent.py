from collections import namedtuple
from settings import Settings
import numpy as np
import pygame
import pdb

Velocity = namedtuple('Velocity', 'x y')

conf = Settings()

class Agent:
    def __init__(self, conf, infected=False):
        self.x = np.random.randint(0, conf.height)
        self.y = np.random.randint(0, conf.width)
        self.velocity = [5,5]
        self.infected = infected
        self.immune = False
        self.time = 0
        self.conf = conf
        self.dead = False

        self.update_infection()

    def update_velocity(self, x, y):
        self.velocity = Velocity(x, y)

    def update_infection(self):
        if self.dead:
            self.col = (102,0,0)
            self.velocity = [0,0]
        elif self.immune:
            self.col = (0, 204, 102)
        elif self.infected:
            self.col = (255,0,0)
            self.time += 1
        else:
            self.col = (255,255,255)

        if self.time > 500:
            if not self.immune:
                if np.random.rand(1)[0] < self.conf.death_rate:
                    self.dead = True
            self.immune = True
            self.infected = False

    def detect_collision(self):
        if self.x >= conf.width-50:
            self.x = conf.width-50

        if self.y >= conf.height-50:
            self.y = conf.height-50

        if self.x < 50:
            self.x = 50

        if self.y < 50:
            self.y = 50

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        rand = np.random.rand(3)

        if rand[0] < 0.05:
            if rand[1] > 0.5:
                idx = 0
            else:
                idx = 1

            if rand[2] > 0.5:
                self.velocity[idx] *= -1
            else:
                self.velocity[idx] *= -1

        self.update_infection()

    def coords(self):
        self.detect_collision()
        return self.x, self.y, 32, 32

    def draw(self, surface):
        pygame.draw.rect(surface, self.col, self.coords())


def conflict(a1, a2, dist):
    if abs(a1.x - a2.x) <= dist:
        if abs(a1.y - a2.y) <= dist:
            return True

    return False


def resolve_infections(a1, a2, prob=0.2, dist=10):
    """Modifies agents in place to resolve infections."""
    if conflict(a1, a2, dist=dist):
        if a1.infected or a2.infected:
            if np.random.rand(1)[0] < prob:
                a1.infected = True
                a2.infected = True


def resolve_collisions(agents, prob=0.2, dist=10):
    """Simple brute force check for collisions."""
    for i in range(len(agents)):
        for j in range(len(agents)):
            if i is not j:
                resolve_infections(agents[i], agents[j], prob=prob, dist=dist)
