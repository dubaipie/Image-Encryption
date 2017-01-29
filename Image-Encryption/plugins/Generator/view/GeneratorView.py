from tkinter import *
from PIL import Image
'''Ajouter l'importation ImageTk à PIL'''
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
        
        self._bouton_generer = Button(self, text=_("Generate"))
        self._bouton_saveas = Button(self, text=_("Save as ..."))
        self._image = Canvas(self, bg='ivory')
        
    def placeComponents(self):    
        label = Label(self._frame1, text=_("Size :"))
        label.grid(row = 1, column = 1)
        label = Label(self._frame1, text = _(" x "))
        label.grid(row = 1, column = 3)
        self._width.grid(row = 1, column = 2)
        self._height.grid(row = 1, column = 4)
        
        self._frame1.grid(row = 1, column = 1, columnspan = 4)
        
        self._image.grid(row = 3, columnspan = 4, column = 1, sticky = W + E + N + S, padx = 5)
        self._bouton_generer.grid(row = 2, columnspan = 4, column = 1, sticky = W + E)
        self._bouton_saveas.grid(row = 4, column = 1, columnspan = 4, sticky = W + E)
        
    def createController(self):
        self._bouton_generer.config(command = self._genererCommand)
        self._bouton_saveas.config(command = self._saveas)
        
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(3, weight = 1)
    
    def _saveas(self):
        repfic = asksaveasfilename(title=_("Save as"), defaultextension=".ppm")
        if len(repfic) > 0:
            try:
                self._model.getKey().save(repfic)
            except AttributeError:
                showerror(_("Saving Error"), _("Please generate a key before saving"))
            except KeyError:
                showerror(_("Saving Error"), _("Saving failed, please check your file name"))
        
    def _genererCommand(self):
        try:
            w = int (self._width.get())
            h = int (self._height.get())
            if w < 0 or h < 0 or w % 2 != 0 or h % 2 != 0:
                showerror(_("Generator"), _("Please type even values"))
            else:
                self._model.setSize(int (self._width.get()), int (self._height.get()))
                self._model.generatorKey()
        except ValueError:
            showerror(_("Generator"), _("Please type integer values"))
        '''
         Insertion de l'image après génération besoin de ImageTk à modifier
        
        self._model.getKey().save("tmp_image")
        monimage = Image.open("tmp_image")
        photo = ImageTk.PhotoImage(monimage) 
        self._image.create_image(85, 85, image = photo)
        os.remove('tmp_image')
        '''