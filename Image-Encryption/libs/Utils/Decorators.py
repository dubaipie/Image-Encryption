"""
Contient tous les décorateurs additionnels utilisés par le programme.
"""


def synchronized_with_attr(lock_name):
    """
    Décorateur permettant de synchroniser une méthode sur un attribut nommé
    lock_name.
    :param lock_name: le nom de l'attribut sur lequel on se synchronise
    :return: la méthode synchronisée
    """
    def decorator(method):
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

        return synced_method

    return decorator