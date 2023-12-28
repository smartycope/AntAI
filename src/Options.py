from collections import OrderedDict
from AddOptions import *

class GenGen(metaclass=AddOptions):
    """ How each generation is generated """
    # Choose `families` couples, and all the ants in a generation are children of those couples (all couples have approximately the same number of children)
    # include_parents: Whether we should add the parents of the previous generation to the new generation
    FamilyLine = OrderedDict(include_parents=False, families=2)
    # Every generation is completely random, every time
    Random = OrderedDict()
    # Instead of breeding, each generation is comprised of mutations of the selected couple (either mother or father, randomly chosen)
    MutationOnly = OrderedDict()

class Breeding(metaclass=AddOptions, min_dna_len=10):
    """ How ants are bred
        min_dna_len: The minimum amount of nucleotides dna must have before it's allowed to be bred
    """
    # Cuts the dna at one point, and takes half from each parent
    # min_cutoff_len: The minimum amount of nucleotides each parent contributes to each of their child's dna cuts
    Cutoff = OrderedDict(min_cutoff_len=10)
    # Cuts the dna at a bunch of points, then takes alternating peices from each parent
    # min_cuts: The minimum amount of cuts multicut cuts
    # max_cuts: The maximum amount of cuts multicut cuts
    MultiCutoff = OrderedDict(min_cutoff_len=10, min_cuts=2, max_cuts=8)
    # Each bit of dna is randomly chosen from each parent
    Induvidual = OrderedDict(father_bias=.5)
    # Just copy the DNA directly from either the selected mother, or the selected father, unmodified
    Identical = OrderedDict()

class Selection(metaclass=AddOptions):
    """ How ants are selected to be bred """
    # Each creature has the same probibility of being bred
    Induvidual = OrderedDict()
    # Breed the best creature and the second best creature
    WinnerSecond = OrderedDict()
    # Breed 2 random creatures, weighted by how good they are
    # weight: How much romance.winnerProb is weighted
    WinnerProb = OrderedDict(weight=.5)
    # Take a random selection of creatures, and breed the best 2 of that group
    GroupWinnerSecond = OrderedDict(group_size=8)
    # Breed the top 2^n creatures with their next best creature, and do that over and over until there's one left
    # num_couples: How many couples inbreed together in romance.royalLine (must be a power of 2)
    RoyalLine = OrderedDict(num_couples=4, breed_method=Breeding.Cutoff)
    # Breed the 2^n random creatures, and do that over and over until there's one left
    # num_couples: How many couples inbreed together in romance.inbreed (must be a power of 2)
    Inbred = OrderedDict(num_couples=4)

class Mutation(metaclass=AddOptions, total_mutation_chance=1):
    """ How ants are mutated
        total_mutation_chance: The percent chance that a particular ant is mutated at all
    """
    # Only keep up to a certain randomized index, then go off in your own direction
    Cutoff = OrderedDict()
    # Change a bunch of randomized chunks of dna, keep the rest
    # min_cuts: The minimum amount of cuts multicut cuts
    # max_cuts: The maximum amount of cuts multicut cuts
    MultiChunk = OrderedDict(min_cuts=2, max_cuts=8)
    # Only change a randomized chunk of the dna, keep the rest
    Chunk = OrderedDict()
    # Randomly change random indecies with random values (random chance or random amount)
    # mutation_chance: The percent chance for each movement to be mutated
    Induvidual = OrderedDict(mutation_chance=.2)
    # Same as chunk, but instead of creating new data there, invert said data
    Invert = OrderedDict()
    # Don't mutate
    Dont = OrderedDict()


# Some small testing
if __name__ == '__main__':
    print(GenGen.FamilyLine.type)
    print(GenGen.FamilyLine.method)
    f = GenGen.FamilyLine(test=9)
    print(f.include_parents)
    print(f.test)
