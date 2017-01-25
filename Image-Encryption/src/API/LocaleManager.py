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
        Constructeur.
        '''
        self._api = api

    @property
    def installedLocale(self):
        '''
        Donne la langue actuellement installée.
        :return:
        '''
        return self._api.getPropertiesManager().getProperty("locales:selected")[0]
    
    def getAvailableLocales(self):
        '''
        Donne l'ensemble des langues disponibles (ie celle qui traduisent l'interface du programme principal).
        '''
        path = self._api.getPropertiesManager().getProperty("locales")[0]
        if not os.path.isdir(path):
            raise NotADirectoryError
        
        return [d for d in os.listdir(path)]

    @installedLocale.setter
    def installedLocale(self, loc):
        '''
        Installe la langue donnée en paramètre.
        :precondition: local in getAvailableLocales()
        '''
        if not loc in self.getAvailableLocales():
            raise AssertionError
        
        path = self._api.getPropertiesManager().getProperty("locales")[0]
        appname = self._api.getPropertiesManager().getProperty("app_name")[0]
        
        self._api.getPropertiesManager().setProperty("locales:selected", loc)
        (gettext.translation(appname, path, languages=[loc])).install()