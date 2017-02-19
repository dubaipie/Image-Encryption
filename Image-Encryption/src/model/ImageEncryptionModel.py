'''
Created on 13 janv. 2017

@author: dubaipie
'''

class ImageEncryptionModel(object):
    '''
    Le modèle de l'application.
    '''

    def __init__(self, api):
        '''
        Constructeur
        @raise ParseError: si le fichier de propriétés ne peut pas être analysé.
        '''
        self._api = api

    @property
    def plugins(self):
        '''
        Permet de récupérer les différents plugins sous forme de dictionnaire
        ou la clé est le nom du plugin et la valeur son IHM.
        @raise NotADirectoryError: Levée lorsque le dossier des plugins n'est pas trouvé.
        '''
        return self._api.getPluginManager().loadedPlugins

    @property
    def availableLocales(self):
        '''
        Permet de récupérer toutes les langues disponibles.
        :return: Une liste de string, représentant l'ensemble des langues.
        :raise: NotADirectoryError: Levée lorsque le dossier des langues n'est pas trouvé.
        '''
        return self._api.getLocaleManager().getAvailableLocales()
    