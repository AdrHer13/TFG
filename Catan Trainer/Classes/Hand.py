from Classes.Materials import Materials


class Hand:
    """
    Clase que representa la mano de los jugadores
    TODO: Hay que poner lo que lleva la clase
    """

    def __init__(self):
        self.resources = Materials()
        return

    def add_material(self, resource, amount):
        """
        Suma amount al material seleccionado (si es negativo lo resta de la cantidad actual)
        :param resource: tipo de recurso a añadir
        :param amount: cantidad del recurso a añadir
        :return: void
        """
        # print('material: ' + str(resource) + ' | amount: ' + str(amount))
        if isinstance(resource, list):
            for material in resource:
                self.add_material(material, amount)

        else:
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

        return

    def remove_material(self, resource, amount):
        """
        Resta amount al material seleccionado
        :param resource: tipo de recurso a quitar
        :param amount: cantidad del recurso a quitar
        :return: void
        """
        if isinstance(resource, list):
            for material in resource:
                self.remove_material(material, amount)
        else:
            if self.get_from_id(resource) >= amount:
                self.add_material(resource, (amount * -1))
        return


    def get_from_id(self, material_id):
        return self.resources.get_from_id(material_id)

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
