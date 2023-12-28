import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, pygame_gui
from pygame_gui.elements import *
from pygame_gui.windows import UIColourPickerDialog, UIFileDialog

from os.path import dirname; DIR = dirname(__file__) + '/../'

# All the different elements the GUIs can have. They're essentially my own wrappers for pygame_gui's UIElements,
#   because they're poorly written (or at least, annoying to interface with).
#   HandleEvent()'s return True is something happened, and false if not (value and None in the case of Slider)

class AbstractElement:
    def __init__(self, uiManager, container, pos, size, defaultX, defaultY, defaultWidth, defaultHeight, labelPos=None):
        self.size = size
        self.pos  = pos
        self.uiManager = uiManager
        self.container = container

        if size[0] is None:
            self.size[0] = defaultWidth
        if size[1] is None:
            self.size[1] = defaultHeight

        if pos[0] is None:
            if defaultX is None:
                self.pos[0] = (self.container.get_size()[0] / 2) - (self.size[0] / 2)
            else:
                self.pos[0] = defaultX
        if pos[1] is None:
            if defaultY is None:
                self.pos[1] = (self.container.get_size()[1] / 2) - (self.size[1] / 2)
            else:
                self.pos[1] = defaultY

        if self.container is None:
            self.container = self.uiManager.get_root_container()

        self.element = None

        self.label = None

    def handleEvent(self, event):
        pass

    def move(self, deltaLoc):
        if deltaLoc[0] is not None:
            self.pos[0] += deltaLoc[0]
            self.element.set_relative_position(self.pos)
        if deltaLoc[1] is not None:
            self.pos[1] += deltaLoc[1]
            self.element.set_relative_position(self.pos)

    def setPos(self, loc):
        deltaLoc = [*loc]
        if loc[0] is not None:
            deltaLoc[0] = loc[0] - self.pos[0]
            self.pos[0] = loc[0]
            self.element.set_relative_position(self.pos)
        if loc[1] is not None:
            deltaLoc[1] = loc[1] - self.pos[1]
            self.pos[1] = loc[1]
            self.element.set_relative_position(self.pos)

        if self.label is not None:
            self.label.move(deltaLoc)


class Button(AbstractElement):
    def __init__(self, pos, uiManager, text, func, *params, label=None, size=[None, None], container=None, **kwparams):
        super().__init__(uiManager, container, pos, size, 
                         None,
                         None,
                         len(text) * 10,
                         30)

        self.func   = func
        self.params = params
        self.kwparams = kwparams

        labelPos = [pos[0] - (self.size[0] / 2), pos[1] - self.size[1]]

       
        self.element = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(self.pos, self.size), text=text, manager=self.uiManager, container=self.container)
        
        if label is not None:
            self.label = Label(labelPos, uiManager, label, container=container)
        else:
            self.label = None

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT and \
           event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
           event.ui_element == self.element:

            self.func(*self.params, **self.kwparams)

            return True
        else:
            return False
        

class ImageButton(AbstractElement):
    def __init__(self, pos, uiManager, image, func, *params, label=None, size=[None, None], container=None, background=None, deltaColor=30, **kwparams):
        super().__init__(uiManager, container, pos, size, 
                         None,
                         None,
                         *image.get_size()
                        )

        self.func   = func
        self.params = params
        self.kwparams = kwparams

        labelPos = [pos[0] - (self.size[0] / 2), pos[1] - self.size[1]]

        self.element = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(self.pos, image.get_size()), text='', manager=self.uiManager, container=self.container)
        

        # Create a darker image to blend
        blend = pygame.Surface(image.get_size(), flags=pygame.SRCALPHA)
        blend.fill([deltaColor, deltaColor, deltaColor, 0])

        hoverImage = image.copy()
        hoverImage.blit(blend, [0, 0], special_flags=pygame.BLEND_RGBA_ADD)

        # Add the background
        backgroundButtonSurf = pygame.Surface(image.get_size())
        if type(background) in [list, tuple, pygame.Color]:
            backgroundButtonSurf.fill(background)
        elif type(background) == pygame.Surface:
            backgroundButtonSurf = background
        elif background is None:
            pass
        else:
            assert(False)

        backgroundButtonSurf2 = backgroundButtonSurf.copy()
        
        backgroundButtonSurf.blit(image, [0, 0])
        image = backgroundButtonSurf

        backgroundButtonSurf2.blit(hoverImage, [0, 0])
        hoverImage = backgroundButtonSurf2
        

        self.element.normal_image = image
        
        self.element.hovered_image = hoverImage
        self.element.selected_image = image

        self.element.rebuild()



        if label is not None:
            self.label = Label(labelPos, uiManager, label, container=container)
        else:
            self.label = None

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT and \
           event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
           event.ui_element == self.element:

            self.func(*self.params, **self.kwparams)

            return True
        else:
            return False


class AnimationButton(AbstractElement):
    def __init__(self, pos, uiManager, animation, func, *params, label=None, size=[None, None], container=None, background=None, deltaColor=30, **kwparams):
        super().__init__(uiManager, container, pos, size, 
                         None,
                         None,
                         *animation.getSize()
                        )

        self.func   = func
        self.params = params
        self.kwparams = kwparams
        self.animation = animation

        labelPos = [pos[0] - (self.size[0] / 2), pos[1] - self.size[1]]

        self.element = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(self.pos, animation.getSize()), text='', manager=self.uiManager, container=self.container)

        # Create a darker image to blend
        self.blendSurf = pygame.Surface(animation.getSize(), flags=pygame.SRCALPHA)
        self.blendSurf.fill([deltaColor, deltaColor, deltaColor, 0])

        # Add the background
        self.backgroundButtonSurf = pygame.Surface(animation.getSize())
        if type(background) in [list, tuple, pygame.Color]:
            self.backgroundButtonSurf.fill(background)
        elif type(background) == pygame.Surface:
            self.backgroundButtonSurf = background
        elif background is None:
            pass
        else:
            assert(False)

        self.backgroundButtonSurf2 = self.backgroundButtonSurf.copy()


        if label is not None:
            self.label = Label(labelPos, uiManager, label, container=container)
        else:
            self.label = None

    
    def animate(self):
        image = self.animation.animate()

        hoverImage = image.copy()
        hoverImage.blit(self.blendSurf, [0, 0], special_flags=pygame.BLEND_RGBA_ADD)
        
        self.backgroundButtonSurf.blit(image, [0, 0])
        image = self.backgroundButtonSurf

        self.backgroundButtonSurf2.blit(hoverImage, [0, 0])
        hoverImage = self.backgroundButtonSurf2
        
        # self.element.normal_image = image
        self.element.hovered_image = hoverImage
        self.element.selected_image = image

        if self.element.hovered:
            self.element.normal_image = hoverImage
        else:
            self.element.normal_image = image

        # hovering = self.element.is_focused

        self.element.rebuild()

        # self.element.is_focused = hovering

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT and \
           event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
           event.ui_element == self.element:

            self.func(*self.params, **self.kwparams)

            return True
        else:
            return False


class ColorPicker(AbstractElement):
    def __init__(self, uiManager, pos=[None, None], size=[None, None], startingColor=None, title=''):
        super().__init__(uiManager, None, pos, size,
                         None,
                         None,
                         390,
                         390)
                         
        self.color = None

        self.element = UIColourPickerDialog(rect=pygame.Rect(self.pos, self.size), manager=self.uiManager, window_title=title, initial_colour=pygame.Color(*startingColor))

    def getColor(self):
        return tuple(self.color)

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT and \
           event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED and \
           event.ui_element == self.element:

            self.color = event.colour
            return self.color


class CheckBox(AbstractElement):
    def __init__(self, pos, uiManager, label, startValue=False, size=[None, None], hoverText='', dragable=False, container=None):
        super().__init__(uiManager, container, pos, size,
                         None,
                         None,
                         25,
                         25)

        # if pos[0] is None:
        #     pos[0] = (container.get_size()[0] / 2) - ((self.width + 5) / 2) - (4.5 * len(label))
        # if pos[1] is None:
        #     pos[1] = (container.get_size()[1] / 2) - (self.height / 2)

        self.dragable = dragable

        labelPos = [pos[0] + self.size[0] + 5, pos[1] + (self.size[1] / 2) - ((self.size[1] - 3) / 4)]

        self.label = Label(labelPos, uiManager, label, container=container)

        self.checked = startValue

        self.element = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(self.pos, self.size), text=' ',
                                                    manager=self.uiManager, container=self.container, tool_tip_text=hoverText, allow_double_clicks=False)

        self.leftButton = True

        # self.startingColor = self.element.normal_image.get_palette()
        self.startingColor = [76, 80, 82, 100]
        self.clickedColor  = [20, 20, 20, 200]

    def handleEvent(self, event, mouseHeld=False):
        if event.type == pygame.USEREVENT and \
           event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
           event.ui_element == self.element:
           
            self.checked = not self.checked

            self.rebuild()


        if self.dragable and mouseHeld and self.leftButton and \
           event.type == pygame.USEREVENT and \
           event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED and \
           event.ui_element == self.element:

            self.checked = True # not self.checked

            self.rebuild()

        if event.type == pygame.USEREVENT and \
           event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED and \
           event.ui_element == self.element:

            self.leftButton = True


        #     return True
        # else:
            # return False


    def rebuild(self):
        if self.checked:
            # self.element.set_text('✓')
            self.element.normal_image = pygame.Surface(self.size, flags=pygame.SRCALPHA)
            self.element.normal_image.fill(self.clickedColor)
        else:
            # self.element.set_text(' ')
            self.element.normal_image = pygame.Surface(self.size, flags=pygame.SRCALPHA)
            self.element.normal_image.fill(self.startingColor)

        self.element.rebuild()


class Slider(AbstractElement):
    def __init__(self, pos, uiManager, label, range=(-10, 10), startValue = 0, size=[None, None], container=None):
        super().__init__(uiManager, container, pos, size,
                         None,
                         None,
                         200,
                         25)

        self.value = startValue

        labelPos = [self.pos[0], self.pos[1] - (self.size[1] / 2) - 5]

        self.label = Label(labelPos, self.uiManager, self.container, label)

        valueLabelPos = [self.pos[0] - 20, self.pos[1] + (self.size[1] / 4) - 1]

        self.valueLabel = Label(valueLabelPos, uiManager, container, str(self.value), size=[25, None])

        self.range = range
        
        self.element = UIHorizontalSlider(relative_rect=pygame.Rect(self.pos, self.size), start_value=startValue, value_range=self.range, manager=self.uiManager, container=self.container)

    def handleEvent(self, event):
        #* If the slider moved
        if event.type == pygame.USEREVENT and \
           event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and \
           event.ui_element == self.element:

            self.value = event.value
            self.element.set_current_value(self.value)
            self.valueLabel.element.set_text(str(self.value))
            return self.value

        #* If the left button is pressed
        elif event.type == pygame.USEREVENT and \
             event.user_type == 'ui_button_pressed' and \
             event.ui_element == self.element.left_button:
                
            if self.value > self.range[0]:
                self.value -= 1
            self.element.set_current_value(self.value)
            self.valueLabel.element.set_text(str(self.value))
            return self.value

        #* If the right button is pressed
        elif event.type == pygame.USEREVENT and \
             event.user_type == 'ui_button_pressed' and \
             event.ui_element == self.element.right_button:
                
            if self.value < self.range[1]:
                self.value += 1
            self.element.set_current_value(self.value)
            self.valueLabel.element.set_text(str(self.value))
            return self.value

        else:
            return None


class Label(AbstractElement):
    def __init__(self, pos, uiManager, text, size=[None, None], container=None):
        super().__init__(uiManager, container, pos, size,
                         None,
                         None,
                         1000,
                         1000)

        self.element = UILabel(pygame.Rect(self.pos, self.size), text, self.uiManager, self.container)

        if size[0] is None or self.size[0] == 1000:
            self.size[0] = self.element.font.size(text)[0] + 30 
        if size[1] is None or self.size[1] == 1000:
            self.size[1] = self.element.font.size(text)[1]

        self.element.set_dimensions(self.size)


class InputBox(AbstractElement):
    def __init__(self, pos, uiManager, label, startingText='', numbersOnly=False,
                 textLengthLimit=None, allowedChars=None, disallowedChars=None, size=[None, None], container=None):
        super().__init__(uiManager, container, pos, size,
                         None,
                         None,
                         70,
                         30)

        labelPos = [pos[0], pos[1] - (size[1] / 2)]
        self.label = Label(labelPos, uiManager, label, container=container)

        self.element = pygame_gui.elements.UITextEntryLine(pygame.Rect(self.pos, self.size), self.uiManager, self.container)

        self.element.set_text(startingText)

        self.numbersOnly = numbersOnly

        if numbersOnly:
            if textLengthLimit is None:
                textLengthLimit = 3
            if allowedChars is None:
                allowedChars = 'numbers'

        if textLengthLimit is not None:
            self.element.set_text_length_limit(textLengthLimit)

        if allowedChars is not None:
            self.element.set_allowed_characters(allowedChars)

        if disallowedChars is not None:
            self.element.set_forbidden_characters(disallowedChars)

    def getInput(self):
        return int(self.element.get_text()) if self.numbersOnly else self.element.get_text()


class ScrollBar(AbstractElement):
    def __init__(self, uiManager, verticalPercentage, pos=[None, None], size=[None, None], container=None):
        super().__init__(uiManager, container, pos, size,
                         container.get_size()[0] - 15 if size[0] is None else size[0],
                         0,
                         15,
                         container.get_size()[1])

        self.percentage = verticalPercentage

        self.element = UIVerticalScrollBar(pygame.Rect(self.pos, self.size), verticalPercentage, self.uiManager, self.container)

    def handleEvent(self, event):
        #* Scroll up
        if event.type == pygame.MOUSEBUTTONDOWN and \
           event.button == 4 and \
           self.container.get_rect().collidepoint(event.pos):
            
            self.element.scroll_wheel_up = True

            if self.element.scroll_position - 7 > 0:
                self.element.scroll_position -= 7
            else:
                self.element.scroll_position = 0
                self.element.start_percentage = 0

        #* Scroll down
        if event.type == pygame.MOUSEBUTTONDOWN and \
           event.button == 5 and \
           self.container.get_rect().collidepoint(event.pos):
            
            self.element.scroll_wheel_down = True

            ARBITRARY_NUMBER = 101
            if self.element.scroll_position + 7 < ARBITRARY_NUMBER:
                self.element.scroll_position += 7
            else:
                self.element.scroll_position = ARBITRARY_NUMBER
                # self.element.start_percentage = self.percentage
        
        tmp = self.element.process_event(event)
        if tmp or self.element.check_has_moved_recently():
            return True
        else:
            return False

    def getPos(self):
        return self.element.start_percentage


class FilePicker(AbstractElement):
    def __init__(self, uiManager, pos=[None, None], size=[None, None], startingPath=DIR, title=''):
        super().__init__(uiManager, None, pos, size,
                         None,
                         None,
                         260,
                         300)

        self.file = None

        self.element = UIFileDialog(pygame.Rect(self.pos, self.size), self.uiManager, window_title=title, initial_file_path=startingPath)

    def getFilepath(self):
        return self.file

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT and \
           event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED and \
           event.ui_element == self.element:

            self.file = event.file
            return self.file



'''
class RenderedText:
    def __init__(self, text, container, pos=[None, None], font=None, size=24):
        if font is None:
            self.font = pygame.font.Font(None, size)
        else:
            self.font = font

        self.text = text
        self.textSurface = self.font.render(self.text, True, pygame.Color(200, 200, 200))

        if pos[0] is None:
            pos[0] = (container.get_size()[0] / 2) - (self.textSurface.get_rect().width / 2)
        if pos[1] is None:
            pos[1] = (container.get_size()[1] / 2) - (self.textSurface.get_rect().height / 2)

        self.pos = pos
        
    def getSize(self):
        return self.textSurface.get_rect()

    def draw(self, surface):
        surface.blit(self.textSurface, self.pos)

'''

# if (event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry'):

# if (event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.test_drop_down):
                    