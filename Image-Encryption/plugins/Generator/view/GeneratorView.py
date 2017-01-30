from PIL import Image
import PIL
from PIL import ImageTk
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
    
    def createView(self):
        self._frame1 = Frame(self)
        self._width = Entry(self._frame1, textvariable="", width=5)
        self._height = Entry(self._frame1, textvariable="", width=5)
        
        self._bouton_generer = Button(self, text = "Générer")
        self._bouton_saveas = Button(self, text = "Enregistrer sous")
        self._image = Canvas(self, bg='ivory')
        
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
        
        self._frame1.grid(row = 1, column = 1, columnspan = 4)
        self._bouton_generer.grid(row = 2, columnspan = 4, column = 1, sticky = W + E)
        
        self._image.grid(row = 3, columnspan = 4, column = 1, padx = 5)
        self._vbar.grid(row=3, column=5, sticky=NW+SE)
        
        self._hbar.grid(row=4, column=1, sticky=NW+SE)
        self._bouton_saveas.grid(row = 5, column = 1, columnspan = 4, sticky = W + E)
        
    def createController(self):
        self._bouton_generer.config(command = self._genererCommand)
        self._bouton_saveas.config(command = self._saveas)
        
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
            w = int (self._width.get())
            h = int (self._height.get())
            if w < 0 or h < 0 or w % 2 != 0 or h % 2 != 0:
                showerror("Générateur", "Veuillez entrer des entiers pair")
            else:
                self._model.setSize(int (self._width.get()), int (self._height.get()))
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
        except ValueError:
            showerror("Générateur", "Veuillez entrer des décimaux")