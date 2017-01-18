from tkinter import *
from PIL import Image
'''Ajouter l'importation ImageTk à PIL'''
from tkinter.messagebox import *
from tkinter.filedialog import *
from Generator.model import GeneratorModel

class GeneratorView(object):
    def __init__(self):
        '''
        Constructeur de la fenêtre.
        '''
        self.createModel()
        self.createView()
        self.placeComponents()
        self.createController()
        
    def display(self):
        '''
        Afficher la fenêtre.
        '''
        self._frame.mainloop()
    
    def createModel(self):
        '''
        Initialisation du model.
        '''
        self._model = GeneratorModel.GeneratorModel()
    
    def createView(self):
        self._frame = Tk()
        self._width = Entry(self._frame, textvariable="", width=5)
        self._height = Entry(self._frame, textvariable="", width=5)
        self._bouton_generer = Button(self._frame, text = "Générer")
        self._bouton_saveas = Button(self._frame, text = "Enregistrer sous :")
        self._image = Canvas(self._frame, width=250, height=50, bg='ivory')
        
    def placeComponents(self):
        label = Label(self._frame, text = "Taille :")
        label.grid(row = 1, column = 1)
        
        self._width.grid(row = 1, column = 2)
        
        label = Label(self._frame, text = " x ")
        label.grid(row = 1, column = 3)
        self._height.grid(row = 1, column = 4)
        
        self._image.grid(row = 3, columnspan = 4, column = 1)
        self._bouton_generer.grid(row = 2, column = 2)
        
        self._bouton_saveas.grid(row = 4, column = 2)
        
        
    def createController(self):
        self._bouton_generer.config(command = self._genererCommand)
        self._bouton_saveas.config(command = self._saveas)
    
    def _saveas(self):
        repfic = asksaveasfilename(title="Enregistrer sous", defaultextension=".ppm") 
        if len(repfic) > 0:
            try:
                self._model.getKey().save(repfic)
            except AttributeError:
                showerror("Sauvegarde", "Veuillez générer une clé avant de sauvegarder")
            except KeyError:
                showerror("Sauvegarde", "Sauvegarde échoué veuillez vérifier que le nom du fichier est correct")
        
    def _genererCommand(self):
        try:
            w = int (self._width.get())
            h = int (self._height.get())
            if w < 0 or h < 0:
                showerror("Générateur", "Veuillez entrer des entiers > 0")
            else:
                self._model.setSize(int (self._width.get()), int (self._height.get()))
                self._model.generatorKey()
        except ValueError:
            showerror("Générateur", "Veuillez entrer des décimaux")
        '''
         Insertion de l'image après génération besoin de ImageTk à modifier
        
        self._model.getKey().save("tmp_image")
        monimage = Image.open("tmp_image")
        photo = ImageTk.PhotoImage(monimage) 
        self._image.create_image(85, 85, image = photo)
        os.remove('tmp_image')
        '''             
                    
if __name__ == "__main__":
    app = GeneratorView()
    app.display()