from CreateOptionMenu import createOptionMenu
from TkOptions import Option
from Scene import *
from Food import Food
from Ant import Ant
from Movement import Movement
from AI import AI
from random import randint
from Generation import getChampiant

class AntScene(Scene):
    food = []
    minFoods =   Option(20,    'Minimum Foods Spawned', 'Scene',                 var='minFoods')
    maxFoods =   Option(100,   'Maximum Foods Spawned', 'Scene',                 var='maxFoods')
    foodColor =  Option([255, 100, 100],  'Food Color', 'Colors', type_='Color', var='foodColor')
    speed =      Option(1,     'Speed',                 'Scene', min=1,          tooltip='How fast the simulation runs')

    def init(self, **params):
        self.food = []

        self.foodCollected = 0
        Ant.center = self.center
        Food.color = ~self.foodColor

        self.ai = AI(Movement, Ant())

        # null, because there is no return type for __init__
        self.null = Option(self.__init__, widgetText='Reset the Simulation', tab='Scene', params=(self.mainSurface,), tooltip='Restart the simulation', var='null')

        #* Generate food
        for _ in range(randint(~self.minFoods, ~self.maxFoods)):
            self.food.append(Food(size=self.getSize()))

        self.prevChampiant = None


    def run(self, deltaTime):
        for _ in range(self.speed.get()):
            ants = self.ai.run()

            for i in ants:
                i.run()
                i.draw(self.mainSurface)

            self.checkAnts(ants)

        for i in self.food:
            i.draw(self.mainSurface)

        pygame.gfxdraw.pixel(self.mainSurface, *self.center.datai(), Ant.homeColor.value)

        return self._menu


    def checkAnts(self, ants):
        #* Check if we're touching food
        for a in ants:
            for f in self.food:
                if isAdj(f.pos, a.pos):
                    if a.food < 1:
                        a.rememberIndex()
                    a.food = 1
                    a.color = ~Ant.carryingAntColor
                    # print(f'{a} is adjacent to food at {f.pos}')

            if a.food and isAdj(self.center, a.pos):
                self.foodCollected += 1
                a.foodCollected    += 1
                a.food = 0
                a.color = ~Ant.goodAntColor
                a.rememberIndex()
                # print(f'{a} is adjacent to the center at {self.center}')

        #* Change the color of the Champiant
        if getChampiant.get():
            champiant = max(ants)
            if self.prevChampiant != champiant:
                champiant.color = Ant.champiantColor.get()
                if self.prevChampiant is not None:
                    self.prevChampiant.color = Ant.antColor.get()
                self.prevChampiant = champiant


    def keyDown(self, event):
        key = super().keyDown(event)

        if key == 'esc' or key == 'escape':
            self.exit()

        if key == 'r':
            self.__init__(self.mainSurface)

        if key == 'g':
            self.ai.newGen()

        if key == 'o':
            createOptionMenu(self, Ant(), self.ai, self.ai.generations[-1], getGlobal=True)

        if key == 'up':
            self.speed.value += 1
        if key == 'down':
            if self.speed.value > 1:
                self.speed.value -= 1
        if key == 'left':
            self.speed.value = 1
        if key == 'right':
            self.speed.value += 3
