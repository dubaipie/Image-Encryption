'''
Created on 21 janv. 2017

@author: dubaipie
'''

class AppLauncher(object):
    """
    Lanceur de l'application, se charge d'initialiser l'application, de
    la lancer et enfin d'effectuer toutes les opérations nécessaires avant de terminer
    l'application.
    """

    def __init__(self):
        '''
        Constructeur.
        '''

    def init(self):
        '''
        Ensemble des opérations à effectuer avant de lancer l'application
        principale.
        '''
        self._libManager = LibManager()
        self._pluginManager = PluginManager()

        self._libManager.loadLibs()
        self._pluginManager.loadPlugins()

    def getPluginManager(self):
        '''
        Donne le pluginManager utilisé.
        '''
        return self._pluginManager

    def getLibManager(self):
        '''
        Donne le chargeur de bibliothèque utilisé.
        '''
        return self._libManager

    def launch(self):
        '''
        Lancement de l'application.
        '''
        self._frame = ImageEncryption(self)
        self._frame.display()

if __name__ == "__main__":
    try:
        from view.ImageEncryption import ImageEncryption
        from API.PluginManager import PluginManager
        from API.LibManager import LibManager

        app = AppLauncher()
        app.init()
        app.launch()

    except ImportError as e:
        import sys
        print("Une erreur s'est produite : " + e.msg, file=sys.stderr)
