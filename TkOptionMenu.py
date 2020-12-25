import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from enum import Enum


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
                # self.newline = 
                tk.Label(self.tabs[-1], text='').pack()
                # self.newline.pack()

        #* Add tab names to the tabs
        for cnt, i in enumerate(self.tabs):
            self.notebook.add(i, text=self.tabNames[cnt])

        self.master.bind('<Escape>', self.exit)
        self.master.bind('o', self.exit)
        self.master.bind('<Return>', self.save)
        # self.master.bind('<Enter>', self.save)

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
                # print(i.name, ': ', i.value, ', ', i._value, sep='')
                i.update()
        self.master.destroy()

    def exit(self, notSure):
        self.master.destroy()
