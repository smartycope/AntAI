import gymnasium as gym
from typing import Literal, List, Tuple
from gymnasium import spaces
import pygame
from pygame import Rect
from pygame import gfxdraw
import numpy as np
from random import randint
from Generation import Generation
import math
from math import cos, sin, tan, pi
from Ant import Ant
from SimpleGym import SimpleGym
from Options import *

class TabletopEnv(SimpleGym):
    min_foods =  20
    max_foods =  100
    min_food_amt = 20
    max_food_amt = 50
    foodColor = [255, 100, 100]
    food_size = ant_size = home_size = 3
    fps = 20

    default_ant_color = (255, 255, 255)
    ant_has_food_color = (229, 169, 66) # Orangy
    ant_collected_food_color = (100, 255, 50) # Green
    ant_collected_and_has_food_color = (120, 160, 70) # military green
    home_color = (210, 40, 250) # Pink
    food_color = (33, 56, 206) # Blue

    verbose = False

    def __init__(self, first_generation, max_steps, screen_size, start_paused, show_events):
        super().__init__(
            max_steps=max_steps,
            screen_size=screen_size,
            start_paused=start_paused,
            show_events=show_events,
            shown_vars={'Frame': 'steps', 'FPS': 'fps', 'Food Gathered': 'food_gathered', 'Food Collected': 'food_collected'}
        )
        # Food found
        self.food_gathered = 0
        # Food brought back to home
        self.food_collected = 0
        # How we handle ants going off the edge of the screen
        self.bound_method = 'clip' # or 'loop'

        #* Generate food
        # self.min_foods, self.max_foods = 2
        self.food = [Rect(randint(0, self.size), randint(0, self.size), self.food_size, self.food_size) for _ in range(randint(self.min_foods, self.max_foods))]
        self.food_amts = [randint(self.min_food_amt, self.max_food_amt) for _ in range(len(self.food))]
        self.prevChampiant = None
        self.generation = first_generation
        self.just_full_reset = False

        # All the ants positions
        self.observation_space = spaces.Box(low=0, high=self.size, dtype=np.int32, shape=(len(self.generation.creatures), 2))
        # All the ants movements
        self.action_space = spaces.Box(low=-1, high=1, dtype=np.int16, shape=(len(self.generation.creatures), 2))

    def _get_obs(self):
        return self.generation

    def _get_info(self):
        return {
            'food': self.food,
            'food amt': self.food_amts,
        }

    def reset(self, seed=None, full=False, options=None):
        if full:
            # Reset the food
            self.food = [Rect(randint(0, self.size), randint(0, self.size), self.food_size, self.food_size) for _ in range(randint(self.min_foods, self.max_foods))]
            self.food_amts = [randint(self.min_food_amt, self.max_food_amt) for _ in range(len(self.food))]
            self.generation = Generation()
            self.just_full_reset = True

        if self.verbose: print(f'The last generation took {self.steps} steps to find {self.food_collected} food')

        self.food_collected = 0
        self.food_gathered = 0

        return super().reset(seed, options)

    def step(self, action):
        # Make the movements
        # self.ants = self.ants + action
        # [ant.wander() for ant in self.ants]
        self.generation = action
        self.generation.step()
        self.just_full_reset = False

        # Make sure we don't leave the observation space
        if self.bound_method == 'clip':
            # self.ants = np.clip(self.ants, 0, self.size)
            for ant in self.generation.creatures:
                ant.pos = np.clip(ant.pos, 0, self.size)
            # self.ants[:, :2] = np.clip(self.ants[:, :2], 0, self.size)
        elif self.bound_method == 'loop':
            raise NotImplementedError
        else:
            raise TypeError(f'Unknown `{self.bound_method}` bound_method provided')

        # Handle getting and returning food
        self.checkAnts()

        return super().step(action)

    def checkAnts(self):
        #* Check if we're touching food
        for ant in self.generation.creatures:
            ant_rect = Rect(*ant.pos, self.ant_size, self.ant_size)
            if (index := ant_rect.collidelist(self.food)) >= 0:
            # Check if the ant is next to food, so it'll pick it up
            # for food in self.food:
                # pygame.Rect
                # if isAdj(food, ant):
                    # if ant.food < 1:
                if self.food_amts[index] > 0 and not ant.food:
                    self.food_amts[index] -= 1
                    self.food_gathered += 1
                    ant.food_gathered += 1
                    ant.food = 1
                    ant.rememberIndex()

            # Check if the ant is at home, so we drop off food
            # if ant.food and isAdj(Ant.home, ant):
            if ant.food and Rect(*Ant.home, self.home_size, self.home_size).colliderect(ant_rect):
                self.food_collected += 1
                ant.food_collected  += 1
                ant.food -= 1
                ant.rememberIndex(home=True)
                # if self.verbose: print('An ant brought back food!')
                # ant.rememberIndex()
                # print(f'{a} is adjacent to the center at {self.center}')

    def render_pygame(self):
        # Draw the home
        pygame.draw.rect(self.surf, self.home_color, Rect(*Ant.home, self.home_size, self.home_size))

        for ant in self.generation.creatures:
            if ant.food:
                if ant.food_collected:
                    color = self.ant_collected_and_has_food_color
                else:
                    color = self.ant_has_food_color
                # print('an ant has food')
            elif ant.food_collected:
                color = self.ant_collected_food_color
            else:
                color = self.default_ant_color

            # ant.draw(self.surf, color)
            # pygame.gfxdraw.pixel(surface, *self.astype(np.int32), color)
            pygame.draw.rect(self.surf, color, Rect(*ant.pos, self.ant_size, self.ant_size))

        for food, amt in zip(self.food, self.food_amts):
            # pygame.gfxdraw.pixel(self.surf, f[0], f[1], self.food_color)
            # print(self.food_color + (amt/255,))
            if amt > 0:
                pygame.draw.rect(self.surf, self.food_color, food)

    def handle_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1:
                        self.food.append(Rect(event.pos, (self.food_size, self.food_size)))
                        self.food_amts.append(randint(self.min_food_amt, self.max_food_amt))
            case pygame.KEYUP:
                match event.unicode:
                    case 'R':
                        self.reset(full=True)
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.fps += 10
                    case pygame.K_DOWN:
                        self.fps -= 10

    def debug_button(self):
        print(any([a.food for a in self.generation.creatures]))

    def _get_reward(self):
        # return np.array([ant.reward() for ant in self.ants])
        return self.generation.reward()
