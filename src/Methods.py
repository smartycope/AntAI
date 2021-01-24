from enum import Enum, auto

# TODO: Add a multiInvert to Mutations
# TODO: Add a weightedInduvidual to GenGen
# Add generation saving
# Add more generation info
# add verbose generation info to options, i.e. food collected that generation, food returned that generation, etc.
# add that info to the menu as well. total food returned, total food returned this generation, stats like that
# add logging to the menu /|\
# add general verboseness (like printing data when an ant collects/returns food) to options
# add an option to incrementally increase the frames per generation with each generation
# maybe add a full auto mode that does /|\ as well as changes the current methods based on different factors (length of time, how well the generations are working, etc.)
# add a Romance method that takes all the ants that have food and breed them, or all the ants that have returned food and breed them, etc.
# make a mutation method or a breeding method or something else that an ant will repeat it's sequence backwards
#   when it finds food, like a real ant would, but with mutations. But add an option to turn it off.
# add a "don't load from save/don't save" parameter to Option
# Make it so if you pass None to OptionMenu, it doesn't create a notebook at all.
# In createOptionsMenu or in OptionsMenu add functionality so it won't create an empty tab
# Check what the list is holding (recursively) and add it to the types displayed in my debug function
# add a feature that makes the ants come out one at a time (on a chance) and have them randomly follow a trail like real ants would
# Multithread Generation


#* Enums
#* How ants are mutated
class Mutations(Enum):
    cutoff     = auto() # Only keep up to a certain randomized index, then go off in your own direction
    chunk      = auto() # Only change a randomized chunk of the dna, keep the rest
    induvidual = auto() # Randomly change random indecies with random values (random chance or random amount)
    invert     = auto() # Same as chunk, but instead of creating new data there, invert said data
    none       = auto() # Don't mutate
    multiChunk = auto() # Change a bunch of randomized chunks of dna, keep the rest

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
    royalLine         = auto() # Breed the top 2^n creatures with their next best creature, and do that over and over until there's one left
    inbred            = auto() # Breed the 2^n random creatures, and do that over and over until there's one left

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
