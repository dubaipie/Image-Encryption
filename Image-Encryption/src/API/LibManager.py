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

    def __init__(self):
        '''
        Constructeur.
        '''
        self._availableLibs = []
        self._path = os.path.abspath("../../libs")

    @property
    def availableLibs(self):
        '''
        Donne un dictionnaire nom : chemin des librairies disponibles.
        :return: un dictionnaire
        '''
        if self._availableLibs == []:
            self._lookInto(self._path)
        return self._availableLibs

    def _lookInto(self, path):
        for d in os.listdir(path):
            self._availableLibs.append(os.path.abspath(os.path.join(path, d)))

    def loadLibs(self):
        '''
        Charger les librairies.
        '''
        sys.path.insert(1, self._path)