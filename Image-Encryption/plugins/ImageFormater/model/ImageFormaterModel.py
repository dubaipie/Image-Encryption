'''
Created on 18 janv. 2017

@author: havarjos
'''

from PIL import Image
import threading


class NoImageToConvert(Exception):
    """
    Exception levée quand aucune image à convertir n'a été trouvée.
    """
    pass


def synchronized_with_attr(lock_name):
    """
    Décorateur permettant de synchroniser une méthode sur un attribut nommé
    lock_name.
    :param lock_name: le nom de l'attribut surlequel on se synchronise
    :return: la méthode synchronisée
    """
    def decorator(method):
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

        return synced_method

    return decorator

class ImageFormaterModel(object):
    def __init__(self):
        """
        Constructeur de convertisseur d'image.
        """
        self._origin = None
        self._converted = None
        self._lock = threading.Lock()

    @property
    @synchronized_with_attr("_lock")
    def originalPicture(self):
        """
        Donne l'image d'origine.
        :return: une instance de PIL.Image ou None
        """
        return self._origin

    @originalPicture.setter
    @synchronized_with_attr("_lock")
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
        if self.originalPicture is None:
            raise NoImageToConvert

        thread = threading.Thread(target=self._convertThread)
        thread.start()

    @property
    @synchronized_with_attr("_lock")
    def convertedPicture(self):
        """
        Donne l'image convertie si un appel avec succès à convert() à eu lieu,
        None sinon.
        :return: L'image convertie ou None
        """
        return self._converted

    @synchronized_with_attr("_lock")
    def _convertThread(self):
        """
        Méthode qui sera appelée par le thread de calcul. Modifie sur place les attributs.
        """
        self._converted = self._origin.convert('1')
        width, height = self._converted.width, self._converted.height
        width *= 2
        height *= 2
        self._converted = self._converted.resize((width, height), Image.BILINEAR)