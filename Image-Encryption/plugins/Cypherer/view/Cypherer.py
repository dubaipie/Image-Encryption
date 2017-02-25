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
from tkinter.constants import DISABLED, NORMAL, BOTH
from tkinter.ttk import Progressbar

from PIL import ImageTk

import PIL
import threading

from Utils.AdditionalWidgets import *
from Utils.EventSystem import PropertyChangeListener, ChangeListener
from Utils.ImageViewer import ImageViewer


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
        self._GenFrame = LabelFrame(self, text="Cryptage")
        
        self._KeyFrame = LabelFrame(self._GenFrame, text="Clé*")
        self._frame1 = Frame(self._KeyFrame)
        self._KeyImage = ImageViewer(self._KeyFrame, text="Aperçu de la clé")
        ToolTips(self._KeyFrame, text="*: La clé n'est pas obligatoire lors du cryptage elle sera générer automatiquement")
        self._ImageFrame = LabelFrame(self._GenFrame, text="Image à crypter")
        self._frame2 = Frame(self._ImageFrame)
        self._Image = ImageViewer(self._ImageFrame, text="Aperçu de l'image")
        
        self._ResFrame = LabelFrame(self, text="Résultat")
        self._frame3 = Frame(self._ResFrame)
        self._Result = ImageViewer(self._ResFrame, text="Aperçu du résultat")
        
        self._ProgressFrame = LabelFrame(self, text="Progression")
        
        #les boutons de recherche de fichiers
        self._keyEntry = Entry(self._frame1)
        self._keyEntry.config(state="readonly", textvariable=self._keyVar)
        
        self._imgEntry = Entry(self._frame2)
        self._imgEntry.config(state="readonly", textvariable=self._imgVar)
        
        self._rslEntry = Entry(self._frame3)
        self._rslEntry.config(state="readonly", textvariable=self._rslVar)
        
        #Boutons
        self._keyButton = Button(self._frame1, text="Ouvrir")
        ToolTips(self._keyButton, text="Permet d'indiquer le chemin de la clé qui va servir à crypter")
        self._imgButton = Button(self._frame2, text="Ouvrir")
        ToolTips(self._imgButton, text="Permet d'indiquer le chemin de l'image à crypter")
        self._rslButton = Button(self._frame3, text="Enregistrer sous")
        ToolTips(self._rslButton, text="Permet d'indiquer le chemin où le résultat du cryptage va être sauvegarder")
        self._cypherButton = Button(self._GenFrame, text="Crypter")
        self._resetButton = Button(self._GenFrame, text=("Réintialiser"))
        
        #ProgressBar
        self._progressBar = Progressbar(self._ProgressFrame, variable=self._progressBarValue)
        ToolTips(self._progressBar, text="La progression du Cryptage")
        
        #RadioButton
        self._byCypherButton = Radiobutton(self._GenFrame, text="Crypter", variable=self._byVar, value=False)
        self._byDecyphererButton = Radiobutton(self._GenFrame, text="Décrypter", variable=self._byVar, value=True)
        
        #Label
        self._label = Label(self._frame2, text="Image à Crypter : ")
        
    def _placeComponents(self):
        
        #GenFrame
        self._byCypherButton.grid(row=1, column=1)
        self._byDecyphererButton.grid(row=1, column=2)
        self._KeyFrame.grid(row=2, column=1, sticky=N+W+S+E)
        self._ImageFrame.grid(row=2, column=2, sticky=N+W+S+E)
        self._cypherButton.grid(row=3, column=1)
        self._resetButton.grid(row=3, column=2)
        self._GenFrame.grid(row=1, column=1, sticky=N+W+S+E)
        
        #KeyFrame
        Label(self._frame1, text="Clé : ").grid(row=1, column=1, sticky=W)
        self._keyEntry.grid(row=1, column=2)
        self._keyButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        self._frame1.grid(row=1, column=1)
        self._KeyImage.grid(row=2, column=1, sticky=NW+SE)
        
        #ImageFrame
        self._label.grid(row=1, column=1)
        self._imgEntry.grid(row=1, column=2)
        self._imgButton.grid(row=1, column=3, sticky=E+W, padx=5, pady=5)
        self._frame2.grid(row=1, column=1)
        self._Image.grid(row=2, column=1, sticky=NW+SE)
        
        #ResFrame
        self._rslEntry.grid(row=1, column=1)
        self._rslButton.grid(row=1, column=2, sticky=E+W, padx=5, pady=5)
        self._frame3.grid(row=1, column=1)
        self._Result.grid(row=2, column=1, sticky=NW+SE)
        self._ResFrame.grid(row=1, column=2, sticky=NW+SE)
        
        self._progressBar.pack(fill = BOTH)
        self._ProgressFrame.grid(row=3,column=1, columnspan=2, sticky=W+E+N+S)
        
    def _createController(self):
        self._keyButton.config(command=self._chooseKey)
        self._imgButton.config(command=self._chooseImg)
        self._rslButton.config(command=self._chooseRsl)
        self._cypherButton.config(command=self._cypher)
        self._resetButton.config(command=self._reset)
        self._byCypherButton.config(command=self._hasByVarChanged)
        self._byDecyphererButton.config(command=self._hasByVarChanged)
        
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight=1)
        
        self._GenFrame.grid_rowconfigure(2, weight=1)
        self._GenFrame.grid_columnconfigure(1, weight=1)
        self._GenFrame.grid_columnconfigure(2, weight=1)
        
        self._KeyFrame.grid_rowconfigure(2, weight=1)
        self._KeyFrame.grid_columnconfigure(1, weight=1)
        self._ImageFrame.grid_rowconfigure(2, weight=1)
        self._ImageFrame.grid_columnconfigure(2, weight=1)
        
        self._ResFrame.grid_columnconfigure(1, weight = 1)
        self._ResFrame.grid_rowconfigure(2, weight = 1)
        
        
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
            self._Image.config(text="Aperçu de l'image crypter")
            self._label.config(text="Image à Décrypter : ")
            self._GenFrame.config(text="Décryptage")
            self._ImageFrame.config(text="Image à Décrypter")
            self._KeyFrame.config(text="Clé")
            ToolTips(self._keyButton, text="Permet d'indiquer le chemin de la clé qui va servir à décrypter")
            ToolTips(self._imgButton, text="Permet d'indiquer le chemin de l'image à décrypter")
            ToolTips(self._rslButton, text="Permet d'indiquer le chemin où le résultat du décryptage va être sauvegarder")
            ToolTips(self._progressBar, text="La progression du Décryptage")
            ToolTips(self._KeyFrame, text="Clé servant au décryptage")
        else:
            self._cypherButton.config(command=self._cypher, text='Crypter')
            self._Image.config(text="Aperçu de l'image")
            self._label.config(text="Image à Crypter : ")
            self._GenFrame.config(text="Cryptage")
            self._KeyFrame.config(text="*Clé")
            self._ImageFrame.config(text="Image à Crypter")
            ToolTips(self._keyButton, text="Permet d'indiquer le chemin de la clé qui va servir à crypter")
            ToolTips(self._imgButton, text="Permet d'indiquer le chemin de l'image à crypter")
            ToolTips(self._rslButton, text="Permet d'indiquer le chemin où le résultat du cryptage va être sauvegarder")
            ToolTips(self._progressBar, text="La progression du Cryptage")
            ToolTips(self._KeyFrame, text="*: La clé n'est pas obligatoire lors du cryptage elle sera générer automatiquement")
            
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
            im = PIL.Image.open(self._model.keyPath)
            w,h = im.size
            im.close()
            self._progressBarValue.set(0)
            self._progressBar.config(maximum=w)
            self._model.cypher()
        except MismatchFormatException:
            messagebox.showerror("Taille", "la taille du masque et de l'image ne correspondent pas")

    def _generateKey(self):
        #  Désactivation des boutons
        self.after(0, self._switchButtonsState, DISABLED)

        #  Récuperation de la taille de l'image
        im = PIL.Image.open(self._model.imagePath)
        x, y = im.size
        im.close()

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
        self._KeyImage.addPicture(None)
        self._Image.addPicture(None)
        self._Result.addPicture(None)
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
            self._KeyImage.addPicture(self._model.keyPath)

    def _updateImageCanvas(self, event):
        """
        Mettre à jour le canvas de l'image.
        :param event: l'événement déclencheur
        """
        if self._model.imagePath is not None:
            self._Image.addPicture(self._model.imagePath)

    def _updateResultCanvas(self, event):
        """
        Mettre à jour le canvas du résultat.
        :param event: l'événement déclencheur
        """
        if self._model.resultPath is not None:
            self._Result.addPicture(self._model.resultPath)
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
