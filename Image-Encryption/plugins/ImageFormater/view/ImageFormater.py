'''
Created on 18 janv. 2017

@author: havarjos
'''
from tkinter import Frame, Entry, Label, Canvas, Button, Scrollbar, LabelFrame
from tkinter import StringVar, HORIZONTAL, VERTICAL, E, W, N, S
from tkinter import filedialog, messagebox
from PIL import ImageTk
from ImageFormater.model.ImageFormaterModel import *


class ImageFormater(Frame):
    FORMATS = [
        ("Bitmap", "*.bmp"),
        ("Encapsulated PostScript", "*.eps"),
        ("Graphics Interchange Format", "*.gif"),
        ("Joint Photographic Experts Group", ("*.jpg", "*.jpeg")),
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
        self._model = ImageFormaterModel()

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
        self._convertedButton = Button(self._dataLabelFrame, text="Parcourir")

        self._convertButton = Button(self._leftFrame, text="Convertir")

        self._rightFrame = Frame(self)
        self._canvasLabelFrame = LabelFrame(self._rightFrame, text="Aperçu")
        self._canvas = Canvas(self._canvasLabelFrame)

        self._hbar = Scrollbar(self._canvasLabelFrame, orient=HORIZONTAL)
        self._vbar = Scrollbar(self._canvasLabelFrame, orient=VERTICAL)

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
        #
        # ---- canvasLabelFrame ----
        self._canvas.grid(row=1, column=1)
        self._hbar.grid(row=2, column=1, sticky=E+W)
        self._vbar.grid(row=1, column=2, sticky=N+S)
        # ----       Fin        ----
        #
        self._canvasLabelFrame.grid_columnconfigure(1, weight=1)
        self._canvasLabelFrame.grid_rowconfigure(1, weight=1)
        self._canvasLabelFrame.grid(row=1, column=1, sticky=N+E+W+S)
        # -----       Fin      ----------
        self._rightFrame.grid_columnconfigure(1, weight=1)
        self._rightFrame.grid_rowconfigure(1, weight=1)
        self._rightFrame.grid(row=1, column=2, sticky=N+S+E+W, padx=10, pady=10)

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

        self._canvas.config(xscrollcommand=self._hbar.set, yscrollcommand=self._vbar.set)
        self._hbar.config(command=self._canvas.xview)
        self._vbar.config(command=self._canvas.yview)

    def _onOriginalButtonClick(self):
        """
        Action déclenchée lors du clic sur le bouton originalButton
        """
        dlg = filedialog.askopenfilename(filetypes=ImageFormater.FORMATS)

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
            picture = self._model.convertedPicture
            picture.save(self._convertedStrVar.get())
            picture = ImageTk.PhotoImage(picture)
            w, h = picture.width(), picture.height()
            self._canvas.config(width=w,
                                height=h,
                                scrollregion=(0, 0, w, h))
            self._canvas.create_image(w / 2, h / 2, image=picture)
            self._canvas.picture = picture
