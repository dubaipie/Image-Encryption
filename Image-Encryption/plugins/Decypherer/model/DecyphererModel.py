'''
Created on 18 janv. 2017

@author: dubaipie
'''

from PIL import Image

class MismatchFormatException(Exception):
    '''
    Exception permettant de signifier que le format de la clé et de 
    l'image ne correspond pas
    '''
    pass


class DecyphererModel(object):
    '''
    Modèle du chiffreur.
    '''


    def __init__(self, imagePath=None, keyPath=None):
        '''
        Constructeur
        @param imagePath: le chemin l'image à décrypter
        @param key: le chemin de la clé utilisée. Si non fournie, générée.
        '''
        self._imagePath = imagePath
        self._keyPath = keyPath
    
    def getImagePath(self):
        '''
        Récupérer le chemin de l'image.
        '''
        return self._imagePath
    
    def getKeyPath(self):
        '''
        Récupérer le chemin de la clé.
        '''
        return self._keyPath

    def setImagePath(self, imagePath):
        '''
        Spécifier le chemin vers l'image.  
        '''
        self._imagePath = imagePath
    
    def setKeyPath(self, keyPath):
        '''
        Spécifier le chemin vers la clé.
        '''
        self._keyPath = keyPath
          
    def decypher(self, resultPath):
        '''
        Permet de chiffrer l'image avec la clé.
        @param resultPath: le chemin qui pointera sur l'image résultante.
        @precondition: getKeyPath() is not None
        @precondition : getImagepath() is not None
        @raise IOError: L'image ou la clé n'a pas pu être chargée ou si l'écriture a échoué.
        '''
        if self.getKeyPath() is None or self.getImagePath() is None:
            raise AssertionError
        
        img = Image.open(self._imagePath)
        key = Image.open(self._keyPath)
        
        if img.size != key.size:
            raise MismatchFormatException
        
        result = Image.new("1", img.size)
        for i in range(0, img.width):
            for j in range(0, img.height):
                value = (img.getpixel((i, j)) + key.getpixel((i, j))) % 2
                result.putpixel((i, j), value)
         
        result.save(resultPath)
        