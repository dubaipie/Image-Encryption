'''
Created on 18 janv. 2017

@author: dubaipie
'''

from PIL import Image

from Utils.EventSystem import PropertyChangeEvent, PropertyChangeListenerSupport, ChangeListenerSupport, ChangeEvent
from Utils.Decorators import *

import threading

class MismatchFormatException(Exception):
    '''
    Exception permettant de signifier que le format de la clé et de 
    l'image ne correspond pas
    '''
    pass


class CyphererModel(object):
    '''
    Modèle du chiffreur.
    '''
    
    #CONSTRUCTEUR
    def __init__(self, imagePath=None, keyPath=None):
        '''
        Constructeur
        :param imagePath: le chemin l'image à décrypter
        :param key: le chemin de la clé utilisée. Si non fournie, générée.
        '''
        self._imagePath = imagePath
        self._keyPath = keyPath
        self._resultPath = None
        self._support = PropertyChangeListenerSupport()
        self._changeSupport = ChangeListenerSupport()
        self._event = ChangeEvent(self)
        self._lock = threading.Lock()
    
    #REQUETES
    @property
    @synchronized_with_attr("_lock")
    def imagePath(self):
        '''
        Récupérer le chemin de l'image.
        '''
        return self._imagePath

    @property
    @synchronized_with_attr("_lock")
    def keyPath(self):
        '''
        Récupérer le chemin de la clé.
        '''
        return self._keyPath

    @property
    @synchronized_with_attr("_lock")
    def resultPath(self):
        """
        Donne le chemin pointant sur l'image résultante.
        :return: un chemin
        """
        return self._resultPath
    
    #COMMANDES
    @resultPath.setter
    @synchronized_with_attr("_lock")
    def resultPath(self, path):
        """
        Fixer le chemin vers l'image résultante.
        :param path: le chemin
        """
        self._resultPath = path
        self._firePropertyStateChanged("resultPath")

    @imagePath.setter
    @synchronized_with_attr("_lock")
    def imagePath(self, imagePath):
        '''
        Spécifier le chemin vers l'image.  
        '''
        self._imagePath = imagePath
        self._firePropertyStateChanged("imagePath")

    @keyPath.setter
    @synchronized_with_attr("_lock")
    def keyPath(self, keyPath):
        '''
        Spécifier le chemin vers la clé.
        '''
        self._keyPath = keyPath
        self._firePropertyStateChanged("keyPath")
    
    @synchronized_with_attr("_lock")
    def reset(self):
        '''
        Réintialise le modèle
        '''
        self._keyPath = None
        self._imagePath = None
        
    def cypher(self):
        """
        Permet de chiffrer l'image avec la clé.
        :param resultPath: le chemin qui pointera sur l'image résultante.
        :precondition: getKeyPath() is not None
        :precondition : getImagepath() is not None
        :raise IOError: L'image ou la clé n'a pas pu être chargée ou si l'écriture a échoué.
        """
        if self.keyPath is None or self.imagePath is None:
            raise AssertionError

        thread = threading.Thread(target=self._cypher)
        thread.start()
    
    #OUTILS
    @synchronized_with_attr("_lock")
    def _cypher(self):
        """
        Méthode appelée sur un thread dédié au calculs.
        :param resultPath: le chemin qui pointera sur l'image résultante.
        :raise IOError: L'image ou la clé n'a pas pu être chargée, ou l'écriture a échouée
        """
        img = Image.open(self._imagePath)
        key = Image.open(self._keyPath)

        if img.size != key.size:
            raise MismatchFormatException
        
        keyList = list(key.getdata())
        imgList = list(img.getdata())
        resultList = list()
        result = Image.new("1", img.size)

        for i in range(0, len(imgList)):
            resultList.append(not(imgList[i] ^ keyList[i]))
            if (i % result.height == 0):
                self._fireStateChanged()
        result.putdata(resultList)
        result.save(self._resultPath)
        
        
        self._firePropertyStateChanged("resultUpdated")  # pas top, à changer
    
    def addChangeListener(self, changeListener):
        """
        Enregistrer un nouveau ChangeListener au-près du modèle.
        :param changeListener: le listener
        :raise TypeError: l'objet n'est pas un ChangeListener
        """
        self._changeSupport.addChangeListener(changeListener)

    def removeChangeListener(self, changeListener):
        """
        Dé-enregistrer un Changelistener.
        :param changeListener: le listener
        """
        self._changeSupport.removeChangeListener(changeListener)

    def _fireStateChanged(self):
        """
        Indique un changement au niveau du calcul des valeurs des pixels
         et en informe les listeners.
        """
        for l in self._changeSupport:
            l.execute(self._event)
    
    def addPropertyChangeListener(self, changelistener):
        """
        Enregistrer un ChangeListener au-près du modèle.
        :param changelistener: le ChangeListener
        :raise TypeError: l'objet n'est pas un ChangeListener
        """
        self._support.addPropertyChangeListener(changelistener)

    def removePropertyChangeListener(self, changeListener):
        """
        Dé-enregistrer un ChangeListener au-près du modèle.
        :param changeListener: le ChangeListener
        """
        self._support.removePropertyChangeListener(changeListener)
    
    def _firePropertyStateChanged(self, propName):
        """
        Permet de notifier les observeurs que le modèle a changé.
        """
        for l in self._support.getPropertyChangeListener(propName):
            l.execute(PropertyChangeEvent(self, propName))