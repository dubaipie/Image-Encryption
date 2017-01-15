'''
Created on 13 janv. 2017

@author: dubaipie
'''
import tkinter
import tkinter.ttk as ttk
import controller.ImageEncryptionController as IEC
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
    
    def createController(self):
        '''
        Initialisation du contrôleur de la fenêtre.
        '''
        #Controleur de l'application.
        self._controller = IEC.ImageEncryptionController(self._model, self)
        
        #Ajout des controleurs au menu 'File'.
        fileMenu = tkinter.Menu(self._menuBar, tearoff=False)
        fileMenu.add_command(label=_("Quit"), command=self._frame.quit)
        self._menuBar.add_cascade(label=_("File"), menu=fileMenu)
        
        #Ajout de controleurs au menu 'Option'
        optMenu = tkinter.Menu(self._menuBar, tearoff=False)
        languageMenu = tkinter.Menu(optMenu, tearoff=False)
        for loc in self._model.getAvailableLocales():
            print("Locale : " + loc)
            languageMenu.add_radiobutton(label=loc, command=lambda: self._controller.changeLocale(loc))
        optMenu.add_cascade(label=_("Languages"), menu=languageMenu)
          
        self._menuBar.add_cascade(label=_("Option"), menu=optMenu)
        
if __name__ == "__main__":
    app = ImageEncryption()
    app.display()