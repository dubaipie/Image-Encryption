from tkinter import Frame, Canvas, Scrollbar
from tkinter import VERTICAL, N, S, W, E, NW, HORIZONTAL
from PIL import ImageTk

import os

class HelpWidget(Frame):
    '''
    Un widget qui contient un aide pour l'utilisation du programme.
    '''
    HELP = os.path.abspath("../../ressources/help/help.jpg")

    def __init__(self, master=None, **options):
        Frame.__init__(self, master, **options)
        self._createView()
        self._placeComponents()
        self._createController()

    # Outils
    def _createView(self):
        self._canvas = Canvas(self)

        picture = ImageTk.PhotoImage(file=HelpWidget.HELP)
        self._canvas.pic = picture
        self._canvas.create_image(0, 0, image=picture, anchor=NW)

        self._yscroll = Scrollbar(self, orient=VERTICAL)
        self._xscroll = Scrollbar(self, orient=HORIZONTAL)

    def _placeComponents(self):
        self._canvas.grid(row=1, column=1, sticky=N+E+W+S)
        self._yscroll.grid(row=1, column=2, sticky=N+S)
        self._xscroll.grid(row=2, column=1, sticky=E+W)

    def _createController(self):
        self._canvas.config(yscrollcommand=self._yscroll.set)
        self._canvas.config(xscrollcommand=self._xscroll.set)
        self._yscroll.config(command=self._canvas.yview)
        self._xscroll.config(command=self._canvas.xview)

        self._canvas.config(scrollregion=(0, 0,
            self._canvas.pic.width(),
            self._canvas.pic.height()))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)