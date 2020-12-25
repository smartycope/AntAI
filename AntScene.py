from Scene     import *
from Point     import *
from Ant       import Ant
from Food      import Food
from copy      import deepcopy
from tkinter   import *
from TkOptions import *


class AntScene(Scene):
    food = []
    minFoods =              Option(20,    'Minimum Foods Spawned')
    maxFoods =              Option(100,   'Maximum Foods Spawned')
    genSize =               Option(100,   'How many ants per generation')
    framesPerGeneration =   Option(300,   'How long each generation lasts')
    doBreeding =            Option(False, 'Breed, or only mutate')
    autoBreed =             Option(True,  'Whether a new generation will be created after a time')

    def init(self, **params):
        self.ants = []
        self.foodCollected = 0
        self.homeColor = Option([32, 60, 105], 'The home base color', _type='Color', widgetText='test')
        self.generation = 0
        self.speedx = Option(1, 'How fast the simulation runs', min=1)
        self.mutationChance = 100
        self.currentFrame = 0

        # Spawn food
        # if not len(self.food):
        #     for _ in range(randint(~self.minFoods, ~self.maxFoods)):
        #         self.food.append(Food(size=self.getSize()))

        self.food = []
        for _ in range(randint(~self.minFoods, ~self.maxFoods)):
            self.food.append(Food(size=self.getSize()))


        # Spawn ants
        for _ in range(~self.genSize):
           self.ants.append(Ant(center=self.center))


    def run(self, deltaTime):
        for _ in range(~self.speedx):
            if ~self.autoBreed:
                self.currentFrame += 1
                if self.currentFrame >= ~self.framesPerGeneration:
                    self.newGen()
                    break

            for i in self.ants:
                i.run()
                i.draw(self.mainSurface)

            for i in self.food:
                i.draw(self.mainSurface)

            pygame.gfxdraw.pixel(self.mainSurface, *self.center.datai(), self.homeColor.value)

            self.checkAnts()

        return self._menu


    def checkAnts(self):
        # Check if we're touching food
        for f in self.food:
            for a in self.ants:
                if isAdj(f.pos, a.pos):
                    a.food = 1

        for a in self.ants:
            if isAdj(Pointi(0, 0), a.pos):
                self.foodCollected += 1 # a.food
                a.foodCollected    += 1 # a.food
                a.food = 0


    def newGen(self):
        self.generation += 1
        self.currentFrame = 0

        # Get the best ant
        self.ants.sort()
        champiant = self.ants[0]
        print(f'The champiant of generation {self.generation} is:', champiant)

        if ~self.doBreeding:
            # Create a new generation of ants based on the champiant and the second place champiant
            runnerUp = self.ants[1]

            self.ants = []
            # champiant.pos = Pointi(self.center)
            # runnerUp.pos  = Pointi(self.center)
            # self.ants.append(champiant)
            # self.ants.append(runnerUp)
            for _ in range(~self.genSize):
                self.ants.append(Ant(father=deepcopy(champiant), mother=deepcopy(runnerUp), mutationChance=self.mutationChance, center=self.center))

        else:
            # Create a new generation of ants based on the champiant's DNA (the path it took)
            self.ants = []
            champiant.pos = Pointi(self.center)
            self.ants.append(champiant)
            for _ in range(~self.genSize):
                ant = Ant(mutationChance=0, center=self.center)
                ant.dna = deepcopy(champiant.dna)
                if percent(self.mutationChance):
                    ant.mutate(ant.mutationMethod)
                self.ants.append(ant)


    def keyDown(self, event):
        key = super().keyDown(event)

        if key == 'esc' or key == 'escape':
            self.exit()

        if key == 'r':
            self.__init__(self.mainSurface)
            # print(len(self.food))
            # for cnt, i in enumerate(self.food):
            #     print(cnt, ': ', i, sep='')

        if key == 'g':
            self.newGen()

        if key == 'o':
            # self.switchMenu('OptionsMenu')

            ant = Ant()
            antMembers = [getattr(ant,  attr) for attr in dir(ant)  if not callable(getattr(ant,  attr)) and not attr.startswith("__") and type(getattr(ant,  attr)) == Option]
            myMembers  = [getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and type(getattr(self, attr)) == Option]
            OptionsMenu(tk.Tk(className='Options'), ['Ant'] + antMembers, ['Global'] + myMembers).mainloop()
            time.sleep(.15) # Escape debouncing

        if key == 'up':
            self.speedx.value += 1
        if key == 'down':
            if self.speedx.value > 1:
                self.speedx.value -= 1
        if key == 'left':
            self.speedx.value = 1
        if key == 'right':
            self.speedx.value += 3

