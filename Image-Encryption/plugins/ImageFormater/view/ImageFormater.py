'''
Created on 18 janv. 2017

@author: havarjos
'''
import tkinter
import ImageFormater.model.ImageFormaterModel as IFM
from tkinter.filedialog import *
import tkinter.ttk as ttk

class ImageFormater(Frame):
    '''
    La vue du modèle ImageFormaterModel
    '''  
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createModel()
        self.createView()
        'self.placeComponents()'
        #self.createController() 
    
    
    '''
    Création du modèle
    '''        
    def createModel(self):
        self.model = IFM.ImageFormaterModel()
    
    '''
    Création des composants graphiques
    '''
    
    def createView(self):
        '''self.saveButton = tkinter.Button(self.frame,"Sauvegarder",cmd = self.saveCmd)'''
        self._loadButton = tkinter.Button(self,text= "Charger",command = self._loadCmd)
        self._loadButton.pack()
    
    '''
    Création des controlleurs
    '''
    def _loadCmd(self):
        pass
        #image_path = tkinter.filedialog.askopenfilename(title = "Ouvrir une image",
                                                        #filetypes = [('ppm files','.ppm')])
        #image = tkinter.filedialog.PhotoImage(file = image_path) 
                    