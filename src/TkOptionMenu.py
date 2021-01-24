from tkinter import Tk
from tkinter.ttk import *
from enum import Enum
from ScrolledFrame import ScrolledFrame
import re, time
from _tkinter import TclError
from Cope import debug, debugged, rgbToHex
import ttkthemes
from TkOptions import Option


SCROLL_SPEED = 1
SCREEN_WIDTH_DIVISOR  = 1.1
SCREEN_HEIGHT_DIVISOR = 1.1


def generateStyle():
    s = ttkthemes.ThemedStyle()
    # s.theme_use('default')

    # bg = rgbToHex((49, 54, 59))
    bg = '#31363b'
    fg = rgbToHex((200, 200, 200))

    s.configure('.',         background=bg)
    s.configure('TLabel',    foreground=fg)
    s.configure('TFrame',    background=bg)
    s.configure('TCombobox', fieldbackground=bg)
    s.configure('TEntry',    fieldbackground=bg)
    s.configure('TSpinbox',  fieldbackground=bg)
    s.configure('TButton',   foreground=fg)
    s.configure('tooltip.TLabel', background=bg, relief='solid', borderwidth=1, wraplength=180, foreground=fg)

    return s


class OptionsMenu(ScrolledFrame):
    def __init__(self, win, *options, styleOptionTab='General'):
        super().__init__(win, backgroundColor=(49, 54, 59))
        self.win = win
        self.win.title = 'Options'

        s = generateStyle()

        #* Add the style Option
        if styleOptionTab is not None and len(styleOptionTab):
            style = Option(s.theme_names(), 'GUI Theme', tab=styleOptionTab, currentItem='default', updateFunc=s.theme_use, tooltip='The theme to use for this options menu', var='style')
            s.theme_use(style.get())
            options += (style,)

        #* Put it in the correct place on screen
        screenXpos = int((self.winfo_screenwidth()  / 2) - 250) # (int(winSize[0]) / 2))
        screenYpos = int((self.winfo_screenheight() / 2) - 150) # (int(winSize[1]) / 2))
        self.win.wm_geometry(f'+{screenXpos}+{screenYpos}')

        self.options = options
        #* A sorted list of unique tabnames
        self.tabNames = sorted(list(set([i.tab for i in options])))
        # Make sure the General tab is first
        if 'General' in self.tabNames:
            self.tabNames.remove('General')
            self.tabNames.insert(0, 'General')
        self.tabs = {}



        #* track changes to the canvas and frame width and sync them,
        #   also updating the scrollbar
        # def _configure_interior(event):
        #     #* update the scrollbars to match the size of the inner frame
        #     size = (scrolledFrame.winfo_reqwidth(), scrolledFrame.winfo_reqheight())
        #     self.canvas.config(scrollregion="0 0 %s %s" % size)
        #     if scrolledFrame.winfo_reqwidth() != self.canvas.winfo_width():
        #         #* update the canvas's width to fit the inner frame
        #         self.canvas.config(width=scrolledFrame.winfo_reqwidth())
        # scrolledFrame.bind('<Configure>', _configure_interior)

        # def _configure_canvas(event):
        #     if frame.winfo_reqwidth() != self.notebook.winfo_width():
        #         #* update the inner frame's width to fill the canvas
        #         self.notebook.itemconfigure(interior_id, width=self.canvas.winfo_width())
        # self.canvas.bind('<Configure>', _configure_canvas)



        self.grid()
        self.createUI()

    def createUI(self):
        def scrollUp(event):
            self.canvas.yview_scroll(-SCROLL_SPEED, 'units')

        def scrollDown(event):
            self.canvas.yview_scroll(SCROLL_SPEED, 'units')

        #* Create a notebook in the scrolled frame
        self.notebook = Notebook(self.scrolledFrame)

        #* Create all the important widgets in the notebook frames
        for i in self.tabNames:
            self.tabs[i] = Frame(self.notebook)
            # HEIGHT_OF_BUTTONS = 100
            # if self.tabs[i].grid_bbox()[3] < self.winfo_height() - HEIGHT_OF_BUTTONS:
                # self.tabs[i].grid_propagate(self.winfo_height() - HEIGHT_OF_BUTTONS)



        currCol = 0

        #* Go through and create the elements
        for i in self.options:
            for tmp in (i.create(self.tabs[i.tab]),):
                title, le = tmp
                label, element = le
                currCol += 1
                if title   is not None: title.grid(row=currCol - 1, column=1)
                if label   is not None: label.grid(column=0, row=currCol, sticky='w')
                if element is not None: element.grid(column=1, row=currCol, sticky='w')
                currCol += 1

        #* Add tab names to the tabs
        for name, tab in self.tabs.items():
            self.notebook.add(tab, text=name)

        def adjustSize(event):
            # self.notebook.configure()
            pass

        self.win.bind('<Escape>', self.exit)
        self.win.bind('o', self.exit)
        self.win.bind('<Return>', self.save)
        self.win.bind('<Button-4>', scrollUp)
        self.win.bind('<Button-5>', scrollDown)
        self.win.bind('<Tab>', self.switchTabForward)
        self.win.bind('<Shift-KeyPress-Tab>', self.switchTabBackward)
        self.win.bind('<Shift-ISO_Left_Tab>', self.switchTabBackward)
        # self.win.bind_all(func=print)
        self.win.bind('<Configure>', print)
        self.win.bind('<Configure>', adjustSize)

        self.notebook.grid(sticky='nsew') #fill='both', side='top'

        # Label( self, text='\n').pack()
        Button(self, text='Save', command=self.save).pack()
        Button(self, text="Cancel", command=self.win.destroy).pack()
        Button(self, text='Restore to Defaults', command=self.restore).pack()

    def switchTabForward(self, event):
        try:
            self.notebook.select(self.notebook.index(self.notebook.select()) + 1)
        except TclError:
            self.notebook.select(0)

    def switchTabBackward(self, event):
        tmp=self.notebook.index(self.notebook.select())

        if tmp == 0:
            self.notebook.select(len(self.tabs) - 1)
        else:
            self.notebook.select(tmp - 1)

    def restore(self):
        for i in self.options:
            i.restoreDefault()

    def save(self, event=None):
        print('Saving settings...')
        for i in self.options:
            i.update()
        self.win.destroy()

    def exit(self, _):
        self.win.destroy()
