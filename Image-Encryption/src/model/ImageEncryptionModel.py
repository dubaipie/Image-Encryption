'''
Created on 13 janv. 2017

@author: dubaipie
'''
import xml.etree.ElementTree as ET
import os
import gettext
import locale
import sys
import inspect

class ImageEncryptionModel(object):
    '''
    Le modèle de l'application.
    '''

    PROPERTIES_PATH = os.path.abspath("../../properties.xml")
    
    def __init__(self):
        '''
        Constructeur
        @raise ParseError: si le fichier de propriétés ne peut pas être analysé.
        '''
        self._root = ET.parse(ImageEncryptionModel.PROPERTIES_PATH)       
    
    def getPlugins(self):
        '''
        Permet de récupérer les différents plugins sous forme de dictionnaire
        ou la clé est le nom du plugin et la valeur son IHM.
        @raise NotADirectoryError: Levée lorsque le dossier des plugins n'est pas trouvé.
        '''
        path = os.path.abspath(self._root.find("plugins").text)
        if not os.path.exists(path):
            raise NotADirectoryError
        return self._loadModules(path)
        
    def getSelectedLocale(self):
        '''
        Permet de récupérer la langue sélectionnée.
        '''
        return self._root.find("locales").attrib.get("selected")
    
    def setSelectedLocale(self, l):
        '''
        Permet de fixer la langue sélectionnée.
        '''
        print(l)
        loc = self._root.find("locales")
        loc.set("selected", l)
        self._root.write(ImageEncryptionModel.PROPERTIES_PATH)#IOException ?
        self._setLocale(l)
    
    def getAvailableLocales(self):
        '''
        Permet de récupérer toutes les langues disponibles.
        @raise NotADirectoryError: Levée lorsque le dossier des langues n'est pas trouvé.
        '''
        path = os.path.abspath(self._root.find("locales").text)
        return [d for d in os.listdir(path)]
    
    def _setLocale(self, l):
        '''
        Change la langue du programme pour celle donnée.
        @raise NotADirectoryError: Utilise getAvailableLocales
        '''
        path = os.path.abspath(self._root.find("locales").text)
        appname = self._root.find("app_name").text
        loc = l
        if loc is None or loc == "None":
            loc = locale.getdefaultlocale()[0][:2]
            if not loc in self.getAvailableLocales():
                loc = "en_GB"
        (gettext.translation(appname, path, languages=[loc])).install()
    
    def _loadModules(self, path):
        result = {}
        for d in os.listdir(path):
            p = os.path.join(path, os.path.join(d, os.path.join("view", d)))
            sys.path.append(p)
            result[d] = __import__(d)
        return result 