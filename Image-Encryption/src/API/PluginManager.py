'''
Created on 20 janv. 2017

@author: dubaipie
'''
import importlib.util
import os

class PluginManager(object):
    '''
    Chargeur de plugins.
    '''


    def __init__(self, api):
        '''
        Constructeur.
        '''
        self._api = api
        self._plugins = []
    
    def loadPlugins(self):
        '''
        Charge les plugins à partir du chemin fourni par l'API. Si le module Initializer
        du plugin n'est pas correctement défini, le plugin est ignoré.
        '''
        path = self._api.getPropertiesManager().getProperty(self._api, "plugins")[0]
        for d in os.listdir(path):
            m = os.path.abspath(os.path.join(path, os.path.join(d, "Initializer.py")))
            if os.path.isfile(m):
                spec = importlib.util.spec_from_file_location("Initializer", m)
                initializerModule = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(initializerModule)
                
                try:
                    initializer = initializerModule.Initializer(self)
                    self._plugins.append(initializer)
                    initializer.initPlugin()
                except ImportError as e:
                    print(e.msg)

    @property
    def API(self):
        '''
        Donne l'interface utilisée pour manipuler le programme principal.
        '''
        return self._api

    @property
    def loadedPlugins(self):
        '''
        Donne un liste de tous les plugins chargés.
        '''
        return self._plugins
    
            