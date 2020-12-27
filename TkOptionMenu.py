import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from enum import Enum
from ScrolledFrame import ScrolledFrame

# Find the nice piano song at the end of Soul (the movie)
#   learn to play it on guitar?

SCROLL_SPEED = 1
SCREEN_WIDTH_DIVISOR  = 1.3
SCREEN_HEIGHT_DIVISOR = 1.3

class OptionsMenu(ScrolledFrame):
    def __init__(self, master, *options):
        super().__init__(master)
        self.master = master
        self.master.title = 'Options'
        self.master.maxsize(int(self.winfo_screenwidth() / SCREEN_WIDTH_DIVISOR), int(self.winfo_screenheight() / SCREEN_HEIGHT_DIVISOR))
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
        def scrollUp(event):
            self.canvas.yview_scroll(-SCROLL_SPEED, 'units')

        def scrollDown(event):
            self.canvas.yview_scroll(SCROLL_SPEED, 'units')

        #* Create a notebook in the scrolled frame
        self.notebook = Notebook(self.scrolledFrame)

        #* Create all the important widgets in the notebook frames
        for k in self.options:
            self.tabs.append(tk.Frame(self.notebook))
            for i in k:
                i.create(self.tabs[-1])
                tk.Label(self.tabs[-1], text='').pack()

        #* Add tab names to the tabs
        for cnt, i in enumerate(self.tabs):
            self.notebook.add(i, text=self.tabNames[cnt])

        self.master.bind('<Escape>', self.exit)
        self.master.bind('o', self.exit)
        self.master.bind('<Return>', self.save)
        self.master.bind('<Button-4>', scrollUp)
        self.master.bind('<Button-5>', scrollDown)
        # self.master.bind('<Enter>', self.save)

        self.notebook.pack(fill='both', side='top')
        tk.Label(self, text='\n').pack(side='bottom')
        tk.Button(self, text="Cancel", command=self.master.destroy).pack(side='bottom')
        tk.Button(self, text='Save', command=self.save).pack(side='bottom')
        tk.Button(self, text='Restore to Defaults', command=self.restore).pack(side='bottom')

    def restore(self):
        for k in self.options:
            for i in k:
                i.restoreDefault()

    def save(self, event=None):
        print('Saving settings...')
        for k in self.options:
            for i in k:
                # print(i.name, ': ', i.value, ', ', i._value, sep='')
                i.update()
        self.master.destroy()

    def exit(self, notSure):
        self.master.destroy()
