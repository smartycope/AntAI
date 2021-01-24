from tkinter.ttk import *
from tkinter import Canvas
from warnings import warn
from Cope import rgbToHex

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class ScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, backgroundColor=(49, 54, 59), *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        #* Create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill='y', side='right', expand=0)
        # parent.grid_rowconfigure(0, weight=8)
        # parent.grid_rowconfigure(1, weight=8)
        # parent.grid_rowconfigure(2, weight=8)

        # vscrollbar.grid(column=10, row=0, rowspan=200, sticky='E')
        self.canvas = Canvas(self, bd=False, highlightthickness=0, yscrollcommand=vscrollbar.set, bg=rgbToHex(backgroundColor))
        self.canvas.pack(side='top', fill='both', expand=1)
        # self.canvas.grid() #row=0, column=0, rowspan=20, columnspan=20)
        vscrollbar.config(command=self.canvas.yview)

        #* Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        #* create a frame inside the canvas which will be scrolled with it
        self.scrolledFrame = scrolledFrame = Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=scrolledFrame, anchor='nw')


        #* Track changes to the canvas and frame width and sync them,
        #   also updating the scrollbar
        def _configure_interior(event):
            #* update the scrollbars to match the size of the inner frame
            size = (scrolledFrame.winfo_reqwidth(), scrolledFrame.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if scrolledFrame.winfo_reqwidth() != self.canvas.winfo_width():
                #* update the canvas's width to fit the inner frame
                self.canvas.config(width=scrolledFrame.winfo_reqwidth())
        scrolledFrame.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if scrolledFrame.winfo_reqwidth() != self.canvas.winfo_width():
                #* update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)
