import threading
import PIL
from PIL import ImageTk
from tkinter import filedialog
from tkinter.messagebox import *
from tkinter.filedialog import *
from Generator.model import GeneratorModel

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
        self._keyWidth = 0
        self._keyHeight = 0
    
    def createView(self):
        self._frame1 = Frame(self)
        self._width = Entry(self._frame1, textvariable=self._widthVar, width=5)
        self._height = Entry(self._frame1, textvariable=self._heightVar, width=5)
        self._imgEntry = Entry(self._frame1,textvariable=self._imgVar) 
        
        self._bouton_generer = Button(self, text = "Générer")
        self._bouton_saveas = Button(self, text = "Enregistrer sous")
        self._bouton_setSize1 = Button(self._frame1, text = "Ok")
        self._bouton_setSize2 = Button(self._frame1, text = "Parcourir")
        self._image = Canvas(self)
        
        # horizontal scrollbar
        self._hbar = Scrollbar(self, orient=HORIZONTAL)
         
        # vertical scrollbar
        self._vbar = Scrollbar(self, orient=VERTICAL)
         
        
    def placeComponents(self):    
        label = Label(self._frame1, text = "Taille :")
        label.grid(row = 1, column = 1)

        label = Label(self._frame1, text = " x ")
        label.grid(row = 1, column = 3)

        self._width.grid(row = 1, column = 2)
        self._height.grid(row = 1, column = 4)
        self._bouton_setSize1.grid(row = 1, columnspan = 1 ,column = 5,sticky = W + E)

        label = Label(self._frame1, text = "          ")
        label.grid(row = 1, column = 6)

        label = Label(self._frame1, text = "Choisir une taille à partir d'une image : ")
        label.grid(row = 1, column = 7)

        self._imgEntry.grid(row = 1, column = 8)
        self._bouton_setSize2.grid(row = 1, columnspan = 1, column = 9, sticky = W + E)
        
        self._frame1.grid(row = 1, column = 1, columnspan = 4)
        self._bouton_generer.grid(row = 2, columnspan = 4, column = 1, sticky = W + E)
        
        self._image.grid(row = 3, columnspan = 4, column = 1, padx = 5)
        self._vbar.grid(row=3, column=5, sticky=NW+SE)
        
        self._hbar.grid(row=4, column=1, sticky=NW+SE)
        self._bouton_saveas.grid(row = 5, column = 1, columnspan = 4, sticky = W + E)
        
    def createController(self):
        self._bouton_generer.config(command = self._genererCommand)
        self._bouton_saveas.config(command = self._saveas)
        self._bouton_setSize1.config(command = self._setSizeWithNumber)
        self._bouton_setSize2.config(command = self._setSizeWithImage)
        
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(3, weight = 1)
        
        self._image.configure(
            xscrollcommand=self._hbar.set,
            yscrollcommand=self._vbar.set
        )
        self._hbar.configure(command=self._image.xview)
        self._vbar.configure(command=self._image.yview)
        
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
            w = self._keyWidth
            h = self._keyHeight
            if w < 0 or h < 0 or w % 2 != 0 or h % 2 != 0:
                showerror("Générateur", "Veuillez entrer des entiers pair")
            else:
                self._model.setSize(int (self._width.get()), int (self._height.get()))
                t = threading.Thread(target=self._execute)
                t.start()
        except ValueError:
            showerror("Générateur", "Veuillez entrer des décimaux")
    
    #OUTILS
    def _execute(self):
        self._bouton_generer.config(state=DISABLED)
        self._model.generatorKey()
        '''Gestion de l'affichage de l'image dans le canvas, le canvas prend la taille de l'image '''
        self._model.getKey().save("tmp_image.ppm")
        monimage = "tmp_image.ppm"
        photo = ImageTk.PhotoImage(file = monimage)
        im = PIL.Image.open(monimage)
        x, y = im.size
        im.close()
        self._image.config(width = x, height = y)
        self._image.config(scrollregion=(0,0,x,y))
        self._image.create_image(x / 2, y / 2, image = photo)
        self._image.image = photo
        os.remove("tmp_image.ppm")
        self._bouton_generer.config(state=NORMAL)
          
    def _setSizeWithNumber(self):
        w = int (self._width.get())
        h = int (self._height.get())
        
        if w < 0 or h < 0 or w % 2 != 0 or h % 2 != 0:
            showerror("Générateur", "Veuillez entrer des entiers pair")
        else:
            self._keyWidth = w
            self._keyHeight = h
                   
    def _setSizeWithImage(self):
        dlg = filedialog.askopenfilename(title="Ouvrir", filetypes=[("PPM", "*.ppm")])
        if dlg != "":
            self._imgVar.set(dlg)
            im = PIL.Image.open(dlg) 
            self._keyWidth = int (im.width)
            self._keyHeight = int (im.height)
            im.close()     
            self._widthVar.set(self._keyWidth)
            self._heightVar.set(self._keyHeight)
        
                