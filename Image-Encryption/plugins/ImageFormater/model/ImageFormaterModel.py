'''
Created on 18 janv. 2017

@author: havarjos
'''

from PIL import ImageTk
from builtins import IOError

class ImageFormaterModel(object):
    
    def setImageToConvert(self, img):
        self._image_to_convert = img
    
    def setKey(self, img):
        self._key = img
        
    def getKey(self):
        '''
        Retourne la clé
        '''
        return self.image_to_convert    
    
    def getImageToConvert(self):
        '''
        Retourne l'image convertit.
        '''
        return self.image_to_convert
    
    '''
    Permet de changer l'image à convertir
    @precondition: image_path != None
    @postcondition: 
    @raise IOError: Si le fichier de l'image n'est pas trouvé   
    '''
    
    def changeImageToConvert(self,image_path):
        if image_path == None:
            raise AssertionError("Chemin null")
        try: 
            self.image_to_convert = Image.open(1,image_path)
        except IOError: 
            print("Image non trouvé")
            raise IOError
        self.image_convert = self.image_to_convert
        
    
    '''
    Convertit self.image_to_convert en une image de résolution 4 fois
    supérieur. 
    @precondition: self.image_to_convert != None 
    @postcondition: self.image_convert.width == 2 * self.image_to_convert.width
                    self.image_convert.height == 2 * self.image_to_convert.height
    '''
    
    def upImageResolution(self):
        if self.image_to_convert == None:
            raise AssertionError("Il n'y a pas d'image!")
        self.image_convert = Image.new(1,
                                       (self.getImageToConvert().width * 2,
                                        self.getImageToConvert().height * 2))
        i=0
        while i < self.getImageToConvert().width:
            j=0
            while j < self.getImageToConvert().height:
                px = self.getImage().getpixel((i,j))
                self.getImageConvert().putpixel((2*i,2*j),px)
                self.getImageConvert().putpixel((2*i + 1,2*j),px)
                self.getImageConvert().putpixel((2*i,2*j + 1),px)
                self.getImageConvert().putpixel((2*i + 1,2*j + 1),px)
                ++j
            ++i    
    
    '''
    Sauvegarde l'image convertit dans le fichier de chemin path_file
    @precondition: pathfile != None and getImageToConvert() != None
    @raise IOError: Si le fichier n'existe pas. 
    '''   
    
    def saveImageConvert(self,path_file):
        if self.getImageToConvert() == None:
            raise AssertionError("Image à sauvegarder null")
        if path_file == None:
            raise AssertionError("Chemin du fichier null")
        try:
            self.getImageConvert().save(path_file,'PPM')
        except IOError:
            print ("Probleme de lecture/écritue")
            raise IOError                               