class ChangeEvent():
    """
    Une événement simple indiquant que quelque chose a changé. Contient une référence
    sur l'objet appelant.
    """

    def __init__(self, source):
        """
        Le constructeur prend en paramètre la source de l'événement.
        :param source: la source de l'événement.
        """
        self._src = source

    @property
    def source(self):
        """
        Permet de ércupérer la source de l'événement.
        :return: la source de l'événement
        """
        return self._src

    @source.setter
    def source(self, src):
        """
        Permet de changer la source de l'événement.
        :param src: la nouvelle source
        """
        self._src = src


class ChangeListener():
    """
    Objet permettant d'effectuer des action lorsqu'un ChangeEvent est lancé
    par un objet et que le changeListener est enregistré auprès de celui-ci.
    """

    def __init__(self, target=None):
        """
        Le constructeur d'un change Listener prend en paramètre une
        fonction de signature foo(event) qui sera exécutée lorsque celui-ci
        sera notifié par un ChangeListener.
        :param target: la fonction exécutée
        """
        self._target = target

    def execute(self, event):
        """
        La méthode exécutée lorsque l'événement event est détecté.
        :param event: l'événement qui a déclenché le changeListener
        :raise TypeError: l'événement n'est pas un ChangeEvent
        """
        if type(event) != ChangeEvent:
            raise TypeError

        if self._target is not None:
            self._target(event)


class ChangeListenerSupport():
    """
    Objet permettant le stockage et la gestion de ChangeListeners.
    """

    def __init__(self):
        """
        Construit un nouveau ChangeListenerSupport.
        """
        self._support = []

    def addChangeListener(self, changeListener):
        """
        Permet d'ajouter un nouveau ChangeListener au support.
        :param changeListener: le nouveau ChangeListener
        :raise TypeError: l'objet n'est pas un ChangeListener
        """
        if not type(changeListener) == ChangeListener:
            raise TypeError

        self._support.append(changeListener)

    def removeChangeListener(self, changeListener):
        """
        Permet de supprimer le CHangeListener du support.
        :param changeListener: le ChangeListener à supprimer
        """
        self._support.remove(changeListener)

    def __iter__(self):
        """
        Permet d'itérer les éléments du support.
        """
        return self._support.__iter__()

    def __len__(self):
        """
        Permet d'obtenir la taille du support.
        """
        return self._support.__len__()


class PropertyChangeEvent(ChangeEvent):
    """
    Un ChangeEvent plus spécifique.
    """

    def __init__(self, source, propertyName):
        """
        Constructeur de PropertyChangeEvent, prend en paramètre la source et le nom de la propriété.
        :param source: la source de l'événement
        :param propertyName:  la propriété concernée
        """
        ChangeEvent.__init__(self, source)
        self._name = propertyName

    @property
    def propertyName(self):
        """
        Permet de donner le nom de la propriété concernée par le changement.
        """
        return self._name

    @propertyName.setter
    def propertyName(self, name):
        """
        Permet de changer le nom de la propriété.
        :param name: le nouveau nom de la propriété
        """
        self._name = name

class PropertyChangeListener():
    """
    Un listener qui peut observer des modèles sources de PropertyChangeEvents.
    """

    def __init__(self, propertyName, target=None):
        """
        Constructeur de PropertyChangeListener, prend en paramètre le nom de la propriété
        observée et la fonction a exécuter de signature foo(event).
        :param propertyName: le nom de la propriété
        :param target: la fonction a exécuter
        """
        self._target = target
        self._propertyName =  propertyName

    @property
    def propertyName(self):
        """
        Permet d'obtenir le nom de la propriété observée.
        """
        return self._propertyName

    def execute(self, event):
        """
        Exécuée lorsqu'un événement est attrappé.
        :param event: l'événement source
        :raise TypeError: l'événement n'est pas un PropertyChangeEvent ou le nom de celui-ci
        ne correspond pas.
        """
        if type(event) != PropertyChangeEvent or event.propertyName != self.propertyName:
            raise TypeError

        if self._target is not None:
            self._target(event)

class PropertyChangeListenerSupport():
    """
    Un support pour gérer les PropertyChangeListener.
    """

    def __init__(self):
        """
        Construit un PropertyChangelistenerSupport vide.
        """
        self._listeners = {}

    def addPropertyChangeListener(self, propertyChangeListener):
        """
        Ajouter un PropertyChangeListener au support.
        :param propertyChangeListener: le PropertyChangeListener
        :raise TypeError: propertyChangeListener n'est pas du bon type
        """
        if type(propertyChangeListener) != PropertyChangeListener:
            raise TypeError

        try:
            self._listeners[propertyChangeListener.propertyName]
        except KeyError:
            self._listeners[propertyChangeListener.propertyName] = []

        self._listeners[propertyChangeListener.propertyName].append(propertyChangeListener)

    def removePropertyChangeListener(self, propertyChangeListener):
        """
        Supprimer du support le propertyChangeListener
        :param propertyChangeListener: le PropertyChangeListener à supprimer
        """
        listener = self._listeners[propertyChangeListener.propertyName]
        if listener is None:
            return

        listener.remove(propertyChangeListener)

    def getPropertyChangeListener(self, propName):
        """
        Donne la liste de tous les PropertyChangeListeners écoutant la propriété de nom
        propertyName.
        :param propName: le nom de la propriété écoutée
        :return: la liste des PropertyChangeListeners
        """
        try:
            return self._listeners[propName]
        except KeyError:
            return []