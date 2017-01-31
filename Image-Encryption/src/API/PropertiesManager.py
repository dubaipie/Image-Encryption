"""
Created on 21 janv. 2017

:author: dubaipie
"""
import os
import xml.etree.ElementTree as ET


class PropertiesFileNotFoundException(Exception):
    """
    Une exception signifiant que le fichier de propriétés n'a pas
    été trouvé.
    """
    pass


class PropertyFormatException(Exception):
    """
    Une exception signifiant que la propriété n'a pas pu être trouvée.
    """
    pass


class PropertiesManager(object):
    """
    Un chargeur de propriétés.
    """

    def __init__(self):
        """
        Constructeur du chargeur de propriétés. initialement, aucune application n'est associée
        à aucun fichier fichier de propriétés.
        """

        # contiendra les arbres des fichiers de propriétés en fonction des applications.
        self._propertyTrees = {}

        # contiendra tous les chemin d'accès aux fichiers repérés par le nom des applications
        self._pathDict = {}

    def addPropertiesFile(self, app, path, filename):
        """
        Permet d'ajouter un fichier de propriétés au PropertiesManager.
        :param app: L'application qui utilisera le fichier de propriété. Il est conseillé
            de passer l'objet lui-même afin de ne pas écraser un autre fichier appartenant
            à une autre application. Aucun test ne sera fait.
        :param path: Le chemin vers le fichier. Si ne pointe pas directement, l'algorithme
            cherchera dans les sous-dossiers.
        :param filename: Le nom du fichier de propriétés.
        :raise PropertiesFileNotFoundException: le fichier n'a pas pu être trouvé.
        :raise ET.ParseError: le fichier n'a pas pu être chargé
        """
        # :raise PropertiesFileNotFoundException:
        path = os.path.abspath(path)
        path_to_file = self._lookIntoDir(path, filename)

        # :raise ET.ParseError:
        propRoot = ET.parse(path_to_file)

        self._propertyTrees[app] = propRoot
        self._pathDict[app] = path_to_file

    def getProperty(self, app, prop):
        """
        Permet de récupérer une propriété particulière.
        :param app: l'application qui demande la propriété. Est utilisé à des fins
            de différenciation des différents fichiers de propriétés.
        :param prop: le nom de la propriété. Elle doit être donnéee sous la forme
            'element[:attribut][*]' où element est le nom de la propriété recherchée, attribut
            est l'attribut deésiré (optionnel) et * permet d'indiquer qu'on veut récupérer toutes
            les valeurs associées à cette propriété (à un attibut particulier si spécifié) (optionnel)
        :return: une liste contenant la ou les valeurs demandées.
        :raise PropertyFormatException: si l'expression est mal formée
        :raise PropertiesFileNotFoundException: si aucun fichier n'est associé à app
        """
        if not app in self._propertyTrees:
            raise PropertiesFileNotFoundException

        # la racine de l'arbre représentant le fichier de propriétés de l'application.
        root = self._propertyTrees[app].getroot()

        # analyse de la propriété
        elem, attribute = self._parseProperty(prop)

        hasAttrib = attribute is not None
        rtrn = []

        # Récupération des éléments xml demandés
        if prop[-1] != '*':
            e = root.find(elem)
            rtrn.append(root.find(elem))
        else:
            rtrn = root.findall(elem)
        
        # exception si la propriété n'a pas été trouvée
        if None in rtrn:
            raise PropertyFormatException
        
        # on récupère les valeurs demandées
        for i in range(len(rtrn)):
            rtrn[i] = rtrn[i].attrib.get(attribute) if hasAttrib else rtrn[i].text

        # Le résultat peut contenir des valeurs non définies, mais pas
        # uniquement de telles valeurs.
        if None in rtrn and len(rtrn) == 1:
            raise PropertyFormatException
        
        return rtrn

    def setPropertyValue(self, app, prop, value):
        """
        Permet de fixer la valeur d'une propriété.
        :param app: l'application concernée
        :param prop: la propriété recherchée, de format 'element[:attribut]*' (voir getProperty())
        :param value: la nouvelle valeur à mettre
        :raise PropertyFormatException: la propriété n'a pas pu être trouvée.
        :raise PropertiesFileNotFoundException: app n'a aucun fichier de propriété associé.
        """
        if not app in self._propertyTrees:
            raise PropertiesFileNotFoundException

        root = self._propertyTrees[app].getroot()

        hasAttrib = ':' in prop
        elem = prop
        attribute = None
        if hasAttrib:
            elem = prop.split(":")[0]
            attribute = prop.split(":")[1]
        
        elemProp = root.find(elem)
        if elemProp is not None:
            if hasAttrib:
                elemProp.set(attribute, value)
            else:
                elemProp.text = value
        else:
            raise PropertyFormatException
        
        self._propertyTrees[app].write(self._pathDict[app])
    
    def _lookIntoDir(self, path, filename):
        """
        Fonction permettant de chercher le fichier filename
        dans le répertoire du programme et d'en retourner le chemin s'il
        existe, une erreur sinon.
        :param path: le chemin à partir duquel doit explorer l'algorithme.
        :param filename: le nom du fichier qui est recherché.
        :raise PropertiesFileNotFoundException: le fichier n'a pas été trouvé.
        """
        dirs = [d for d in os.listdir(path)]
        for d in dirs :
            if not os.path.isdir(d):
                if d == filename:
                    return os.path.join(path, d)
            else:
                self._lookIntoDir(os.path.join(path, d), filename)
        raise PropertiesFileNotFoundException

    def _parseProperty(self, prop):
        """
        Permet de découper un propriété selon le format element[:attrib]
        :param prop: la propriété à analyser.
        :return: un tuple prop, attrib où attrib peut être None
        :raise PropertyFormatException: le format ne correspond pas.
        """
        hasAttrib = False

        separatorAmount = prop.count(":")
        if separatorAmount > 0:
            hasAttrib = True
            if separatorAmount > 1:
                raise PropertyFormatException

        elem = prop
        attribute = None

        if hasAttrib:
            elem = prop.split(":")[0]
            if prop[-1] == '*':
                attribute = prop.split(":")[1][:-1]
            else:
                attribute = prop.split(":")[1]
        return elem, attribute