'''
Created on 18 janv. 2017

@author: dubaipie
'''
import PIL
import Cypherer.model.CyphererModel as DM
import os
import threading
from tkinter import Entry, Button, StringVar, Frame, Canvas, Label, LabelFrame
from PIL import ImageTk
from tkinter import filedialog
from tkinter import messagebox
from Generator.model.GeneratorModel import GeneratorModel
from Cypherer.model.CyphererModel import MismatchFormatException
from tkinter import W, E, HORIZONTAL, VERTICAL, N, S, NW, SE
from tkinter.constants import DISABLED, NORMAL
from Utils.AutoScrollbar import *


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
        
        self._l = [None,None,None]
        self._keyVar = StringVar()
        self._imgVar = StringVar()
        self._rslVar = StringVar()
    
    def _createView(self):
        #Frame
        self._frame1 = Frame(self)
        self._frame2 = Frame(self)
        self._frame3 = Frame(self)
        self._frame4 = LabelFrame(self, text="Aperçu de la clé")
        self._frame5 = LabelFrame(self, text="Aperçu de l'image")
        self._frame6 = LabelFrame(self, text="Aperçu du résultat")
        
        #les boutons de recherche de fichiers
        self._keyEntry = Entry(self._frame1)
        self._keyEntry.config(state="readonly", textvariable=self._keyVar)
        
        self._imgEntry = Entry(self._frame2)
        self._imgEntry.config(state="readonly", textvariable=self._imgVar)
        
        self._rslEntry = Entry(self._frame3)
        self._rslEntry.config(state="readonly", textvariable=self._rslVar)
        
        #Boutons
        self._keyButton = Button(self._frame1, text=_("Find"))
        self._imgButton = Button(self._frame2, text=_("Find"))
        self._rslButton = Button(self._frame3, text=_("Save as"))
        self._cypherButton = Button(self, text=_("Cypher"))
        self._resetButton = Button(self._frame3, text=("Reset"))
        
        #Canvas
        self._resultCanvas = Canvas(self._frame6)
        self._keyCanvas = Canvas(self._frame4)
        self._imgCanvas = Canvas(self._frame5)
        
        # horizontal AutoScrollbar
        self._hbar = AutoScrollbar(self._frame4, orient=HORIZONTAL)
        self._hbar2 = AutoScrollbar(self._frame5, orient=HORIZONTAL)
        self._hbar3 = AutoScrollbar(self._frame6, orient=HORIZONTAL)
        
        # vertical AutoScrollbar
        self._vbar = AutoScrollbar(self._frame4, orient=VERTICAL)
        self._vbar2 = AutoScrollbar(self._frame5, orient=VERTICAL)
        self._vbar3 = AutoScrollbar(self._frame6, orient=VERTICAL)
        
    def _placeComponents(self):
        #FRAME1
        Label(self._frame1, text=_("Key : ")).grid(row=1, column=1, sticky=W)
        self._keyEntry.grid(row=1, column=2)
        self._keyButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        self._frame1.grid(row=1, column=1)
        
        #FRAME4
        self._keyCanvas.grid(row = 1, column = 1, sticky=NW+SE)
        self._hbar.grid(row=2, column=1, sticky=W+E)
        self._vbar.grid(row=1, column=2, sticky=N+S)
        self._frame4.grid(row=2, column=1, sticky=NW+SE)
        
        #FRAME2
        Label(self._frame2, text=_("Cyphered Picture : ")).grid(row=1, column=1, sticky=W)
        self._imgEntry.grid(row=1, column=2)
        self._imgButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        self._frame2.grid(row=1, column=2)
                
        #FRAME5
        self._imgCanvas.grid(row = 1, column = 1, sticky=NW+SE)
        self._hbar2.grid(row=2, column=1, sticky=W+E)
        self._vbar2.grid(row=1, column=2, sticky=N+S)
        self._frame5.grid(row=2, column=2, sticky=NW+SE)
        
        #FRAME3
        Label(self._frame3, text=_("Destination file : ")).grid(row=1, column=1, sticky=W)
        self._rslEntry.grid(row=1, column=2)
        self._rslButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        self._resetButton.grid(row=1, column=4)
        self._frame3.grid(row=1, column=3)
        
        #FRAME6
        self._resultCanvas.grid(row = 1, column = 1, sticky=NW+SE)
        self._hbar3.grid(row=2, column=1, sticky=W+E)
        self._vbar3.grid(row=1, column=2, sticky=N+S)
        self._frame6.grid(row=2, column=3, sticky=NW+SE)
        
        self._cypherButton.grid(row=3, column=1, columnspan=3, sticky=E+W)
        
        self._imgCanvas.delete()

    def _createController(self):
        self._keyButton.config(command=self._chooseKey)
        self._imgButton.config(command=self._chooseImg)
        self._rslButton.config(command=self._chooseRsl)
        self._cypherButton.config(command=self._cypher)
        self._resetButton.config(command=self._reset)
        
        self.grid_rowconfigure(2, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_columnconfigure(3, weight = 1)
        self.grid_rowconfigure(3, weight = 1)
        
        self._frame4.grid_columnconfigure(1, weight = 1)
        self._frame4.grid_rowconfigure(1, weight = 1)
        
        self._frame5.grid_columnconfigure(1, weight = 1)
        self._frame5.grid_rowconfigure(1, weight = 1)
        
        self._frame6.grid_columnconfigure(1, weight = 1)
        self._frame6.grid_rowconfigure(1, weight = 1)
        
        self._keyCanvas.configure(
            xscrollcommand=self._hbar.set,
            yscrollcommand=self._vbar.set
        )
        self._hbar.configure(command=self._keyCanvas.xview)
        self._vbar.configure(command=self._keyCanvas.yview)
        
        self._imgCanvas.configure(
            xscrollcommand=self._hbar2.set,
            yscrollcommand=self._vbar2.set
        )
        self._hbar2.configure(command=self._imgCanvas.xview)
        self._vbar2.configure(command=self._imgCanvas.yview)
        
        self._resultCanvas.configure(
            xscrollcommand=self._hbar3.set,
            yscrollcommand=self._vbar3.set
        )
        self._hbar3.configure(command=self._resultCanvas.xview)
        self._vbar3.configure(command=self._resultCanvas.yview)
        
    def _chooseKey(self):
        dlg = filedialog.askopenfilename(title="Ouvrir", filetypes=[("PPM", "*.ppm")])
        
        if dlg != "":
            self._model.keyPath = dlg
            self._keyVar.set(dlg)
            self._addImageInCanvas(self._keyCanvas, dlg, 0)
            
    def _chooseImg(self):
        dlg = filedialog.askopenfilename(title="Ouvrir", filetypes=[("PPM", "*.ppm")] )
    
        if dlg != "":
            self._model.imagePath = dlg
            self._imgVar.set(dlg)
            self._addImageInCanvas(self._imgCanvas, dlg, 1)
    
    def _chooseRsl(self):
        dlg = filedialog.asksaveasfilename(title="Enregistrer sous", defaultextension=".ppm") 
        if dlg != "":
            self._rslVar.set(dlg)
    
    def _cypher(self):
        if (self._model.imagePath is None
                or self._rslVar.get() == ''):
            messagebox.showerror("Data error", "Please fill all inputs")
            return
        if (self._model.keyPath is None):
            t2 = threading.Thread(target=self._generateKey())
            t2.start()
        else:
            t = threading.Thread(target=self._execute)
            t.start()
    
    def _execute(self):
        self._cypherButton.config(state=DISABLED)
        try :
            self._model.cypher(self._rslVar.get())
            self._addImageInCanvas(self._resultCanvas, self._rslVar.get(), 2)
        except MismatchFormatException:
            messagebox.showerror("Taille", "la taille du masque et de l'image ne corresponde pas")
        self._cypherButton.config(state=NORMAL)
            
    def _addImageInCanvas(self, canvas, img, i):
        im = PIL.Image.open(img)
        x,y = im.size
        im.close()
        canvas.picture = ImageTk.PhotoImage(file=img)
        self._l[i] = canvas.create_image(x/2, y/2, image=canvas.picture)
        canvas.config(scrollregion=(0,0,x,y))

    def _generateKey(self):
        self._cypherButton.config(state=DISABLED)
        obj = GeneratorModel()
        #Récuperation de la taille de l'image
        im = PIL.Image.open(self._model.imagePath)
        x, y = im.size
        im.close()
        obj.setSize(x,y)
        obj.generatorKey()
        #voir où l'enregistrer
        img = "tmp_masque.ppm"
        obj.getKey().save(img)
        self._model.keyPath = img
        self._keyVar.set(img)
        self._addImageInCanvas(self._keyCanvas, img, 0)
        messagebox.showinfo("Masque", "La clé a été générer sous: " + os.getcwd() + "/" + img)
        self._cypherButton.config(state=NORMAL)
        self._execute()
    
    def _reset(self):
        if (self._l[0] is not None):
            self._keyCanvas.delete(self._l[0])
            self._keyCanvas.config(scrollregion=(0,0,0,0))
        if (self._l[1] is not None):
            self._imgCanvas.delete(self._l[1])
            self._imgCanvas.config(scrollregion=(0,0,0,0))
        if (self._l[2] is not None):
            self._resultCanvas.delete(self._l[2])
            self._resultCanvas.config(scrollregion=(0,0,0,0))
        self._rslVar.set('')
        self._imgVar.set('')
        self._keyVar.set('')
        self._model.keyPath = None
        self._model.imagePath = None