from Cope import reprise

class Pointi:
    def __init__(self, x = None, y = None):
        if (type(x) == Pointi or type(x) == Pointf) and y is None:
            self.x = int(x.x)
            self.y = int(x.y)
        elif (type(x) == tuple or type(x) == list) and y is None:
            self.x = int(x[0])
            self.y = int(x[1])
        else:
            if x is None:
                self.x = None
            else:
                self.x = int(x)

            if y is None:
                self.y = None
            else:
                self.y = int(y)
    def __eq__(self, a):
        try:
            return self.x == a.x and self.y == a.y
        except:
            return False
    def __str__(self):
        return f'({self.x}, {self.y})'
    def __repr__(self):
        return f'({self.x}, {self.y})'
    def __getitem__(self, key):
        if key == 0:
            return int(self.x)
        elif key == 1:
            return int(self.y)
        else:
            raise IndexError
    def __setitem__(self, key, value):
        if key == 0:
            self.x = int(value)
        elif key == 1:
            self.y = int(value)
        else:
            raise IndexError
    def __add__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            return Pointi(self.x + value.x, self.y + value.y)
        elif type(value) in [list, tuple]:
            return Pointi(self.x + value[0], self.y + value[1])
        else:
            try:
                return Pointi(self.x + value, self.y + value)
            except:
                raise ValueError
    def __sub__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            return Pointi(self.x - value.x, self.y - value.y)
        elif type(value) in [list, tuple]:
            return Pointi(self.x - value[0], self.y - value[1])
        else:
            try:
                return Pointi(self.x - value, self.y - value)
            except:
                raise ValueError
    def __mul__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            return Pointi(self.x * value.x, self.y * value.y)
        elif type(value) in [list, tuple]:
            return Pointi(self.x * value[0], self.y * value[1])
        else:
            try:
                return Pointi(self.x * value, self.y * value)
            except:
                raise ValueError
    def __truediv__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            return Pointi(self.x / value.x, self.y / value.y)
        elif type(value) in [list, tuple]:
            return Pointi(self.x / value[0], self.y / value[1])
        else:
            try:
                return Pointi(self.x / value, self.y / value)
            except:
                raise ValueError
    def __mod__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            return Pointi(self.x % value.x, self.y % value.y)
        elif type(value) in [list, tuple]:
            return Pointi(self.x % value[0], self.y % value[1])
        else:
            try:
                return Pointi(self.x % value, self.y % value)
            except:
                raise ValueError
    def __iadd__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            self.x += int(value.x)
            self.y += int(value.y)
        elif type(value) in [list, tuple]:
            self.x += int(value[0])
            self.y += int(value[1])
        else:
            try:
                self.x += int(value)
                self.y += int(value)
            except:
                raise ValueError
        return self
    def __isub__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            self.x -= int(value.x)
            self.y -= int(value.y)
        elif type(value) in [list, tuple]:
            self.x -= int(value[0])
            self.y -= int(value[1])
        else:
            try:
                self.x -= int(value)
                self.y -= int(value)
            except:
                raise ValueError
        return self
    def __imul__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            self.x *= int(value.x)
            self.y *= int(value.y)
        elif type(value) in [list, tuple]:
            self.x *= int(value[0])
            self.y *= int(value[1])
        else:
            try:
                self.x *= int(value)
                self.y *= int(value)
            except:
                raise ValueError
        return self
    def __idiv__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            self.x /= int(value.x)
            self.y /= int(value.y)
        elif type(value) in [list, tuple]:
            self.x /= int(value[0])
            self.y /= int(value[1])
        else:
            try:
                self.x /= int(value)
                self.y /= int(value)
            except:
                raise ValueError
        return self
    def __imod__(self, value):
        if type(value) == Pointi or type(value) == Pointf:
            self.x %= int(value.x)
            self.y %= int(value.y)
        elif type(value) in [list, tuple]:
            self.x %= int(value[0])
            self.y %= int(value[1])
        else:
            try:
                self.x %= int(value)
                self.y %= int(value)
            except:
                raise ValueError
        return self
    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        return self
    def __pos__(self):
        self.x = abs(self.x)
        self.y = abs(self.y)
        return self
    def __invert__(self):
        self.x = ~self.x
        self.y = ~self.y
        return self
    def data(self):
        return [self.x, self.y]
    def datai(self):
        return [int(self.x), int(self.y)]
    def dataf(self):
        return [float(self.x), float(self.y)]


class Pointf:
    def __init__(self, x = None, y = None):
        if (type(x) == Pointf or type(x) == Pointi) and y is None:
            self.x = float(x.x)
            self.y = float(x.y)
        if (type(x) == tuple or type(x) == list) and y is None:
            self.x = float(x[0])
            self.y = float(x[1])
        else:
            if x is None:
                self.x = None
            else:
                self.x = float(x)

            if y is None:
                self.y = None
            else:
                self.y = float(y)
    def __eq__(self, a):
        try:
            return self.x == a.x and self.y == a.y
        except:
            return False
    def __str__(self):
        return f'({round(self.x, 5)}, {round(self.y, 5)})'
    def __repr__(self):
        return f'({round(self.x, 5)}, {round(self.y, 5)})'
    def __getitem__(self, key):
        if key == 0:
            return float(self.x)
        elif key == 1:
            return float(self.y)
        else:
            raise IndexError
    def __setitem__(self, key, value):
        if key == 0:
            self.x = float(value)
        elif key == 1:
            self.y = float(value)
        else:
            raise IndexError
    def __add__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            return Pointf(self.x + value.x, self.y + value.y)
        elif type(value) in [list, tuple]:
            return Pointf(self.x + value[0], self.y + value[1])
        else:
            try:
                return Pointf(self.x + value, self.y + value)
            except:
                raise ValueError
    def __sub__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            return Pointf(self.x - value.x, self.y - value.y)
        elif type(value) in [list, tuple]:
            return Pointf(self.x - value[0], self.y - value[1])
        else:
            try:
                return Pointf(self.x - value, self.y - value)
            except:
                raise ValueError
    def __mul__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            return Pointf(self.x * value.x, self.y * value.y)
        elif type(value) in [list, tuple]:
            return Pointf(self.x * value[0], self.y * value[1])
        else:
            try:
                return Pointf(self.x * value, self.y * value)
            except:
                raise ValueError
    def __truediv__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            return Pointf(self.x / value.x, self.y / value.y)
        elif type(value) in [list, tuple]:
            return Pointf(self.x / value[0], self.y / value[1])
        else:
            try:
                return Pointf(self.x / value, self.y / value)
            except:
                raise ValueError
    def __mod__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            return Pointf(self.x % value.x, self.y % value.y)
        elif type(value) in [list, tuple]:
            return Pointf(self.x % value[0], self.y % value[1])
        else:
            try:
                return Pointf(self.x % value, self.y % value)
            except:
                raise ValueError
    def __iadd__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            self.x += float(value.x)
            self.y += float(value.y)
        elif type(value) in [list, tuple]:
            self.x += float(value[0])
            self.y += float(value[1])
        else:
            try:
                self.x += float(value)
                self.y += float(value)
            except:
                raise ValueError
        return self
    def __isub__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            self.x -= float(value.x)
            self.y -= float(value.y)
        elif type(value) in [list, tuple]:
            self.x -= float(value[0])
            self.y -= float(value[1])
        else:
            try:
                self.x -= float(value)
                self.y -= float(value)
            except:
                raise ValueError
        return self
    def __imul__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            self.x *= float(value.x)
            self.y *= float(value.y)
        elif type(value) in [list, tuple]:
            self.x *= float(value[0])
            self.y *= float(value[1])
        else:
            try:
                self.x *= float(value)
                self.y *= float(value)
            except:
                raise ValueError
        return self
    def __idiv__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            self.x /= float(value.x)
            self.y /= float(value.y)
        elif type(value) in [list, tuple]:
            self.x /= float(value[0])
            self.y /= float(value[1])
        else:
            try:
                self.x /= float(value)
                self.y /= float(value)
            except:
                raise ValueError
        return self
    def __imod__(self, value):
        if type(value) == Pointf or type(value) == Pointi:
            self.x %= float(value.x)
            self.y %= float(value.y)
        elif type(value) in [list, tuple]:
            self.x %= float(value[0])
            self.y %= float(value[1])
        else:
            try:
                self.x %= float(value)
                self.y %= float(value)
            except:
                raise ValueError
        return self
    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        return self
    def __pos__(self):
        self.x = abs(self.x)
        self.y = abs(self.y)
        return self
    def __invert__(self):
        self.x = ~self.x
        self.y = ~self.y
        return self
    def data(self):
        return [self.x, self.y]
    def datai(self):
        return [int(self.x), int(self.y)]
    def dataf(self):
        return [float(self.x), float(self.y)]


from random import randint
import math

# TODO This only returns integers at the moment
def randomPointf(minX=0, maxX=100, minY=0, maxY=100):
    return Pointf(randint(minX, maxX), randint(minY, maxY))

def randomPointi(minX=0, maxX=100, minY=0, maxY=100):
    return Pointi(randint(minX, maxX), randint(minY, maxY))


def isAdj(p1, p2):
    return math.isclose(p1.x, p2.x, abs_tol=1) and math.isclose(p1.y, p2.y, abs_tol=1)


def dist(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)



class Foo(object):
    def __new__(cls, param=None):
        print('new called')
        print('param =', param)
        return object.__new__(cls)
    def __init__(self, param=None):
        print('init called')
        print('param =', param)
