from Point import *
from Movement import Movement
# from copy import deepcopy
from random import randint
import pygame.gfxdraw
from TkOptions import *
from Methods import *


mutationsTooltip = '''
How ants are mutated\n
    cutoff:     Only keep up to a certain randomized index, then go off in your own direction\n
    chunk:      Only change a randomized chunk of the dna, keep the rest\n
    induvidual: Randomly change random indecies with random values (random chance or random amount)\n
    invert:     Same as chunk, but instead of creating new data there, invert said data
'''

breedingTooltip = '''
How ants are bred\n
    cutoff:      Cuts the dna at one point, and takes half from each parent\n
    multiCutoff: Cuts the dna at a bunch of points, then takes alternating peices from each parent\n
    induvidual:  Each bit of dna is randomly chosen from each parent
'''

romanceTooltip = '''
How ants are selected to be bred\n
    induvidual:         Each creature has the same probibility of being bred\n
    winnerSecond:       Breed the best creature and the second best creature\n
    winnerProb:         Breed 2 random creatures, weighted by how good they are\n
    groupWinnerSecond:  Take a random selection of creatures, and breed the best 2 of that group\n
    inbred:             Breed the top 2^n creatures with their next best creature, and do that over and over until there's one left
'''

GenGenTooltip = '''
How each generation is generated\n
    familyLine:   Choose one couple, and all the ants in a generation are children of that couple\n
    induvidual:   Repeat the Romance method for n times to get n couples, and the ants in a generation are children of those parents (all couples have approximately the same number of children)\n
    none:         Every generation is completely random, every time\n
    mutationOnly: Instead of breeding, each generation is comprised of mutations of the selected couple (either mother or father, randomly chosen)
'''

minCutoffBreedingLen =      Option(10, 'I don\'t remember what this does')
minBreedingMultiCuts =      Option(3, 'The minimum amount of cuts multicut cuts')
maxBreedingMultiCuts =      Option(20, 'The maximum amount of cuts multicut cuts')
minMutateChunkLen    =      Option(5, 'The minimum amount of movements a chunk can have')
mutateChunkDivisor   =      Option(1.1, 'What amount of the end of the dna to disallow chunking')

class Ant:
    mutationMethod =            Option(Mutations, 'Which Mutation method to use', Mutations.chunk, tooltip=mutationsTooltip)
    breedingMethod =            Option(Breeding, 'Which breeding method to use', Breeding.induvidual, tooltip=breedingTooltip)
    romanceMethod  =            Option(Romance, 'Which method of selecting ants to be bred to use', Romance.winnerSecond, tooltip=romanceTooltip)
    genGenMethod   =            Option(GenGen, 'Which method of generating the next Generation to use', GenGen.familyLine, tooltip=GenGenTooltip)
    induvidualMutationChance =  Option(20, 'The percent chance for each movement to be mutated')

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





def mutate(ant, method):
    mutated = Ant()

    if method == Mutations.cutoff:
        cutoff = randint(0, len(ant.dna) - 1)
        mutated.dna = ant.dna[cutoff:] if percent(50) else ant.dna[:cutoff]

    if method == Mutations.chunk:
        chunkLen = randint(~minMutateChunkLen, int(len(ant.dna) / ~mutateChunkDivisor))
        chunkStart = randint(0, len(ant.dna) - chunkLen)

        generatedData = []
        for _ in range(chunkLen):
            generatedData.append(Movement())

        ant.dna = ant.dna[:chunkStart] + generatedData + ant.dna[chunkStart+chunkLen:]

    if method == Mutations.induvidual:
        for i in ant.dna:
            if percent(~induvidualMutationChance):
                i = Movement()

    if method == Mutations.invert:
        chunkLen = randint(~minChunkLen, len(ant.dna) / ~chunkDivisor)
        chunkStart = randint(0, len(ant.dna) - chunkLen)

        for i in range(chunkLen):
            # You cannot combine this. This is a facinating error.
            ~ant.dna[chunkStart+i]
            ant.dna[chunkStart+1] += 1

    return mutated
    


# TODO MultiCutoff does't do exactly what it's supposed to, but it's close enough for now.
def breed(father, mother, method):
    # I don't care what the parameters actually are, the father is the ant with the longer dna list
    tmpFather = max(father, mother)
    tmpMother = min(father, mother)
    father = tmpFather
    mother = tmpMother

    child = Ant()
    
    if method == Breeding.cutoff:
        # Get a random index in father
        cutoff = randint(0, len(father.dna) - ~minCutoffBreedingLen)
        # Randomly assign one 'half' of each to their child
        child.dna = father.dna[:cutoff] + mother[cutoff:] if percent(50) else mother[:cutoff] + father.dna[cutoff:]

    if method == Breeding.multiCutoff:
        indecies = [randint(0, len(father.dna) - ~minCutoffBreedingLen) for _ in range(randint(~minBreedingMultiCuts, ~maxBreedingMultiCuts))]

        indecies.sort()

        # Just to make the loop a little easier
        indecies.append(0)
        chunks = []

        for i in range(len(indecies) - 1):
            if i % 2:
                chunks.append(father.dna[indecies[i-1]:indecies[i]])
                father.dna = father.dna[indecies[i]:]
            else:
                chunks.append(mother[indecies[i-1]:indecies[i]])
                mother.dna = mother.dna[indecies[i]:]

        for i in chunks:
            child.extend(i)

    if method == Breeding.induvidual:
        # for i in range(len(father.dna)):
        while True:
            # We only need one, because we're replacing, not filling
            if percent(50):
                try:
                    father.dna[i] = mother[i]
                except IndexError:
                    child.dna = father.dna
                    return child
    
    return child



# For testing mutliCutoff
'''
def multiCutoff(father, mother):
    indecies = [randint(0, len(father) - minCutoffBreedingLen) for _ in range(randint(minBreedingMultiCuts, maxBreedingMultiCuts))]
    indecies.sort()
    # Just to make the loop a little easier
    indecies.append(0)
    chunks = []
    for i in range(len(indecies) - 1):
        if i % 2:
            chunks.append(father[indecies[i-1]:indecies[i]])
            father = father[indecies[i]:]
        else:
            chunks.append(mother[indecies[i-1]:indecies[i]])
            mother = mother[indecies[i]:]
    child = []
    for i in chunks:
        child.extend(i)
    return child

multiCutoff(all1, all0)
'''