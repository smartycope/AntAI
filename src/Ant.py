from Point import Pointi, dist
from Movement import Movement
from random import randint
import pygame.gfxdraw
from TkOptions import Option
from Cope import reprise, debug, closeEnough
from Creature import Creature
from copy import copy, deepcopy


@reprise
class Ant(Creature):
    center = None
    homeColor =        Option([32, 60, 105],   'The home base color', 'Colors', type_='Color',                                                                                           var='homeColor')
    carryingAntColor = Option([0, 0, 255],     'Carrying ant color',  'Colors', type_='Color', tooltip='If an ant is carrying food, they turn this color',                               var='carryingAntColor')
    antColor =         Option([255, 255, 255], 'Defualt ant color',   'Colors', type_='Color', tooltip='The default ant color',                                                          var='antColor')
    goodAntColor =     Option([255, 255, 0],   'Good ant color',      'Colors', type_='Color', tooltip='If an ant has returned food to home, they turn this color.',                     var='goodAntColor')
    parentAntColor =   Option([100, 255, 100], 'Parent ant color',    'Colors', type_='Color', tooltip='If an ant is a parent of the current generation, they start out as this color.', var='parentAntColor')
    champiantColor =   Option([50, 100, 50],   'Chamipant Color',     'Colors', type_='Color', var='champiantColor')

    def init(self):
        self.pos = Pointi(self.center)
        self.food = 0
        self.foodCollected = 0
        self.color = ~self.antColor
        self.movementIndex = 0
        #* Indecies of the places that we got food, or returned food
        #   (to incentivize more direct paths)
        self.goodPlaces = [0,]

    def initCopy(self, instance):
        self.init()

    def initAsParent(self):
        self.init()
        self.color = ~self.parentAntColor

    def initCopyAsParent(self, instance):
        self.initAsParent()


    def wander(self):
        if self.movementIndex >= len(self.dna) - 1:
            self.dna.append(Movement())

        self.pos += self.dna[self.movementIndex].data()
        self.movementIndex += 1


    def run(self):
        self.wander()


    def draw(self, surface):
        pygame.gfxdraw.pixel(surface, *self.pos.datai(), self.color)


    def getScore(self):
        score = 0
        score += self.foodCollected * 10000
        score += self.food * 5000

        #* If we have food, get as close to the center as we can.
        #   If not, go as far away as we can (to explore)
        if self.food:
            score -= dist(self.pos, self.center) * 5
        else:
            score += dist(self.pos, self.center) * 5

        for i in range(len(self.goodPlaces) - 1):
            score -= (self.goodPlaces[i+1] - self.goodPlaces[i]) * 3

        return round(score)


    def rememberIndex(self):
        self.goodPlaces.append(self.movementIndex)


    def __gt__(self, ant):
        # Go by amount of food returned.
        # Otherwise go by amount of food on me.
        # Otherwise, go by the score
        if self.foodCollected > ant.foodCollected:
            return True
        elif self.foodCollected == ant.foodCollected:
            if self.food > ant.food:
                return True
            elif self.food == ant.food:
                return self.getScore() > ant.getScore()
                # selfDist = dist(self.pos, self.center)
                # antDist  = dist(ant.pos, self.center)
                # if self.food > 0:
                #     if closeEnough(selfDist, antDist, ~self.lengthOverDistWeight):
                #         return len(self.dna) < len(ant.dna)
                #     elif selfDist < antDist:
                #         return True
                # elif self.food == 0 and selfDist > antDist:
                #     return True

        # return False

    def __lt__(self, ant):
        if self.foodCollected < ant.foodCollected:
            return True
        elif self.foodCollected == ant.foodCollected:
            if self.food < ant.food:
                return True
            elif self.food == ant.food:
                return self.getScore() < ant.getScore()
                # selfDist = dist(self.pos, self.center)
                # antDist  = dist(ant.pos, self.center)
                # if self.food > 0:
                #     if closeEnough(selfDist, antDist, ~self.lengthOverDistWeight):
                #         return len(self.dna) > len(ant.dna)
                #     elif selfDist > antDist:
                #         return True
                # elif self.food == 0 and selfDist < antDist:
                #     return True

        # return False

    def __str__(self):
        return f'Ant[pos=({self.pos.x}, {self.pos.y}), food collected={self.foodCollected}, food={self.food}, score={self.getScore()}, len(dna)={len(self.dna)}]'






'''
@reprise
class Ant:
    center = None
    homeColor =            Option([32, 60, 105],   'The home base color', _type='Color', tooltip='(homeColor')
    carryingAntColor =     Option([0, 0, 255],     'Carrying ant color',  _type='Color', tooltip='If an ant is carrying food, they turn this color\n(carryingAntColor)')
    antColor =             Option([255, 255, 255], 'Defualt ant color',   _type='Color', tooltip='The default ant color\n(antColor)')
    goodAntColor =         Option([255, 255, 0],   'Good ant color',      _type='Color', tooltip='If an ant has returned food to home, they turn this color.\n(goodAntColor)')
    parentAntColor =       Option([100, 255, 100], 'Parent ant color',    _type='Color', tooltip='If an ant is a parent of the current generation, they start out as this color.\n(parentAntColor)')
    lengthOverDistWeight = Option(10,              'Lenght weight',                      tooltip='How close the distances from the center of 2 ants have to be before you sort them by length of path instead of distance from center\n(lengthOverDistWeight)')


    def __init__(self):
        self.dna = []
        self.pos = Pointi(self.center)
        self.movementIndex = 0
        self.food = 0
        self.foodCollected = 0
        self.color = ~self.antColor


    def wander(self):
        if self.movementIndex >= len(self.dna) - 1:
            self.dna.append(Movement())
        self.movementIndex += 1
        # print(self.movementIndex)
        # print(len(self.dna))
        self.pos -= self.dna[self.movementIndex - 1].data()


    def run(self):
        self.wander()


    def draw(self, surface):
        pygame.gfxdraw.pixel(surface, *self.pos.datai(), self.color)


    def strip(self):
        """ Strips the ant so only it's dna is left """
        self.pos = Pointi(self.center)
        self.movementIndex = 0
        self.food = 0
        self.foodCollected = 0
        self.color = ~self.antColor
        return self


    def setAsParent(self):
        self.color = ~self.parentAntColor
        return self


    def __gt__(self, ant):
        # Go by amount of food returned.
        # Otherwise go by amount of food on me.
        # Otherwise, if I have food, the closer one to center wins.
        # Otherwise, if I don't have food, the furthest one from center wins.
        if self.foodCollected > ant.foodCollected:
            return True
        elif self.foodCollected == ant.foodCollected:
            if self.food > ant.food:
                return True
            elif self.food == ant.food:
                selfDist = dist(self.pos, self.center)
                antDist  = dist(ant.pos, self.center)
                if self.food > 0:
                    if closeEnough(selfDist, antDist, ~self.lengthOverDistWeight):
                        return len(self.dna) < len(ant.dna)
                    elif selfDist < antDist:
                        return True
                elif self.food == 0 and selfDist > antDist:
                    return True

        return False

    def __lt__(self, ant):
        if self.foodCollected < ant.foodCollected:
            return True
        elif self.foodCollected == ant.foodCollected:
            if self.food < ant.food:
                return True
            elif self.food == ant.food:
                selfDist = dist(self.pos, self.center)
                antDist  = dist(ant.pos, self.center)
                if self.food > 0:
                    if closeEnough(selfDist, antDist, ~self.lengthOverDistWeight):
                        return len(self.dna) > len(ant.dna)
                    elif selfDist > antDist:
                        return True
                elif self.food == 0 and selfDist < antDist:
                    return True

        return False

    def __str__(self):
        return f'Ant[{self.pos.x}, {self.pos.y}: {self.foodCollected}, {self.food}: {len(self.dna)}]'

'''
