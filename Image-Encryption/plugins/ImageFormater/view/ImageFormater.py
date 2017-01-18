'''
Created on 18 janv. 2017

@author: havarjos
'''
import tkinter

class ImageFormater(object):
    '''
    La vue du modèle ImageFormaterModel
    '''
    import tkinter
    from ImageFormater.model import ImageFormaterModel as IFM
    from tkinter.filedialog import *
    import tkinter.ttk as ttk
    
    
    def __init__(self, params):
        self.createModel()
        self.createView()
        self.placeComponents()
        self.createController() 
    
    '''
     Afficher la fenêtre.
    '''
    def display(self):
        self.frame.mainloop()
    
    '''
    Création du modèle
    '''        
    def createModel(self):
        self.model = IFM.ImageFormaterModel()
    
    '''
    Création des composants graphiques
    '''
    
    def createView(self):
        self.frame = tkinter.Tk()
        self.frame.title("Formatage d'image")
        self._frame.minsize(600, 400)
        '''self.saveButton = tkinter.Button(self.frame,"Sauvegarder",cmd = self.saveCmd)'''
        self.loadButton = tkinter.Button(self.frame,"Charger",cmd = self.load)
    
    '''
    Création des controlleurs
    '''
    def loadCmd(self):
        image_path = tkinter.filedialog.askopenfilename(title = "Ouvrir une image",
                                                        filetypes = [('ppm files','.ppm')])
        image = tkinter.filedialog.PhotoImage(file = image_path) 
                    