'''
Created on 18 janv. 2017

@author: dubaipie
'''
import tkinter
from PIL import ImageTk
from tkinter import filedialog
from tkinter import messagebox
import Cypherer.model.CyphererModel as DM
from tkinter import W, E


class Cypherer(tkinter.Frame):
    '''
    Vue du modèle CyphererModel.
    '''

    def __init__(self, master=None):
        '''
        Constructeur de l'interface.
        '''
        
        tkinter.Frame.__init__(self, master)
        
        self._createModel()
        self._createView()
        self._placeComponents()
        self._createController()
    
    def _createModel(self):
        self._model = DM.CyphererModel()
        
        self._keyVar = tkinter.StringVar()
        self._imgVar = tkinter.StringVar()
        self._rslVar = tkinter.StringVar()
    
    def _createView(self):
        self._keyEntry = tkinter.Entry(self)
        self._keyEntry.config(state="readonly", textvariable=self._keyVar)
       
        self._imgEntry = tkinter.Entry(self)
        self._imgEntry.config(state="readonly", textvariable=self._imgVar)
        
        self._rslEntry = tkinter.Entry(self)
        self._rslEntry.config(state="readonly", textvariable=self._rslVar)
        
        self._keyButton = tkinter.Button(self, text=_("Find"))
        self._imgButton = tkinter.Button(self, text=_("Find"))
        self._rslButton = tkinter.Button(self, text=_("Save as"))
        
        self._resultCanvas = tkinter.Canvas(self, bg="white")
        
        self._cypherButton = tkinter.Button(self, text=_("Cypher"))
    
    def _placeComponents(self):
        tkinter.Label(self, text=_("Key : ")).grid(row=1, column=1, sticky=W)
        self._keyEntry.grid(row=1, column=2)
        self._keyButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        
        tkinter.Label(self, text=_("Cyphered Picture : ")).grid(row=2, column=1, sticky=W)
        self._imgEntry.grid(row=2, column=2)
        self._imgButton.grid(row=2, column=3, sticky=E+W, padx=5, pady=5)
        
        tkinter.Label(self, text=_("Destination file : ")).grid(row=3, column=1, sticky=W)
        self._rslEntry.grid(row=3, column=2)
        self._rslButton.grid(row=3, column=3, sticky=E+W, padx=5, pady=5)
        
        self._cypherButton.grid(row=4, column=1, columnspan=3, sticky=E+W)
        
        self._resultCanvas.grid(row=1, rowspan=4, column=4, columnspan=3)
    
    def _createController(self):
        self._keyButton.config(command=self._chooseKey)
        self._imgButton.config(command=self._chooseImg)
        self._rslButton.config(command=self._chooseRsl)
        self._cypherButton.config(command=self._cypher)
        
    def _chooseKey(self):
        dlg = filedialog.askopenfilename()
        
        if dlg != "":
            self._model.keyPath(dlg)
            self._keyVar.set(dlg)
    
    def _chooseImg(self):
        dlg = filedialog.askopenfilename()
        
        if dlg != "":
            self._model.imagePath(dlg)
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