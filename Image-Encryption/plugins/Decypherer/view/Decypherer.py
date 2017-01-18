'''
Created on 18 janv. 2017

@author: dubaipie
'''
import tkinter
from Decypherer.model.DecyphererModel import DecyphererModel

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
        self._model = DecyphererModel()
    
    def _createView(self):
        self._keyEntry = tkinter.Entry(self)
        self._imgEntry = tkinter.Entry(self)
        
        self._keyButton = tkinter.Button(self, text="Parcourir")
        self._imgButton = tkinter.Button(self, text="Parcourir")
        
        self._resultCanvas = tkinter.Canvas(self)
        
        self._decypherButton = tkinter.Button(self, text="Déchiffrer")
    
    def _placeComponents(self):
        tkinter.Label(self, text="Image chiffrée").grid(row=1, column=1)
        self._keyEntry.grid(row=1, column=2)
        self._keyButton.grid(row=1, column=3)
        
        tkinter.Label(self, text="Clé").grid(row=2, column=1)
        self._imgEntry.grid(row=2, column=2)
        self._imgButton.grid(row=2, column=3)
        
        self._decypherButton.grid(row=3, column=2, columnspan=2)
        
        self._resultCanvas.grid(row=1, rowspan=3, column=4, columnspan=3)
    
    def _createController(self):
        pass
        
    
if __name__ == "__main__":
    app = Decypherer()
    app.mainloop()      