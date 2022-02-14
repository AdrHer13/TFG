from Classes.Materials import Materials


class Hand:
    """
    Clase que representa la mano de los jugadores
    """
    resources = Materials(0, 0, 0, 0, 0)

    def __init__(self):
        return

    def add_material(self, resource, amount):
        """
        Suma amount al material seleccionado (si es negativo lo resta de la cantidad actual)
        :param resource: tipo de recurso a añadir
        :param amount: cantidad del material a añadir
        :return: void
        """
        if resource == 0:
            self.resources.add_cereal(amount)
        elif resource == 1:
            self.resources.add_mineral(amount)
        elif resource == 2:
            self.resources.add_clay(amount)
        elif resource == 3:
            self.resources.add_wood(amount)
        elif resource == 4:
            self.resources.add_wool(amount)
        else:
            return None

    def get_resources(self):
        return self.resources
