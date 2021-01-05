import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from enum import Enum
from ScrolledFrame import ScrolledFrame
import re, time
# from Point import debug
from _tkinter import TclError

# Find the nice piano song at the end of Soul (the movie)
#   learn to play it on guitar?

SCROLL_SPEED = 1
SCREEN_WIDTH_DIVISOR  = 1.1
SCREEN_HEIGHT_DIVISOR = 1.1

"""
class OptionsMenu(ScrolledFrame):
    def __init__(self, win, *options):
        super().__init__(win)
        self.win = win
        self.win.title = 'Options'
        self.win.maxsize(int(self.winfo_screenwidth() / SCREEN_WIDTH_DIVISOR), int(self.winfo_screenheight() / SCREEN_HEIGHT_DIVISOR))
        # self.win.minsize(int(self.winfo_screenwidth() / (SCREEN_WIDTH_DIVISOR + .9)), int(self.winfo_screenheight() / (SCREEN_HEIGHT_DIVISOR + .9)))
        self.win.minsize(500, 300)
        # winSize = re.findall(r'\d+', self.master.winfo_geometry())
        # print(self.winfo_geometry())
        # print(winSize)
        # print(int(int(winSize[0]) / 2))
        screenXpos = int((self.winfo_screenwidth()  / 2) - 250) # (int(winSize[0]) / 2))
        screenYpos = int((self.winfo_screenheight() / 2) - 150) # (int(winSize[1]) / 2))
        self.win.wm_geometry(f'+{screenXpos}+{screenYpos}')

        self.options = options
        self.tabNames = []
        self.tabs = []

        for i in self.options:
            self.tabNames.append(i[0])
            del i[0]

        # self.pack()
        # self.grid
        self.createUI()

    def createUI(self):
        currentRow = tk.IntVar(self);    currentRow.set(1)
        currentColumn = tk.IntVar(self); currentColumn.set(0)

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
                i.create(self.tabs[-1], row=currentRow, column=currentColumn)
                tk.Label(self.tabs[-1], text='').grid(row=currentRow.get(), column=currentColumn.get())
                currentColumn.set(currentColumn.get() + 1)

        #* Add tab names to the tabs
        for cnt, i in enumerate(self.tabs):
            self.notebook.add(i, text=self.tabNames[cnt])

        self.win.bind('<Escape>', self.exit)
        self.win.bind('o', self.exit)
        self.win.bind('<Return>', self.save)
        self.win.bind('<Button-4>', scrollUp)
        self.win.bind('<Button-5>', scrollDown)
        # self.win.bind('<Configure>', self.configWin)
        # self.win.bind('<Configure>', self.reconfigure)
        def tmp(event):
            if event.y:
                self.configure(width=event.width, height=event.height)
        #     if event.y:
        #         print(event)
        # self.win.bind('<Configure>', tmp)
        # self.master.bind('<Enter>', self.save)

        self.notebook.grid(row=0, column=0)  #.pack(fill='both', side='top')
        tk.Label(self, text='\n').grid(row=currentRow.get(), column=currentColumn.get());                                         currentColumn.set(currentColumn.get() + 1) # .pack(side='bottom')
        tk.Button(self, text="Cancel", command=self.win.destroy).grid(row=currentRow.get(), column=currentColumn.get());          currentColumn.set(currentColumn.get() + 1) # .pack(side='bottom')
        tk.Button(self, text='Save', command=self.save).grid(row=currentRow.get(), column=currentColumn.get());                   currentColumn.set(currentColumn.get() + 1) # .pack(side='bottom')
        tk.Button(self, text='Restore to Defaults', command=self.restore).grid(row=currentRow.get(), column=currentColumn.get()); currentColumn.set(currentColumn.get() + 1) # .pack(side='bottom')

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
        self.win.destroy()

    def exit(self, notSure):
        self.win.destroy()

"""



class OptionsMenu(ScrolledFrame):
    def __init__(self, win, *options):
        super().__init__(win)
        self.win = win
        self.win.title = 'Options'
        self.win.maxsize(int(self.winfo_screenwidth() / SCREEN_WIDTH_DIVISOR), int(self.winfo_screenheight() / SCREEN_HEIGHT_DIVISOR))
        # self.win.minsize(int(self.winfo_screenwidth() / (SCREEN_WIDTH_DIVISOR + .9)), int(self.winfo_screenheight() / (SCREEN_HEIGHT_DIVISOR + .9)))
        self.win.minsize(500, 300)
        # winSize = re.findall(r'\d+', self.master.winfo_geometry())
        # print(self.winfo_geometry())
        # print(winSize)
        # print(int(int(winSize[0]) / 2))
        screenXpos = int((self.winfo_screenwidth()  / 2) - 250) # (int(winSize[0]) / 2))
        screenYpos = int((self.winfo_screenheight() / 2) - 150) # (int(winSize[1]) / 2))
        self.win.wm_geometry(f'+{screenXpos}+{screenYpos}')

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

        self.win.bind('<Escape>', self.exit)
        self.win.bind('o', self.exit)
        self.win.bind('<Return>', self.save)
        self.win.bind('<Button-4>', scrollUp)
        self.win.bind('<Button-5>', scrollDown)
        self.win.bind('<Tab>', self.switchTabForward)
        self.win.bind('<Shift-KeyPress-Tab>', self.switchTabBackward)
        self.win.bind('<Shift-ISO_Left_Tab>', self.switchTabBackward)
        self.win.bind('<Key>', self.keyHandler)
        # self.win.bind('<Configure>', self.configWin)
        # self.win.bind('<Configure>', self.reconfigure)
        def tmp(event):
            if event.y:
                self.configure(width=event.width, height=event.height)
        #     if event.y:
        #         print(event)
        # self.win.bind('<Configure>', tmp)
        # self.master.bind('<Enter>', self.save)

        self.notebook.pack(fill='both', side='top')
        tk.Label(self, text='\n').pack(side='bottom')
        tk.Button(self, text="Cancel", command=self.win.destroy).pack(side='bottom')
        tk.Button(self, text='Save', command=self.save).pack(side='bottom')
        tk.Button(self, text='Restore to Defaults', command=self.restore).pack(side='bottom')

    def keyHandler(self, event):
        # debug(event, color=5)
        pass

    def switchTabForward(self, event):
        try:
            self.notebook.select(self.notebook.index(self.notebook.select()) + 1)
        except TclError:
            self.notebook.select(0)

    def switchTabBackward(self, event):
        tmp=self.notebook.index(self.notebook.select())

        # debug(tmp)

        if tmp == 0:
            self.notebook.select(len(self.tabs) - 1)
        else:
            self.notebook.select(tmp - 1)

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
        self.win.destroy()

    def exit(self, notSure):
        self.win.destroy()
