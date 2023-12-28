from random import randint
from Nucleotide import Nucleotide
import numpy as np

class Movement(np.ndarray, Nucleotide):
    max_movement = 1
    # Because numpy handles subclassing differently than most things
    def __new__(cls, x=None, y=None):
        obj= np.asarray([
                randint(-cls.max_movement, cls.max_movement) if x is None else x,
                randint(-cls.max_movement, cls.max_movement) if y is None else y
            ], dtype=np.int32).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return

    def __invert__(self):
        return super().__invert__() + self.max_movement

    # def __str__(self):
        # return str(self)


if __name__ == '__main__':
    # print(Movement())
    # print(Movement(2, 3))
    # print(~Movement(-1, 1))
    print(np.array([Movement(1, 2) for _ in range(20)]).view(Movement)[4].test)
    # print(Movement[:3])
