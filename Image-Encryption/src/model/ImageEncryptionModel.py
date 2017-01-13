'''
Created on 13 janv. 2017

@author: dubaipie
'''
import xml.etree.ElementTree as ET
import os.path

class ImageEncryptionModel(object):
    '''
    Le modèle de l'application.
    '''

    PROPERTIES_PATH = os.path.abspath("../../properties.xml")
    
    def __init__(self):
        '''
        Constructeur
        '''
        self._root = ET.parse(ImageEncryptionModel.PROPERTIES_PATH)       
    
    def getPlugins(self):
        '''
        Permet de récupérer les différents plugins sous forme de dictionnaire
        ou la clé est le nom du plugin et la valeur sont IHM.
        '''
        path = os.path.abspath(self._root.find("plugins").text)
        plugins = {}
        for d in os.listdir(path):
            plugins[d] = None
        return plugins
        