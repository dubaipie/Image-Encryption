"""
Contient l'ensemble des classes nécessaires au fonctionnement de ImageViewer.
"""
from tkinter import LabelFrame, Canvas, Scale, Label, Frame
from tkinter import HORIZONTAL, VERTICAL, E, S, W, N, NW

from PIL import ImageTk, Image

from Utils.AdditionalWidgets import AutoScrollbar
from Utils.EventSystem import PropertyChangeListenerSupport, PropertyChangeEvent

class ImageViewer(LabelFrame):
    """
    Composant graphique permettant de visualiser une image.
    """
    DEFAULT_CURSOR = "@../../ressources/pictures/hand.cur"
    GRAB_CURSOR = "@../../ressources/pictures/hand_grab.cur"

    def __init__(self, master=None, **options):
        """
        Constructeur de l'élément graphique. Prend en paramètre le parent (master)
        et les options.
        :param master: le parent
        :param **options: les options de configuration classiques d'une LabelFrame
        """
        super().__init__(master, **options)
        self._createModel()
        self._createView()
        self._placeComponents()
        self._createController()

    @property
    def picture(self):
        """
        Donne l'image (originale) actuellement dans le canvas.
        :return: l'image (instance de Image) dans le canvas
        """
        return self._model.picture

    def addPicture(self, path_or_file):
        """
        Permet d'ajouter une image dans le canvas.
        :param path_or_file: le chemin vers l'image ou une instance de Image.
        """
        self._model.picture = path_or_file

    def _createModel(self):
        self._model = ImageViewerModel()
        self._mousePos = 0, 0

    def _createView(self):
        self._model.canvas = Canvas(self)
        self._model.canvas.config(cursor=ImageViewer.DEFAULT_CURSOR)

        self._toolsFrame = Frame(self)
        self._scaler = Scale(self._toolsFrame, from_=0.1, to=20, resolution=0.1, orient=HORIZONTAL, showvalue=0)
        self._scaler.set(1.0)

        self._hbar = AutoScrollbar(self, orient=HORIZONTAL)
        self._vbar = AutoScrollbar(self, orient=VERTICAL)

    def _placeComponents(self):
        self._model.canvas.grid(row=1, column=1, sticky=N+E+W+S)
        self._hbar.grid(row=2, column=1, sticky=E+W)
        self._vbar.grid(row=1, column=2, sticky=N+S)

        Label(self._toolsFrame, text=" - ").grid(row=1, column=1, sticky=E+W)
        self._scaler.grid(row=1, column=2, columnspan=1, sticky=E+W)
        Label(self._toolsFrame, text=" + ").grid(row=1, column=3, sticky=E+W)

        self._toolsFrame.grid(row=3, column=1, columnspan=2, sticky=E+W)

        self._toolsFrame.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _createController(self):
        self._hbar.config(command=self._model.canvas.xview)
        self._vbar.config(command=self._model.canvas.yview)

        self._model.canvas.config(xscrollcommand=self._hbar.set, yscrollcommand=self._vbar.set)
        self._model.canvas.bind("<B1-Motion>", self._moveCanvasView)
        self._model.canvas.bind("<Button-1>", self._setMousePos)
        self._model.canvas.bind("<ButtonRelease-1>",
                         lambda event: self._model.canvas.config(cursor=ImageViewer.DEFAULT_CURSOR))

        self._scaler.config(command=self._setScale)

    def _setMousePos(self, event):
        self._mousePos = (event.x, event.y)
        self._model.canvas.config(cursor=ImageViewer.GRAB_CURSOR)

    def _moveCanvasView(self, event):
        """
        Méthode appelée lors d'un drag'&'drop.
        :param event: l'événement à l'origine du déclenchement
        """

        delta_x = self._mousePos[0] - event.x
        delta_y = self._mousePos[1] - event.y

        hbar_delta = self._hbar.delta(delta_x, delta_y)
        vbar_delta = self._vbar.delta(delta_x, delta_y)

        hbar_pos = self._hbar.get()[0] + hbar_delta
        vbar_pos = self._vbar.get()[0] + vbar_delta

        self._model.canvas.xview_moveto(hbar_pos)
        self._model.canvas.yview_moveto(vbar_pos)

        self._mousePos = event.x, event.y

    def _setScale(self, s):
        """
        Changer l'échelle du modèle.
        :param s: la nouvelle échelle
        """
        self._model.scale = float(s)


class ImageViewerModel(object):
    """
    Le modèle du composant graphique ImageViewer.
    """

    def __init__(self):
        """
        Constructeur du modèle.
        """
        self._picture = None
        self._canvas = None
        self._propertySupport = PropertyChangeListenerSupport()
        self._isFromCanvas = False
        self._scale = 1.0
        self._currentWidth = 0
        self._currentHeight = 0

    @property
    def width(self):
        """
        La taille du canvas.
        :return: la taille du canvas
        """
        return self.canvas.winfo_reqwidth()

    @property
    def height(self):
        """
        Donne la hauteur du canvas.
        :return: la hauteur de canvas
        """
        return self.canvas.winfo_reqheight()

    @property
    def canvas(self):
        """
        Permet de récupérer le canvas du model.
        :return: le canvas
        """
        return self._canvas

    @canvas.setter
    def canvas(self, canvas):
        """
        Permet de fixer le canvas géré par le modèle.
        """
        self._canvas = canvas
        self._canvas.config(highlightthickness=0)
        self._canvas.bind("<Configure>", self._updateCanvasSize)
        self._scale = 1.0
        self._firePropertyChange("canvas")

    @property
    def picture(self):
        """
        Donne l'image affichée dans le canvas.
        :return: une instance de ImageTk
        """
        return self._picture

    @picture.setter
    def picture(self, path_or_picture=None):
        """
        Permet de fixer l'imagec affichée dans le modèle.
        :param path_or_picture: le chemin vers l'image ou une instance de Image
        """
        self.canvas.delete(self.picture)
        if path_or_picture is None:
            self._picture = None
        elif type(path_or_picture) == Image.Image:
            self._picture = path_or_picture
            self._drawImageIntoCanvas()
        else:
            self._picture = Image.open(path_or_picture)
            self._drawImageIntoCanvas()
        self._firePropertyChange("picture")

    @property
    def scale(self):
        """
        Donne l'échelle actuelle de l'image.
        """
        return self._scale

    @scale.setter
    def scale(self, s):
        """
        Fixe l'échelle de l'image et met à jour le modèle
        :param s: la nouvelle échelle > 0. 1 pour la taille réelle, < 1 pour rétrécir, > 1 pour agrandir
        """
        if s > 0:
            self._scale = s
            if self.picture is not None:
                self._drawImageIntoCanvas()

    def _updateCanvasSize(self, event):
        """
        Permet de rafraîchir l'affichage du canvas.
        :param event: l'événement à l'origine
        """
        if not self._isFromCanvas:
            self.canvas.config(width=event.width, height=event.height)
            self._isFromCanvas = True
            if self.picture is not None:
                x, y = self._computeUpperLeftCorner()
                self.canvas.coords("all", x, y)
        else:
            self._isFromCanvas = False

    def _drawImageIntoCanvas(self):
        """
        Permet de dessiner l'image dans le canvas.
        """
        picture = self._cropPicture()
        x, y = self._computeUpperLeftCorner()
        self._canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, self._currentWidth, self._currentHeight))
        self.canvas.create_image(x, y, image=picture, anchor=NW)
        self.canvas.pic = picture

    def _computeUpperLeftCorner(self):
        """
        Effectue le calcul des coordonnées du point en haut à gauche
        pour que l'image soit centrée.
        :return: x,y les coordonnées du point
        """
        x = 0 if self.width <= self._currentWidth else (self.width - self._currentWidth) / 2
        y = 0 if self.height <= self._currentHeight else (self.height - self._currentHeight) / 2
        return x, y

    def _cropPicture(self):
        """
        Créé une image de type ImageTk à la dimension demandée.
        :return: L'image demandée.
        """
        image = self.picture.copy()
        self._currentWidth = int(image.width * self._scale)
        self._currentHeight = int(image.height * self._scale)
        image = image.transform((self._currentWidth, self._currentHeight),
                                Image.EXTENT, (0, 0, image.width, image.height))
        return ImageTk.PhotoImage(image)

    def _firePropertyChange(self, propname):
        """
        Permet de lancer des propertyChangeEvents
        :param propname: le nom de la propriété
        """
        for l in self._propertySupport.getPropertyChangeListener(propname):
            l.execute(PropertyChangeEvent(self, propname))
