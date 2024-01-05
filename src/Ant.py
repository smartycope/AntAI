# from Point import Pointi, dist
from Movement import Movement
from random import randint
import pygame.gfxdraw
import pygame
from Creature import Creature
# from scipy.spatial.distance import cdist
from copy import copy, deepcopy
import numpy as np
import math
from typing import Tuple


def dist(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


class Ant(Creature):
    # These are set externally
    home = None
    start = None
    limit_after_collected = False
    verbose = False
    rounds = True
    memory = 200
    stomach = 50
    food_capacity = 2
    max_age = None

    def __init__(self, dna=[]):
        self.pos = self.start.copy()
        self.hunger = 0
        self.food = 0
        self.dead = False
        self.food_collected = 0
        self.food_gathered = 0
        self.movement_index = 0
        self.good_indicies = []
        self.steps_since_collected_food = 0
        self.age = 0
        self._limit_index = 0
        super().__init__(dna.copy())

    def __getitem__(self, key):
        return self.pos[key]

    def __setitem__(self, key, value):
        self.pos[key] = value

    def wander(self):
        if self.dead:
            return

        self.steps_since_collected_food += 1
        self.age += 1
        self.hunger += 1

        if self.movement_index >= len(self.dna) - 1:
            self.dna.append(Movement())
        # If we're simulating real time, and the index isn't at the end, *then* increment it
        elif not self.rounds:
            self.movement_index += 1

        self.pos += self.dna[self.movement_index]

        # If we're doing rounds, dna just keeps growing (unless it's limited)
        if self.rounds:
            self.movement_index += 1
        # Otherwise, movement_index doesn't change, but we do need to drop the other end
        elif len(self.dna) > self.memory:
            self.dna.pop(0)

        if not self.rounds:
            # Kill if we haven't eaten in too long
            if self.hunger >= self.stomach:
                if self.food:
                    self.food -= 1
                    self.hunger = 0
                # We haven't eaten in too long, and we aren't holding food
                else:
                    self.dead = True
            # Kill if we're too old
            if self.max_age is not None and self.age > self.max_age:
                self.dead = True

    def reset(self, to=None):
        # TODO should I reset the dna here?
        self[0] = self.home[0] if to is None else to[0]
        self[1] = self.home[1] if to is None else to[1]
        self.food = 0
        self.food_collected = 0
        self.food_gathered = 0
        self.movement_index = 0
        self.hunger = 0
        self.dead = False
        self.steps_since_collected_food = 0

    _rewards = {
        # The starting amount
        'base': 0,
        'food_collected multiplier': 100_000,
        'has food bonus': 1000,
        # If we have food, how bad is it we're away from home per pixel
        'distance to home penalty': 10,
        # If we don't have food, how good is it we're away from home pixel
        'distance from home bonus': 1000,
        'age bonus': 5,
        'hunger penalty': 100,
        # If it's taken you 500 steps since you last got food, you may not be going anywhere
        'steps since food penalty': 100_000 / 200,
        'route length penalty': 20,
        'dead score': -100_000,
    }

    def reward_bounds(self) -> Tuple[min, max]:
        score = self._rewards['base']
        # Not realistic, but good for using the bounds to determine the ant's color
        score += 1 * self._rewards['food_collected multiplier']
        if self.rounds:
            score += max(self.food_capacity * self._rewards['has food bonus'], dist(self.pos, self.home) * self._rewards['distance from home bonus'])
        else:
            score += self.food_capacity * self._rewards['has food bonus']
            score += self.memory * self._rewards['age bonus']
        # Being dead *should* return the lowest reward possible
        return self._rewards['dead score'], score

    def reward(self):
        score = self._rewards['base']
        score += self.food_collected * self._rewards['food_collected multiplier']
        score += self.food * self._rewards['has food bonus']

        # If we have food, get as close to the center as we can.
        # If not, go as far away as we can (to explore)
        assert self.home is not None
        if self.food:
            # score -= cdist(self, self.home, metric='cityblock') * 5
            score -= dist(self.pos, self.home) * self._rewards['distance to home penalty']
        elif self.rounds:
            # score += cdist(self, self.home, metric='cityblock') * 5
            score += dist(self.pos, self.home) * self._rewards['distance from home bonus']

        if not self.rounds:
            # Incentivize quicker routes
            for i in range(len(self.good_indicies)-1):
                score -= (self.good_indicies[i+1] - self.good_indicies[i]) * self._rewards['route length penalty']
        else:
            score += self.age * self._rewards['age bonus']
            score -= self.hunger * self._rewards['hunger penalty']
            score -= self.steps_since_collected_food * self._rewards['steps since food penalty']

        if self.dead and not self.rounds:
            score = self._rewards['dead score']

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
