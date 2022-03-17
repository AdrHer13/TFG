from Classes.Materials import Materials


class Hand:
    """
    Clase que representa la mano de los jugadores
    """
    resources = Materials(0, 0, 0, 0, 0)

    def __init__(self):
        self.resources = Materials(0, 0, 0, 0, 0)
        return

    def add_material(self, resource, amount):
        """
        Suma amount al material seleccionado (si es negativo lo resta de la cantidad actual)
        :param resource: tipo de recurso a añadir
        :param amount: cantidad del material a añadir
        :return: void
        """
        # print('material: ' + str(resource) + ' | amount: ' + str(amount))
        if isinstance(resource, list):
            # print('###########')
            # print(str(len(resource)))
            for material in resource:
                self.add_material(material, amount)
            # print('###########')
        else:
            if resource == 0:
                print('add_cereal')
                self.resources.add_cereal(amount)
                pass
            elif resource == 1:
                print('add_mineral')
                self.resources.add_mineral(amount)
                pass
            elif resource == 2:
                print('add_clay')
                self.resources.add_clay(amount)
                pass
            elif resource == 3:
                print('add_wood')
                self.resources.add_wood(amount)
                pass
            elif resource == 4:
                print('add_wool')
                self.resources.add_wool(amount)
                pass
            else:
                print('add_desert')
        return

    def get_resources(self):
        return self.resources
