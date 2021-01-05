from copy import deepcopy
from enum import Enum, auto
from random import choice, randint
from warnings import warn
from Cope import reprise, debug, percent
from Ant import Ant
# from AntScene import AntScene
from Methods import *
from Movement import Movement
from Point import Pointi
from TkOptions import Option, Tracker

@reprise
class Generation:
    breedingCutoffMinLen =              Option(10,  'I don\'t remember what this does', tooltip='(breedingCutoffMinLen)')
    breedingMultiCutsMin =              Option(3,   'Min multiCuts',                    tooltip='The minimum amount of cuts multicut cuts\n(breedingMultiCutsMin)')
    breedingMultiCutsMax =              Option(20,  'Max multiCuts',                    tooltip='The maximum amount of cuts multicut cuts\n(breedingMultiCutsMax)')
    mutationsChunkMinLen =              Option(5,   'Minimum chunk length',             tooltip='The minimum amount of movements a chunk can have\n(mutationsChunkMinLen)')
    # mutationsChunkDivisor =             Option(1.1, 'No longer used',                   tooltip='What amount of the end of the dna to disallow chunking/n(mutationsChunkDivisor)')
    mutationsInduvidualChance =         Option(30,  'Induvitual mutation chance',       tooltip='The percent chance for each movement to be mutated\n(mutationsInduvidualChance)')
    romanceWinnerProbWeight =           Option(1,   'WinnerProb probibility weight',    tooltip='How much romance.winnerProb is weighted\n(romanceWinnerProbWeight)')
    romanceGroupWinnerSecondGroupSize = Option(20,  'Group Size for GroupWinnerSecond', tooltip='How many end children to inbreed together in romance.inbreed (must be a power of 2)\n(romanceGroupWinnerSecondGroupSize)')
    romanceInbredN =                    Option(8,   'Inbreeding count',                 tooltip='How many end children to inbreed together in romance.inbreed (must be a power of 2)\n(romanceInbredN)')
    genGenInduvidualNumCouples =        Option(10,  'Number of Couples',                tooltip='The "n" in GenGen Induvidual\n(genGenInduvidualNumCouples)')
    genGenIncludeParents =              Option(True, widgetText='Include Parents',      tooltip='Whether we should add the parents of the previous generation to the new generation\n(genGenIncludeParents)')
    doMutation =                        Option(True, widgetText='Mutate',               tooltip='Whether or not to mutate each Generation\n(doMutation)')
    genSize =                           Option(100,   'How many ants per generation',   tooltip='(genSize)')
    framesPerGeneration =               Option(300,   'How long each generation lasts', tooltip='(framesPerGeneration)', min=~mutationsChunkMinLen)

    mutationMethod =                    Option(Mutations, 'Mutation method', Mutations.chunk,                            tooltip=mutationsTooltip)
    breedingMethod =                    Option(Breeding,  'Breeding method', Breeding.induvidual,                        tooltip=breedingTooltip)
    romanceMethod =                     Option(Romance,   'Method of selecting ants to be bred', Romance.winnerSecond,   tooltip=romanceTooltip)
    genGenMethod =                      Option(GenGen,    'Method of generating the next Generation', GenGen.familyLine, tooltip=GenGenTooltip)
    

    def __init__(self, prevGen=None):
        self.ants = []

        if prevGen is None:
            self.num = Tracker(0, 'Which generation this is')
            self.generate(prevGen, method=GenGen.none)

        elif type(prevGen) is Generation:
            self.num = Tracker(prevGen.num.get() + 1, 'Which generation this is')
            self.generate(prevGen)

        elif type(prevGen) in (tuple, list):
            self.num = Tracker(max(prevGen, key=lambda g: g.num.get()).num.get(), 'Which generation this is')
            self.generate(max(prevGen))

        else:
            raise TypeError('PrevGen is not of type Generation, tuple, or list')

        # self.num = Tracker(self.num, 'Which generation this is')


    def selectAnts(self, ants=None):
        if ants is None:
            ants = self.ants

        returnAnts = []

        if ~self.romanceMethod == Romance.induvidual:
            tmp = choice(ants)
            returnAnts.append(tmp)
            del tmp # ants[ants.index(tmp)]
            returnAnts.append(choice(ants))

        if ~self.romanceMethod == Romance.winnerSecond:
            ants.sort()
            returnAnts = ants[-3: -1]
            
        if ~self.romanceMethod == Romance.winnerProb:
            chanceList = []
            ants.sort()

            for cnt, ant in enumerate(ants):
                chanceList += [ant] * (cnt * ~self.romanceWinnerProbWeight)
            
            returnAnts.append(choice(chanceList))
            returnAnts.append(choice(chanceList))

        if ~self.romanceMethod == Romance.groupWinnerSecond:
            group = []

            for _ in range(~self.romanceGroupWinnerSecondGroupSize):
                tmp = choice(ants)
                group.append(tmp)
                del tmp


            group.sort()
            returnAnts = group[-3: -1]

        if ~self.romanceMethod == Romance.inbred:
            # self.selectAnts()
            warn('Inbreed Method is not yet implemented')
            '''
            def breedOnce(amt, ants):
                ants.sort()
                for i in range(int(amt / 2)):
                    ants[i*2]
            '''

        return returnAnts


    def mutate(self, ant):
        mutated = Ant()

        if ~self.mutationMethod == Mutations.cutoff:
            cutoff = randint(0, len(ant.dna) - 1)
            mutated.dna = ant.dna[cutoff:] if percent(50) else ant.dna[:cutoff]

        if ~self.mutationMethod == Mutations.chunk:
            chunkLen = randint(~self.mutationsChunkMinLen, len(ant.dna) - ~self.mutationsChunkMinLen)
            chunkStart = randint(0, len(ant.dna) - chunkLen)

            generatedData = []
            for _ in range(chunkLen):
                generatedData.append(Movement())

            mutated.dna = ant.dna[:chunkStart] + generatedData + ant.dna[chunkStart+chunkLen:]

        if ~self.mutationMethod == Mutations.induvidual:
            mutated.dna = ant.dna
            for cnt in range(len(ant.dna)):
                if percent(~self.mutationsInduvidualChance):
                    mutated.dna[cnt] = Movement()

        if ~self.mutationMethod == Mutations.invert:
            mutated.dna = ant.dna
            if len(ant.dna) < (~self.mutationsChunkMinLen * 2) + 1:
                warn('The last generation was too short, skipping mutating for this generation...')
                return ant

            chunkLen = randint(~self.mutationsChunkMinLen, len(ant.dna) - ~self.mutationsChunkMinLen)
            chunkStart = randint(0, len(ant.dna) - chunkLen)

            # debug(chunkLen, chunkStart, mutated, ant)

            for i in range(chunkLen):
                mutated.dna[chunkStart+i] = ~ant.dna[chunkStart+i]

        return mutated


    def breed(self, father, mother):
        #* Check that the generation isn't too small
        if len(father.dna) < ~self.mutationsChunkMinLen or len(mother.dna) < ~self.mutationsChunkMinLen:
            warn('The last generation was too short, skipping breeding for this generation...')
            # debug(f)

        #* I don't care what the parameters actually are, the father is the ant with the longer dna list
        try:
            father = deepcopy(max(father, mother, key=lambda x: len(x.dna)))
            mother = deepcopy(min(father, mother, key=lambda x: len(x.dna)))
        except TypeError:
            # print(f'Type of father: {type(father)}\n Type of mother: {type(mother)}')
            print(f'Type of father: {max(father, mother, key=lambda x: len(x.dna))}')

        child = Ant()
        
        if ~self.breedingMethod == Breeding.cutoff:
            # Get a random index in father
            cutoff = randint(0, len(father.dna) - ~self.breedingCutoffMinLen)
            # Randomly assign one 'half' of each to their child
            child.dna = father.dna[:cutoff] + mother.dna[cutoff:] if percent(50) else mother.dna[:cutoff] + father.dna[cutoff:]

        if ~self.breedingMethod == Breeding.multiCutoff:
            if len(father.dna) - self.breedingCutoffMinLen.value < self.mutationsChunkMinLen.value:
                warn('The last generation was too short, skipping breeding for this generation...')
                return mother, father

            indecies = [randint(0, len(father.dna) - ~self.breedingCutoffMinLen) for _ in range(randint(~self.breedingMultiCutsMin, ~self.breedingMultiCutsMax))]

            indecies.sort()

            # Just to make the loop a little easier
            indecies.append(0)
            chunks = []

            for i in range(len(indecies) - 1):
                if i % 2:
                    chunks.append(father.dna[indecies[i-1]:indecies[i]])
                    father.dna = father.dna[indecies[i]:]
                else:
                    chunks.append(mother.dna[indecies[i-1]:indecies[i]])
                    mother.dna = mother.dna[indecies[i]:]

            for i in chunks:
                child.dna.extend(i)

        if ~self.breedingMethod == Breeding.induvidual:
            # for i in range(len(father.dna)):
            i = 0
            while True:
                # We only need one, because we're replacing, not filling
                if percent(50):
                    try:
                        father.dna[i] = mother.dna[i]
                    except IndexError:
                        child.dna = father.dna
                        return child
                i += 1
        
        return child


    def generate(self, prevGen, method=None):
        if method is None:
            method = ~self.genGenMethod

        print(f'Generating Generation {self.num.get()}')

        debug(len(self.ants), calls=1, name='length of ants')
        debug(self.num.value, method)

        # if ~self.num:
        #     debug(self.ants[0])

        #* Get the best ant
        if prevGen is not None and method in (GenGen.familyLine, GenGen.induvidual):
            prevGen.ants.sort()
            debug(prevGen, prevGen.ants)
            # debug(max(prevGen.ants), calls=1)
            debug(len(prevGen.ants), calls=1, name='length of ants')

            if not len(prevGen.ants):
                raise UserWarning('The last generation doesn\'t have any ants in it for some reason')

            champiant = max(prevGen.ants)
            debug(champiant)
            debug(f'{prevGen.ants.index(champiant)}')
            print(f'The champiant of generation {prevGen.num.get()} is:', champiant)

        if method == GenGen.familyLine:
            father, mother = self.selectAnts(prevGen.ants)

            if ~self.genGenIncludeParents:
                newFather = father.strip()
                newMother = mother.strip()
                newFather.color = newMother.color = Ant.parentAntColor
                self.ants.append(newFather)
                self.ants.append(newMother)
                # self.ants += [father.strip().setAsParent(), mother.strip().setAsParent()]

            for _ in range(~self.genSize):
                self.ants.append(self.breed(father, mother))

        if method == GenGen.induvidual:
            couples = []
            selectedCouple = 0

            for _ in range(~self.genGenInduvidualNumCouples):
                couples.append(self.selectAnts(prevGen.ants))

            if ~self.genGenIncludeParents:
                for i in couples:
                    newFather = i[0].strip()
                    newMother = i[1].strip()
                    newFather.color = newMother.color = Ant.parentAntColor
                    self.ants.append(newFather)
                    self.ants.append(newMother)
                    # self.ants += [father.strip().setAsParent(), mother().setAsParent()]

            while len(self.ants) < ~self.genSize:
                father, mother = couples[selectedCouple % len(couples)]
                self.ants.append(self.breed(father, mother))
                selectedCouple += 1

        if method == GenGen.none:
            for _ in range(~self.genSize):
                self.ants.append(Ant())
            
        if method == GenGen.mutationOnly:
            for i in self.ants:
                i.strip()

        if ~self.doMutation and method != GenGen.none:
            for i in self.ants:
                i = self.mutate(i.strip())

        print(f'{len(self.ants)} new ants generated in this generation.')

        return self.ants


    def __lt__(self, gen):
        assert(type(gen) == Generation)
        if not len(self.ants) or not len(gen.ants):
            return True
        #* Go by the best ant in each generation
        return max(self.ants) > max(gen.ants)

    def __gt__(self, gen):
        assert(type(gen) == Generation)
        if not len(self.ants) or not len(gen.ants):
            return True
        return max(self.ants) < max(gen.ants)

    def __str__(self):
        return f'Gen[num={~self.num}, len(ants)={len(self.ants)}]'
