'''
Created on 20 janv. 2017

@author: dubaipie
'''
from Cypherer.view.Cypherer import Cypherer

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

    def getFrame(self, master=None):
        '''
        Récupérer la fenêtre.
        '''
        return Cypherer(master)
    
    def getName(self):
        '''
        Récupérer le nom du plugin.
        '''
        return "Cypherer"