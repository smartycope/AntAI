from copy import deepcopy
from warnings import warn


class Creature(object):
    """ A Creature is an object that will be "bred" and be "mutated" to produce
        it's optimal self, optimal being described by the </> operator
        overloads.
    """
    def __new__(cls, copyInstance=None, parent=False):
        _self = super(Creature, cls).__new__(cls)

        if copyInstance is None:
            _self.initAsParent() if parent else _self.init()
            return _self
        else:
            _self.dna = deepcopy(copyInstance.dna)
            _self.initCopyAsParent(copyInstance) if parent else _self.initCopy(copyInstance)
            return _self

    def __init__(self, copyInstance=None, parent=False):
        if copyInstance is None:
            self.dna = []

    def init(self):
        """ Initializes the class.
            Takes the place of __init__.
        """
        raise NotImplementedError

    def initCopy(self, instance):
        """ A copy constructor. when initializing and instance from another instance.
            Don't forget to use deepcopy()!!
        """
        raise NotImplementedError

    def initAsParent(self):
        """ Initialize the object as a parent creature.
            By default, this will just call init()
        """
        self.init()

    def initCopyAsParent(self, instance):
        """ Initialize the object as a parent creature from another instance.
            By default, this will just call initCopy()
            Don't forget to use deepcopy()!!
        """
        self.initCopy()

    def getScore(self) -> float:
        """ The function that defines how to weight the creature's data members
        """
        raise NotImplementedError

    def __lt__(self, creature) -> bool:
        """ Less than operator. By default it simply compares the scores
            of the 2 creatures. Can be overriden to intentionally weight
            certain values.
        """
        self.getScore() < creature.getScore()

    def __gt__(self, creature) -> bool:
        """ Greater than operator. By default it simply compares the scores
            of the 2 creatures. Can be overriden to intentionally weight
            certain values.
        """
        self.getScore() > creature.getScore()

    def __str__(self):
        """ How to print the creature. It's recommended that this is overriden,
            but not strictly nessicary.
        """
        warn('Creature doesn\'t have __str__ overloaded')
