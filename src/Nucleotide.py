from abc import ABC

class Nucleotide(ABC):
    """ This class describes an object that is one bit, part, segment,
        item, whatever you want to call it, of a Creature's dna.
    """
    def __invert__(self):
        """ Describes how to invert when using the Mutations.invert method.
        """
        raise NotImplementedError
