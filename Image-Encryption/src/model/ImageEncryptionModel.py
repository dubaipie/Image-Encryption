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
        #self._root = ET.parse(ImageEncryptionModel.PROPERTIES_PATH)       
    
    def getPlugins(self):
        '''
        Permet de récupérer les différents plugins sous forme de dictionnaire
        ou la clé est le nom du plugin et la valeur son IHM.
        @raise NotADirectoryError: Levée lorsque le dossier des plugins n'est pas trouvé.
        '''
        #path = os.path.abspath(self._root.find("plugins").text)
        #if not os.path.exists(path):
        #    raise NotADirectoryError
        #return self._loadModules(path)
        return self._api.getPluginManager().getLoadedPlugins()
        
    def getSelectedLocale(self):
        '''
        Permet de récupérer la langue sélectionnée.
        '''
        return self._api.getPropertiesManager().getProperty("locales:selected")[0]
        #return self._root.find("locales").attrib.get("selected")
    
    def setSelectedLocale(self, l):
        '''
        Permet de fixer la langue sélectionnée.
        '''
        #loc = self._root.find("locales")
        #loc.set("selected", l)
        #self._root.write(ImageEncryptionModel.PROPERTIES_PATH)#IOException ?
        #self._setLocale(l)
        self._api.getLocaleManager().setInstalledLocale(l)
    
    def getAvailableLocales(self):
        '''
        Permet de récupérer toutes les langues disponibles.
        @raise NotADirectoryError: Levée lorsque le dossier des langues n'est pas trouvé.
        '''
        return self._api.getLocaleManager().getAvailableLocales()
    