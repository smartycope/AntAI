# import tkinter as tk
from tkinter.ttk import *
# from tkinter import ttk
from tkinter import colorchooser, IntVar, StringVar, DoubleVar, BooleanVar
from enum import Enum
from types import *

from os.path import dirname; DIR = dirname(__file__)
import os

# from TkOptionMenu import generateStyle
from Tooltip import Tooltip

import json
from Cope import reprise, debug, rgbToHex, darken

RESET_FILE = False

SETTINGS_FILE = DIR + '/settings.json'
FUNC_TYPES = (FunctionType, BuiltinFunctionType, BuiltinMethodType, LambdaType, MethodWrapperType, MethodType)
LABEL_TYPES = (StringVar, 'label', 'tracker')

globalsDict = globals()

def getOptions(obj=None, namespace=None):
    ''' Gets all the Option members in the passed in class. The passed in class must have a default constructor. '''
    global globalsDict

    if obj is None:
        if namespace is None:
            options = [globalsDict[attr] for attr in globalsDict if not callable(globalsDict[attr]) and not attr.startswith("__") and type(globalsDict[attr]) == Option]
        else:
            options = [namespace[attr] for attr in namespace if not callable(namespace[attr]) and not attr.startswith("__") and type(namespace[attr]) == Option]
    else:
        options = [getattr(obj, attr) for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__") and type(getattr(obj, attr)) == Option]
    return options


@reprise
class Option:
    """
        A class that automatically handles options for you.

                  title
               ____________
        label [ widgetText ]
               ------------

        Params:
            value: The default value of the option. The type of
                element created will be automatically determined
                based on the type of this parameter, unless
                explicitly overwritten by the type_ parameter.
                Will get overwritten by the value in settings.json
            label: The text to the left of the element
            tab: The tab the option goes under
            widgetText: The text that goes on the element, if applicable
            title: The text that goes above the element
            currentItem: The default selected item in a drop-down box.
                Will get overwritten by the value in settings.json.
            tooltip: The text that appears magically when the element
                is hovered over
            min/max: The minimum and maximum values a spinbox will allow.
            var: The name of the variable this is assigned to. (if specified,
                it appears at the bottom of the tooltip in parenthesis)
            type_: Manually specify the type of element to use.
                NOTE: When making a color Option, this must be 'Color'.
                NOTE: When making a stationary label element, the value param
                    should be a tk.StringVar, or this should be specified as
                    'Label' or 'Tracker'
            updateFunc: A function that is called when an option is changed
                in some way. DO NOT USE THIS WITH A BUTTON OR A COLOR
            params/kwparams: A LIST and DICT (Not starred!) of parameters
                passed into the function call, if the element is a button
                or updateFunc is specified.


        Notes:
            To access the Option, you must use the get() and set() functions.
            The ~ (invert) operator is also overloaded to be equivelent to the
            get() function for easy access, but may cause occasional issues.

    """
    order = [bool, Enum, list, tuple, set, str, float, int, 'color', *FUNC_TYPES, *LABEL_TYPES]

    def __init__(self, value, label='', tab='General', widgetText='', title='', currentItem=None, tooltip='',
                 min=None, max=None, var='', type_=None, updateFunc=lambda value, *a, **kw: None, params=(), kwparams={}):
        self.defaultValue = value
        self.type = type_
        self.tab = tab
        self.title = title
        self.updateFunc = updateFunc
        self.params = params
        self.kwparams = kwparams

        #* Add the (variable) to the end of the tooltip
        if len(var):
            tooltip +=  f'\n({var})' if len(tooltip) else ''

        if type(self.type) is str:
            self.type = self.type.lower()

        validTypeList = self.order


        #* If value is an Enum
        if type(value) not in validTypeList and issubclass(value, Enum) and type_ is None:
            self.enum = value
            self.type = list
            self.options = [var for var, member in value.__members__.items()]
            if currentItem is not None:
                try:
                    self.value = currentItem.name
                    self.defaultValue = currentItem.name
                except AttributeError:
                    raise UserWarning("The value given to the option is not in the enum provided.")
            else:
                try:
                    self.value = value(1).name
                    self.defaultValue = value(1).name
                except ValueError:
                    raise UserWarning("No current value for the enum was provided")
        else:
            self.enum = None
            self.value = value
            if type_ is None:
                self.type = type(value)

            if self.type in (list, tuple, set):
                if currentItem is None:
                    self.options = value
                    try:
                        self.value = value[0]
                        self.defaultValue = value[0]
                    except IndexError:
                        raise UserWarning("You can't pass an empty list into an Option")
                else:
                    self.options = value
                    self.value = currentItem
                    self.defaultValue = currentItem

            elif self.type is StringVar:
                self.value = value.get()
                self._value = value

        if self.type not in validTypeList:
            raise TypeError(f"The Option class only supports ints, float, bools, tuples, lists, enums, and strings, not {self.type}")

        self.min = min
        if self.min is None:
            if self.type in (int, float):
                self.min = 0

        self.max = max
        if self.max is None:
            if self.type in (int, float):
                self.max = 100000

        if self.value is None:
            if self.type in (tuple, list, set):
                self.value = self.value[0]

        self.element = None
        if not len(label) and not len(widgetText) and not len(tooltip) and not len(title) and not len(var):
            raise UserWarning('This option has no labels!')
        self.saveName = var if len(var) else label if len(label) else widgetText if len(widgetText) else title if len(title) else tooltip
        self.label = label
        self._value = None
        self.widgetText = widgetText
        self.tooltip = tooltip

        if self.type in FUNC_TYPES:
            self.func = value
            # self.func = lambda self: self.returnVal = value(*self.params, **self.kwparams)
            self.value = None
            self.defaultValue = None

        if RESET_FILE:
            self.restoreDefault()

        #* Load the value from the settings file over the given default value
        if not os.path.exists(SETTINGS_FILE):
            os.system('touch ' + SETTINGS_FILE)
            with open(SETTINGS_FILE, 'r+') as f:
                json.dump({}, f)

            self.restoreDefault()
        else:
            # If we have just added a new option in code, it will throw an error. Catch that error, restore to defaults, and try again
            try:
                with open(SETTINGS_FILE, 'r+') as f:
                    self.value = json.load(f)[self.saveName]
            except KeyError:
                self.restoreDefault()
                with open(SETTINGS_FILE, 'r+') as f:
                    self.value = json.load(f)[self.saveName]

    def callback(self):
        self._value = self.value = self.func(*self.params, **self.kwparams)

    def restoreDefault(self):
        print(f'Reseting {self.value} to {self.defaultValue}')
        self.value = self.defaultValue
        if self._value is not None and self.type != 'color':
            self._value.set(self.defaultValue)
        elif self.type =='color':
            self._value = self.defaultValue

        try:
            with open(SETTINGS_FILE, "r") as jsonFile:
                data = json.load(jsonFile)
        except json.decoder.JSONDecodeError:
            with open(SETTINGS_FILE, "w") as jsonFile:
                json.dump({}, jsonFile)
            with open(SETTINGS_FILE, "r") as jsonFile:
                data = json.load(jsonFile)

        data[self.saveName] = self.defaultValue

        with open(SETTINGS_FILE, "w") as jsonFile:
            json.dump(data, jsonFile)

    def create(self, root):
        if self.type == int:
            self._value = IntVar(root, self.value)
        elif self.type == bool:
            self._value = BooleanVar(root, self.value)
        elif self.type == float:
            self._value = DoubleVar(root, self.value)
        elif self.type in (str, tuple, list, set, *LABEL_TYPES):
            self._value = StringVar(root, self.value)
        elif self.type == 'color':
            self._value = self.value

        if len(self.title):
            title = Label(root, text=self.title)
        else:
            title = None
        if len(self.label):
            label = Label(root, text=self.label)
        else:
            label = None


        if self.type is int:
            self.element = Spinbox(root, from_=self.min, to=self.max, textvariable=self._value)

        elif self.type is float:
            self.element = Entry(root, textvariable=self._value)

        elif self.type is bool:
            self.element = Checkbutton(root, text=self.widgetText, variable=self._value)

        elif self.type is str:
            self.element = Entry(root, text=self.widgetText, textvariable=self._value, exportselection=False)

        elif self.type in (tuple, list, set):
            # print(self._value)
            self.element = Combobox(root, values=self.options, textvariable=self._value)
            # debug(self.value, self.options)
            self.element.current(self.options.index(self.value))
            # self.element.current(0)
            # print(self.element.get())

        elif self.type == 'color':
            self.buttonColor = Style(root)
            self.buttonColor.configure(f'{self.saveName}.TButton', background=rgbToHex(self.value), focuscolor='maroon')#rgbToHex(darken(self.value, 20)))
            self.element = Button(root, command=self.colorPicker, text=self.widgetText, style=f'{self.saveName}.TButton')

        elif self.type in FUNC_TYPES:
            self.element = Button(root, command=self.callback, text=self.widgetText)

        elif self.type in LABEL_TYPES:
            self._value.trace_add('write', self.update)
            self.element = Label(root, textvariable=self._value)


        #* Add the tooltip
        if len(self.tooltip):
            self.tooltipObj = Tooltip(self.element, self.tooltip)

        #* Add the update function, if there is one.
        if self.type not in FUNC_TYPES and self.type != 'color':
            def _update(*_):
                self.update()
                self.updateFunc(self.value, *self.params, **self.kwparams)

            self._value.trace_add('write', _update)

        #* Return the elements to options menu so it can take care of packing them
        return (title, (label, self.element))

    def colorPicker(self):
        self._value = colorchooser.askcolor(title="Choose Color")[0]
        if self._value is not None:
            self.buttonColor.configure(f'{self.saveName}.TButton', background=rgbToHex(self._value), focuscolor='maroon')#rgbToHex(darken(self.value, 20)))
            # self.buttonColor.configure(rgbToHex(self._value)

    def call(self, params=None, kwparams={}):
        if self.type in FUNC_TYPES:
            if params is None:
                params = self.params
            if kwparams is None:
                kwparams = self.kwparams

            self.returnVal = self.value = self.func(*params, *kwparams)
            return self.returnVal
        else:
            raise AttributeError("Cannot call a non-function option")

    def update(self, *_):
        if self.type == 'color':
            if self._value is not None:
                self.value = self._value
        elif self.type in FUNC_TYPES:
            self.value = self._value
        elif self.type in (tuple, list, set):
            self.value = self.element.get()
        else:
            self.value = self._value.get()

        self.save()

    def get(self):
        if self.enum is not None:
            return getattr(self.enum, self.value)
        else:
            return self.value

    def set(self, val):
        if isinstance(val, Enum):
            self.value = val.name
        else:
            self.value = val

            if self.type in LABEL_TYPES:
                try:
                    self._value.set(val)
                except AttributeError:
                    self.value = val

    def __invert__(self):
        if self.enum is not None:
            return getattr(self.enum, self.value)
        else:
            return self.value

    def truth(self):
        if self.enum is not None:
            return getattr(self.enum, self.value)
        else:
            return self.value

    def save(self):
        with open(SETTINGS_FILE, "r") as jsonFile:
            data = json.load(jsonFile)

        data[self.saveName] = self.value

        with open(SETTINGS_FILE, "w") as jsonFile:
            json.dump(data, jsonFile)

    def __lt__(self, option):
        myIndex    = self.order.index(self.type)
        theirIndex = self.order.index(option.type)
        if myIndex == theirIndex:
            if self.label == option.label:
                if self.title == option.title:
                    return self.widgetText < option.widgetText
                else:
                    return self.title < option.title
            else:
                return self.label < option.label
        else:
            return myIndex < theirIndex

    def __gt__(self, option):
        myIndex    = self.order.index(self.type)
        theirIndex = self.order.index(option.type)
        if myIndex == theirIndex:
            if self.label == option.label:
                if self.title == option.title:
                    return self.widgetText > option.widgetText
                else:
                    return self.title > option.title
            else:
                return self.label > option.label
        else:
            return myIndex > theirIndex

    def __str__(self):
        return f'Opt[{self.type}: {self.value}, {self._value}]'
