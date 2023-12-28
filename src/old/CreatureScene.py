from AI import AI
from Ant import Ant
from Scene import *
from Point import *
from Movement import Movement
from TkOptions import Option
from CreateOptionMenu import createOptionMenu


class CreatureScene(Scene):
    def init(self, **params):
        Ant.center = self.center
        self.ai = AI(Movement, Ant())

        # null, because there is no return type for __init__
        self.null = Option(self.__init__, 'Reset the Simulation', 'Scene', params=(self.mainSurface,), tooltip='Restart the simulation', var='null')


    def run(self, deltaTime):
        for i in self.ai.run():
            i.run()
            i.draw(self.mainSurface)

            self.check()

        return self._menu


    def check(self):
        pass
        # #* Check if we're touching food
        # for a in self.generations[-1].ants:
        #     for f in self.food:
        #         if isAdj(f.pos, a.pos):
        #             a.food = 1
        #             a.color = ~Ant.carryingAntColor
        #             # print(f'{a} is adjacent to food at {f.pos}')

        #     if a.food and isAdj(self.center, a.pos):
        #         self.foodCollected += 1
        #         a.foodCollected    += 1
        #         a.food = 0
        #         a.color = ~Ant.goodAntColor
        #         # print(f'{a} is adjacent to the center at {self.center}')


    def keyDown(self, event):
        key = super().keyDown(event)

        if key == 'esc' or key == 'escape':
            self.exit()

        if key == 'r':
            self.__init__(self.mainSurface)

        if key == 'g':
            self.ai.newGen()

        if key == 'o':
            createOptionMenu(self, Ant(), self.ai, self.ai.generations[-1], AntScene='Global', getGlobal=False, trackers=False)

        if key == 'up':
            self.ai.speedUp(1)
        if key == 'down':
            self.ai.speedUp(-1)
        if key == 'left':
            self.ai.speedUp(None)
        if key == 'right':
            self.ai.speedUp(3)
