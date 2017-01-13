'''
Created on 13 janv. 2017

@author: dubaipie
'''
import tkinter
import tkinter.ttk as ttk
import os
import controller.ImageEncryptionController as IEC
import model.ImageEncryptionModel as IEM

class ImageEncryption(object):
    '''
    La classe principale de l'application.
    '''
    PLUGINS_PATH = "../../plugins"
    

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
        self._model = IEM.ImageEncryptionModel()
    
    def createView(self):
        '''
        Création des différents widgets de la fenêtre.
        '''
        self._frame = tkinter.Tk()
        self._frame.title("Image Encryption")
        
        self._pluginTabs = [tkinter.Frame() for _ in os.listdir(ImageEncryption.PLUGINS_PATH)]
        
        self._menuBar = tkinter.Menu(self._frame)
    
    def placeComponents(self):
        '''
        Placement des composants sur la fenêtre.
        '''
        tabs = ttk.Notebook(self._frame)
        for plugin in self._pluginTabs:
            tabs.add(plugin)
            tabs.pack(plugin)
        
        self._frame.config(menu=self._menuBar)
    
    def createController(self):
        '''
        Initialisation du contrôleur de la fenêtre.
        '''
        self._controller = IEC.ImageEncryptionController(self._model, self)
        
        fileMenu = tkinter.Menu(self._menuBar, tearoff=False)
        fileMenu.add_command(label="Quit", command=self._frame.quit)
        self._menuBar.add_cascade(label="File", menu=fileMenu)
        
        optMenu = tkinter.Menu(self._menuBar, tearoff=False)
        self._menuBar.add_cascade(label="Option", menu=optMenu)
        
if __name__ == "__main__":
    app = ImageEncryption()
    app.display()