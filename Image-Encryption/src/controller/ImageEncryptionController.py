'''
Created on 13 janv. 2017

@author: dubaipie
'''

class ImageEncryptionController(object):
    '''
    Permet de gérer la communication entre le modèle et la vue.
    '''


    def __init__(self, model, view):
        '''
        Constructeur.
        @param model: le modèle associé
        @param view: la vue associée
        @precondition: model is not None
        @precondition: view is not None
        '''
        if model is None or view is None:
            raise AssertionError
        self._model = model
        self._view = view
    
    def changeLocale(self, loc):
        '''
        Permet de changer la langue.
        '''
        self._model.setSelectedLocale(loc)