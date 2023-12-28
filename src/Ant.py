# from Point import Pointi, dist
from Movement import Movement
from random import randint
import pygame.gfxdraw
import pygame
# from TkOptions import Option
# from Cope import reprise, debug, closeEnough
from Creature import Creature
from scipy.spatial.distance import cdist
from copy import copy, deepcopy
import numpy as np
import math


def dist(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


class Ant(Creature):
    # These are set externally
    home = None
    start = None
    limit_after_collected = False
    verbose = False

    def __init__(self, dna=[]):
        self.pos = self.start.copy()
        self.food = 0
        self.food_collected = 0
        self.food_gathered = 0
        self.movement_index = 0
        self.good_indicies = []
        self._limit_index = 0
        super().__init__(dna.copy())

    def __getitem__(self, key):
        return self.pos[key]

    def __setitem__(self, key, value):
        self.pos[key] = value

    def wander(self):
        if self.movement_index >= len(self.dna) - 1:
            self.dna.append(Movement())

        self.pos += self.dna[self.movement_index]
        self.movement_index += 1

    def reset(self, to=None):
        # TODO should I reset the dna here?
        self[0] = self.home[0] if to is None else to[0]
        self[1] = self.home[1] if to is None else to[1]
        self.food = 0
        self.food_collected = 0
        self.food_gathered = 0
        self.movement_index = 0

    def reward(self):
        score = 0
        score += self.food_collected * 100000
        score += self.food * 5000

        # If we have food, get as close to the center as we can.
        # If not, go as far away as we can (to explore)
        assert self.home is not None
        if self.food:
            # score -= cdist(self, self.home, metric='cityblock') * 5
            score -= dist(self, self.home)
        else:
            # score += cdist(self, self.home, metric='cityblock') * 5
            score += dist(self, self.home)

        # Incentivize quicker routes
        for i in range(len(self.good_indicies)-1):
            score -= (self.good_indicies[i+1] - self.good_indicies[i]) * 30

        return score

    def rememberIndex(self, home=False):
        self.good_indicies.append(self.movement_index)
        # This means we just brought food back to home
        # if np.all(self.pos == self.home) and self.movement_index != 0:
        if home:
            self._limit_index = self.movement_index

    def limit(self):
        if self._limit_index == 0:
            return

        if self.verbose:
            print(f'limiting to {self._limit_index}')

        self.dna = self.dna[:self._limit_index]
        self.movement_index = self._limit_index

    def __str__(self):
        return str(self.pos)

    def __repr__(self):
        return f'Ant(collected: {self.food_collected}, gathered: {self.food_gathered}, food: {self.food}, reward: {round(self.reward())})'
