from enum import Enum, auto

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
    familyLine = auto() # Choose one couple, and all the ants in a generation are children of that couple
    induvidual = auto() # Repeat the Romance method for n times to get n couples, and the ants in a generation are children of those parents (all couples have approximately the same number of children)
    none       = auto() # Every generation is completely random, every time
    mutationOnly = auto() # Instead of breeding, each generation is comprised of mutations of the selected couple (either mother or father, randomly chosen)