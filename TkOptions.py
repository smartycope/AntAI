import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from tkinter import colorchooser
from enum import Enum
from types import *

from os.path import dirname; DIR = dirname(__file__)
import os

from TkOptionMenu import OptionsMenu
from Tooltip import Tooltip

import json
from Cope import reprise, debug


# TODO: Option, if passed an enum, value will be a string to the option selected, instead of the actual Enum Option. I think it was intentional, but I don't like it now, so change it back.


def rgbToHex(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'

RESET_FILE = False

SETTINGS_FILE = DIR + '/settings.json'
FUNC_TYPES = (FunctionType, BuiltinFunctionType, BuiltinMethodType, LambdaType, MethodWrapperType, MethodType)

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


def getTrackers(obj=None, namespace=None):
    ''' Gets all the Option members in the passed in class. The passed in class must have a default constructor. '''
    global globalsDict

    if obj is None:
        if namespace is None:
            options = [globalsDict[attr] for attr in globalsDict if not callable(globalsDict[attr]) and not attr.startswith("__") and type(globalsDict[attr]) == Tracker]
        else:
            options = [namespace[attr] for attr in namespace if not callable(namespace[attr]) and not attr.startswith("__") and type(namespace[attr]) == Tracker]            
    else:
        options = [getattr(obj, attr) for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__") and type(getattr(obj, attr)) == Tracker]
    return options




@reprise
class Option:
    order = [Enum, list, tuple, str, float, int, 'color', bool, *FUNC_TYPES]
    
    def __init__(self, value, label='', currentItem=None, widgetText='', tooltip=None, min=None, max=None, _type=None, params=(), kwparams={}):
        self.defaultValue = value
        self.type = _type
        if type(self.type) is str:
            self.type = self.type.lower()

        validTypeList = (int, float, bool, str, tuple, list, 'color') + FUNC_TYPES

        #* If value is an Enum
        if type(value) not in validTypeList and issubclass(value, Enum) and _type is None:
            self.enum = value
            self.type = list
            self.options = [name for name, member in value.__members__.items()]
            if currentItem is not None:
                try:
                    self.value = currentItem.name
                    self.defaultValue = self.value
                except AttributeError:
                    raise UserWarning("The value given to the option is not in the enum provided.")
        else:
            self.enum = None
            self.value = value
            if _type is None:
                self.type = type(value)

        if self.type not in validTypeList:
            raise TypeError("The Option class only supports ints, float, bools, tuples, lists, enums, and strings.")
        
        self.min = min
        if self.min is None:
            if self.type in (int, float):
                self.min = 0

        self.max = max        
        if self.max is None:
            if self.type in (int, float):
                self.max = 100000

        if self.value is None:
            if self.type in (tuple, list):
                self.value = self.value[0]

        self.element = None
        self.label   = None
        self.name = label
        self._value = None
        self.widgetText = widgetText
        self.tooltip = tooltip

        if self.type in FUNC_TYPES:
            self.params = params
            self.kwparams = kwparams
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
                    self.value = json.load(f)[self.name]
            except KeyError:
                self.restoreDefault()
                with open(SETTINGS_FILE, 'r+') as f:
                    self.value = json.load(f)[self.name]

    def callback(self):
        self._value = self.func(*self.params, **self.kwparams)

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

        data[self.name] = self.defaultValue

        with open(SETTINGS_FILE, "w") as jsonFile:
            json.dump(data, jsonFile)

    def create(self, root, row=None, column=None, **kwparams):
        if self.type == int:
            self._value = tk.IntVar(root, self.value)
        elif self.type == bool:
            self._value = tk.BooleanVar(root, self.value)
        elif self.type == float:
            self._value = tk.DoubleVar(root, self.value)
        elif self.type in (str, tuple, list):
            self._value = tk.StringVar(root, self.value)
        elif self.type == 'color':
            self._value = self.value
        # elif self.type in FUNC_TYPES:

        # elif self.type in (tuple, list):
            # self._value = tk.StringVar(r)

        if len(self.name): # and self.type is not bool:
            # self.label = 
            tk.Label(root, text=self.name, pady=0).pack() #grid(row=row.get() - 1, column=column.get())
            # column.set(column.get() + 1)
            # self.label.pack()
            # print(row.get())

        if self.type is int:
            self.element = tk.Spinbox(root, from_=self.min, to=self.max, textvariable=self._value)

        elif self.type is float:
            self.element = tk.Entry(root, textvariable=self._value)

        elif self.type is bool:
            # NOTE: Not tk.Checkbutton
            self.element = Checkbutton(root, text=self.widgetText, variable=self._value) #, onvalue=True, offvalue=False)
            # self.element.bind('<Button-1>', self.invertCheckbox)

        elif self.type is str:
            self.element = tk.Entry(root, text=self.startText, textvariable=self._value, exportselection=False)

        elif self.type in (tuple, list):
            # NOTE: Not tk.Combobox
            self.element = Combobox(root, values=self.options, textvariable=self._value)
            self.element.current(self.options.index(self.value))

        elif self.type == 'color':
            self.element = tk.Button(root, command=self.colorPicker, text=self.widgetText, bg=rgbToHex(self.value))

        elif self.type in FUNC_TYPES:
            self.element = tk.Button(root, command=self.callback, text=self.widgetText)

        for key, val in kwparams.items():
            # print(f'[{key}, {val}]')
            self.element[key] = val

        self.element.pack() # grid(row=row.get(), column=column.get())
        # column.set(column.get() + 1)
        if self.tooltip is not None:
            self.tooltipObj = Tooltip(self.element, self.tooltip)

    def colorPicker(self):
        self._value = colorchooser.askcolor(title="Choose Color")[0]
        if self._value is not None:
            self.element['bg'] = rgbToHex(self._value)
        # print(self._value)

    def call(self, params=None, kwparams={}):
        if self.type in FUNC_TYPES:
            if params is None:
                params = self.params
            if kwparams is None:
                kwparams = self.kwparams

            self.returnVal = self.func(*params, *kwparams)
            return self.returnVal
        else:
            raise AttributeError("Cannot call a non-function option")

    def update(self):
        if self.type == 'color':
            if self._value is not None:
                self.value = self._value
        elif self.type in FUNC_TYPES:
            self.value = self._value
        else:
            self.value = self._value.get()
            
        self.save()

    def get(self):
        if self.enum is not None:
            return getattr(self.enum, self.value)
        else:
            return self.value            
    
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

        data[self.name] = self.value

        with open(SETTINGS_FILE, "w") as jsonFile:
            json.dump(data, jsonFile)

    def __lt__(self, option):
        return self.order.index(self.type) < self.order.index(option.type)

    def __gt__(self, option):
        return self.order.index(self.type) > self.order.index(option.type)

    def __str__(self):
        return f'Opt[{self.type}: {self.value}, {self._value}]'




@reprise
class Tracker:
    # order = [Enum, list, tuple, str, float, int, 'color', bool, *FUNC_TYPES]
    
    def __init__(self, variable, label='', tooltip=None):
        self.tooltip = tooltip
        self.value = variable
        self.label = label
        self._value = None
        # if typ == int:
        #     self._value = tk.IntVar(root, self.value)
        # elif typ == bool:
        #     self._value = tk.BooleanVar(root, self.value)
        # elif typ == float:
        #     self._value = tk.DoubleVar(root, self.value)
        # elif typ in (str, tuple, list):
        #     self._value = tk.StringVar(root, self.value)
        # self.type = type(variable)

    def create(self, root, row=None, column=None, **kwparams):
        # self._value = tk.StringVar(root, self.value)
        typ = type(self.value)
        if typ == int:
            self._value = tk.IntVar(root, self.value)
        elif typ == bool:
            self._value = tk.BooleanVar(root, self.value)
        elif typ == float:
            self._value = tk.DoubleVar(root, self.value)

        tk.Label(root, text=self.label, pady=0).pack() #grid(row=row.get() - 1, column=column.get())
        self.element = tk.Label(root, text=str(self._value.get()), pady=0)
        self.element.pack()

        # column.set(column.get() + 1)
        if self.tooltip is not None:
            self.tooltipObj = Tooltip(self.element, self.tooltip)


    def update(self):
        try:
            self.element['text'] = self._value.get()
            self.value = self._value.get()
        except AttributeError:
            pass
    
    def __invert__(self):
        try:
            self.value = self._value.get()
        except AttributeError:
            pass
        return self.value

    def get(self):
        try:
            self.value = self._value.get()
        except AttributeError:
            pass
        return self.value

    def truth(self):
        try:
            self.value = self._value.get()
        except AttributeError:
            pass
        return self.value
    
    def __lt__(self, option):
        self.update()
        try:
            return self.value < option.value
        except AttributeError:
            return self.value < option

    def __gt__(self, option):
        self.update()
        try:
            return self.value > option.value
        except AttributeError:
            return self.value > option

    def __str__(self):
        return f'Track[{self.value}, {self._value}]'
