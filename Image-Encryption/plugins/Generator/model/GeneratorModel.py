
from PIL import Image 
import random

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
    
    ImagePossibility = create_image()
    
    def __init__(self):
        self._height = 0
        self._width = 0
        
    def generatorKey(self):
        self._key = Image.new('1', (self._width, self._height))
        x = 0
        y = 0
        '''Parcous l'image pour insérer les blocs générer de façon aléatoirement'''
        for y in range(0, self._height, 2):
            for x in range(0, self._width, 2):
                img = self.ImagePossibility[random.randint(0, 1)]
                self._key.putpixel((x, y), img.getpixel((0,0)))
                self._key.putpixel((x + 1, y), img.getpixel((1, 0)))
                self._key.putpixel((x, y + 1), img.getpixel((0, 1)))
                self._key.putpixel((x + 1, y + 1), img.getpixel((1, 1)))
    
    def getKey(self):
        '''
        Renvoie la clé 
        @raise IOError: la clé n'a pas encore été généré
        '''
        
        if self._key is None:
            raise AssertionError
        return self._key
    
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