from copy import deepcopy
from random import choice, randint, sample
from warnings import warn
from multiprocessing import Pool
from math import ceil
from Creature import Creature
from Nucleotide import Nucleotide
from Options import *
# This isn't actually necissary
from Ant import Ant
from typing import List


def percent(percentage):
    ''' Usage:
        if (percent(50)):
            <has a 50% chance of running>
    '''
    return randint(1, 100) < percentage


class Generation:
    # TODO: parrelelize breeding and mutation generations
    processes = 4
    creature_type = Creature
    nucleotide_type = Nucleotide
    # Generations are sorted by the total scores of their top this many of creatures
    score_by_top_n = 20
    # How many creatures are in each generation
    size = 20
    verbose = False

    def __init__(self, creatures=None, dna=[]):
        # Imply neucleotide type, if it doesn't exist already
        self._steps = 0
        self.creatures = [self.creature_type(dna=dna) for _ in range(self.size)] if creatures is None else creatures

    @classmethod
    def select(cls, method:Selection, creatures:List[Creature]) -> tuple:
        """ Select a couple for breeding out of self.creatures
            returns: tuple of 2 creatures
        """
        match method.method:
            case 'Induvidual':
                rtn = sample(creatures, 2)

            case 'WinnerSecond':
                rtn = sorted(creatures)[-3: -1]

            case 'WinnerProb':
                chanceList = ()
                creatures.sort()

                for cnt, c in enumerate(creatures):
                    chanceList += (c,) * (cnt * method.weight)

                rtn = sample(chanceList, 2)

            case 'GroupWinnerSecond':
                rtn = sorted(sample(creatures, method.group_size))[-3: -1]

            case 'RoyalLine':
                assert(isPowerOf2(method.num_couples))

                couples = sorted(creatures)[-method.num_couples-1: -1] \
                        if not isPowerOf2(len(creatures)) \
                        else creatures
                        # if len(creatures) >= len(self.creatures) or not isPowerOf2(len(creatures)) \

                children = [cls.breed(method.breeding_method, couples[i], couples[i+1])
                            for i in range(0, len(couples), 2)]

                rtn = children if len(children) == 2 else cls.select(Selection.RoyalLine, children)

            case 'Inbred':
                assert(isPowerOf2(method.num_couples))

                couples = sample(creatures, method.num_couples) \
                        if not isPowerOf2(len(creatures)) \
                        else creatures
                        # if len(creatures) >= len(self.creatures) or not isPowerOf2(len(creatures)) \

                children = [cls.breed(couples[i], couples[i+1]) for i in range(0, len(couples), 2)]

                rtn = children if len(children) == 2 else cls.select(Selection.Inbred, children)

        if cls.verbose:
            print('Selecting ants:', f'Mother: {repr(rtn[0])}', f'Father: {repr(rtn[1])}', sep='\n')

        if Ant.limit_after_collected:
            rtn[0].limit()
            rtn[1].limit()
        return rtn

    @classmethod
    def mutate(cls, method:Mutation, creature:Creature) -> Creature:
        if percent(method.total_mutation_chance*100):
            # If it wasn't specified (it was supposed to be), then try to imply it
            if cls.nucleotide_type is Nucleotide and len(creature.dna):
                cls.nucleotide_type = type(creature.dna[0])
            mutated = cls.creature_type(creature.dna.copy())
            match method.method:
                case 'Cutoff':
                    cutoff = randint(0, len(creature.dna) - 1)
                    mutated.dna = creature.dna[cutoff:] if percent(50) else creature.dna[:cutoff]

                case 'Chunk':
                    start, end = sorted(sample(range(len(creature.dna)), 2))
                    mutated.dna = creature.dna[:start] + [cls.nucleotide_type() for _ in range(end-start)] + creature.dna[end:]

                case 'Induvidual':
                    for cnt in range(len(mutated.dna)):
                        if percent(method.mutation_chance*100):
                            mutated.dna[cnt] = cls.nucleotide_type()

                case 'Invert':
                    start, end = sorted(sample(range(len(creature.dna)), 2))

                    for i in range(start, end):
                        mutated.dna[i] = ~mutated.dna[i]

                case 'Dont':
                    pass

                case 'MultiChunk':
                    # Get a random number of indecies between the min and max cut amounts from the length of creatures's dna
                    indecies = sorted(sample(range(len(creature.dna) - ~method.min_cutoff_len),
                                                    randint(method.min_cuts * 2, method.max_cuts * 2)))

                    for i in range(len(indecies)):
                        if i % 2:
                            mutated.dna[indecies[i-1]:indecies[i]] = [cls.nucleotide_type() for _ in range(indecies[i]-indecies[i-1])]

            return mutated
        else:
            return creature

    @classmethod
    def breed(cls, method:Breeding, father, mother) -> Creature:
        """ Breed 2 creatures together and mix their dna according to the method specified.
            params:
                father, mother: the creatures to breed together
        """
        # Check that the dna isn't too short to effectively breed
        if len(father.dna) < method.min_dna_len or len(mother.dna) < method.min_dna_len:
            warn('The last generation was too short, skipping breeding for this generation...')
            return father if percent(50) else mother

        dna = []

        match method.method:
            case 'Cutoff':
                # Get a random index in father
                cutoff = randint(0, len(father.dna) - method.min_cutoff_len)
                # Randomly assign one 'half' of each to their child
                dna = father.dna[:cutoff] + mother.dna[cutoff:] if percent(50) else mother.dna[:cutoff] + father.dna[cutoff:]

            case 'MultiCutoff':
                if len(father.dna) - method.min_cutoff_len < method.min_dna_len:
                    warn('The last generation was too short, skipping breeding for this generation...')
                    return father if percent(50) else mother

                # Get a random number of indecies between the min and max cut amounts from the length of father's dna
                indecies = sample(range(len(father.dna) - method.min_cutoff_len), randint(method.min_cuts, method.max_cuts))

                # Just to make the loop a little easier
                indecies.append(0)
                indecies.append(len(father.dna))
                indecies.sort()

                chunks = []

                for i in range(len(indecies)):
                    # if i % 2:
                    if percent(50):
                        chunks.append(father.dna[indecies[i-1]:indecies[i]])
                    else:
                        chunks.append(mother.dna[indecies[i-1]:indecies[i]])

                for i in chunks:
                    dna.extend(i)

            case 'Induvidual':
                for f, m in zip(father.dna, mother.dna):
                    dna.append(f if percent(method.father_bias*100) else m)

            case 'Identical':
                dna = father.dna if percent(50) else mother.dna

            case 'Reverse':
                dna = list(reversed(father.dna if percent(50) else mother.dna))

        return cls.creature_type(dna=dna)

    def generate(self, gengen:GenGen, breeding:Breeding, mutation:Mutation, selection:Selection) -> 'Generation':
        match gengen.method:
            case "FamilyLine":
            #     father, mother = self.select(selection, self.creatures)
            #     gen_size = len(self.creatures) - (2 if gengen.include_parents else 0)
            #     # TODO: parellelize this with process pool
            #     creatures = [self.breed(breeding, father, mother) for _ in range(gen_size)]

            #     #* Include Parents
            #     if gengen.include_parents:
            #         creatures += [father, mother]

            # case 'MultiFamilyLine':
                couples = []

                for _ in range(gengen.families):
                    couples.append(self.select(selection, self.creatures))

                gen_size = len(self.creatures) - ((len(couples) * 2) if gengen.include_parents else 0)

                # TODO parrellelize this
                creatures = [
                    self.breed(breeding, father, mother)
                    for father, mother in
                    couples * ceil(gen_size / len(couples))
                ]

                # Remove random creatures until we have the right amount
                while len(creatures) > gen_size:
                    creatures.pop(randint(0, len(creatures)-1))

                #* Include Parents
                if gengen.include_parents:
                    for i in couples:
                        creatures += i

            case 'MutationOnly':
                creatures = self.creatures

            case 'Random':
                creatures = [self.creature_type() for _ in range(self.size)]

        # We don't need to mutate if they're all random anyway
        if gengen.method != 'Random':
            # TODO: Parellelize this
            creatures = [self.mutate(mutation, i) for i in creatures]

        if self.verbose:
            print(f'Generated {len(creatures)} new ants')

        return Generation(creatures)

    def reward(self) -> int:
        points = 0
        # If we do this, because ants are incentivised to gather food, as well as return it, it
        # incentivizes larger generations to hover around food instead of learning to bring it back
        # Sum the rewards of the best ants
        for i in sorted(self.creatures, reverse=True)[:self.score_by_top_n]:
            points += i.reward()
        # Incentivize shorter rounds
        # this won't change anything if the rounds are all the same length.
        # but if the rounds are dynamic, this will incentivize shorter rounds, which is good
        points -= self._steps * 2500
        return points

    def step(self):
        self._steps += 1
        [creature.wander() for creature in self.creatures]

    def __lt__(self, gen):
        assert(type(gen) == Generation)

        #* *Don't* go by the best creature in each generation.
        # return max(self.creatures) < max(gen.creatures)
        #* Go by the collective score of it's contained creatures
        return self.reward() < gen.reward()

    def __gt__(self, gen):
        assert(type(gen) == Generation)

        # return max(self.creatures) > max(gen.creatures)
        return self.reward() > gen.reward()

    def __repr__(self):
        return f'Gen[score={self.reward()}, len(creatures)={len(self.creatures)}]'
