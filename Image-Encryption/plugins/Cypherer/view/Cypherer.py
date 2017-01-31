'''
Created on 18 janv. 2017

@author: dubaipie
'''
from tkinter import Entry, Button, Scrollbar, StringVar, Frame, Canvas, Label
from PIL import ImageTk
from tkinter import filedialog
from tkinter import messagebox
import Cypherer.model.CyphererModel as DM
from tkinter import W, E, HORIZONTAL, VERTICAL


class Cypherer(Frame):
    '''
    Vue du modèle CyphererModel.
    '''

    def __init__(self, master=None):
        '''
        Constructeur de l'interface.
        '''
        
        Frame.__init__(self, master)
        
        self._createModel()
        self._createView()
        self._placeComponents()
        self._createController()
    
    def _createModel(self):
        self._model = DM.CyphererModel()
        
        self._keyVar = StringVar()
        self._imgVar = StringVar()
        self._rslVar = StringVar()
    
    def _createView(self):
        self._keyEntry = Entry(self)
        self._keyEntry.config(state="readonly", textvariable=self._keyVar)
       
        self._imgEntry = Entry(self)
        self._imgEntry.config(state="readonly", textvariable=self._imgVar)
        
        self._rslEntry = Entry(self)
        self._rslEntry.config(state="readonly", textvariable=self._rslVar)
        
        self._keyButton = Button(self, text=_("Find"))
        self._imgButton = Button(self, text=_("Find"))
        self._rslButton = Button(self, text=_("Save as"))
        
        self._resultCanvas = Canvas(self, bg="white")
        
        self._cypherButton = Button(self, text=_("Cypher"))

        # horizontal scrollbar
        self._hbar = Scrollbar(self, orient=HORIZONTAL)

        # vertical scrollbar
        self._vbar = Scrollbar(self, orient=VERTICAL)
    
    def _placeComponents(self):
        Label(self, text=_("Key : ")).grid(row=1, column=1, sticky=W)
        self._keyEntry.grid(row=1, column=2)
        self._keyButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        
        Label(self, text=_("Cyphered Picture : ")).grid(row=2, column=1, sticky=W)
        self._imgEntry.grid(row=2, column=2)
        self._imgButton.grid(row=2, column=3, sticky=E+W, padx=5, pady=5)
        
        Label(self, text=_("Destination file : ")).grid(row=3, column=1, sticky=W)
        self._rslEntry.grid(row=3, column=2)
        self._rslButton.grid(row=3, column=3, sticky=E+W, padx=5, pady=5)
        
        self._cypherButton.grid(row=4, column=1, columnspan=3, sticky=E+W)
        
        self._resultCanvas.grid(row=1, rowspan=4, column=4, columnspan=3)
    
    def _createController(self):
        self._keyButton.config(command=self._chooseKey)
        self._imgButton.config(command=self._chooseImg)
        self._rslButton.config(command=self._chooseRsl)
        self._cypherButton.config(command=self._cypher)

        self._resultCanvas.config(
            xscrollcommand=self._hbar.set,
            yscrollcommand=self._vbar.set
        )
        self._hbar.configure(command=self._resultCanvas.xview)
        self._vbar.configure(command=self._resultCanvas.yview)
        
    def _chooseKey(self):
        dlg = filedialog.askopenfilename()
        
        if dlg != "":
            self._model.keyPath = dlg
            self._keyVar.set(dlg)
    
    def _chooseImg(self):
        dlg = filedialog.askopenfilename()
        
        if dlg != "":
            self._model.imagePath = dlg
            self._imgVar.set(dlg)
    
    def _chooseRsl(self):
        dlg = filedialog.asksaveasfilename()
        
        if dlg != "":
            self._rslVar.set(dlg)
    
    def _cypher(self):
        if (self._model.keyPath is None
                or self._model.imagePath is None
                or self._rslVar.get() == ''):
            messagebox.showerror("Data error", "Please fill all inputs")
        else:
            self._model.cypher(self._rslVar.get())

            self._resultCanvas.picture = ImageTk.PhotoImage(file=self._rslVar.get())
            self._resultCanvas.create_image(0, 0, image=self._resultCanvas.picture)