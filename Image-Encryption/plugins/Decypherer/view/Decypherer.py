'''
Created on 1 févr. 2017

@author: havarjos
'''

import Cypherer.model.CyphererModel as DM
from tkinter import Entry, Button, Scrollbar, StringVar, Frame, Canvas, Label
from PIL import ImageTk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import W, E, HORIZONTAL, VERTICAL

class Decypherer(Frame):
    
    '''
    Vue du modèle de Decypherer, le même
    que celui du Cypherer.
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
        self._img_Cypher_Var = StringVar() 
        self._img_Decypher_Var = StringVar()
        
    def _createView(self):
        self._keyEntry = Entry(self)
        self._keyEntry.config(state="readonly", textvariable=self._keyVar)
       
        self._imgCypherEntry = Entry(self)
        self._imgCypherEntry.config(state="readonly", textvariable=self._img_Cypher_Var)
        
        self._imgDecypherEntry = Entry(self)
        self._imgDecypherEntry.config(state="readonly", textvariable=self._img_Decypher_Var)
        
        self._keyButton = Button(self, text=_("Find"))
        self._imgCypherButton = Button(self, text=_("Find"))
        self._imgDecypherButton = Button(self, text=_("Save as"))
        
        self._resultCanvas = Canvas(self, bg="white")
        
        self._DecypherButton = Button(self, text=_("Decypher"))
        
        # horizontal scrollbar
        self._hbar = Scrollbar(self, orient=HORIZONTAL)

        # vertical scrollbar
        self._vbar = Scrollbar(self, orient=VERTICAL)
        
    def _placeComponents(self):
        Label(self, text=_("Key : ")).grid(row=1, column=1, sticky=W)
        self._keyEntry.grid(row=1, column=2)
        self._keyButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        
        Label(self, text=_("Cyphered Picture : ")).grid(row=2, column=1, sticky=W)
        self._imgCypherEntry.grid(row=2, column=2)
        self._imgCypherButton.grid(row=2, column=3, sticky=E+W, padx=5, pady=5)
        
        Label(self, text=_("Destination file : ")).grid(row=3, column=1, sticky=W)
        self._imgDecypherEntry.grid(row=3, column=2)
        self._imgDecypherButton.grid(row=3, column=3, sticky=E+W, padx=5, pady=5)
        
        self._DecypherButton.grid(row=4, column=1, columnspan=3, sticky=E+W)
        
        self._resultCanvas.grid(row=1, rowspan=4, column=4, columnspan=3)     
          
    def _createController(self):
        self._keyButton.config(command=self._chooseKey)
        self._imgCypherButton.config(command=self._chooseImgCypher)
        self._imgDecypherButton.config(command=self._chooseDecypher)
        self._DecypherButton.config(command=self._decypher)

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
    
    def _chooseImgCypher(self):
        dlg = filedialog.askopenfilename()
        
        if dlg != "":
            self._model.imagePath = dlg
            self._img_Cypher_Var.set(dlg)
    
    def _chooseDecypher(self):
        dlg = filedialog.asksaveasfilename()
        
        if dlg != "":
            self._img_Decypher_Var.set(dlg) 
    
    def _decypher(self):
        if (self._model.keyPath is None
                or self._model.imagePath is None
                or self._img_Decypher_Var.get() == ''):
            messagebox.showerror("Data error", "Please fill all inputs")
        else:
            self._model.cypher(self._img_Decypher_Var.get())

            self._resultCanvas.picture = ImageTk.PhotoImage(file=self._img_Decypher_Var.get())
            self._resultCanvas.create_image(0, 0, image=self._resultCanvas.picture)   