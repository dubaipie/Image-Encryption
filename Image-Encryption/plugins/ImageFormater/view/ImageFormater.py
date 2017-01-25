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
        self._model = IFM.ImageFormaterModel()
    
    '''
    Création des composants graphiques
    '''
    
    def createView(self):
        self.saveButton = tkinter.Button(self,"Sauvegarder",command = self._saveCmd)
        self._loadButton = tkinter.Button(self,text= "Charger",command = self._loadCmd)
        self._loadButton.pack()
        self._canvas = tkinter.Canvas(self,width = 500,height = 500, bg = 'blue')
        self._canvas.pack()
        self._resolutionButton(self,"Changer la résolution",command = self._changeResolution)
    
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
            
                
          
        
          
                    