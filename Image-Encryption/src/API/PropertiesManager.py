'''
Created on 21 janv. 2017

@author: dubaipie
'''
import os
import xml.etree.ElementTree as ET

class PropertiesFileNotFoundException(Exception):
    '''
    Une exception signifiant que le fichier de propriétés n'a pas
    été trouvé.
    '''
    pass

class PropertyFormatException(Exception):
    '''
    Une exception signifiant que la propriété n'a pas pu être trouvée.
    '''
    pass

class PropertiesManager(object):
    '''
    Un chargeur de propriétés.
    '''
    
    PROPERTIES_FILE_NAME = "properties.xml"

    def __init__(self, path=os.getcwd()):
        '''
        Constructeur du chargeur de propriétés.
        @raise PropertiesFileNotFoundException: le fichier n'a pas été trouvé
        @raise ParseError: si le fichier de propriétés ne peut pas être analysé.
        '''
        
        #recherche du fichier de propriété
        self._path = self._lookIntoDir(path)
        
        #chargement des propriétés
        self._root = ET.parse(self._path)
    
    def getProperty(self, prop):
        '''
        Permet de récupérer une propriété particulière.
        @param prop: le nom de la propriété. Elle doit être donnéee sous la forme
            'element[:attribut][*]'
        @return: une liste contenant la ou les valeurs demandées.
        '''
        hasAttrib = ':' in prop
        elem = prop
        attribute = None
        rtrn = []
        if hasAttrib:
            elem = prop.split(":")[0]
            if prop[-1] == '*':
                attribute = prop.split(":")[1][:-1]
            else:
                attribute = prop.split(":")[1]
        if prop[-1] != '*':
            rtrn.append(self._root.find(elem))
        else:
            rtrn = self._root.findall(elem)
        
        #exception si la propriété n'a pas été trouvée
        if None in rtrn:
            raise PropertyFormatException
        
        #on récupère les valeurs demandées
        for i in range(len(rtrn)):
            rtrn[i] = rtrn[i].attrib.get(attribute) if hasAttrib else rtrn[i].text
        
        if None in rtrn:
            raise PropertyFormatException
        
        return rtrn
    
    def setProperty(self, prop, value):
        '''
        Permet de fixer la valeur d'une propriété. Si celle-ci n'existe pas, sera créée.
        @param prop: le nom de la propriété. Elle doit être donnéee sous la forme
            'element[:attribut]'
        '''
        hasAttrib = ':' in prop
        elem = prop
        attribute = None
        if hasAttrib:
            elem = prop.split(":")[0]
            attribute = prop.split(":")[1]
        
        root = self._root.find(elem)
        if root != None:
            if hasAttrib:
                root.set(attribute, value)
            else:
                root.text = value
        else:
            if hasAttrib:
                attribute = {attribute : value}
            else:
                attribute = {}
            ET.SubElement(self._root.getroot(), elem, attribute)
        self._root.write(self._path)
    
    def _lookIntoDir(self, path):
        '''
        Fonction permettant de chercher le fichier PROPERTIES_FILE_NAME
        dans le répertoire du programme et d'en retourner le chemin s'il
        existe, une erreur sinon.
        @param path: le chemin à partir duquel doit explorer l'algorithme.
        @raise PropertiesFileNotFoundException: le fichier n'a pas été trouvé
        '''
        dirs = [d for d in os.listdir(path)]
        for d in dirs :
            if not os.path.isdir(d):
                if d == PropertiesManager.PROPERTIES_FILE_NAME:
                    return os.path.join(path, d)
            else:
                self._lookIntoDir(os.path.join(path, d))
        raise PropertiesFileNotFoundException