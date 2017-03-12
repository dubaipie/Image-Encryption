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
    