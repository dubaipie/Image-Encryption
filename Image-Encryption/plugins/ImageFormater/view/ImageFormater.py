'''
Created on 18 janv. 2017

@author: havarjos
'''
import tkinter
from PIL import ImageTk
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
        #self.creteController() 
    
    
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
        self._canvas = tkinter.Canvas(self,width = 500,height = 500, bg = 'blue')
        self._canvas.pack()
    
    '''
    Création des controlleurs
    '''
    def _loadCmd(self):
        
        picture_path = tkinter.filedialog.askopenfilename(title = "Ouvrir une image",
                                                        filetypes = [('gif files','.gif')])
        picture = tkinter.filedialog.PhotoImage(file = picture_path) 
        self._canvas.create_image(0,0,anchor = CENTER,image = picture )
        self._canvas.image = picture
        self._canvas.pack()
        
                    