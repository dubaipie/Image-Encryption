'''
Created on 1 févr. 2017

@author: havarjos
'''

import PIL
import Cypherer.model.CyphererModel as DM
from tkinter import Entry, Button, Scrollbar, StringVar, Frame, Canvas, Label
from PIL import ImageTk
from Cypherer.model.CyphererModel import MismatchFormatException
from tkinter import filedialog
from tkinter import messagebox
from tkinter import W, E, HORIZONTAL, VERTICAL, N, S, NW, SE

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
        #Frame
        self._frame1 = Frame(self)
        self._frame2 = Frame(self)
        self._frame3 = Frame(self)
        self._frame4 = Frame(self)
        self._frame5 = Frame(self)
        self._frame6 = Frame(self)
        
        #Les barres de texte pour la recherche de fichier
        
        self._keyEntry = Entry(self._frame1)
        self._keyEntry.config(state="readonly", textvariable=self._keyVar)
       
        self._imgCypherEntry = Entry(self._frame2)
        self._imgCypherEntry.config(state="readonly", textvariable=self._img_Cypher_Var)
        
        self._imgDecypherEntry = Entry(self._frame3)
        self._imgDecypherEntry.config(state="readonly", textvariable=self._img_Decypher_Var)
        
        #Les Boutons
        
        self._keyButton = Button(self._frame1, text=_("Find"))
        self._imgCypherButton = Button(self._frame2, text=_("Find"))
        self._imgDecypherButton = Button(self._frame3, text=_("Save as"))
        self._decypherButton = Button(self, text=_("Decypher"))
        
        #Les Canvas
        
        self._keyCanvas = Canvas(self._frame4, bg="white")
        self._imgCypherCanvas = Canvas(self._frame5, bg="white")
        self._imgDecypherCanvas = Canvas(self._frame6, bg="white")
        
        self._DecypherButton = Button(self, text=_("Decypher"))
        
        # horizontal scrollbar
        self._hbar1 = Scrollbar(self._frame4, orient=HORIZONTAL)
        self._hbar2 = Scrollbar(self._frame5, orient=HORIZONTAL)
        self._hbar3 = Scrollbar(self._frame6, orient=HORIZONTAL)

        # vertical scrollbar
        self._vbar1 = Scrollbar(self._frame4, orient=VERTICAL)
        self._vbar2 = Scrollbar(self._frame5, orient=VERTICAL)
        self._vbar3 = Scrollbar(self._frame6, orient=VERTICAL)
        self._frame1.grid(row=1, column=1)
    def _placeComponents(self):
        
        #FRAME1
        Label(self._frame1, text=_("Key : ")).grid(row=1, column=1, sticky=W)
        self._keyEntry.grid(row=1, column=2)
        self._keyButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        self._frame1.grid(row=1, column=1)
        
        #FRAME2
        Label(self._frame2, text=_("Cyphered Picture : ")).grid(row=2, column=1, sticky=W)
        self._imgCypherEntry.grid(row=2, column=2)
        self._imgCypherButton.grid(row=2, column=3, sticky=E+W, padx=5, pady=5)
        self._frame2.grid(row=1,column=2)
        
        #FRAME3
        Label(self._frame3, text=_("Destination file : ")).grid(row=3, column=1, sticky=W)
        self._imgDecypherEntry.grid(row=3, column=2)
        self._imgDecypherButton.grid(row=3, column=3, sticky=E+W, padx=5, pady=5)
        self._frame3.grid(row=1,column=3)
        
        #FRAME4
        self._keyCanvas.grid(row = 1, column = 1, sticky=NW+SE)
        self._hbar1.grid(row=2, column=1, sticky=W+E)
        self._vbar1.grid(row=1, column=2, sticky=N+S)
        self._frame4.grid(row=2, column=1, sticky=NW+SE)
        
        #FRAME5
        self._imgCypherCanvas.grid(row = 1, column = 1, sticky=NW+SE)
        self._hbar2.grid(row=2, column=1, sticky=W+E)
        self._vbar2.grid(row=1, column=2, sticky=N+S)
        self._frame5.grid(row=2, column=2, sticky=NW+SE)
        
        #FRAME6
        self._imgDecypherCanvas.grid(row = 1, column = 1, sticky=NW+SE)
        self._hbar3.grid(row=2, column=1, sticky=W+E)
        self._vbar3.grid(row=1, column=2, sticky=N+S)
        self._frame6.grid(row=2, column=3, sticky=NW+SE)
        
        self._decypherButton.grid(row=3, column=1, columnspan=3, sticky=E+W)
           
          
    def _createController(self):
        self._keyButton.config(command=self._chooseKey)
        self._imgCypherButton.config(command=self._chooseImgCypher)
        self._imgDecypherButton.config(command=self._chooseDecypher)
        self._decypherButton.config(command=self._decypher)

        self.grid_rowconfigure(2, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_rowconfigure(3, weight = 1)
        
        self._frame4.grid_columnconfigure(1, weight = 1)
        self._frame4.grid_rowconfigure(1, weight = 1)
        
        self._frame5.grid_columnconfigure(1, weight = 1)
        self._frame5.grid_rowconfigure(1, weight = 1)
        
        self._frame6.grid_columnconfigure(1, weight = 1)
        self._frame6.grid_rowconfigure(1, weight = 1)
        
        self._keyCanvas.configure(
            xscrollcommand=self._hbar1.set,
            yscrollcommand=self._vbar1.set
        )
        
        self._hbar1.configure(command=self._keyCanvas.xview)
        self._vbar1.configure(command=self._keyCanvas.yview)
        
        self._imgCypherCanvas.configure(
            xscrollcommand=self._hbar2.set,
            yscrollcommand=self._vbar2.set
        )
        
        self._hbar2.configure(command=self._imgCypherCanvas.xview)
        self._vbar2.configure(command=self._imgCypherCanvas.yview)
        
        self._imgDecypherCanvas.configure(
            xscrollcommand=self._hbar3.set,
            yscrollcommand=self._vbar3.set
        )
        self._hbar3.configure(command=self._imgDecypherCanvas.xview)
        self._vbar3.configure(command=self._imgDecypherCanvas.yview)
        
    def _chooseKey(self):
        dlg = filedialog.askopenfilename(title="Ouvrir", filetypes=[("PPM", "*.ppm")])
        
        if dlg != "":
            self._model.keyPath = dlg
            self._keyVar.set(dlg)
            self._addImageInCanvas(self._keyCanvas, dlg)
    
    def _chooseImgCypher(self):
        dlg = filedialog.askopenfilename(title="Ouvrir", filetypes=[("PPM", "*.ppm")] )
    
        if dlg != "":
            self._model.imagePath = dlg
            self._img_Cypher_Var.set(dlg)
            self._addImageInCanvas(self._imgCypherCanvas, dlg)
    
    def _chooseDecypher(self):
        dlg = filedialog.asksaveasfilename(title="Enregistrer sous", defaultextension=".ppm") 
        if dlg != "":
            self._img_Decypher_Var.set(dlg)
    
    def _decypher(self):
        if (self._model.keyPath is None  or self._model.imagePath is None
                or self._img_Decypher_Var.get() == ''):
            messagebox.showerror("Data error", "Please fill all inputs")
        else :
            
            try :
                self._model.cypher(self._img_Decypher_Var.get())
                self._addImageInCanvas(self._imgDecypherCanvas, self._img_Decypher_Var.get())
            except MismatchFormatException:
                messagebox.showerror("Taille", "la taille du masque et de l'image ne corresponde pas")
    
    def _addImageInCanvas(self, canvas, img):
        im = PIL.Image.open(img)
        x,y = im.size
        im.close()
        canvas.picture = ImageTk.PhotoImage(file=img)
        canvas.create_image(x/2, y/2, image=canvas.picture)
        canvas.config(scrollregion=(0,0,x,y))