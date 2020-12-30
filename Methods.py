from enum import Enum, auto
from Ant import Ant
from TkOptions import Option
from random import randint, choice
from copy import deepcopy
from Point import debug, percent

# TODO Breed.MultiCutoff does't do exactly what it's supposed to, but it's close enough for now.
# TODO: Add a multiCutoff to Mutations
# TODO: Add a multiInvert to Mutations
# TODO: Add a weightedInduvidual to GenGen
# TODO: Make the parent ants be a different color


#* Enums
#* How ants are mutated
class Mutations(Enum):
    cutoff     = auto() # Only keep up to a certain randomized index, then go off in your own direction
    chunk      = auto() # Only change a randomized chunk of the dna, keep the rest
    induvidual = auto() # Randomly change random indecies with random values (random chance or random amount)
    invert     = auto() # Same as chunk, but instead of creating new data there, invert said data

#* How ants are bred
class Breeding(Enum):
    cutoff      = auto() # Cuts the dna at one point, and takes half from each parent
    multiCutoff = auto() # Cuts the dna at a bunch of points, then takes alternating peices from each parent
    induvidual  = auto() # Each bit of dna is randomly chosen from each parent

#* How ants are selected to be bred
class Romance(Enum):
    induvidual        = auto() # Each creature has the same probibility of being bred
    winnerSecond      = auto() # Breed the best creature and the second best creature
    winnerProb        = auto() # Breed 2 random creatures, weighted by how good they are
    groupWinnerSecond = auto() # Take a random selection of creatures, and breed the best 2 of that group
    inbred            = auto() # Breed the top 2^n creatures with their next best creature, and do that over and over until there's one left

#* How each generation is generated
class GenGen(Enum):
    familyLine   = auto() # Choose one couple, and all the ants in a generation are children of that couple
    induvidual   = auto() # Repeat the Romance method for n times to get n couples, and the ants in a generation are children of those parents (all couples have approximately the same number of children)
    none         = auto() # Every generation is completely random, every time
    mutationOnly = auto() # Instead of breeding, each generation is comprised of mutations of the selected couple (either mother or father, randomly chosen)


#* Descriptions
mutationsTooltip = '''
How ants are mutated\n
 cutoff: Only keep up to a certain randomized index, then go off in your own direction\n
 chunk: Only change a randomized chunk of the dna, keep the rest\n
 induvidual: Randomly change random indecies with random values (random chance or random amount)\n
 invert: Same as chunk, but instead of creating new data there, invert said data
 \n(mutationMethod)
'''

breedingTooltip = '''
How ants are bred\n
 cutoff: Cuts the dna at one point, and takes half from each parent\n
 multiCutoff: Cuts the dna at a bunch of points, then takes alternating peices from each parent\n
 induvidual: Each bit of dna is randomly chosen from each parent
 \n(breedingMethod)
'''

romanceTooltip = '''
How ants are selected to be bred\n
 induvidual: Each creature has the same probibility of being bred\n
 winnerSecond: Breed the best creature and the second best creature\n
 winnerProb: Breed 2 random creatures, weighted by how good they are\n
 groupWinnerSecond: Take a random selection of creatures, and breed the best 2 of that group\n
 inbred: Breed the top 2^n creatures with their next best creature, and do that over and over until there's one left
 \n(romanceMethod)
'''

GenGenTooltip = '''
How each generation is generated\n
 familyLine: Choose one couple, and all the ants in a generation are children of that couple\n
 induvidual: Repeat the Romance method for n times to get n couples, and the ants in a generation are children of those parents (all couples have approximately the same number of children)\n
 none: Every generation is completely random, every time\n
 mutationOnly: Instead of breeding, each generation is comprised of mutations of the selected couple (either mother or father, randomly chosen)
 \n(genGenMethod)
'''


#* Options
breedingCutoffMinLen =              Option(10,  'I don\'t remember what this does', tooltip='(breedingCutoffMinLen)')
breedingMultiCutsMin =              Option(3,   'Min multiCuts',                    tooltip='The minimum amount of cuts multicut cuts\n(breedingMultiCutsMin)')
breedingMultiCutsMax =              Option(20,  'Max multiCuts',                    tooltip='The maximum amount of cuts multicut cuts\n(breedingMultiCutsMax)')
mutationsChunkMinLen =              Option(5,   'Minimum chunk length',             tooltip='The minimum amount of movements a chunk can have\n(mutationsChunkMinLen)')
mutationsChunkDivisor =             Option(1.1, 'No longer used',                   tooltip='What amount of the end of the dna to disallow chunking/n(mutationsChunkDivisor)')
mutationsInduvidualChance =         Option(30,  'Induvitual mutation chance',       tooltip='The percent chance for each movement to be mutated\n(mutationsInduvidualChance)')
romanceWinnerProbWeight =           Option(1,   'WinnerProb probibility weight',    tooltip='How much romance.winnerProb is weighted\n(romanceWinnerProbWeight)')
romanceGroupWinnerSecondGroupSize = Option(20,  'Group Size for GroupWinnerSecond', tooltip='How many end children to inbreed together in romance.inbreed (must be a power of 2)\n(romanceGroupWinnerSecondGroupSize)')
romanceInbredN =                    Option(8,   'Inbreeding count',                 tooltip='How many end children to inbreed together in romance.inbreed (must be a power of 2)\n(romanceInbredN)')
genGenInduvidualNumCouples =        Option(10,  'Number of Couples',                tooltip='The "n" in GenGen Induvidual\n(genGenInduvidualNumCouples)')
genGenIncludeParents =              Option(True, widgetText='Include Parents',      tooltip='Whether we should add the parents of the previous generation to the new generation\n(genGenIncludeParents)')
doMutation =                        Option(True, widgetText='Mutate',               tooltip='Whether or not to mutate each Generation\n(doMutation)')

mutationMethod =                    Option(Mutations, 'Which Mutation method to use', Mutations.chunk,                            tooltip=mutationsTooltip)
breedingMethod =                    Option(Breeding,  'Which breeding method to use', Breeding.induvidual,                        tooltip=breedingTooltip)
romanceMethod =                     Option(Romance,   'Which method of selecting ants to be bred to use', Romance.winnerSecond,   tooltip=romanceTooltip)
genGenMethod =                      Option(GenGen,    'Which method of generating the next Generation to use', GenGen.familyLine, tooltip=GenGenTooltip)


def selectAnts(ants, method=romanceMethod):
    if type(method.value) == str:
        method = getattr(Romance, ~method)

    returnAnts = []

    if method == Romance.induvidual:
        tmp = choice(ants)
        returnAnts.append(tmp)
        del ants[ants.index(tmp)]
        returnAnts.append(choice(ants))

    if method == Romance.winnerSecond:
        ants.sort()
        returnAnts = ants[0:2]
        
    if method == Romance.winnerProb:
        chanceList = []
        ants.sort()

        for cnt, ant in enumerate(ants):
            chanceList += [ant] * (cnt * ~self.romanceWinnerProbWeight)
        
        returnAnts.append(choice(chanceList))
        returnAnts.append(choice(chanceList))

    if method == Romance.groupWinnerSecond:
        group = []

        for i in range(~self.romanceGroupWinnerSecondGroupSize):
            tmp = choice(ants)
            group.append(tmp)
            del ants[ants.index(tmp)]

        group.sort()
        returnAnts = group[0:1]

    if method == Romance.inbred:
        selectAnts(ants, Romance.winnerSecond)
        warn('Inbreed Method is not yet implemented')
        '''
        def breedOnce(amt, ants):
            ants.sort()
            for i in range(int(amt / 2)):
                ants[i*2]
        '''

    return returnAnts


def mutate(ant, method=mutationMethod):
    if type(method.value) == str:
        method = getattr(Mutations, ~method)

    mutated = Ant()

    if method == Mutations.cutoff:
        cutoff = randint(0, len(ant.dna) - 1)
        mutated.dna = ant.dna[cutoff:] if percent(50) else ant.dna[:cutoff]

    if method == Mutations.chunk:
        chunkLen = randint(~minMutateChunkLen, len(ant.dna) - ~minMutateChunkLen)
        chunkStart = randint(0, len(ant.dna) - chunkLen)

        generatedData = []
        for _ in range(chunkLen):
            generatedData.append(Movement())

        mutated.dna = ant.dna[:chunkStart] + generatedData + ant.dna[chunkStart+chunkLen:]

    if method == Mutations.induvidual:
        mutated.dna = ant.dna
        for cnt in range(len(ant.dna)):
            if percent(~induvidualMutationChance):
                mutated[cnt] = Movement()

    if method == Mutations.invert:
        chunkLen = randint(~minMutateChunkLen, len(ant.dna) - ~minMutateChunkLen)
        chunkStart = randint(0, len(ant.dna) - chunkLen)

        for i in range(chunkLen):
            # You cannot combine this. This is a facinating error.
            mutated.dna[chunkStart+i] = ~ant.dna[chunkStart+1] + 1

    return mutated
    

def breed(father, mother, method=breedingMethod):
    if type(method.value) == str:
        method = getattr(Breeding, ~method)

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


def generateGeneration(ants, genSize: Option, method=genGenMethod, breedMethod=breedingMethod, selectionMethod=romanceMethod, mutateMethod=mutationMethod, generation:int=None) -> list:
    if type(method.value) == str:
        method = getattr(GenGen, ~method)

    debug(method)

    print('Generating Generation!')

    # Get the best ant
    if generation is not None and method in (GenGen.familyLine, GenGen.induvidual):
        ants.sort()
        champiant = ants[0]
        print(f'The champiant of generation {generation} is:', champiant)

    newGen = []

    if method == GenGen.familyLine:
        debug()
        father, mother = selectAnts(ants, selectionMethod)

        if ~genGenIncludeParents:
            newGen.append(father)
            newGen.append(mother)

        for _ in range(~genSize):
            newGen.append(breed(father, mother, breedMethod))

        debug(len(newGen))

    if method == GenGen.induvidual:
        couples = []
        selectedCouple = 0

        if ~genGenIncludeParents: 
            for i in couples:
                newGen += i

        for _ in range(~genGenInduvidualNumCouples):
            couples.append(selectAnts(ants, selectionMethod))
        while len(newGen) < 100:
            father, mother = couples[selectedCouple % len(couples)]
            newGen.append(breed(father, mother, breedMethod))
            selectedCouple += 1

    if method == GenGen.none or method == GenGen.mutationOnly:
        for _ in range(~genSize):
           newGen.append(Ant())

    if ~doMutation:
        for i in newGen:
            i = deepcopy(mutate(i, mutationMethod))

    print(len(newGen))

    return newGen

