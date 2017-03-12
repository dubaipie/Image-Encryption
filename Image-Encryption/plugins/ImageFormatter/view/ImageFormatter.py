from tkinter import Entry, Button
from tkinter import StringVar
from tkinter import filedialog, messagebox

from ImageFormatter.model.ImageFormatterModel import *

from Utils.AdditionalWidgets import *
from Utils.EventSystem import PropertyChangeListener
from Utils.ImageViewer import *

class ImageFormatter(Frame):
    FORMATS = [
        ("Joint Photographic Experts Group", ("*.jpg", "*.jpeg")),
        ("Bitmap", "*.bmp"),
        ("Encapsulated PostScript", "*.eps"),
        ("Graphics Interchange Format", "*.gif"),
        ("Portable Network Graphics", "*.png"),
        ("Portable pixmap", ("*.ppm", "*.pgm", "*.pbm")),
        ("All file", "*.*")
    ]

    def __init__(self, master=None):
        """
        Le constructeur de la fenêtre.
        :param master: le parent dans la hiérarchie d'affichage.
        """
        Frame.__init__(self, master)

        self._createModel()
        self._createView()
        self._placeComponents()
        self._createController()

    def _createModel(self):
        """
        Création du modèle associé à la vue.
        """
        self._model = ImageFormatterModel()

        self._originalStrVar = StringVar()
        self._convertedStrVar = StringVar()

    def _createView(self):
        """
        Création des éléments composant la vue.
        """

        self._leftFrame = Frame(self)
        self._dataLabelFrame = LabelFrame(self._leftFrame, text="Données")

        self._originalEntry = Entry(self._dataLabelFrame)
        self._originalEntry.config(state="readonly", textvariable=self._originalStrVar)

        self._convertedEntry = Entry(self._dataLabelFrame)
        self._convertedEntry.config(state="readonly", textvariable=self._convertedStrVar)

        self._originalButton = Button(self._dataLabelFrame, text="Parcourir")
        ToolTips(self._originalButton, text="Chercher l'image à formater")

        self._convertedButton = Button(self._dataLabelFrame, text="Parcourir")
        ToolTips(self._convertedButton, text="Enregistrer l'image formatée sous ...")

        self._convertButton = Button(self._leftFrame, text="Convertir")
        ToolTips(self._convertButton, text="Formater l'image")

        self._pictureView = ImageViewer(self, text="Aperçu")

    def _placeComponents(self):
        """
        Permet de placer les composants dans la vue.
        """
        # -----   leftFrame    ----------
        #
        # ----- dataLabelFrame -----
        Label(self._dataLabelFrame, text="Image originale").grid(row=1, column=1, sticky=E+W)
        self._originalEntry.grid(row=1, column=2, padx=5, sticky=E+W)
        self._originalButton.grid(row=1, column=3, sticky=E+W)

        Label(self._dataLabelFrame, text="Image convertie").grid(row=2, column=1, sticky=E+W)
        self._convertedEntry.grid(row=2, column=2, padx=5, sticky=E+W)
        self._convertedButton.grid(row=2, column=3, sticky=E+W)
        # ------      Fin      -----
        #
        self._dataLabelFrame.grid_columnconfigure(1, weight=1)  # 1/4
        self._dataLabelFrame.grid_columnconfigure(2, weight=2)  # 1/2
        self._dataLabelFrame.grid_columnconfigure(3, weight=1)  # 1/4
        self._dataLabelFrame.grid(row=1, column=1, columnspan=2, ipadx=15, ipady=10, sticky=E+W)
        self._convertButton.grid(row=2, column=2, sticky=E+W)
        # -----       Fin      ----------

        self._leftFrame.grid_columnconfigure(1, weight=1)
        self._leftFrame.grid_columnconfigure(2, weight=1)
        self._leftFrame.grid(row=1, column=1, sticky=E+W+N, padx=10, pady=10)

        # -----   rightFrame   ----------
        self._pictureView.grid(row=1, column=2, sticky=N+E+W+S, padx=10, pady=10)
        # -----       Fin      ----------

        # Distribution de l'espace restant dans la frame principale
        self.grid_columnconfigure(1, weight=1, minsize=400)  # 1/3 pour la partie gauche
        self.grid_columnconfigure(2, weight=2)  # 2/3 pour la partie droite
        self.grid_rowconfigure(1, weight=1)  # la totalité

    def _createController(self):
        """
        Création des contrôleurs de la vue et du model.
        """
        self._originalButton.config(command=self._onOriginalButtonClick)
        self._convertedButton.config(command=self._onConvertedButtonClick)
        self._convertButton.config(command=self._onConvertButtonClick)

        self._model.addPropertyChangeListener(PropertyChangeListener(
            propertyName="convertedPicture",
            target = lambda event: self.after(0, self._pictureView.addPicture(self._model.convertedPicture))
        ))

        self._model.addPropertyChangeListener(PropertyChangeListener(
            propertyName="convertedPicture",
            target=lambda event: self._model.convertedPicture.save(self._convertedStrVar.get())
        ))

    def _onOriginalButtonClick(self):
        """
        Action déclenchée lors du clic sur le bouton originalButton
        """
        dlg = filedialog.askopenfilename(filetypes=ImageFormatter.FORMATS)

        if dlg != "":
            try:
                self._model.originalPicture = dlg
                self._originalStrVar.set(dlg)
            except NoImageToConvert:
                messagebox.showerror("Erreur",
                                     "Entrez un chemin vers une image valide")
            except IOError:
                messagebox.showerror("Erreur",
                                     "Erreur lors de l'ouverture de l'image")

    def _onConvertedButtonClick(self):
        """
        Action déclenchée lors du clic sur le bouton convertedButton
        """
        dlg = filedialog.asksaveasfilename(defaultextension=".ppm", filetypes=[("PPM", "*.ppm")])

        if dlg != "":
            self._convertedStrVar.set(dlg)

    def _onConvertButtonClick(self):
        """
        Action effectuée lors du clic sur le bouton convertButton
        """
        if self._model.originalPicture is not None and self._convertedStrVar is not None:
            self._model.convert()
