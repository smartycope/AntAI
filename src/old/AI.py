from Cope import reprise, debug, debugged, percent, isPowerOf2, timeFunc
# from random import randint, choice, sample
from TkOptions import Option
# from warnings import warn
# from Point     import *
from Generation import Generation
from copy      import deepcopy



@reprise
class AI:
    framesPerGeneration = Option(300, 'How long each generation lasts', 'Generation', min=10, var='framesPerGeneration')

    def __init__(self, nucleotideType, adam):
        """ Initializes the AI.
            params:
                nucleotideType: The class that is used for induvidual 'bits' of 'dna'.
                                Must have a defualt constructor that creates a 'random'
                                (however you define random in your context) instance.
                                Must have an invert operator overload in order for
                                the Mutations.invert method to work.

                adam: The first instance of the class we're trying to optimize.
                      Must have a copy constructor, a dna data member, a draw function that
                      takes in only a pygame surface as a parameter, and </> operator overloads
                      that describe how to weight the variables.

                optimizeMember: A string with the name of the data member of adam's class that
                                we are trying to optimize.
        """

        self.nucleotideType = nucleotideType
        self.creatureType = type(adam)
        self.generations = [Generation(creatureType=self.creatureType, nucleotideType=self.nucleotideType)]
        self.total = 0
        self.currentFrame = 0

        self.autoBreed =  Option(True, 'Auto-Breed',           'Generation', tooltip='Whether a new generation will be created after a time',                                             var='autoBreed')
        self.skipBadGen = Option(True, 'Skip bad generations', 'Generation', tooltip='Sort the Generations and create a new Generation from the best one, instead of just the last one.', var='skipBadGen')

    def newGen(self):
        self.currentFrame = 0
        for i in self.generations[-1].creatures:
            i.rememberIndex()

        gen = Generation(self.generations if self.skipBadGen.get() else self.generations[-1])

        #* A check to make sure the ants are truely new ants, not copies from the previous generation
        for ant1 in gen.creatures:
            for ant2 in max(self.generations).creatures if self.skipBadGen.get() else self.generations[-1].creatures:
                if ant1 == ant2:
                    raise UserWarning("The ants are shallow copying again!")

        self.generations.append(gen)


    def run(self):
        """ Runs the AI. Returns the current generation's creatures so they can be drawn/checked
        """
        if self.autoBreed.get():
            self.currentFrame += 1
            if self.currentFrame >= self.framesPerGeneration.get():
                self.newGen()

        return self.generations[-1].creatures


    def speedUp(self, amount=1):
        if amount is None:
            self.speed.value = 1
        elif self.speed.value > -amount:
            self.speed.value += amount


    def fix(self):
        print('Turning off and back on again... Fixed!')












'''

Creature.center = Pointi(111, 111)


creature1 = Creature()
creature2 = Creature()

creature1.dna = [0] * 50
creature2.dna = [1] * 50

debug(creature1.dna, creature2.dna, name=('creature1', 'creature2'), color=2)
debug(creature1, creature2, name=('creature1', 'creature2'), color=2)

creatures = []
for i in range(50):
    tmp = Creature()
    tmp.pos = Pointi(-i, i)
    tmp.dna = [i] * 50
    creatures.append(tmp)


class PsuedoInt(int):
    def __new__(cls):
        return 1 #randint(0, 1)


Generation.genSize.value = 50
Generation.romanceMethod.set(Romance.induvidual)
Generation.mutationMethod.set(Mutations.induvidual)
Generation.genGenMethod.set(GenGen.mutationOnly)
gen = Generation(creatureType=Creature, nucleotideType=PsuedoInt)
gen.creatures=[creature1, creature2]

gen2 = Generation(gen)

debug(gen2.creatures)

# mother, father = gen.selectCreatures(creatures, method=Romance.royalLine)

# debug(father.pos, mother.pos, itemLimit=100, name=('father', 'mother'))

'''