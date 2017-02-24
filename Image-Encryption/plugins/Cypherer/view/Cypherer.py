'''
Created on 18 janv. 2017

@author: dubaipie
'''

import Cypherer.model.CyphererModel as DM
from Generator.model.GeneratorModel import GeneratorModel
from Cypherer.model.CyphererModel import MismatchFormatException

from tkinter import Entry, Button, StringVar, Frame, Canvas, LabelFrame,\
    IntVar, BooleanVar
from tkinter import filedialog, messagebox, Radiobutton
from tkinter import W, E, HORIZONTAL, VERTICAL, N, S, NW, SE
from tkinter.constants import DISABLED, NORMAL
from tkinter.ttk import Progressbar

from PIL import ImageTk

import threading

from Utils.AdditionalWidgets import *
from Utils.EventSystem import PropertyChangeListener, ChangeListener


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
        self._byVar = BooleanVar()
        self._progressBarValue= IntVar()

    def _createView(self):
        # fixme: add tooltips
        #Frame
        self._frame = Frame(self)
        self._frame0 = Frame(self._frame)
        self._frame1 = Frame(self._frame)
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
        self._keyButton = Button(self._frame1, text="Find")
        self._imgButton = Button(self._frame2, text="Find")
        self._rslButton = Button(self._frame3, text="Save as")
        self._cypherButton = Button(self, text="Cypher")
        self._resetButton = Button(self._frame3, text=("Reset"))
        
        #Canvas
        self._resultCanvas = Canvas(self._frame6) # fixme: use ImageViewer instance instead
        self._keyCanvas = Canvas(self._frame4)  # fixme: use ImageViewer instance instead
        self._imgCanvas = Canvas(self._frame5)  # fixme: use ImageViewer instance instead
        
        # horizontal AutoScrollbar
        self._hbar = AutoScrollbar(self._frame4, orient=HORIZONTAL)
        self._hbar2 = AutoScrollbar(self._frame5, orient=HORIZONTAL)
        self._hbar3 = AutoScrollbar(self._frame6, orient=HORIZONTAL)
        
        # vertical AutoScrollbar
        self._vbar = AutoScrollbar(self._frame4, orient=VERTICAL)
        self._vbar2 = AutoScrollbar(self._frame5, orient=VERTICAL)
        self._vbar3 = AutoScrollbar(self._frame6, orient=VERTICAL)
        
        #ProgressBar
        self._progressBar = Progressbar(self, variable=self._progressBarValue)
        
        #RadioButton
        self._byCypherButton = Radiobutton(self._frame0, text="crypter", variable=self._byVar, value=False)
        self._byDecyphererButton = Radiobutton(self._frame0, text="décrypter", variable=self._byVar, value=True)
        
        #Label
        self._label = Label(self._frame2, text="Image à Crypter : ")
        
    def _placeComponents(self):
        #FRAME
        self._frame.grid(row=1, column=1)
        
        #FRAME0
        self._byCypherButton.grid(row=1, column=1, sticky=E+W)
        self._byDecyphererButton.grid(row=2, column=1)
        self._frame0.grid(row=1, column=1,  sticky=E+W)
        
        #FRAME1
        Label(self._frame1, text="Clé : ").grid(row=1, column=1, sticky=W)
        self._keyEntry.grid(row=1, column=2)
        self._keyButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        self._frame1.grid(row=1, column=2)
        
        #FRAME4
        self._keyCanvas.grid(row = 1, column = 1, sticky=NW+SE)
        self._hbar.grid(row=2, column=1, sticky=W+E)
        self._vbar.grid(row=1, column=2, sticky=N+S)
        self._frame4.grid(row=2, column=1, sticky=NW+SE)
        
        #FRAME2
        self._label.grid(row=1, column=1, sticky=W)
        self._imgEntry.grid(row=1, column=2)
        self._imgButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        self._frame2.grid(row=1, column=2)
                
        #FRAME5
        self._imgCanvas.grid(row = 1, column = 1, sticky=NW+SE)
        self._hbar2.grid(row=2, column=1, sticky=W+E)
        self._vbar2.grid(row=1, column=2, sticky=N+S)
        self._frame5.grid(row=2, column=2, sticky=NW+SE)
        
        #FRAME3
        Label(self._frame3, text="Chemin de retour : ").grid(row=1, column=1, sticky=W)
        self._rslEntry.grid(row=1, column=2)
        self._rslButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        self._resetButton.grid(row=1, column=4)
        self._frame3.grid(row=1, column=3)
        
        #FRAME6
        self._resultCanvas.grid(row = 1, column = 1, sticky=NW+SE)
        self._hbar3.grid(row=2, column=1, sticky=W+E)
        self._vbar3.grid(row=1, column=2, sticky=N+S)
        self._frame6.grid(row=2, column=3, sticky=NW+SE)
        
        self._cypherButton.grid(row=4, column=1, columnspan=3, sticky=E+W)
        self._progressBar.grid(row=3, column=1, columnspan=3, sticky=E+W)

    def _createController(self):
        self._keyButton.config(command=self._chooseKey)
        self._imgButton.config(command=self._chooseImg)
        self._rslButton.config(command=self._chooseRsl)
        self._cypherButton.config(command=self._cypher)
        self._resetButton.config(command=self._reset)
        self._byCypherButton.config(command=self._hasByVarChanged)
        self._byDecyphererButton.config(command=self._hasByVarChanged)
        
        self.grid_rowconfigure(2, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_columnconfigure(3, weight = 1)
        
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

        self._model.addPropertyChangeListener(PropertyChangeListener(
            "resultUpdated",
            lambda event: self.after(0, self._updateResultCanvas, event)
        ))

        self._model.addPropertyChangeListener(PropertyChangeListener(
            "keyPath",
            lambda event: self.after(0, self._updateKeyCanvas, event)
        ))

        self._model.addPropertyChangeListener(PropertyChangeListener(
            "imagePath",
            lambda event: self.after(0, self._updateImageCanvas, event)
        ))
        
        self._model.addChangeListener(ChangeListener(
            target=lambda event: self.after(0, self._updateProgressBarValue, event)
        ))

    def _chooseKey(self):
        dlg = filedialog.askopenfilename(title="Ouvrir", filetypes=[("PPM", "*.ppm")])
        
        if len(dlg) > 0:
            self._model.keyPath = dlg
            self._keyVar.set(dlg)
            
    def _chooseImg(self):
        dlg = filedialog.askopenfilename(title="Ouvrir", filetypes=[("PPM", "*.ppm")] )
    
        if len(dlg) > 0:
            self._model.imagePath = dlg
            self._imgVar.set(dlg)
    
    def _chooseRsl(self):
        dlg = filedialog.asksaveasfilename(title="Enregistrer sous", defaultextension=".ppm") 

        if len(dlg) > 0:
            self._model.resultPath = dlg
            self._rslVar.set(dlg)
    
    def _hasByVarChanged(self):
        self._reset()
        if self._byVar.get():
            self._cypherButton.config(command=self._decypher, text='Décrypter')
            self._frame5.config(text="Aperçu de l'image crypter")
            self._label.config(text="Image à Décrypter : ")
        else:
            self._cypherButton.config(command=self._cypher, text='crypter')
            self._frame5.config(text="Aperçu de l'image")
            self._label.config(text="Image à Crypter : ")
    
    def _decypher(self):
        if self._model.imagePath is None or self._model.keyPath is None or self._rslVar.get() == '':
            messagebox.showerror("Data error", "Please fill all inputs")
        else:
            self._execute()
            
    def _cypher(self):
        if self._model.imagePath is None or self._rslVar.get() == '':
            messagebox.showerror("Data error", "Please fill all inputs")
            return
        if self._model.keyPath is None:
            thread = threading.Thread(target=self._generateKey)
            thread.start()
        else :
            self._execute()
    
    def _execute(self):
        self._switchButtonsState(DISABLED)
        try :
            im = self._imgCanvas.picture
            w = im.width()
            self._progressBarValue.set(0)
            self._progressBar.config(maximum=w)
            self._model.cypher()
        except MismatchFormatException:
            messagebox.showerror("Taille", "la taille du masque et de l'image ne correspondent pas")
            
    def _addImageInCanvas(self, canvas, img, i):
        """Ajoute une image dans un canvas """
        canvas.picture = ImageTk.PhotoImage(file=img)
        x, y = canvas.picture.width(), canvas.picture.height()
        self._l[i] = canvas.create_image(x/2, y/2, image=canvas.picture)
        canvas.config(scrollregion=(0,0,x,y))

    def _generateKey(self):
        #  Désactivation des boutons
        self.after(0, self._switchButtonsState, DISABLED)

        #  Récuperation de la taille de l'image
        im = self._imgCanvas.picture
        x, y = im.width(), im.height()

        #  Configuration de la barre de progression
        self._progressBarValue.set(0)
        self._progressBar.config(maximum=y)

        #  Génération de la clé
        obj = GeneratorModel()
        obj.addChangeListener(ChangeListener(
            target=lambda event: self.after(0, self._updateProgressBarValue, event)
        ))
        obj.setSize(x,y)
        obj.generateKey()

        #  Enregistrement de la clé générée
        dlg = filedialog.asksaveasfilename(title="Choisir un emplacement pour la clé",
                                           defaultextension=".ppm")

        if len(dlg) > 0:
            obj.getKey().save(dlg)
            self._model.keyPath = dlg
            self._keyVar.set(dlg)
            #  Poursuite de l'exécution
            self._execute()
    
    def _reset(self):
        """ Réintialise le model et les canvas """
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
        self._model.reset()
        self._progressBarValue.set(0)

    def _updateKeyCanvas(self, event):
        """
        Mettre à jour le canvas de la clé
        :param event: l'événement déclencheur.
        """
        if self._model.keyPath is not None:
            self._addImageInCanvas(self._keyCanvas, self._model.keyPath, 0)

    def _updateImageCanvas(self, event):
        """
        Mettre à jour le canvas de l'image.
        :param event: l'événement déclencheur
        """
        if self._model.imagePath is not None:
            self._addImageInCanvas(self._imgCanvas, self._model.imagePath, 1)

    def _updateResultCanvas(self, event):
        """
        Mettre à jour le canvas du résultat.
        :param event: l'événement déclencheur
        """
        if self._model.resultPath is not None:
            self._addImageInCanvas(self._resultCanvas, self._model.resultPath, 2)
        self._switchButtonsState(NORMAL)

    def _switchButtonsState(self, state):
        """
        Permet de désactiver ou d'activer tous les boutons.
        :param state: l'état des boutons
        """
        self._cypherButton.config(state=state)
        self._imgButton.config(state=state)
        self._keyButton.config(state=state)
        self._rslButton.config(state=state)
        self._resetButton.config(state=state)
        self._byCypherButton.config(state=state)
        self._byDecyphererButton.config(state=state)
        
    def _updateProgressBarValue(self, event):
        """
        Mettre à jour la valeur de la barre de progression.
        :param event: l'événement à l'origine de la mise à jour
        """
        self._progressBarValue.set(self._progressBarValue.get() + 1)
