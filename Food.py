from Point import *
import pygame.gfxdraw
from Cope import reprise, debug

@reprise
class Food:
    minFood = 50
    maxFood = 1000
    color   = [255, 100, 100]

    def __init__(self, pos=None, size=None):
        if pos is None:
            self.pos = randomPointi(maxX=size[0], maxY=size[1])
        else:
            self.pos = pos

        self.food = randint(self.minFood, self.maxFood)

    def draw(self, surface):
        pygame.gfxdraw.pixel(surface, *self.pos.datai(), self.color)

    # def isTouching(self, point):
        

    def __str__(self):
        return f'Food[{self.pos.x}, {self.pos.y}: {self.food}]'