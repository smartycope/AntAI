from random import randint
import math
from time import process_time

dontDebug = False
try:
    from varname import nameof, VarnameRetrievingError
    from inspect import stack
except ImportError:
    dontDebug = True


from os.path import basename
from copy    import deepcopy

# Override the debug parameters and display the file/function for each debug call
#   (useful for finding debug calls you left laying around and forgot about)
debugCount = 0

DISPLAY_FILE = False
DISPLAY_FUNC = False

def debug(var=None, *more_vars, prefix: str='', name=None, merge: bool=False, repr: bool=False, calls: int=0,
          color: int=1, background: bool=False, itemLimit: int=10, showFunc: bool=False, showFile: bool=False,
          _isDebuggedCall: bool=False, _noRecall: bool=False) -> None: # pylint: disable=redefined-builtin
    """Print variable names and values for easy debugging.

    Call with no parameters to tell if its getting called at all, and call with a only a string to just display the string

    The format goes: Global_debug_counter[file->function()->line_number]: prefix data_type variable_name = variable_value

    Args:
        var: The variable or variables to print
        prefix: An additional string to print for each line
        merge: Put all the variables on the same line
        repr: Use __repr__() instead of __str__()
        calls: If you're passing in a return from a function, say calls=1
        color: 0-5. 5 different preset colors for easy distinction
        background: Use the background color instead of the forground color
        showFunc: Display what function you're calling from
        showFile: Display waht file you're calling from

    Usage:
        debug() -> prints 'HERE! HERE!' in bright red for you
        debug('I got to this point') -> prints that message for you
        debug(var) -> prints the type(var) var = {var}
        debug(func()) -> prints what the function returns
        debug(var, var1, var2) -> prints each var on their own line
        debug(var, name='variable') -> prints type(var) variable = {var}
        debug(var, var1, var2, name=('variable', 'variable2', 'variable3')) ->
            prints each var on their own line with the appropriate name
    """
    if not dontDebug:
        #* Make sure to always reset the color back to normal, in case we have an error inside this function
        try:
            global debugCount, DISPLAY_FUNC, DISPLAY_FILE
            debugCount += 1

            #* Get the function, file, and line number of the call
            s = stack()[(0 if _isDebuggedCall else 1) + calls]
            stackData = str(s.lineno)


            if itemLimit < 0:
                itemLimit = 1000000

            #* Colors
            # none, blue, green, orange, purple, cyan, alert red
            colors = ['0', '34', '32', '33', '35', '36', '31']

            if background:
                color += 10

            c = f'\033[{colors[color]}m'

            if var is None:
                if color == 1:
                    print(f'\033[{colors[-1]}m', end='')
                else:
                    print(c, end='')
            else:
                print(c, end='')

            #* Just print the "HERE! HERE!" message
            if var is None:
                print(f'{debugCount}[{stackData}]: HERE! HERE!')
                print('\033[0m', end='')
                return


            #* Shorten var if var is a list or a tuple
            # variables is a tuple of 2 item tuples that have the type as a string, and then the actual variable
            variables = ()
            for v in (var, *more_vars):
                if type(v) in (tuple, list, set) and len(v) > itemLimit:
                    variables += ((type(v).__name__, str(v[0:round(itemLimit/2)])[:-1] + f', \033[0m...{c} ' + str(v[-round(itemLimit/2)-1:-1])[1:] + f'(len={len(v)})'),)
                elif type(v) in (tuple, list, set):
                    variables += ((type(v).__name__, str(v) + f'(len={len(v)})'),)
                else:
                    variables += ((type(v).__name__, v),)

            if DISPLAY_FUNC or showFunc:
                stackData = s.function + '()->' + stackData
            if DISPLAY_FILE or showFile:
                stackData = basename(s.filename) + '->' + stackData

            #* Actually get the names
            try:
                if name is None:
                    try:
                        var_names = nameof(*[i[1] for i in variables], caller=2+calls, full=True)
                    except VarnameRetrievingError:
                        var_names = nameof(*[i[1] for i in variables], caller=2+calls)
                else:
                    # This should work for tuples too
                    if type(name) is list:
                        name = tuple(name)
                    var_names = name

            #* If only a string literal is passed in, display it
            except VarnameRetrievingError as err:
                if type(var) is str:
                    print(f"{debugCount}[{stackData}]: {prefix} {var}")
                    print('\033[0m', end='')
                    return
                else:
                    raise err

            #* If it's not already a tuple, turn it into one
            if not isinstance(var_names, tuple):
                var_names = (var_names, )

            name_and_values = [f"{var_name} = {variables[i][1]!r}" if repr
                        else f"{var_name} = {variables[i][1]}"
                        for i, var_name in enumerate(var_names)]

            if merge:
                print(f"{debugCount}[{stackData}]: {prefix}{', '.join(name_and_values)}")
            else:
                for cnt, name_and_value in enumerate(name_and_values):
                    print(f"{debugCount}[{stackData}]: {prefix}{variables[cnt][0].title()} {name_and_value}")
                    # debugCount += 1

            print('\033[0m', end='')
        #* Catch the error and try again with an additional call
        except VarnameRetrievingError as err:
            if not _noRecall:
                debug(var, more_vars, prefix=prefix, name=name, repr=repr, merge=merge, calls=calls+2, color=color, background=background,
                        itemLimit=itemLimit, showFunc=showFunc, showFile=showFile, _isDebuggedCall=False, _noRecall=True)
            else:
                raise err


        finally:
            print('\033[0m', end='')


def debugged(var, prefix: str='', name=None, repr: bool=False, calls: int=0,
          color: int=1, background: bool=False, itemLimit: int=10, showFunc: bool=False, showFile: bool=False):
    """ An inline version of debug
    """

    debug(var, prefix=prefix, name=name, repr=repr, calls=calls+1, color=color, background=background,
          itemLimit=itemLimit, showFunc=showFunc, showFile=showFile, _isDebuggedCall=True)

    return var



#* Set the __repr__ function to the __str__ function of a class. Useful for custom classes with overloaded string functions
def reprise(obj, *args, **kwargs):
    obj.__repr__ = obj.__str__
    return obj



def percent(percentage):
    ''' Usage:
        if (percent(50)):
            <has a 50% chance of running>
    '''
    return randint(1, 100) < percentage



def closeEnough(a, b, tolerance):
    return a <= b + tolerance and a >= b - tolerance



# Finds the closest point in the list to what it's given
def findClosestPoint(target, comparatorList):
    finalDist = 1000000

    for i in comparatorList:
        current = getDist(target, i)
        if current < finalDist:
            finalDist = current

    return finalDist



def findClosestXPoint(target, comparatorList, offsetIndex = 0):
    finalDist = 1000000
    result = 0

    # for i in range(len(comparatorList) - offsetIndex):
    for current in comparatorList:
        # current = comparatorList[i + offsetIndex]
        currentDist = abs(target.x - current.x)
        if currentDist < finalDist:
            result = current
            finalDist = currentDist

    return result



def getPointsAlongLine(p1, p2):
    p1 = Pointi(p1)
    p2 = Pointi(p2)

    returnMe = []

    dx = p2.x - p1.x
    dy = p2.y - p1.y

    for x in range(p1.x, p2.x):
        y = p1.y + dy * (x - p1.x) / dx
        returnMe.append(Pointf(x, y))

    return returnMe



def rotatePoint(p, angle, pivotPoint, radians = False):
    if not radians:
        angle = math.radians(angle)
    # p -= pivotPoint
    # tmp = pygame.math.Vector2(p.data()).normalize().rotate(amount)
    # return Pointf(tmp.x, tmp.y) + pivotPoint

    dx = p.x - pivotPoint.x
    dy = p.y - pivotPoint.y
    newX = dx * math.cos(angle) - dy * math.sin(angle) + pivotPoint.x
    newY = dx * math.sin(angle) + dy * math.cos(angle) + pivotPoint.y

    return Pointf(newX, newY)



def getMidPoint(p1, p2):
    return Pointf((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


#* A function decorator that prints how long it takes for a function to run
def timeFunc(func, accuracy=5):
    def wrap(*params, **kwparams):
        t = process_time()

        returns = func(*params, **kwparams)

        t2 = process_time()
        elapsed_time = round(t2 - t, accuracy)
        name = func.__name__
        print(name, ' ' * (10 - len(name)), 'took', elapsed_time if elapsed_time >= 0.00001 else 0.00000, '\ttime to run.')
        return returns
    return wrap



class getTime:
    """ A class to use with a with statement like so:
        with getTime('sleep'):
            time.sleep(10)
        It will then print how long the enclosed code took to run.
    """
    def __init__(self, name, accuracy=5):
        self.name = name
        self.accuracy = accuracy

    def __enter__(self):
        self.t = process_time()

    def __exit__(self, *args):
        # args is completely useless, not sure why it's there.
        t2 = process_time()
        elapsed_time = round(t2 - self.t, self.accuracy)
        print(self.name, ' ' * (10 - len(self.name)), 'took', f'{elapsed_time:.5f}', '\ttime to run.')




def isBetween(val, start, end, beginInclusive=False, endInclusive=False):
    return (val >= start if beginInclusive else val > start) and \
           (val <= end   if endInclusive   else val < end)



def insertChar(string, index, char):
    return string[:index] + char + string[index+1:]



def constrain(val, low, high):
    return min(high, max(low, val))



def rgbToHex(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'



def darken(rgb, amount):
    """ Make amount negative to lighten
    """
    return [i+amount for i in rgb]








#* API Specific functions

#* Tkinter (ttk specifically)

import tkinter as tk
import tkinter.ttk as ttk
from contextlib import redirect_stdout
# import ttkthemes

def stylenameElementOptions(stylename):
    '''Function to expose the options of every element associated to a widget
       stylename.'''
    with open('tmp.del', 'a') as f:
        with redirect_stdout(f):
            print('\n-----------------------------------------------------------------------------\n')
            try:
                # Get widget elements
                style = ttk.Style()
                layout = str(style.layout(stylename))
                print('Stylename = {}'.format(stylename))
                print('Layout    = {}'.format(layout))
                elements=[]
                for n, x in enumerate(layout):
                    if x=='(':
                        element=""
                        for y in layout[n+2:]:
                            if y != ',':
                                element=element+str(y)
                            else:
                                elements.append(element[:-1])
                                break
                print('\nElement(s) = {}\n'.format(elements))
                # Get options of widget elements
                for element in elements:
                    print('{0:30} options: {1}'.format(
                        element, style.element_options(element)))
            except tk.TclError:
                print('_tkinter.TclError: "{0}" in function'
                    'widget_elements_options({0}) is not a regonised stylename.'
                    .format(stylename))


# for i in ['TButton', 'TCheckbutton', 'TCombobox', 'TEntry', 'TFrame', 'TLabel', 'TLabelFrame', 'TMenubutton', 'TNotebook', 'TPanedwindow', 'Horizontal.TProgressbar', 'Vertical.TProgressbar', 'TRadiobutton', 'Horizontal.TScale', 'Vertical.TScale', 'Horizontal.TScrollbar', 'Vertical.TScrollbar', 'TSeparator', 'TSizegrip', 'Treeview', 'TSpinbox']:
#     stylenameElementOptions('test.' + i)

# stylenameElementOptions('me.TButton')




#* Pygame






'''
from Point import *
import os, math
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

class Pointer:
    def __init__(self, val):
        self.value = val

    def get(self):



def loadAsset(dir, name, extension='png'):
    return loadImage(dir + name + '.' + extension)



def getDist(a, b):
    return math.sqrt(((b.x - a.x)**2) + ((b.y - a.y)**2))


def getGroundPoints(groundPoints):
    returnMe = []
    for i in range(len(groundPoints) - 1):
        returnMe += getPointsAlongLine(groundPoints[i], groundPoints[i + 1])

    return returnMe



def portableFilename(filename):
    return os.path.join(*filename.split('/'))


def loadImage(filename):
    # if pygame.image.get_extended():
    filename = '/' + portableFilename(DATA + '/' + filename)

    image = pygame.image.load(filename)
    # self.image = self.image.convert()
    image = image.convert_alpha()
    # else:
    #     assert(not f"Cannot support the file extension {}")
    return image


def drawAllGroundPoints(surface, gp):
    for i in gp:
        pygame.gfxdraw.pixel(surface, *i.datai(), [255, 0, 0])


def rotateSurface(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


'''
