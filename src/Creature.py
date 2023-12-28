from copy import deepcopy
from warnings import warn
from abc import ABC

class Creature(ABC):
    """ A Creature is an object that will be "bred" and be "mutated" to produce
        it's optimal self, optimal being described by the </> operator
        overloads.
    """

    def __init__(self, dna=[]):
        self.dna = dna

    def reward(self):
        raise NotImplementedError

    def __lt__(self, creature) -> bool:
        """ Less than operator. By default it simply compares the scores
            of the 2 creatures. Can be overriden to intentionally weight
            certain values.
        """
        return self.reward() < creature.reward()

    def __gt__(self, creature) -> bool:
        """ Greater than operator. By default it simply compares the scores
            of the 2 creatures. Can be overriden to intentionally weight
            certain values.
        """
        return self.reward() > creature.reward()

    def __str__(self):
        """ How to print the creature. It's recommended that this is overriden,
            but not strictly nessicary.
        """
        warn('Creature doesn\'t have __str__ overloaded')
