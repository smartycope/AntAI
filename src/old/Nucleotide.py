class Nucleotide:
    """ This class describes an object that is one bit, part, segment,
        item, whatever you want to call it, of a Creature's dna.
    """
    def __init__(self):
        """ Initializes an instance of the class.
            Must initialize it to be "random"
            (However you define random in your context)
        """
        raise NotImplementedError

    def __invert__(self):
        """ Describes how to invert when using the Mutations.invert method.
        """
        raise NotImplementedError
