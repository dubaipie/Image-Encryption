from PIL import Image
from Utils.EventSystem import PropertyChangeEvent, PropertyChangeListenerSupport
from Utils.EventSystem import ChangeEvent, ChangeListenerSupport
from Utils.Decorators import *

import threading
import random
import PIL

def create_image():
    '''Créer les possibilités d'images'''
    i = 0
    l = []
    while i < 2:
        img = Image.new('1',(2,2))
        l.append(img)
        if i == 0:
            l[i].putpixel((0,0),1)
            l[i].putpixel((1,1),1) 
        if i == 1:
            l[i].putpixel((1,0),1) 
            l[i].putpixel((0,1),1) 
        i += 1
    return l


class GeneratorModel(object):
    """
    Classe permettant de créer des objets capables de générer des clés.
    """
    
    ImagePossibility = create_image()
    
    #CONSTRUCTEUR
    def __init__(self):
        """
        Constructeur de générateur de clés. Initialement, la taille de la clé est nulle.
        """
        self._height = 0
        self._width = 0
        self._key = None
        self._support = PropertyChangeListenerSupport()
        self._changeSupport = ChangeListenerSupport()
        self._event = ChangeEvent(self)
        self._lock = threading.Lock()
    
    #REQUETES
    def generateKey(self):
        """
        Permet de générer une clé. Les calculs sont effectués avec un thread dédié.
        """
        thread = threading.Thread(target=self._generate)
        thread.start()
    
    @synchronized_with_attr("_lock")
    def getKey(self):
        '''
        Renvoie la clé 
        @raise IOError: la clé n'a pas encore été générée
        '''
        
        if self._key is None:
            raise AssertionError
        return self._key
    
    @synchronized_with_attr("_lock")
    def getSize(self):
        '''
        Renvoie la taille du masque
        '''
        return self._width, self._height
    
    #COMMANDES
    @synchronized_with_attr("_lock")
    def _generate(self):
        """
        Effectue les calculs pour générer la clé.
        """
        self._key = Image.new('1', (self._width, self._height))
        #  Parcourt l'image pour insérer les blocs générés de façon aléatoire
        for y in range(0, self._height, 2):
            for x in range(0, self._width, 2):
                img = self.ImagePossibility[random.randint(0, 1)]
                self._key.paste(im = img, box = (x,y))
            self._fireStateChanged()

        self._firePropertyStateChange("key")


    @synchronized_with_attr("_lock")
    def setSize(self, w, h):
        '''
        Permet de fixer la taille de la clé.
        @param w,h: la largeur et la hauteur de l'image
        @precondition: w < 0 && w % 2 == 0
        @precondition : h < 0 && h % 2 == 0
        @raise IOError: La largeur ou la hauteur ne sont pas correct.
        '''
        if w < 0 or h < 0 or w % 2 != 0 or h % 2 != 0:
            raise AssertionError
        self._width = w
        self._height = h
        
    #OUTILS
    
    def addPropertyChangeListener(self, propertyChangeListener):
        """
        Enregistrer un ChangeListener au-près du modèle.
        :param changelistener: le PropertyChangeListener
        :raise TypeError: l'objet n'est pas un PropertyChangeListener
        """
        self._support.addPropertyChangeListener(propertyChangeListener)

    def removePropertyChangeListener(self, propertyChangeListener):
        """
        Dé-enregistrer un ChangeListener au-près du modèle.
        :param changeListener: le PropertyChangeListener
        """
        self._support.removePropertyChangeListener(propertyChangeListener)

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

    def _firePropertyStateChange(self, propName):
        """
        Permet de notifier les observeurs de propname que la valeur de la
        propriété a changée.
        :param propName: le nom de la propriété qui a changée
        """
        for l in self._support.getPropertyChangeListener(propName):
            thread = threading.Thread(target=l.execute, args=[PropertyChangeEvent(self, propName)])
            thread.start()

    def _fireStateChanged(self):
        """
        Indique un changement au niveau du calcul des valeurs des pixels
         et en informe les listeners.
        """
        for l in self._changeSupport:
            l.execute(self._event)
