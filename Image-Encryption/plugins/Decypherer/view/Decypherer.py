'''
Created on 18 janv. 2017

@author: dubaipie
'''
import tkinter
from tkinter import filedialog
import Decypherer.model.DecyphererModel as DM

class Decypherer(tkinter.Frame):
    '''
    Vue du modèle DecyphererModel.
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
        self._model = DM.DecyphererModel()
    
    def _createView(self):
        self._keyEntry = tkinter.Entry(self)
        self._keyEntry.config(state="readonly")
        self._imgEntry = tkinter.Entry(self)
        self._imgEntry.config(state="readonly")
        
        self._keyButton = tkinter.Button(self, text=_("Find"))
        self._imgButton = tkinter.Button(self, text=_("Find"))
        
        self._resultCanvas = tkinter.Canvas(self, bg="blue")
        
        self._decypherButton = tkinter.Button(self, text=_("Decypher"))
    
    def _placeComponents(self):
        tkinter.Label(self, text=_("Key")).grid(row=1, column=1)
        self._keyEntry.grid(row=1, column=2)
        self._keyButton.grid(row=1, column=3)
        
        tkinter.Label(self, text=_("Cyphered Picture")).grid(row=2, column=1)
        self._imgEntry.grid(row=2, column=2)
        self._imgButton.grid(row=2, column=3)
        
        self._decypherButton.grid(row=3, column=2, columnspan=2)
        
        self._resultCanvas.grid(row=1, rowspan=3, column=4, columnspan=3)
    
    def _createController(self):
        self._keyButton.config(command=self._chooseKey)
        self._imgButton.config(command=self._chooseImg)
    
    def _chooseKey(self):
        dlg = filedialog.askopenfilename()
        
        if dlg != "":
            self._model.setKeyPath(dlg)
            self._keyEntry.delete(0, tkinter.END)
            self._keyEntry.insert(0, dlg)
    
    def _chooseImg(self):
        dlg = filedialog.askopenfilename()
        
        if dlg != "":
            self._model.setImgPath(dlg)
            self._imgEntry.delete(0, tkinter.END)
            self._imgEntry.insert(0, dlg)
