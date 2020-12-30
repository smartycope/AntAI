from Point import *
from Movement import Movement
# from copy import deepcopy
from random import randint
import pygame.gfxdraw
from TkOptions import *
# from Methods import *


class Ant:
    center = None

    def __init__(self):
        # if father is None and mother is not None or father is not None and mother is None:
        #     raise UserWarning('Ant needs a mother and a father, or neither')

        # if father is None and mother is None:
        #     self.dna = []
        # else:
        #     self.dna = father.dna
        #     self.breed(mother.dna, ~self.breedingMethod)

        self.dna = []
        self.pos = Pointi(self.center)
        self.movementIndex = 0
        self.food = 0
        self.foodCollected = 0
        self.color = [255, 255, 255]
        # if center is not None:
        #     self.center = center
        # print(self.center)

        # if percent(mutationChance) and len(self.dna):
        #     self.mutate(~self.mutationMethod)


    def wander(self):
        if self.movementIndex >= len(self.dna) - 1:
            self.dna.append(Movement())
        self.movementIndex += 1
        # print(self.movementIndex)
        # print(len(self.dna))
        self.pos -= self.dna[self.movementIndex - 1].data()


    def run(self):
        self.wander()


    def draw(self, surface):
        pygame.gfxdraw.pixel(surface, *self.pos.datai(), self.color)


    def __gt__(self, ant):
        # Go by amount of food returned. 
        # Otherwise go by amount of food on me. 
        # Otherwise, if I have food, the closer one to center wins.
        # Otherwise, if I don't have food, the furthest one from center wins.
        if self.foodCollected > ant.foodCollected:
            return True
        elif self.foodCollected == ant.foodCollected:
            if self.food > ant.food:
                return True
            elif self.food == ant.food:
                if self.food > 0 and dist(self.pos, self.center) < dist(ant.pos, self.center):
                    return True
                elif self.food == 0 and dist(self.pos, self.center) > dist(ant.pos, self.center):
                    return True

        return False
        
    def __lt__(self, ant):
        if self.foodCollected < ant.foodCollected:
            return True
        elif self.foodCollected == ant.foodCollected:
            if self.food < ant.food:
                return True
            elif self.food == ant.food:
                if self.food > 0 and dist(self.pos, self.center) > dist(ant.pos, self.center):
                    return True
                elif self.food == 0 and dist(self.pos, self.center) < dist(ant.pos, self.center):
                    return True
                    
        return False

    def __str__(self):
        return f'Ant[{self.pos.x}, {self.pos.y}: {self.foodCollected}, {self.food}]'

