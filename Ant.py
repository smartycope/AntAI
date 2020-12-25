from Point import *
from Movement import Movement
# from copy import deepcopy
from random import randint
from enum import Enum, auto
import pygame.gfxdraw
from TkOptions import *

class Mutations(Enum):
    cutoff     = auto() # Only keep up to a certain randomized index, then go off in your own direction
    chunk      = auto() # Only change a randomized chunk of the dna, keep the rest
    induvidual = auto() # Randomly change random indecies with random values (random chance or random amount)
    invert     = auto() # Same as chunk, but instead of creating new data there, invert said data

class Breeding(Enum):
    cutoff      = auto() # Cuts the dna at one point, and takes half from each parent
    multiCutoff = auto() # Cuts the dna at a bunch of points, then takes alternating peices from each parent
    induvidual  = auto() # Each bit of dna is randomly chosen from each parent


class Ant:
    mutationMethod =            Option(Mutations, 'Which Mutation method to use', Mutations.chunk)
    breedingMethod =            Option(Breeding, 'Which breeding method to use', Breeding.induvidual)
    minChunkLen  =              Option(5, 'The minimum amount of movements a chunk can have')
    chunkDivisor =              Option(1.1, 'What amount of the end of the dna to disallow chunking')
    induvidualMutationChance =  Option(20, 'The percent chance for each movement to be mutated') # Edit this to actually use a percentage
    minCutoffBreedingLen =      Option(10, 'I don\'t remember what this does')
    minBreedingMultiCuts =      Option(3, 'The minimum amount of cuts multicut cuts')
    maxBreedingMultiCuts =      Option(20, 'The maximum amount of cuts multicut cuts')

    def __init__(self, mother=None, father=None, mutationChance=50, center=Pointi(0, 0)):
        if father is None and mother is not None or father is not None and mother is None:
            raise UserWarning('Ant needs a mother and a father, or neither')

        if father is None and mother is None:
            self.dna = []
        else:
            self.dna = father.dna
            self.breed(mother.dna, ~self.breedingMethod)

        self.pos = Pointi(center)
        self.movementIndex = 0
        self.food = 0
        self.foodCollected = 0
        self.color = [255, 255, 255]
        self.center = center

        if percent(mutationChance) and len(self.dna):
            self.mutate(~self.mutationMethod)

        # If we're inheriting dna
        # if not len(dna):
        #     if len(dna) < 2:
        #         raise IndexError("Try increasing the amount of time a generation runs for.")
        #     self.mutate(~self.mutationMethod)


    def mutate(self, method):
        if method == Mutations.cutoff:
            cutoff = randint(0, len(self.dna) - 1)
            self.dna = self.dna[:cutoff]

        if method == Mutations.chunk:
            chunkLen = randint(~self.minChunkLen, int(len(self.dna) / ~self.chunkDivisor))
            chunkStart = randint(0, len(self.dna) - chunkLen)

            generatedData = []
            for _ in range(chunkLen):
                generatedData.append(Movement())

            self.dna = self.dna[:chunkStart] + generatedData + self.dna[chunkStart+chunkLen:]

        if method == Mutations.induvidual:
            for i in self.dna:
                if randint(0, ~self.induvidualMutationChance) == 0:
                    i = Movement()

        if method == Mutations.invert:
            chunkLen = randint(~self.minChunkLen, len(self.dna) / ~self.chunkDivisor)
            chunkStart = randint(0, len(self.dna) - chunkLen)

            for i in range(chunkLen):
                # You cannot combine this. This is a facinating error.
                ~self.dna[chunkStart+i]
                self.dna[chunkStart+1] += 1


    def breed(self, dna, method):
        if method == Breeding.cutoff:
            cutoff = randint(0, len(self.dna) - ~self.minCutoffBreedingLen)
            if randint(0, 1) == 0:
                self.dna = self.dna[:cutoff] + dna[cutoff:]
            else:
                self.dna = dna[:cutoff] + self.dna[cutoff:]

        if method == Breeding.multiCutoff:
            indecies = [randint(0, len(self.dna) - ~self.minCutoffBreedingLen) for _ in range(randint(~self.minBreedingMultiCuts, ~self.maxBreedingMultiCuts))]

            indecies.sort()
            # Just to make the loop a little easier
            indecies.append(0)
            chunks = []

            for i in range(len(indecies) - 1):
                if i % 2:
                    chunks.append(self.dna[indecies[i-1]:indecies[i]])
                    self.dna = self.dna[indecies[i]:]
                else:
                    chunks.append(dna[indecies[i-1]:indecies[i]])
                    self.dna = self.dna[indecies[i]:]

        if method == Breeding.induvidual:
            for i in range(len(self.dna)):
                # We only need one, because we're replacing, not filling
                if randint(0, 1) == 0:
                    try:
                        self.dna[i] = dna[i]
                    except IndexError:
                        return


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
        # Go by amount of food returned. Otherwise go by amount of food collected. Otherwise go by length of dna.
        if self.foodCollected < ant.foodCollected:
            return True
        elif self.foodCollected == ant.foodCollected and self.food < ant.food:
            return True
        # elif self.foodCollected == ant.foodCollected and self.food == ant.food and len(self.dna) < len(ant.dna):
        #     return True
        elif self.foodCollected == ant.foodCollected and self.food == ant.food and self.food and dist(self.pos, self.center) > dist(ant.pos, self.center):
            return True
        else:
            return False
        
    def __lt__(self, ant):
        # Go by amount of food returned. Otherwise go by amount of food collected. Otherwise go by length of dna.
        if self.foodCollected > ant.foodCollected:
            return True
        elif self.foodCollected == ant.foodCollected and self.food > ant.food:
            return True
        elif self.foodCollected == ant.foodCollected and self.food == ant.food and self.food and dist(self.pos, self.center) < dist(ant.pos, self.center):
            return True
        else:
            return False

    def __str__(self):
        return f'Ant[{self.pos.x}, {self.pos.y}: {self.foodCollected}, {self.food}]'