from warnings import warn
from Cope import debug
from Scene     import *
from Point     import *
from Ant       import *
from Food      import Food
from copy      import deepcopy
from tkinter   import *
from TkOptions import *
from Methods   import *
from random    import randint, choice
from CreateOptionMenu import createOptionMenu
from Generation import Generation

class AntScene(Scene):
    food = []
    minFoods =   Option(20,    'Minimum Foods Spawned',                tooltip='(minFoods)')
    maxFoods =   Option(100,   'Maximum Foods Spawned',                tooltip='(maxFoods)')
    autoBreed =  Option(True,  widgetText='Auto-Breed',                tooltip='Whether a new generation will be created after a time\n(autoBreed)')
    foodColor =  Option([255, 100, 100],  'Food Color', _type='Color', tooltip='(foodColor')
    skipBadGen = Option(True,  widgetText='Skip bad generations',      tooltip='If the last generation was worse than the one before it, generate a new generation based on the one before it instead of just the last generation.\n(skipBadGen)')

    def init(self, **params):
        # self.ants = []
        self.foodCollected = 0
        # self.generation = 0
        self.speedx = Option(1, 'How fast the simulation runs', min=1)
        # self.mutationChance = 100
        self.currentFrame = 0
        # null, because there is no return type for __init__
        self.null = Option(self.__init__, widgetText='Reset the Simulation', params=(self.mainSurface,), tooltip='Restart the simulation\n(null)')
        self.food = []

        #* Generate food
        for _ in range(randint(~self.minFoods, ~self.maxFoods)):
            self.food.append(Food(size=self.getSize()))

        Ant.center = self.center
        Food.color = ~self.foodColor

        #* Spawn the first generateion of ants
        self.generations = [Generation(None)]


    def run(self, deltaTime):
        for _ in range(~self.speedx):

            if ~self.autoBreed:
                self.currentFrame += 1
                if self.currentFrame >= ~Generation.framesPerGeneration:
                    self.newGen()
                    break

            for i in self.generations[-1].ants:
                i.run()
                i.draw(self.mainSurface)

            for i in self.food:
                i.draw(self.mainSurface)

            pygame.gfxdraw.pixel(self.mainSurface, *self.center.datai(), Ant.homeColor.value)

            self.checkAnts()

        return self._menu


    def checkAnts(self):
        #* Check if we're touching food
        for a in self.generations[-1].ants:
            for f in self.food:
                if isAdj(f.pos, a.pos):
                    a.food = 1
                    a.color = ~Ant.carryingAntColor
                    # print(f'{a} is adjacent to food at {f.pos}')

            if a.food and isAdj(self.center, a.pos):
                self.foodCollected += 1
                a.foodCollected    += 1
                a.food = 0
                a.color = ~Ant.goodAntColor
                # print(f'{a} is adjacent to the center at {self.center}')


    def newGen(self):
        self.currentFrame = 0
        gen = Generation(self.generations if ~self.skipBadGen else self.generations[-1])
        self.generations.append(gen)


    def keyDown(self, event):
        key = super().keyDown(event)

        if key == 'esc' or key == 'escape':
            self.exit()

        if key == 'r':
            self.__init__(self.mainSurface)

        if key == 'g':
            self.newGen()

        if key == 'o':
            createOptionMenu(self, Ant(), self.generations[-1], AntScene='Global', getGlobal=False)
            # This spot is as good as any to update this
            Food.color = ~self.foodColor

        if key == 'up':
            self.speedx.value += 1
        if key == 'down':
            if self.speedx.value > 1:
                self.speedx.value -= 1
        if key == 'left':
            self.speedx.value = 1
        if key == 'right':
            self.speedx.value += 3
