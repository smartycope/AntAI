from copy import deepcopy
from enum import Enum, auto
from Methods import Romance, romanceTooltip, Mutations, mutationsTooltip, GenGen, GenGenTooltip, Breeding, breedingTooltip
from random import choice, randint, sample
from warnings import warn
from Cope import reprise, debug, percent, isPowerOf2, timeFunc, getTime
from TkOptions import Option
from multiprocessing import Pool
from math import ceil


getChampiant =                         Option(True, 'Display Champiant',                         'General', tooltip='Determines whether to display the best and of the current generation or not.',                 var='getChampiant')

@reprise
class Generation:
    minDnaLen =                         Option(5,    'Minimum chunk width',                       'General', tooltip='The minimum amount of nucleotides any given chunk must have',                                  var='minDnaLen')
    breedingCutoffMinLen =              Option(10,   'cutoff - Minimum cut width',               'Breeding', tooltip='The minimum amount of nucleotides each parent contributes to each of their child\'s dna cuts', var='breedingCutoffMinLen')
    breedingMultiCutsMin =              Option(3,    'multiCut - Minimum cuts',                  'Breeding', tooltip='The minimum amount of cuts multicut cuts',                                                     var='breedingMultiCutsMin')
    breedingMultiCutsMax =              Option(15,   'multiCut - Maximum cuts',                  'Breeding', tooltip='The maximum amount of cuts multicut cuts',                                                     var='breedingMultiCutsMax')
    mutationsInduvidualChance =         Option(20,   'induvidual - Mutation chance',             'Mutating', tooltip='The percent chance for each movement to be mutated',                                           var='mutationsInduvidualChance')
    mutationsMultiCutsMax =             Option(15,   'multiCut - Maximum cuts',                  'Mutating', tooltip='The maximum amount of cuts multicut cuts',                                                     var='mutationsMultiCutsMax')
    mutationsMultiCutsMin =             Option(3,    'multiCut - Minimum cuts',                  'Mutating', tooltip='The minimum amount of cuts multicut cuts',                                                     var='mutationsMultiCutsMin')
    romanceWinnerProbWeight =           Option(1,    'winnerProb - Probibility weight',         'Selection', tooltip='How much romance.winnerProb is weighted',                                                      var='romanceWinnerProbWeight')
    romanceGroupWinnerSecondGroupSize = Option(20,   'groupWinnerSecond - Group size',          'Selection',                                                                                                         var='romanceGroupWinnerSecondGroupSize')
    romanceInbredCouples =              Option(8,    'inbred - Number of couples',              'Selection', tooltip='How many couples inbreed together in romance.inbreed (must be a power of 2)',                  var='romanceInbredCouples')
    romanceRoyalLineCouples =           Option(8,    'royalLine - Number of couples',           'Selection', tooltip='How many couples inbreed together in romance.royalLine (must be a power of 2)',                var='romanceRoyalLineCouples')
    genGenInduvidualNumCouples =        Option(10,   'induvidual - Number of Couples',         'Generation', tooltip='The "n" in GenGen Induvidual',                                                                 var='genGenInduvidualNumCouples')
    genGenIncludeParents =              Option(True, 'Include Parents',                        'Generation', tooltip='Whether we should add the parents of the previous generation to the new generation',           var='genGenIncludeParents')
    mutateAtAll =                       Option(100,  'Mutation Chance',                        'Generation', tooltip='The percent chance that a particular ant is mutated at all.',                                  var='mutateAtAll')
    genSize =                           Option(100,  'Creatures per generation',               'Generation',                                                                                                         var='genSize')
    genScoreBy =                        Option(10,   'Sort Generations by their top N creatures', 'General', tooltip='Generations are sorted by the total scores of their top this many of creatures.',              var='genScoreBy')

    mutationMethod =                    Option(Mutations, 'Mutation method',   'Mutating',   currentItem=Mutations.chunk,      tooltip=mutationsTooltip)
    breedingMethod =                    Option(Breeding,  'Breeding method',   'Breeding',   currentItem=Breeding.induvidual,  tooltip=breedingTooltip)
    romanceMethod =                     Option(Romance,   'Selection Method',  'Selection',  currentItem=Romance.winnerSecond, tooltip=romanceTooltip)
    genGenMethod =                      Option(GenGen,    'Generation Method', 'Generation', currentItem=GenGen.familyLine,    tooltip=GenGenTooltip)

    currentGeneration =                 Option('0', 'Generation ', type_='Label', var='currentGeneration')

    def __init__(self, prevGen=None, nucleotideType=None, creatureType=None):
        self.creatures = []

        if creatureType is None:
            assert(prevGen is not None)
            if type(prevGen) in (list, set, tuple):
                self.creatureType = prevGen[-1].creatureType
            else:
                self.creatureType = prevGen.creatureType
        else:
            self.creatureType = creatureType

        if nucleotideType is None:
            assert(prevGen is not None)
            if type(prevGen) in (list, set, tuple):
                self.nucleotideType = prevGen[-1].nucleotideType
            else:
                self.nucleotideType = prevGen.nucleotideType
        else:
            self.nucleotideType = nucleotideType

        if prevGen is None:
            debug("Creating the first generation", color=6)
            self.num = 0
            self.generate(None, method=GenGen.none)

        elif type(prevGen) is Generation:
            debug(prevGen.num)
            # debug()
            self.num = prevGen.num + 1
            self.generate(prevGen)

        elif type(prevGen) in (tuple, list, set):
            self.num = len(prevGen) #max(prevGen, key=lambda g: g.num).num + 1
            # _prevGen = sorted(prevGen)
            # debug(_prevGen, color=6)
            if getChampiant.get():
                print(f'The best generation so far is Generation {max(prevGen)}')

            # for cnt, i in enumerate(prevGen):
            # bestGen = max(prevGen)

            self.generate(max(prevGen))

        else:
            raise TypeError('PrevGen is not of type Generation, tuple, set, or list')

        # debug(self.mutationMethod.get(), self.breedingMethod.get(), self.romanceMethod.get(), self.genGenMethod.get(), name=('Method',) * 4, color=2)
        # debug(self.creatures, itemLimit=4)
        self.currentGeneration.set(self.num)

    # @timeFunc
    def selectCreatures(self, creatures=None, method=None):
        """ Select a couple for breeding out of self.creatures
            returns: tuple of 2 creatures
        """
        if method is None:
            method = self.romanceMethod.get()

        if creatures is None:
            creatures = self.creatures

        if   method == Romance.induvidual:
            return sample(creatures, 2)

        elif method == Romance.winnerSecond:
            return sorted(creatures)[-3: -1]

        elif method == Romance.winnerProb:
            chanceList = ()
            creatures.sort()

            for cnt, c in enumerate(creatures):
                chanceList += (c,) * (cnt * self.romanceWinnerProbWeight.get())

            return sample(chanceList, 2)

        elif method == Romance.groupWinnerSecond:
            return sorted(sample(creatures, self.romanceGroupWinnerSecondGroupSize.get()))[-3: -1]

        elif method == Romance.royalLine:
            assert(isPowerOf2(self.romanceRoyalLineCouples.get()))

            couples = sorted(creatures)[-self.romanceRoyalLineCouples.get()-1: -1] \
                      if len(creatures) >= self.genSize.get() or not isPowerOf2(len(creatures)) \
                      else creatures

            children = [self.breed(couples[i], couples[i+1])
                        for i in range(0, len(couples), 2)]

            return children \
                   if len(children) == 2 \
                   else self.selectCreatures(children, Romance.royalLine)

        elif method == Romance.inbred:
            assert(isPowerOf2(self.romanceInbredCouples.get()))

            couples = sample(creatures, self.romanceInbredCouples.get()) \
                      if len(creatures) >= self.genSize.get() or not isPowerOf2(len(creatures)) \
                      else creatures

            children = [self.breed(couples[i], couples[i+1]) for i in range(0, len(couples), 2)]

            return children \
                   if len(children) == 2 \
                   else self.selectCreatures(children, Romance.inbred)

        else:
            UserWarning('Generation.romanceMethod is incorrect')

    # @timeFunc
    def mutate(self, creature, method=None):
        if method is None:
            method = self.mutationMethod.get()

        if percent(self.mutateAtAll.get()):
            mutated = self.creatureType(creature)

            if   method == Mutations.cutoff:
                cutoff = randint(0, len(creature.dna) - 1)
                mutated.dna = creature.dna[cutoff:] if percent(50) else creature.dna[:cutoff]

            elif method == Mutations.chunk:
                start, end = sorted(sample(range(len(creature.dna)), 2))
                mutated.dna = creature.dna[:start] + [self.nucleotideType() for _ in range(end-start)] + creature.dna[end:]

            elif method == Mutations.induvidual:
                for cnt in range(len(mutated.dna)):
                    if percent(~self.mutationsInduvidualChance):
                        mutated.dna[cnt] = self.nucleotideType()

            elif method == Mutations.invert:
                try:
                    getattr(self.nucleotideType, '__invert__')
                except NotImplementedError:
                    warn('NucleotideType doesn\'t have an invert operator overload, not mutating...')
                    return creature
                except AttributeError:
                    raise UserWarning('The Nucleotide class you\'re using doesn\'t inhearit from Nucleotide!')

                start, end = sorted(sample(range(len(creature.dna)), 2))

                for i in range(start, end):
                    mutated.dna[i] = ~mutated.dna[i]

            elif method == Mutations.none:
                pass

            elif method == Mutations.multiChunk:
                # Get a random number of indecies between the min and max cut amounts from the length of creatures's dna
                indecies = sorted(sample(range(len(creature.dna) - ~self.breedingCutoffMinLen),
                                                randint(self.mutationsMultiCutsMin.get() * 2, self.mutationsMultiCutsMax.get() * 2)))


                for i in range(len(indecies)):
                    if i % 2:
                        mutated.dna[indecies[i-1]:indecies[i]] = [self.nucleotideType() for _ in range(indecies[i]-indecies[i-1])]

            else:
                UserWarning('Generation.mutationMethod is incorrect')

            return mutated

        else:
            return creature

    # @timeFunc
    def breed(self, father, mother, method=None):
        """ Breed 2 creatures together and mix their dna according to the method specified.
            params:
                father, mother: the creatures to breed together
        """

        if method is None:
            method = self.breedingMethod.get()

        #* Check that the generation isn't too small
        if len(father.dna) < self.minDnaLen.get() or len(mother.dna) < self.minDnaLen.get():
            warn('The last generation was too short, skipping breeding for this generation...')

        child = self.creatureType(father if percent(50) else mother)
        child.dna = []

        if   method == Breeding.cutoff:
            # Get a random index in father
            cutoff = randint(0, len(father.dna) - ~self.breedingCutoffMinLen)
            # Randomly assign one 'half' of each to their child
            child.dna = father.dna[:cutoff] + mother.dna[cutoff:] if percent(50) else mother.dna[:cutoff] + father.dna[cutoff:]

        elif method == Breeding.multiCutoff:
            if len(father.dna) - self.breedingCutoffMinLen.value < self.minDnaLen.value:
                warn('The last generation was too short, skipping breeding for this generation...')
                return father

            # Get a random number of indecies between the min and max cut amounts from the length of father's dna
            indecies = sample(range(len(father.dna) - ~self.breedingCutoffMinLen), randint(~self.breedingMultiCutsMin, ~self.breedingMultiCutsMax))

            # Just to make the loop a little easier
            indecies.append(0)
            indecies.append(len(father.dna))
            indecies.sort()

            chunks = []

            for i in range(len(indecies)):
                if i % 2:
                    chunks.append(father.dna[indecies[i-1]:indecies[i]])
                else:
                    chunks.append(mother.dna[indecies[i-1]:indecies[i]])

            for i in chunks:
                child.dna.extend(i)

        elif method == Breeding.induvidual:
            for f, m in zip(father.dna, mother.dna):
                child.dna.append(f if percent(50) else m)


            '''
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
            '''

        else:
            UserWarning('Generation.breedingMethod is incorrect')

        return child

    @timeFunc
    def generate(self, prevGen, method=None):
        if method is None:
            method = self.genGenMethod.get()

        print(f'Generating Generation {self.num}')

        #* Get the best creature
        if getChampiant.get() and prevGen is not None and method in (GenGen.familyLine, GenGen.induvidual):
            if not len(prevGen.creatures):
                raise UserWarning('The last generation doesn\'t have any creatures in it for some reason')

            print(f'The champiant of generation {prevGen.num} is: {max(prevGen.creatures)}')


        if   method == GenGen.familyLine:
            father, mother = self.selectCreatures(prevGen.creatures)

            # for _ in range(self.genSize.get()):
            #     self.creatures.append(self.breed(father, mother))
            with getTime('breeding'):
                with Pool(1) as process:
                    self.creatures = process.starmap_async(self.breed, ((father, mother),) * self.genSize.get()).get()

            #* Include Parents
            if self.genGenIncludeParents.get():
                self.creatures += [self.creatureType(mother, parent=True), self.creatureType(father, parent=True)]


        elif method == GenGen.induvidual:
            couples = []
            selectedCouple = 0

            for _ in range(~self.genGenInduvidualNumCouples):
                couples.append(self.selectCreatures(prevGen.creatures))

            with Pool(1) as process:
                self.creatures = process.starmap_async(self.breed, couples * ceil(self.genSize.get() / len(couples)),
                                                       self.genSize.get() / 2).get()

            # while len(self.creatures) < self.genSize.get():
            #     father, mother = couples[selectedCouple % len(couples)]
            #     self.creatures.append(self.breed(father, mother))
            #     selectedCouple += 1

            #* Include Parents
            if self.genGenIncludeParents.get():
                for i in couples:
                    self.creatures += [self.creatureType(i[0], parent=True), self.creatureType(i[1], parent=True)]


        elif method == GenGen.none:
            for _ in range(~self.genSize):
                self.creatures.append(self.creatureType())

        elif method == GenGen.mutationOnly:
            self.creatures = prevGen.creatures

        else:
            UserWarning('Generation.genGenMethod is incorrect')

        if method != GenGen.none:
            # Standard:             0.30496
            # Pool():               0.27703
            # Pool(64):             0.93315
            # Pool(16):             0.30685
            # Pool(2):              0.14833
            # Pool(1):              0.10099
            # Pool(1, tasks=None):  0.10288
            # Pool(1, tasks=2):     -------
            # Pool(16, tasks=20):   0.34784
            # Pool(16, tasks=None): 0.3588
            # ThreadPoolExecuter:   0.47117
            # ProcessPoolExecuter:  0.62925
            # Pool(4, tasks=400):   0.13842


            # for i in range(len(self.creatures)):
            #     self.creatures[i] = self.mutate(self.creatures[i])

            # with concurrent.futures.ProcessPoolExecutor() as executor:
            #     for i, mutated in zip(range(len(self.creatures)), executor.map(self.mutate, self.creatures)):
            #         self.creatures[i] = mutated

            with getTime('mutating'):
                with Pool(1) as process:
                    self.creatures = process.map_async(self.mutate, self.creatures).get()

            # with concurrent.futures.ProcessPoolExecutor() as executor:
                # self.creatures = list(executor.map(self.mutate, self.creatures))
                # future = executor.submit(self.mutate, )
                # return_value = future.result()
                # print(return_value)

            # processes = set()
            # for i in range(len(self.creatures)):
            #     p = Process(target = self.mutate, args=(self.creatures[i],))
            #     p.start()
            #     processes.add(p)
            # self.creatures = []
            # for i in processes:
            #     self.creatures.append(i.join())

            # print(self.creatures)

            # with concurrent.futures.ProcessPoolExecutor() as executor:
            #     for i, mutated in zip(range(len(self.creatures)), executor.map(self.mutate, self.creatures)):
            #         self.creatures[i] = mutated

        print(f'{len(self.creatures)} new creatues generated in this generation.')

        # return self.creatures


    def getScore(self):
        total = 0
        for i in sorted(self.creatures)[:self.genScoreBy.get()]:
            total += i.getScore()
        return round(total)


    def __lt__(self, gen):
        assert(type(gen) == Generation)
        if not len(self.creatures) or not len(gen.creatures):
            return True

        #* *Don't* go by the best creature in each generation.
        # return max(self.creatures) < max(gen.creatures)
        #* Go by the collective score if it's contained creatures
        return self.getScore() < gen.getScore()

    def __gt__(self, gen):
        assert(type(gen) == Generation)
        if not len(self.creatures) or not len(gen.creatures):
            return True

        # return max(self.creatures) > max(gen.creatures)
        return self.getScore() > gen.getScore()

    def __str__(self):
        return f'Gen[num={self.num}, score={self.getScore()}, len(creatures)={len(self.creatures)}]'
