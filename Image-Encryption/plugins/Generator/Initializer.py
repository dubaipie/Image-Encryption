'''
Created on 20 janv. 2017

@author: dubaipie
'''
from Generator.view.GeneratorView import GeneratorView


class Initializer(object):
    '''
    La classe d'initialisation du plugin.
    '''

    def __init__(self, loader):
        '''
        Constructeur.
        '''
        self._loader = loader
    
    def initPlugin(self):
        '''
        Initialiser le plugin (langues, configuration ...)
        '''
        self._loader.API.getPropertiesManager().addPropertiesFile(
            self, "../../plugins/Generator", "properties.xml")
        self._loader.getLocaleManager().addLocalePath(
            self._loader.API.getPropertiesManager().getProperty(self, "appname"),
            self._loader.API.getPropertiesManager().getProperty(self, "locales"))

    def getFrame(self, master=None):
        '''
        Récupérer la fenêtre.
        '''
        return GeneratorView(master)
    
    def getName(self):
        '''
        Récupérer le nom du plugin.
        '''
        #return self._loader.API.getPropertiesManager().getProperty(self, "appname")
        return "Generator"