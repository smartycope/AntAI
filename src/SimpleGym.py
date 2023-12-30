import gymnasium as gym
from typing import Literal, List, Tuple
from gymnasium import spaces
import pygame
from pygame import Rect
import numpy as np
from random import randint
import math
from abc import ABC

class SimpleGym(gym.Env, ABC):
    """ A simplified Gymnasium enviorment that uses pygame and handles some stuff for you, like rendering
        keeping track of steps, returning the right things from the right functions, event handling,
        including some default keyboard shortcuts, and some debugging features. Includes a .print()
        and .step_print() functions that print directly to the screen.
        By default:
            q closes the window
            p toggles pause
            s sets increment to True
            u runs the debug_button()
            r runs reset()

        NOTE: pause and increment are not implemented internally, they must be implemented by the user.
            However, step stops incrementing if paused.

        In order to use this effectively, you need to overload:
            __init__(), if you want to add any members
            _get_obs()
            _get_info()
            _get_terminated()
            _get_reward()
            reset(seed, options), if you need any custom reset code
            step(action), if you want to do anything
            render_pygame(), render to self.surf
        and optionally:
            handle_event(event), for handling events
            debug_button(), for debugging when you press the u key

        To check if the enviorment was reset, check .just_reset in between calling .render() and .step()
    """
    def __init__(self, max_steps, screen_size=300, shown_vars={'Frame': 'steps'}, start_paused=False, show_events=False, render_mode='pygame'):
        """ super should be called first, if you  want to use the members like self.size
            shown_vars is a dictionary of {name: member} of members to display on the screen (for debuggin purposes)
        """

        self.metadata = {"render_modes": ['pygame'], "render_fps": 4}
        assert render_mode is None or render_mode in self.metadata["render_modes"], render_mode
        self.size = screen_size

        self.background_color = (20, 20, 20)
        self.print_color = (20, 200, 200, 0)

        self.show_events = show_events

        self.render_mode = render_mode
        self.max_steps = max_steps
        self.steps = 0
        self.screen_size = np.array((self.size, self.size))
        self.screen = None
        self.surf = None
        self.userSurf = None
        self.pause = start_paused
        self.increment = False
        self.font = None
        self.shown_vars = shown_vars
        self.userSurfOffset = len(shown_vars) * 10
        self.just_reset = False

    def _get_obs(self):
        raise NotImplementedError

    def _get_info(self):
        raise NotImplementedError

    def _get_terminated(self):
        """ By default this just terminates after max_steps have been reached """
        if self.steps > self.max_steps:
            return True

        return False

    def _get_reward(self):
        raise NotImplementedError

    def reset(self, seed=None, options=None):
        """ This sets the self.np_random to use the seed given, resets the steps, and returns the
            observation and info. Needs to be called first, if you're depending on self.np_random,
            or steps equalling 0, but also needs to return what this returns.
        """
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self.steps = 0
        self.just_reset = True

        return self._get_obs(), self._get_info()

    def step(self, action):
        """ Call this last, and return it """
        if not self.pause:
            self.steps += 1
        self.just_reset = False
        #                                                            truncated?
        return self._get_obs(), self._get_reward(), self._get_terminated(), False, self._get_info()

    def _init_pygame(self):
        if self.screen is None:
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption('Tabletop')
            self.screen = pygame.display.set_mode(self.screen_size)

        if self.font is None:
            self.font = pygame.font.SysFont("Verdana", 10)

        if self.surf is None:
            self.surf = pygame.Surface(self.screen_size)
            self.surf.convert()
            self.surf.fill((255, 255, 255))

        if self.userSurf is None:
            self.userSurf = pygame.Surface(self.screen_size)
            self.userSurf.convert()
            self.userSurf.fill(self.background_color)

    def render(self):
        if self.render_mode == 'pygame':
            self._init_pygame()

            # This doesn't need to be in self, but it is because of the way Python interacts with pygame (I think)
            self.surf.fill(self.background_color)

            # Draw the text from the custom prints
            self.surf.blit(self.userSurf, (0, 0))

            self.render_pygame()

            # Draw the helpful texts
            length = len(max(self.shown_vars.keys(), key=len))
            strings = [f'{name}: {" "*(length - len(name))} {getattr(self, var, 'Not a Member')}' for name, var in self.shown_vars.items()]

            # For some dumb error I don't understand
            try:
                for offset, string in enumerate(strings):
                    self.surf.blit(self.font.render(string, True, self.print_color), (5, 5 + offset*10))
            except:
                self.font = pygame.font.SysFont("Verdana", 10)
                for offset, string in enumerate(strings):
                    self.surf.blit(self.font.render(string, True, self.print_color), (5, 5 + offset*10))

            # I don't remember what this does, but I think it's important
            self.surf = pygame.transform.scale(self.surf, self.screen_size)

            # Display to screen
            self.screen.blit(self.surf, (0, 0))
            self._handle_events()
            pygame.display.flip()

        else:
            raise TypeError(f"Unknown render mode {self.render_mode}")

    def debug_button(self):
        pass

    def _handle_events(self):
        for e in pygame.event.get():
            match e.type:
                case pygame.QUIT:
                    self.close()
                    exit(0)
                case pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.close()
                        exit(0)
                    match e.unicode:
                        case 'p':
                            self.pause = not self.pause
                        case 'q':
                            self.close()
                            exit(0)
                        case 'u':
                            self.debug_button()
                        case 's' | 'n':
                            self.increment = True
                            print(f'Incrementing to frame {self.steps + 1}')
                        case 'r':
                            self.reset()
                        case _:
                            self.handle_event(e)
                case _:
                    self.handle_event(e)
                    if self.show_events and e.type != pygame.MOUSEMOTION:
                        print(e)
        pygame.event.pump()

    def handle_event(self, event):
        pass

    def print(self, string):
        """ Prints `string` directly to the screen. Only needs to be called once. """
        self._init_pygame()

        self.userSurf.blit(self.font.render(str(string), True, self.print_color), (5 + ((self.userSurfOffset // 40) * 100), 5 + (self.userSurfOffset % 40)))
        self.userSurfOffset += 10

    def step_print(self, string):
        """ Prints `string` directly to the screen. Must be called once per render. """
        self._init_pygame()

        text_surf = self.font.render(str(string), True, self.print_color)
        text_rect = text_surf.get_rect()
        pygame.draw.rect(self.userSurf, self.background_color, Rect(5 + ((self.userSurfOffset // 40) * 100), 5 + (self.userSurfOffset % 40), text_rect.width, text_rect.height))
        self.userSurf.blit(text_surf, (5 + ((self.userSurfOffset // 40) * 100), 5 + (self.userSurfOffset % 40)))

    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()
            self.screen = None
            self.font = None


if __name__ == '__main__':
    import time
    FPS = 20
    table = AntEnv()
    ants, info = table.reset()
    i = 0
    # table.print('hello world')
    while i < 1000:
        table.render()
        if table.pause:
            i -= 1
            if table.increment:
                table.increment = False
                table.step(np.array([ant.wander() for ant in ants]))
            continue
        table.step(np.array([ant.wander() for ant in ants]))
        time.sleep(1/FPS)
    table.close()
