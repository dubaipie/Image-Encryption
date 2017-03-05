'''
Created on 13 janv. 2017

@author: dubaipie
'''
from tkinter import Tk, Menu
import tkinter.ttk as ttk
import model.ImageEncryptionModel as IEM

class ImageEncryption(object):
    '''
    La classe principale de l'application.
    '''

    def __init__(self, api):
        '''
        Constructeur de la fenêtre.
        :param api: Le lanceur de l'application.
        '''
        self._createModel(api)
        self._createView()
        self._placeComponents()
        self._createController()
    
    def display(self):
        '''
        Afficher la fenêtre.
        '''
        self._frame.mainloop()
    
    def _createModel(self, api):
        '''
        Initialisation du model.
        '''
        self._model = IEM.ImageEncryptionModel(api)
                
    def _createView(self):
        '''
        Création des différents widgets de la fenêtre.
        '''
        #La fenêtre principale
        self._frame = Tk()
        self._frame.title("Image Encryption")
        self._frame.minsize(600, 400)
        try:
            self._frame.iconbitmap("../../ressources/pictures/icon.ico")
        except:
            pass

        self._tabs = ttk.Notebook(self._frame)
        
        #Les différents onglets correspondant à chaque plugin
        self._pluginTabs = []
        for init in self._model.plugins:
            frame = init.getFrame(self._tabs)
            frame.tabText = init.getName()
            self._pluginTabs.append(frame)

        #La barre des menus de l'application
        self._menuBar = Menu(self._frame)
    
    def _placeComponents(self):
        '''
        Placement des composants sur la fenêtre.
        '''
        #Placement des onglets dans la fenêtre.
        for plugin in self._pluginTabs:
            self._tabs.add(plugin, text=plugin.tabText)
        self._tabs.pack(fill="both", expand=True)
        
        #Ajout de la barre des menus.
        self._frame.config(menu=self._menuBar)
    
    def _createController(self): #SECTION A RETRAVAILLER
        '''
        Initialisation du contrôleur de la fenêtre.
        '''
        self._createMenu()

    def _createMenu(self):
        #-- Ajout des controleurs au menu 'File'. --#
        fileMenu = Menu(self._menuBar, tearoff=0)
        #  Ajout de l'item quitter  #
        fileMenu.add_command(label="Quitter", command=self._frame.quit)
        self._menuBar.add_cascade(label="Fichier", menu=fileMenu)
        #-------------------------------------------#
        
        #-- Ajout de controleurs au menu 'Option' --#
        optMenu = Menu(self._menuBar, tearoff=False)
        
        self._menuBar.add_cascade(label="Option", menu=optMenu)