'''
Created on 18 janv. 2017

@author: havarjos
'''
from tkinter import Frame, Entry, Label, Canvas, Button, Scrollbar, LabelFrame
from tkinter import StringVar, HORIZONTAL, VERTICAL
from tkinter import filedialog, messagebox
from PIL import ImageTk
from ImageFormater.model.ImageFormaterModel import *


class ImageFormater(Frame):
    '''
    La vue du modèle ImageFormaterModel
    '''  
    
    """
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createModel()
        self.createView()
        'self.placeComponents()'
        #self.creteController() 
    
    
    '''
    Création du modèle
    '''        
    def createModel(self):
        self._model = IFM.ImageFormaterModel()
    
    '''
    Création des composants graphiques
    '''
    
    def createView(self):
        #self.saveButton = tkinter.Button(self,"Sauvegarder",command = self._saveCmd)
        #self._loadButton = tkinter.Button(self,text= "Charger",command = self._loadCmd)
        #self._loadButton.pack()
        #self._canvas = tkinter.Canvas(self,width = 500,height = 500, bg = 'blue')
        #self._canvas.pack()
        #self._resolutionButton(self,"Changer la résolution",command = self._changeResolution)
        pass
    
    '''
    Création des controlleurs
    '''
    def _loadCmd(self):
        
        picture_path = tkinter.filedialog.askopenfilename(title = "Ouvrir une image",
                                                            filetypes = [('gif files','.gif'),('ppm files','.ppm')])
        picture = tkinter.filedialog.PhotoImage(file = picture_path) 
        self._canvas.create_image(0,0,anchor = CENTER,image = picture )
        self._canvas.image = picture
        self._canvas.pack()
        self._model.changeImageToConvert(picture_path)
    
    def _saveCmd(self):
        picture_path = tkinter.filedialog.askopenfilename(title = "Enregistrer sous",
                                                            filetypes = [('gif files','.gif'),('ppm files','.ppm')])
        picture = tkinter.filedialog.PhotoImage(file = picture_path)
        self._model.saveImageConvert(picture)
    
    def _changeResolution(self):
        if self._model.getImageToConvert() == None:
            messagebox.showerror("Erreur","Impossible de trouver l'image à convertir")
        else:
            self._model.upImageResolution()    
            
    """
    FORMATS = (
        ("Bitmap", "*.bmp"),
        ("Encapsulated PostScript", "*.eps"),
        ("Graphics Interchange Format", "*.gif"),
        ("Joint Photographic Experts Group", ("*.jpg", "*.jpeg")),
        ("Portable Network Graphics", "*.png"),
        ("Portable pixmap", ("*.ppm", "*.pgm", "*.pbm")),
        ("All file", "*.*")
    )

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
        self._originalEntry = Entry(self)
        self._originalEntry.config(state="readonly", textvariable=self._originalStrVar)

        self._convertedEntry = Entry(self)
        self._convertedEntry.config(state="readonly", textvariable=self._convertedStrVar)

        self._originalButton = Button(self, text="Parcourir")
        self._convertedButton = Button(self, text="Parcourir")

        self._canvas = Canvas(self)

        self._convertButton = Button(self, text="Convertir")

        self._hbar = Scrollbar(self, orient=HORIZONTAL)
        self._vbar = Scrollbar(self, orient=VERTICAL)

    def _placeComponents(self):
        """
        Permet de placer les composants dans la vue.
        """
        Label(self, text="Image originale").grid(row=1, column=1)
        self._originalEntry.grid(row=1, column=2)
        self._originalButton.grid(row=1, column=3)

        Label(self, text="Image convertie").grid(row=2, column=1)
        self._convertedEntry.grid(row=2, column=2)
        self._convertedButton.grid(row=2, column=3)

        self._convertButton.grid(row=3, column=2, columnspan=2)

        self._canvas.grid(row=1, rowspan=3, column=4)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def _createController(self):
        """
        Création des contrôleurs de la vue et du model.
        """
        self._originalButton.config(command=self._onOriginalButtonClick)
        self._convertedButton.config(command=self._onConvertedButtonClick)
        self._convertButton.config(command=self._onConvertButtonClick)

        self._canvas.config(xscrollcommand=self._hbar, yscrollcommand=self._vbar)
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
                                     "Erreur lors de l'ouerture de l'image")

    def _onConvertedButtonClick(self):
        """
        Action déclenchée lors du clic sur le bouton convertedButton
        """
        dlg = filedialog.asksaveasfilename(defaultextension=".ppm")

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
