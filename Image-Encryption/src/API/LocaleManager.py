'''
Created on 21 janv. 2017

@author: dubaipie
'''
import os
import gettext


class LocaleManager(object):
    '''
    Objet permettant de gérer les langues du programme.
    '''

    def __init__(self, api):
        '''
        Constructeur, prennant en paramètre l'api utilisée par le programme.
        (à des fins d'enregistrement de la langue sélectionnée)
        :param api: l'api utilisée.
        '''
        self._api = api
        self._localePaths = {}

    def addLocalePath(self, appname, path):
        """
        Permet d'ajouter un chemin vers un dossier de langue, permettant plus tard de
        traduire un programme.
        :param appname: Le nom de l'application qui sera traduite, les fichiers de traduction
            devant avoir le format appname.mo (norme POSIX)
        :param path: le chemin vers le dossier contenant les langues.
        :raise NotADirectoryError: le chemin ne pointe pas sur un dossier.
        """
        if not os.path.isdir(path):
            raise NotADirectoryError

        self._localePaths[appname] = path

    @property
    def installedLocale(self):
        '''
        Donne la langue actuellement installée.
        :return: une string donnant l'abbréviation de la langue
        '''
        return self._api.getPropertiesManager().getProperty(self._api, "locales:selected")[0]
    
    def getAvailableLocales(self):
        '''
        Donne l'ensemble des langues disponibles sous forme d'un set.
        Attention, rien ne garantit que toutes les composantes du programme disposent d'une traduction
        pour les-dites langues.
        '''
        rtrn = set()
        for _, path in self._localePaths.items():
            for d in os.listdir(path):
                rtrn.add(d)
        return rtrn

    @installedLocale.setter
    def installedLocale(self, loc):
        '''
        Installe la langue donnée en paramètre.
        :raise AssertionError: si loc n'est pas dans l'ensemble des langues disponibles.
        '''

        if not loc in self.getAvailableLocales():
            raise AssertionError
        
        for appname, path in self._localePaths.items():
            (gettext.translation(appname, path, languages=[loc])).install()
        
        self._api.getPropertiesManager().setPropertyValue(self._api, "locales:selected", loc)