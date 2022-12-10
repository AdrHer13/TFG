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
                # print('add_cereal')
                self.resources.add_cereal(amount)
                pass
            elif resource == 1:
                # print('add_mineral')
                self.resources.add_mineral(amount)
                pass
            elif resource == 2:
                # print('add_clay')
                self.resources.add_clay(amount)
                pass
            elif resource == 3:
                # print('add_wood')
                self.resources.add_wood(amount)
                pass
            elif resource == 4:
                # print('add_wool')
                self.resources.add_wool(amount)
                pass
            # else:
            #     print('add_desert')

        # TODO: arreglar el problema con los negativos. Esto es un fix temporal que puede ser abusable
        if not isinstance(resource, list) and self.get_from_id(resource) < 0:
            self.add_material(resource, (self.get_from_id(resource) * -1))
        return

    def remove_material(self, resource, amount):
        """
        Resta amount al material seleccionado
        :param resource: tipo de recurso a añadir
        :param amount: cantidad del material a añadir
        :return: true/false?
        """
        if self.get_from_id(resource) >= 1:
            self.add_material(resource, (amount * -1))
            return True
        else:
            # TODO: comprobar por qué la excepción se lanza cuando alguien tiene 1 material pese a estar como válido si es >=1
            # raise Exception("Cantidad de materiales negativa. Cancelando partida")
            return False

    def get_from_id(self, material_id):
        return self.resources.get_from_id(material_id)

    def get_resources(self):
        return self.resources

    def get_cereal(self):
        return self.resources.cereal

    def get_mineral(self):
        return self.resources.mineral

    def get_clay(self):
        return self.resources.clay

    def get_wood(self):
        return self.resources.wood

    def get_wool(self):
        return self.resources.wool

    def get_total(self):
        return self.get_cereal() + self.get_mineral() + self.get_clay() + self.get_wood() + self.get_wool()

    def __str__(self):
        return 'Hand(' + str(self.resources) + ')'
