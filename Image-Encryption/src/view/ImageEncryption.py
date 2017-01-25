'''
Created on 13 janv. 2017

@author: dubaipie
'''
import tkinter
import sys
import os
import tkinter.ttk as ttk
import model.ImageEncryptionModel as IEM
import xml.etree.ElementTree as ET
import traceback

class ImageEncryption(object):
    '''
    La classe principale de l'application.
    '''
    

    def __init__(self, api):
        '''
        Constructeur de la fenêtre.
        '''
        self.createModel(api)
        self.createView()
        self.placeComponents()
        self.createController()
    
    def display(self):
        '''
        Afficher la fenêtre.
        '''
        self._frame.mainloop()
    
    def createModel(self, api):
        '''
        Initialisation du model.
        '''
        try:
            self._model = IEM.ImageEncryptionModel(api)
            self._model.selectedLocale = self._model.selectedLocale
        except ET.ParseError:
            tkinter.messagebox.showerror(_("Properties file error"),
                                         _("An error occurs during properties file parsing"))
                
    def createView(self):
        '''
        Création des différents widgets de la fenêtre.
        '''
        #La fenêtre principale
        self._frame = tkinter.Tk()
        self._frame.title(_("Image Encryption"))
        self._frame.minsize(600, 400)
        
        self._tabs = ttk.Notebook(self._frame)
        
        #Les différents onglets correspondant à chaque plugin
        self._pluginTabs = []
        try:
            for init in self._model.plugins:
                try:
                    frame = init.getFrame(self._tabs)
                    frame.tabText = init.getName()
                    self._pluginTabs.append(frame)
                except :
                    #les modules non conforme sont ignorés
                    #print("error")
                    #traceback.print_exc()
                    pass
        except NotADirectoryError:
            tkinter.messagebox.showerror(_("Plugin directory error"),
                                         _("Plugin directory not found"))
        
        #La barre des menus de l'application
        self._menuBar = tkinter.Menu(self._frame)
    
    def placeComponents(self):
        '''
        Placement des composants sur la fenêtre.
        '''
        #Placement des onglets dans la fenêtre.
        for plugin in self._pluginTabs:
            self._tabs.add(plugin, text=plugin.tabText)
        self._tabs.pack(fill="both", expand=True)
        
        #Ajout de la barre des menus.
        self._frame.config(menu=self._menuBar)
    
    def createController(self): #SECTION A RETRAVAILLER
        '''
        Initialisation du contrôleur de la fenêtre.
        '''
        self._createMenu()        
    
    def _restart(self):
        '''
        Redémarrer le programme.
        '''
        pgrm = sys.executable
        os.execl(pgrm, pgrm, *sys.argv)
    
    def _reloadWithLocale(self, loc, *args):
        self._model.selectedLocale = loc
        self._restart()
    
    def _createMenu(self):
        #-- Ajout des controleurs au menu 'File'. --#
        fileMenu = tkinter.Menu(self._menuBar, tearoff=False)
        #  Ajout de l'item quitter  #
        fileMenu.add_command(label=_("Quit"), command=self._frame.quit)
        self._menuBar.add_cascade(label=_("File"), menu=fileMenu)
        #-------------------------------------------#
        
        #-- Ajout de controleurs au menu 'Option' --#
        optMenu = tkinter.Menu(self._menuBar, tearoff=False)
        #  Ajout du sous-menu langage  #
        languageMenu = tkinter.Menu(optMenu, tearoff=False)
        localeChoosed = tkinter.StringVar()
        for loc in self._model.availableLocales:
            languageMenu.add_radiobutton(label=loc, variable=localeChoosed, value=loc)
            if loc == self._model.selectedLocale:
                localeChoosed.set(loc)
        localeChoosed.trace("w", lambda *args: self._reloadWithLocale(localeChoosed.get(), args))
        optMenu.add_cascade(label=_("Languages"), menu=languageMenu)
        #-------------------------------------------#
        
        self._menuBar.add_cascade(label=_("Option"), menu=optMenu)

if __name__ == "__main__":
    app = ImageEncryption()
    app.display()