from Scene import *
from Elements import *
import pygame_gui

GUI_THEME_FILE = ''

class GuiScene(Scene):
    def init(self, **params):
        self.showMouse(True)
        self.setKeyRepeat(200, 20)
        self.uiManager = pygame_gui.UIManager(self.getSize(), GUI_THEME_FILE)
        self.background = self.uiManager.get_theme().get_colour('dark_bg')
        self.elements = ()
        self.renderUI()
        self.debug = False

        # PackageResource(package='data.themes', resource='theme_2.json'))

        # self.uiManager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
        #                                {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
        #                                {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
        #                                {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
        #                                {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
        #                                ])


    def renderUI(self):
        self.uiManager.set_window_resolution(self.getSize())
        self.uiManager.clear_and_reset()

        # self.UIbackgroundSurface = pygame.Surface(self.options.resolution)
        # self.UIbackgroundSurface.fill()


    def handleEvent(self, event):
        for i in self.elements:
            i.handleEvent(event)

        super().handleEvent(event)

        self.uiManager.process_events(event)


    def run(self, deltaTime):
        if self.debug:
            self.uiManager.set_visual_debug_mode(self.debug)
            print("self.uiManager.focused_set:", self.uiManager.focused_set)

        # respond to input
        self.uiManager.update(deltaTime)

        self.uiManager.draw_ui(self.mainSurface)

        return self._menu
