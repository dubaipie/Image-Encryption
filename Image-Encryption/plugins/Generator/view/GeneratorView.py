import PIL
from PIL import ImageTk

from tkinter import filedialog
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import Progressbar

from Generator.model import GeneratorModel
from Utils.AdditionalWidgets import *
from Utils.EventSystem import PropertyChangeListener, ChangeListener

class GeneratorView(Frame):
    
    def __init__(self, master=None):
        '''
        Constructeur de la fenêtre.
        '''
        Frame.__init__(self, master)
        self.createModel()
        self.createView()
        self.placeComponents()
        self.createController()
    
    def createModel(self):
        '''
        Initialisation du model.
        '''
        self._model = GeneratorModel.GeneratorModel()
        
        self._imgVar = StringVar()
        self._widthVar = StringVar()
        self._heightVar = StringVar()
        self._progressBarValue= IntVar()
    
    def createView(self):
        self._frame1 = Frame(self)
        self._width = Entry(self._frame1, textvariable=self._widthVar, width=5)
        self._height = Entry(self._frame1, textvariable=self._heightVar, width=5)
        self._imgEntry = Entry(self._frame1,textvariable=self._imgVar) 
        
        self._bouton_generer = Button(self, text = "Générer")
        self._bouton_saveas = Button(self, text = "Enregistrer sous")
        self._bouton_setSize2 = Button(self._frame1, text = "Parcourir")
        self._progressBar = Progressbar(self, variable=self._progressBarValue)
        self._image = Canvas(self)
        
        # horizontal AutoScrollbar
        self._hbar = AutoScrollbar(self, orient=HORIZONTAL)
         
        # vertical AutoScrollbar
        self._vbar = AutoScrollbar(self, orient=VERTICAL)
         
        
    def placeComponents(self):    
        label = Label(self._frame1, text = "Taille :")
        label.grid(row = 1, column = 1)

        label = Label(self._frame1, text = " x ")
        label.grid(row = 1, column = 3)

        self._width.grid(row = 1, column = 2)
        self._height.grid(row = 1, column = 4)

        label = Label(self._frame1, text = "          ")
        label.grid(row = 1, column = 6)

        label = Label(self._frame1, text = "Choisir une taille à partir d'une image : ")
        label.grid(row = 1, column = 7)

        self._imgEntry.grid(row = 1, column = 8)
        self._bouton_setSize2.grid(row = 1, columnspan = 1, column = 9, sticky = W + E)

        self._progressBar.grid(row=5, column=1, columnspan=4, sticky=W+E)
        
        self._frame1.grid(row = 1, column = 1, columnspan = 4)
        self._bouton_generer.grid(row = 2, columnspan = 4, column = 1, sticky = W + E)
        
        self._image.grid(row = 3, columnspan = 4, column = 1, padx = 5)
        self._vbar.grid(row=3, column=5, sticky=NW+SE)
        
        self._hbar.grid(row=4, column=1, sticky=NW+SE)
        self._bouton_saveas.grid(row = 6, column = 1, columnspan = 4, sticky = W + E)
        
    def createController(self):
        self._bouton_generer.config(command = self._genererCommand)
        self._bouton_saveas.config(command = self._saveas)
        self._bouton_setSize2.config(command = self._setSizeWithImage)
        
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(3, weight = 1)
        
        self._image.configure(
            xscrollcommand=self._hbar.set,
            yscrollcommand=self._vbar.set
        )
        self._hbar.configure(command=self._image.xview)
        self._vbar.configure(command=self._image.yview)

        self._model.addPropertyChangeListener(PropertyChangeListener(
            propertyName="key",
            target=lambda event: self.after(0, self._updateCanvasDisplay, event)
        ))

        self._model.addChangeListener(ChangeListener(
            target=lambda event: self.after(0, self._updateProgressBarValue, event)
        ))
        
    def _saveas(self):
        repfic = asksaveasfilename(title="Enregistrer sous", defaultextension=".ppm") 
        if len(repfic) > 0:
            try:
                self._model.getKey().save(repfic)
                showinfo("Sauvegarde", "La clé à été enregistrée sous :" + repfic)
            except AttributeError:
                showerror("Sauvegarde", "Veuillez générer une clé avant de sauvegarder")
            except KeyError:
                showerror("Sauvegarde", "Sauvegarde échoué veuillez vérifier que le nom du fichier est correct")
        
    def _genererCommand(self):
        try:
            w = int (self._widthVar.get())
            h = int (self._heightVar.get())
            if w < 0 or h < 0 or w % 2 != 0 or h % 2 != 0:
                showerror("Générateur", "Veuillez entrer des entiers pair")
            else:
                self._model.setSize(w, h)
                self._progressBarValue.set(0)
                self._progressBar.config(maximum=h)
                self._bouton_generer.config(state=DISABLED)
                self._model.generatorKey()
        except ValueError:
            showerror("Générateur", "Veuillez entrer des décimaux")
            
    
    #OUTILS
    def _updateCanvasDisplay(self, event):
        """
        Permet de mettre à jour l'image affichée lors de la génération
        d'une nouvelle clé.
        :param event: l'événement à l'origine du rafraichissement
        """
        self._model.getKey().save("tmp_image.ppm")
        monimage = "tmp_image.ppm"
        photo = ImageTk.PhotoImage(file=monimage)
        im = PIL.Image.open(monimage)
        x, y = im.size
        im.close()
        self._image.config(width=x, height=y)
        self._image.config(scrollregion=(0, 0, x, y))
        self._image.create_image(x / 2, y / 2, image=photo)
        self._image.image = photo
        os.remove("tmp_image.ppm")
        self._bouton_generer.config(state=NORMAL)

    def _updateProgressBarValue(self, event):
        """
        Mettre à jour la valeur de la barre de progression.
        :param event: l'événement déclencheur
        """
        self._progressBarValue.set(self._progressBarValue.get() + 1)
                   
    def _setSizeWithImage(self):
        dlg = filedialog.askopenfilename(title="Ouvrir", filetypes=[("PPM", "*.ppm")])
        if dlg != "":
            self._imgVar.set(dlg)
            self._model.setSizeImage(dlg)
            w,h = self._model.getSize() 
            self._widthVar.set(w)
            self._heightVar.set(h)
