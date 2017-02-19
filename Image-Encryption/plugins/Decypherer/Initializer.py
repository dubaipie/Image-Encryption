'''
Created on 1 févr. 2017

@author: havarjos
'''
from Decypherer.view.Decypherer import Decypherer

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
        return Decypherer(master)
    
    def getName(self):
        '''
        Récupérer le nom du plugin.
        '''
        return "Déchiffreur"