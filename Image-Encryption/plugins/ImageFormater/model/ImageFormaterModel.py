'''
Created on 18 janv. 2017

@author: havarjos
'''

from PIL import Image


class NoImageToConvert(Exception):
    """
    Exception levée quand aucune image à convertir n'a été trouvée.
    """
    pass


class ImageFormaterModel(object):
    """
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
    """
    def __init__(self):
        """
        Constructeur de convertisseur d'image.
        """
        self._origin = None
        self._converted = None

    @property
    def originalPicture(self):
        """
        Donne l'image d'origine.
        :return: une instance de PIL.Image ou None
        """
        return self._origin

    @originalPicture.setter
    def originalPicture(self, path_or_image):
        """
        Permet de spécifier l'image qui sera convertie lors d'un appel à convert()
        :param path_or_image: le chemin vers l'image ou bien l'immage elle-même.
        :raise TypeError: le type ne permet pas le chargement de l'image.
        :raise IOError: le chemin ne pointe pas sur une image valide.
        """
        if type(path_or_image) is str:
            self._origin = Image.open(path_or_image)
        elif type(path_or_image) is Image:
            self._origin = path_or_image
        else:
            raise TypeError

    def convert(self):
        """
        Convertit l'image originale en sa transformée, 2x plus grande.
        :raise NoImageToConvert: s'il n'y a pas d'image originale.
        """
        if self._origin is None:
            raise NoImageToConvert

        self._converted = self._origin.convert('1')
        width, height = self._converted.width, self._converted.height
        width *= 2
        height *= 2
        self._converted = self._converted.resize((width, height), Image.BILINEAR)

    @property
    def convertedPicture(self):
        """
        Donne l'image convertie si un appel avec succès à convert() à eu lieu,
        None sinon.
        :return: L'image convertie ou None
        """
        return self._converted