import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from tkinter import colorchooser
from enum import Enum

from os.path import dirname; DIR = dirname(__file__)
import os

import json

RESET_FILE = True

SETTINGS_FILE = DIR + '/settings.json'

class Option:
    def __init__(self, value, label='', currentItem=None, widgetText='', min=None, max=None, _type=None):
        self.defaultValue = value
        self.type = _type
        if type(self.type) is str:
            self.type = self.type.lower()
        validTypeList = (int, float, bool, str, tuple, list, 'color')

        #* If value is an Enum
        if type(value) not in validTypeList and issubclass(value, Enum) and _type is None:
            self.type = list
            self.options = [name for name, member in value.__members__.items()]
            if currentItem is not None:
                try:
                    self.value = currentItem.name
                    self.defaultValue = self.value
                except AttributeError:
                    raise UserWarning("The value given to the option is not in the enum provided.")
        else:
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

        if RESET_FILE:
            self.restoreDefault()

        #* Load the value from the settings file over the given default value
        if not os.path.exists(SETTINGS_FILE):
            os.system('touch ' + SETTINGS_FILE)
            with open(SETTINGS_FILE, 'r+') as f:
                json.dump({}, f)

            self.restoreDefault()
        else:
            with open(SETTINGS_FILE, 'r+') as f:
                self.value = json.load(f)[self.name]

    def restoreDefault(self):
        print(f'Reseting {self.value} to {self.defaultValue}')
        self.value = self.defaultValue
        if self._value is not None:
            self._value.set(self.defaultValue)

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

    def create(self, root):
        if self.type == int:
            self._value = tk.IntVar(root, self.value)
        elif self.type == bool:
            self._value = tk.BooleanVar(root, self.value)
        elif self.type == float:
            self._value = tk.DoubleVar(root, self.value)
        elif self.type in (str, tuple, list):
            self._value = tk.StringVar(root, self.value)
        # elif self.type in (tuple, list):
            # self._value = tk.StringVar(r)

        if len(self.name): # and self.type is not bool:
            self.label = tk.Label(root, text=self.name)
            self.label.pack()

        if self.type is int:
            self.element = tk.Spinbox(root, from_=self.min, to=self.max, textvariable=self._value)

        elif self.type is float:
            self.element = tk.Entry(root, textvariable=self._value)

        elif self.type is bool:
            # NOTE: Not tk.Checkbutton
            self.element = Checkbutton(root, text=self.widgetText, variable=self._value) #, onvalue=True, offvalue=False)
            # self.element.bind('<Button-1>', self.invertCheckbox)

        elif self.type is str:
            self.element = tk.Entry(root, text=self.startText, textvariable=self._value)

        elif self.type in (tuple, list):
            # NOTE: Not tk.Combobox
            self.element = Combobox(root, values=self.options, textvariable=self._value)
            self.element.current(self.options.index(self.value))

        elif self.type.lower() == 'color':
            self.element = tk.Button(root, command=self.colorPicker, text=self.widgetText, fg=self._value)

        self.element.pack()

    def colorPicker(self):
        self._value = colorchooser.askcolor(title="Choose Color")[0]
        # print(self._value)

    def update(self):
        if self.type not in (tuple, list):
            self.value = self._value.get()
        else:
            self.value = self._value
        self.save()

    def get(self):
        return self.value
            
    def __invert__(self):
        return self.value

    def truth(self):
        return self.value
    
    def save(self):
        with open(SETTINGS_FILE, "r") as jsonFile:
            data = json.load(jsonFile)

        data[self.name] = self.value

        with open(SETTINGS_FILE, "w") as jsonFile:
            json.dump(data, jsonFile)



class OptionsMenu(tk.Frame):
    def __init__(self, master, *options):
        super().__init__(master)
        self.master = master
        self.master.title = 'Options'
        # self.master.maxsize(1000, 600)
        self.master.minsize(500,  300)

        self.options = options
        self.tabNames = []
        self.tabs = []

        for i in self.options:
            self.tabNames.append(i[0])
            del i[0]

        self.pack()
        self.createUI()

    def createUI(self):
        self.notebook = Notebook(self)

        #* Create all the important widgets
        for k in self.options:
            self.tabs.append(tk.Frame(self.notebook))
            for i in k:
                i.create(self.tabs[-1])
                self.newline = tk.Label(self.tabs[-1], text='')
                self.newline.pack()

        #* Add tab names to the tabs
        for cnt, i in enumerate(self.tabs):
            self.notebook.add(i, text=self.tabNames[cnt])

        self.master.bind('<Escape>', self.exit)
        self.master.bind('o', self.exit)
        self.master.bind('<Return>', self.save)
        self.master.bind('<Enter>', self.save)

        # self.scrollbar = Scrollbar(self)
        # self.scrollbar.pack(side='right')

        self.notebook.pack(expand=1, fill='both')

        self.newline = tk.Label(self, text='\n')
        self.newline.pack()

        self.quit = tk.Button(self, text="Cancel", command=self.master.destroy)
        # self.quit.pack(side='bottom')
        # self.quit.pack(side='bottom', padx=, pady=0)
        self.quit.pack()
        # self.quit.place(rely=0.0, relx=0.0, x=0, y=0, anchor='s')

        self.saveButton = tk.Button(self, text='Save', command=self.save)
        # self.saveButton.pack(side="bottom")
        # self.saveButton.pack(side='bottom', padx=0, pady=5)
        self.saveButton.pack()
        # self.saveButton.place(rely=0.0, relx=0.0, x=0, y=0, anchor='s')

        self.restoreButton = tk.Button(self, text='Restore to Defaults', command=self.restore, padx=100)
        self.restoreButton.pack(side='bottom')
        # self.restoreButton.gri

        
        # self.restoreButton.pack(side='bottom', padx=0, pady=10)
        # self.restoreButton.pack()
        # self.restoreButton.place(relx=1)

        # self.scrollbar.config(command=self.scrollStuff)

    def restore(self):
        for k in self.options:
            for i in k:
                i.restoreDefault()

    def scrollStuff(self, param):
        self.newline.pady - 1
        self.quit.pady - 1
        self.saveButton.pady - 1
        for i in self.options:
            i.pady - 1

    def save(self, event=None):
        print('Saving settings...')
        for k in self.options:
            for i in k:
                i.update()
        self.master.destroy()

    def exit(self, notSure):
        self.master.destroy()