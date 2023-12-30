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
from Movement import Movement
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
    max_ants = 1000
    age_of_maturity = 50
    # How we handle ants going off the edge of the screen
    bound_method = 'clip' # or 'loop'

    default_ant_color = (255, 255, 255)
    ant_has_food_color = (229, 169, 66) # Orangy
    ant_collected_food_color = (100, 255, 50) # Green
    ant_collected_and_has_food_color = (120, 160, 70) # military green
    home_color = (210, 40, 250) # Pink
    food_color = (33, 56, 206) # Blue
    dead_ant_color = (120, 120, 120) # Gray

    verbose = False
    color_by_reward = True
    rounds = True

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

        #* Generate food
        self.food = [Rect(*self.rand_pos(), self.food_size, self.food_size) for _ in range(randint(self.min_foods, self.max_foods))]
        self.food_amts = [randint(self.min_food_amt, self.max_food_amt) for _ in range(len(self.food))]
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

    def rand_pos(self):
        return np.array((randint(0, self.size), randint(0, self.size)))

    def reset(self, seed=None, full=False, options=None):
        if full or not self.rounds:
            # Reset the food
            self.food = [Rect(*self.rand_pos(), self.food_size, self.food_size) for _ in range(randint(self.min_foods, self.max_foods))]
            self.food_amts = [randint(self.min_food_amt, self.max_food_amt) for _ in range(len(self.food))]
            self.generation = Generation()
            self.just_full_reset = True
            if not self.rounds:
                # Reset all the ant positions induvidually, since I want them to start spread out, instead of all at the same spot
                for ant in self.generation.creatures:
                    ant.pos = self.rand_pos()# np.array((randint(0, screen_size), randint(0, screen_size)))

        if self.verbose: print(f'The last generation took {self.steps} steps to find {self.food_collected} food')

        self.food_collected = 0
        self.food_gathered = 0

        return super().reset(seed, options)

    def step(self, action, breed_method=None, mutation_method=None):
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
            for ant in self.generation.creatures:
                for i in range(2):
                    if ant[i] < 0:
                        ant[i] = self.size
                    if ant[i] > self.size:
                        ant[i] = 0
        else:
            raise TypeError(f'Unknown `{self.bound_method}` bound_method provided')

        # If we have too many ants, get rid of the worst ones
        if len(self.generation.creatures) > self.max_ants:
            self.generation.creatures = sorted(self.generation.creatures, reverse=True)[:self.max_ants]

        # Handle getting and returning food
        self.checkAnts(breed_method, mutation_method)

        return super().step(action)

    def checkAnts(self, breed_method=None, mutation_method=None):
        # Check if we're touching food
        for ant in self.generation.creatures:
            ant_rect = Rect(*ant.pos, self.ant_size, self.ant_size)
            if (index := ant_rect.collidelist(self.food)) >= 0:
                # Check if the ant is on food, so it'll pick it up
                # This may have an off-by-1 error where say it takes 2, and the food only has 1 food
                # in it, but I don't care enough to fix it.
                if self.food_amts[index] > 0 and not ant.food:
                    taking = Ant.food_capacity - ant.food
                    self.food_amts[index] -= taking
                    self.food_gathered += taking
                    ant.food_gathered += taking
                    ant.food = Ant.food_capacity
                    ant.rememberIndex()

            # Check if the ant is at home, so we drop off food
            if (ant.food or not self.rounds) and Rect(*Ant.home, self.home_size, self.home_size).colliderect(ant_rect):
                if self.verbose: print(f'An ant brought back food {giving}!')

                giving = ant.food if self.rounds else (Ant.food_capacity // 2)
                self.food_collected += giving
                ant.food_collected  += giving
                ant.food -= giving
                ant.rememberIndex(home=True)
                # If we're not doing rounds, we need food to survive. If we're at home, and we're gonna
                # die, take some food from home, if we can
                desire = Ant.food_capacity // 2
                if not self.rounds and ant.food < desire and self.food_gathered >= desire:
                    self.food_gathered -= desire
                    ant.food += desire

            # Check if the ant is next to another ant so they can breed
            # Note that this will run twice, once for each ant
            if not self.rounds:
                ant_rects = [Rect(*a.pos, self.ant_size, self.ant_size) for a in self.generation.creatures if a != ant]
                    # If 2 ants are touching...
                if ((index := ant_rect.collidelist(ant_rects)) >= 0 and
                    # ...and both ants have food...
                    ant.food and self.generation.creatures[index].food and
                    # ...and both ants are old enough...
                    ant.movement_index >= self.age_of_maturity and self.generation.creatures[index].movement_index >= self.age_of_maturity
                ):
                # ...THEN breed the ants
                    baby = Generation.mutate(mutation_method, Generation.breed(breed_method, ant, self.generation.creatures[index]))
                    baby.pos = ant.pos + Movement.max_movement
                    self.generation.creatures.append(baby)

            # Check if the ant is dead
            # Don't delete dead ants, just change the color; the ant limit will clean them up for us
            # if ant.dead:
                # if self.verbose: print('ant is dead, removing')
                # del ant

    def render_pygame(self):
        # Draw the home
        pygame.draw.rect(self.surf, self.home_color, Rect(*Ant.home, self.home_size, self.home_size))

        for ant in self.generation.creatures:
            if self.color_by_reward:
                lower, upper = ant.reward_bounds()
                lower = 0
                upper -= Ant._rewards['food_collected multiplier']
                color = (max(min((ant.reward() - lower) / (upper - lower) * 255, 255), 0), 100, 0) #if not ant.food_collected else (255, 255, 255)
            else:
                if ant.food:
                    if ant.food_collected:
                        color = self.ant_collected_and_has_food_color
                    else:
                        color = self.ant_has_food_color
                elif ant.food_collected:
                    color = self.ant_collected_food_color
                else:
                    color = self.default_ant_color
            # Always show it's dead if it's dead
            if ant.dead:
                color = self.dead_ant_color
            pygame.draw.rect(self.surf, color, Rect(*ant.pos, self.ant_size, self.ant_size))

        for food, amt in zip(self.food, self.food_amts):
            if amt > 0:
                pygame.draw.rect(self.surf, self.food_color, food)

    def handle_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1:
                        self.food.append(Rect(event.pos, (self.food_size, self.food_size)))
                        self.food_amts.append(randint(self.min_food_amt, self.max_food_amt))
                    case 3:
                        if not self.rounds:
                            ant = Ant()
                            ant.pos = event.pos
                            self.generation.creatures.append(ant)
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
                    case pygame.K_a:
                        if not self.rounds:
                            ant = Ant()
                            ant.pos = self.rand_pos()
                            self.generation.creatures.append(ant)

    def debug_button(self):
        print(f'Ants: {len(self.generation.creatures)}')
        print(f'avg dna len: {sum(map(lambda a: len(a.dna), self.generation.creatures))/len(self.generation.creatures)}')

    def _get_reward(self):
        # return np.array([ant.reward() for ant in self.ants])
        return self.generation.reward()
