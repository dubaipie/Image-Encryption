from PIL import ImageTk

from tkinter import LabelFrame, Radiobutton, Button, Entry, Frame
from tkinter import IntVar, StringVar, BooleanVar
from tkinter import N, E, S, W, BOTH, CENTER, DISABLED, NORMAL
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

from Generator.model.GeneratorModel import GeneratorModel

from Utils.AdditionalWidgets import *
from Utils.EventSystem import PropertyChangeListener, ChangeListener
from Utils.ImageViewer import ImageViewer

class GeneratorView(Frame):
    
    def __init__(self, master=None):
        '''
        Constructeur de la fenêtre.
        '''
        Frame.__init__(self, master)
        self._createModel()
        self._createView()
        self._placeComponents()
        self._createController()
    
    def _createModel(self):
        '''
        Initialisation du model.
        '''
        self._model = GeneratorModel()

        self._byVar = BooleanVar()

        self._widthVar = IntVar()
        self._heightVar = IntVar()

        self._picturePathVar = StringVar()

        self._progressVar = IntVar()
    
    
    def _createView(self):
        self._dataFrame = Frame(self)
        self._genFrame = LabelFrame(self._dataFrame, text="Génération")
        self._propFrame = LabelFrame(self._dataFrame, text="Propriétés")
        self._progressFrame = LabelFrame(self, text="Progression")

        self._byValueButton = Radiobutton(self._genFrame, text="par valeurs", variable=self._byVar, value=True)
        ToolTips(self._byValueButton, text="Entrer une taille manuellement")
        self._byPictureButton = Radiobutton(self._genFrame, text="par image", variable=self._byVar, value=False)
        ToolTips(self._byPictureButton, text="Choisir une taille à partir d'une image")

        self._widthEntry = Entry(self._genFrame, textvariable=self._widthVar, width=10, justify=CENTER, state=DISABLED)
        ToolTips(self._widthEntry, text="Largeur de la clé")
        self._heightEntry = Entry(self._genFrame, textvariable=self._heightVar, width=10, justify=CENTER, state=DISABLED)
        ToolTips(self._heightEntry, text="Hauteur de la clé")

        self._genButton = Button(self._genFrame, text="Générer")
        ToolTips(self._genButton, text="Générer la clé")

        self._loadButton = Button(self._genFrame, text="Charger")
        ToolTips(self._loadButton, text="Choisir l'image dont il faut la taille")
        self._genViewFrame = ImageViewer(self._genFrame, text="Aperçu")

        self._widthLabel = Label(self._propFrame, textvariable=self._widthVar)
        ToolTips(self._widthLabel, text="Largeur de la clé générée")
        self._heightLabel = Label(self._propFrame, textvariable=self._heightVar)
        ToolTips(self._heightLabel, text="Hauteur de la clé générée")

        self._picturePathLabel = Label(self._propFrame, textvariable=self._picturePathVar, wraplength=275)
        ToolTips(self._picturePathLabel, text="L'emplacement de la clé générée")

        self._progressBar = Progressbar(self._progressFrame, variable=self._progressVar)
        ToolTips(self._progressBar, text="La progression de la génération de la clé")

         #Aperçu
        self._viewFrame = ImageViewer(self, text="Aperçu")
        
    def _placeComponents(self):
        self._dataFrame.grid(row=1, column=1, sticky=N+E+W+S, padx=5, pady=5)

        self._genFrame.grid(row=1, column=1, sticky=N+E+W)

        self._byValueButton.grid(row=1, column=1)

        self._widthEntry.grid(row=2, column=2)
        label = Label(self._genFrame, text=" * ")
        label.grid(row=2, column=3)
        self._heightEntry.grid(row=2, column=4)

        self._byPictureButton.grid(row=3, column=1)

        self._loadButton.grid(row=4, column=2, columnspan=2, sticky=E+W)

        self._genViewFrame.grid(row=5, column=1, columnspan=4, sticky=E+W+N+S, padx=5, pady=5)

        self._genButton.grid(row=6, column=2, columnspan=2, sticky=E+W, padx=5, pady=5)


        self._propFrame.grid(row=2, column=1, sticky=N+E+W)

        label = Label(self._propFrame, text="Taille de la clé : ")
        label.grid(row=1, column=1)
        self._widthLabel.grid(row=1, column=2, sticky=W+E)
        label = Label(self._propFrame, text=" * ")
        label.grid(row=1, column=3, sticky=W+E)
        self._heightLabel.grid(row=1, column=4, sticky=W+E)

        label = Label(self._propFrame, text="Chemin vers la clé : ")
        label.grid(row=2, column=1)
        self._picturePathLabel.grid(row=2, column=2, columnspan=3, sticky=W+E)

        
        #Image générée
        self._viewFrame.grid(row=1, column=2, sticky=N+E+W+S, padx=5, pady=5)

        self._progressFrame.grid(row=2, column=1, columnspan=2, sticky=N+E+W+S, padx=5)

        self._progressBar.pack(fill=BOTH, padx=5, pady=5)

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._viewFrame.grid_columnconfigure(1, weight=1)
        self._viewFrame.grid_rowconfigure(1, weight=1)

    def _createController(self):
        self._byPictureButton.config(command=self._hasByVarChanged)
        self._byValueButton.config(command=self._hasByVarChanged)

        self._loadButton.config(command=self._onLoadButtonClick)
        self._genButton.config(command=self._onGenButtonClick)

        self._model.addPropertyChangeListener(PropertyChangeListener(
            propertyName="key",
            target=lambda event: self.after(0, self._savePicture, event)
        ))

        self._model.addChangeListener(ChangeListener(
            target=lambda event: self.after(0, self._updateProgressBarValue, event)
        ))

    # OUTILS
    def _hasByVarChanged(self):
        """
        Méthode appelée lorsque la valeur de la variable self._byVar a changé.
        Permet d'activer / désactiver les éléments de chaque catégorie.
        """
        if self._byVar.get():
            #Désactivation des widgets liés à la sélection par image
            self._loadButton.config(state=DISABLED)
            #Activation de ceux liés à la sélection par valeurs
            self._heightEntry.config(state=NORMAL)
            self._widthEntry.config(state=NORMAL)
        else:
            # Désactivation des widgets liés à la sélection par valeurs
            self._heightEntry.config(state=DISABLED)
            self._widthEntry.config(state=DISABLED)
            # Activation de ceux liés à la sélection par images
            self._loadButton.config(state=NORMAL)

    def _savePicture(self, event):
        """
        Permet l'ouverture d'une boîte de dialogue demandant de choisir un nom de fichier, puis enregistre
        la clé avec ce nom de fichier.
        :raise AttributeError: la clé n'a pas été générée
        """
        try:
            self._model.getKey().save(self._picturePathVar.get())
            self._updateCanvasDisplay()
        except KeyError:
            messagebox.showerror("Sauvegarde", "Sauvegarde échoué veuillez vérifier que le nom du fichier est correct")

    def _validateEntry(self):
        """
        Méthode appelée lorsque l'utilisateur entre des données dans les widgets self._widthEntry et
        self._heightEntry. Permet de contrôler que les valeurs entrées sont des nombres positifs et pairs.
        :return: False si les données sont non conformes, True sinon
        """
        w = int(self._widthVar.get())
        h = int(self._heightVar.get())
        if w <= 0 or h <= 0 or w % 2 != 0 or h % 2 != 0:
            messagebox.showerror("Génération", "Veuillez entrer des entiers pair")
            return False
        return True

    def _onGenButtonClick(self):
        if self._validateEntry():
            self._model.setSize(self._widthVar.get(), self._heightVar.get())
            self._progressVar.set(0)
            self._progressBar.config(maximum=self._heightVar.get()//2)
            refpic = filedialog.asksaveasfilename(title="Enregistrer la clé sous ...", defaultextension=".ppm")
            if len(refpic) > 0:
                self._genButton.config(state=DISABLED)
                self._picturePathVar.set(refpic)
                self._model.generateKey()

    def _updateCanvasDisplay(self):
        """
        Permet de mettre à jour l'image affichée lors de la génération
        d'une nouvelle clé.
        :param event: l'événement à l'origine du rafraichissement
        """
        self._viewFrame.addPicture(self._picturePathVar.get())
        self._genButton.config(state=NORMAL)

    def _updateProgressBarValue(self, event):
        """
        Mettre à jour la valeur de la barre de progression.
        :param event: l'événement déclencheur
        """
        self._progressVar.set(self._progressVar.get() + 1)

    def _onLoadButtonClick(self):
        """
        Lorsque le bouton _loadButton est cliqué, une boite de dialogue s'ouvre et demande
        l'image dont on souhaite avoir les dimensions.
        """
        refpic = filedialog.askopenfilename(filetypes=[("PPM", "*.ppm")], title="Ouvrir une image ...")
        if len(refpic) > 0:
            self._genViewFrame.addPicture(refpic)
            self._widthVar.set(self._genViewFrame.picture.width)
            self._heightVar.set(self._genViewFrame.picture.height)