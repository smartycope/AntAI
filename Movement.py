from random import randint
from Cope import reprise, debug

@reprise
class Movement:
    MAX_MOVEMENT = 1
    def __init__(self, x=None, y=None):
        if x is None:
            self.x = randint(-self.MAX_MOVEMENT, self.MAX_MOVEMENT)
        else:
            self.x = x

        if y is None:
            self.y = randint(-self.MAX_MOVEMENT, self.MAX_MOVEMENT)
        else:
            self.y = y

    def data(self):
        return [self.x, self.y]
    
    def __str__(self):
        return f'Movement[{self.x}, {self.y}]'

    def __invert__(self):
        self.x = ~self.x + 1
        self.y = ~self.y + 1
        return self