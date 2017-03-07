'''
Created on 20 janv. 2017

@author: dubaipie
'''
from ImageFormatter.view.ImageFormatter import ImageFormatter

class Initializer(object):
    '''
    La classe d'initialisation du plugin.
    '''

    def __init__(self, loader):
        '''
        Constructeur.
        '''
        self._loader = loader

    def getFrame(self, master=None):
        '''
        Récupérer la fenêtre.
        '''
        return ImageFormatter(master)
    
    def getName(self):
        '''
        Récupérer le nom du plugin.
        '''
        return "Convertisseur d'images"