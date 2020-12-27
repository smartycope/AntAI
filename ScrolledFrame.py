import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class ScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill='y', side='right', expand=0)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=1)
        vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.scrolledFrame = scrolledFrame = Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=scrolledFrame, anchor='nw')

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event=None):
            print('here')
            # update the scrollbars to match the size of the inner frame
            size = (scrolledFrame.winfo_reqwidth(), scrolledFrame.winfo_reqheight())
            self.canvas.config(scrollregion=f"0 0 {size[0]} {size[1]}")
            if scrolledFrame.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=scrolledFrame.winfo_reqwidth())
        scrolledFrame.bind('<Configure>', _configure_interior)

        # I don't feel like moving this into a better scope.
        self.configureInterior = _configure_interior

        def _configure_canvas(event):
            print('there')
            if scrolledFrame.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)
