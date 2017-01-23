'''
Created on 22 janv. 2017

@author: dubaipie
'''
import os
import sys

class LibManager(object):
    '''
    Objet permettant de chager les librairies nécessaires à l'application.
    '''


    def __init__(self, api):
        '''
        Constructeur.
        '''
        self._api = api
    
    def loadLibs(self):
        path = os.path.abspath(self._api.getPropertiesManager().getProperty("libs")[0])
        self._lookInto(path)
    
    def _lookInto(self, path):
        for d in os.listdir(path):
            sys.path.append(os.path.abspath(os.path.join(path, d)))