'''
Created on 13 janv. 2017

@author: dubaipie
'''
import tkinter
import sys
import os
import tkinter.ttk as ttk
import model.ImageEncryptionModel as IEM

class ImageEncryption(object):
    '''
    La classe principale de l'application.
    '''
    

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
        self._model.setSelectedLocale(self._model.getSelectedLocale())
    
    def createView(self):
        '''
        Création des différents widgets de la fenêtre.
        '''
        #La fenêtre principale
        self._frame = tkinter.Tk()
        self._frame.title(_("Image Encryption"))
        self._frame.minsize(600, 400)
        
        #Les différents onglets pour chaque plugin
        self._pluginTabs = []
        for d in self._model.getPlugins():
            frame = tkinter.Frame()
            frame.tabText = d
            self._pluginTabs.append(frame)
        
        #La barre des menus de l'application
        self._menuBar = tkinter.Menu(self._frame)
    
    def placeComponents(self):
        '''
        Placement des composants sur la fenêtre.
        '''
        #Placement des onglets dans la fenêtre.
        tabs = ttk.Notebook(self._frame)
        for plugin in self._pluginTabs:
            tabs.add(plugin, text=plugin.tabText)
        tabs.pack(fill="both")
        
        #Ajout de a barre des menus.
        self._frame.config(menu=self._menuBar)
    
    def createController(self): #SECTION A RETRAVAILLER
        '''
        Initialisation du contrôleur de la fenêtre.
        '''
        
        #Ajout des controleurs au menu 'File'.
        fileMenu = tkinter.Menu(self._menuBar, tearoff=False)
        fileMenu.add_command(label=_("Quit"), command=self._frame.quit)
        self._menuBar.add_cascade(label=_("File"), menu=fileMenu)
        
        #Ajout de controleurs au menu 'Option'
        optMenu = tkinter.Menu(self._menuBar, tearoff=False)
        languageMenu = tkinter.Menu(optMenu, tearoff=False)
        
        localeChoosed = tkinter.StringVar()
        for loc in self._model.getAvailableLocales():
            print("Locale : " + loc)
            languageMenu.add_radiobutton(label=loc, variable=localeChoosed, value=loc)
            if loc == self._model.getSelectedLocale():
                localeChoosed.set(loc)
        localeChoosed.trace("w", lambda *args: self._reloadWithLocale(localeChoosed.get(), args))
        
        optMenu.add_cascade(label=_("Languages"), menu=languageMenu)
          
        self._menuBar.add_cascade(label=_("Option"), menu=optMenu)
    
    def _restart(self):
        '''
        Redémarrer le programme.
        '''
        pgrm = sys.executable
        os.execl(pgrm, pgrm, *sys.argv)
    
    def _reloadWithLocale(self, loc, *args):
        self._model.setSelectedLocale(loc)
        self._restart()

if __name__ == "__main__":
    app = ImageEncryption()
    app.display()