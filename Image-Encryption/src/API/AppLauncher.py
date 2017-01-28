'''
Created on 21 janv. 2017

@author: dubaipie
'''
from view.ImageEncryption import ImageEncryption
from API.PropertiesManager import PropertiesManager
from API.PluginManager import PluginManager

import os
from API.LocaleManager import LocaleManager
from API.LibManager import LibManager

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
        self._properties = PropertiesManager()
        self._properties.addPropertiesFile(self,
                                           os.path.abspath(os.path.join(os.getcwd(), "../..")),
                                           "properties.xml")

        self._pluginManager = PluginManager(self)
        self._localeManager = LocaleManager(self)
        self._libManager = LibManager(self)

        self._libManager.loadLibs()

        self._pluginManager.loadPlugins()


    def getPluginManager(self):
        '''
        Donne le pluginManager utilisé.
        '''
        return self._pluginManager

    def getPropertiesManager(self):
        '''
        Donne le PropertiesManager utilisé.
        '''
        return self._properties

    def getLocaleManager(self):
        '''
        Donne le localeManager utilisé.
        '''
        return self._localeManager

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
    app = AppLauncher()
    app.init()
    app.launch()