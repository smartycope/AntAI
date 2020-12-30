from warnings import warn

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

class AntScene(Scene):
    food = []
    minFoods =              Option(20,    'Minimum Foods Spawned',                                                               tooltip='\n(minFoods)')
    maxFoods =              Option(100,   'Maximum Foods Spawned',                                                               tooltip='\n(maxFoods)')
    genSize =               Option(100,   'How many ants per generation',                                                        tooltip='\n(genSize)')
    framesPerGeneration =   Option(300,   'How long each generation lasts',                                                      tooltip='\n(framesPerGeneration)')
    autoBreed =             Option(True,  'Whether a new generation will be created after a time', widgetText='Auto-Breed',      tooltip='\n(autoBreed)')
    homeColor =             Option([32, 60, 105], 'The home base color', _type='Color',                                          tooltip='\n(homeColor')

    def init(self, **params):
        self.ants = []
        self.foodCollected = 0
        self.generation = 0
        self.speedx = Option(1, 'How fast the simulation runs', min=1)
        self.mutationChance = 100
        self.currentFrame = 0
        # null, because there is no return type for __init__
        self.null = Option(self.__init__, widgetText='Reset the Simulation', params=(self.mainSurface,), tooltip='Restart the simulation\n(null)')

        self.food = []
        for _ in range(randint(~self.minFoods, ~self.maxFoods)):
            self.food.append(Food(size=self.getSize()))

        Ant.center = self.center

        # Spawn the first generateion of ants
        self.ants = generateGeneration(None, self.genSize, GenGen.none)


    def run(self, deltaTime):
        # print(len(self.ants))
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
        self.ants = generateGeneration(self.ants, self.genSize, generation=self.generation)


    def keyDown(self, event):
        key = super().keyDown(event)

        if key == 'esc' or key == 'escape':
            self.exit()

        if key == 'r':
            self.__init__(self.mainSurface)

        if key == 'g':
            self.newGen()

        if key == 'o':
            # antMembers = getOptions(Ant)
            # myMembers  = [getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and type(getattr(self, attr)) == Option]
            # # antMembers += [minCutoffBreedingLen, minBreedingMultiCuts, maxBreedingMultiCuts]

            # globalMembers = getOptions()
            # OptionsMenu(tk.Tk(className='Options'), ['Ant'] + antMembers, ['Global'] + myMembers).mainloop()
            # time.sleep(.15) # Escape debouncing
            createOptionMenu(self, AntScene='Global', Global='Breeding & Mutating')

        if key == 'up':
            self.speedx.value += 1
        if key == 'down':
            if self.speedx.value > 1:
                self.speedx.value -= 1
        if key == 'left':
            self.speedx.value = 1
        if key == 'right':
            self.speedx.value += 3
