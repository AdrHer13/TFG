class Materials:
    """
    Clase que representa los materiales. Se usa tanto en la mano de los jugadores como en las ofertas
    """

    def __init__(self, cereal=0, mineral=0, clay=0, wood=0, wool=0):
        self.cereal = cereal
        self.mineral = mineral
        self.clay = clay
        self.wood = wood
        self.wool = wool
        self.array_ids = [cereal, mineral, clay, wood, wool]
        return

    def get_from_id(self, material_constant):
        self.array_ids = [self.cereal, self.mineral, self.clay, self.wood, self.wool]
        return self.array_ids[material_constant]

    # getters #####
    def get_cereal(self):
        return self.cereal

    def get_mineral(self):
        return self.mineral

    def get_clay(self):
        return self.clay

    def get_wood(self):
        return self.wood

    def get_wool(self):
        return self.wool

    # adders #####
    def add_cereal(self, amount):
        self.cereal = self.get_cereal() + amount
        return None

    def add_mineral(self, amount):
        self.mineral = self.get_mineral() + amount
        return None

    def add_clay(self, amount):
        self.clay = self.get_clay() + amount
        return None

    def add_wood(self, amount):
        self.wood = self.get_wood() + amount
        return None

    def add_wool(self, amount):
        self.wool = self.get_wool() + amount
        return None

    def has_this_more_materials(self, materials):
        """
        Si le llega otra clase Materials() comprobará si hay más o igual materiales que los que hay en el parámetro y
        si le llega un string con lo que se quiere construir comprobará si tiene suficiente material para hacerlo.
        :param materials: (str o Materials()) Nombre de lo que se quiere construir o materiales.
        :return: bool
        """
        if isinstance(materials, str):
            if materials == 'town':
                materials = Materials(1, 0, 1, 1, 1)
            elif materials == 'city':
                materials = Materials(2, 3, 0, 0, 0)
            elif materials == 'road':
                materials = Materials(0, 0, 1, 1, 0)
            elif materials == 'card':
                materials = Materials(1, 1, 0, 0, 1)
            else:
                return False

        if isinstance(materials, Materials):
            if self.cereal < materials.cereal or self.mineral < materials.mineral or self.clay < materials.clay or \
               self.wood < materials.wood or self.wool < materials.wool:

                return False

            return True
        else:
            return False

    def __str__(self):
        return 'Materials( Cereal: ' + str(self.cereal) + ', Mineral:' + str(self.mineral) + ', Clay:' + str(
            self.clay) + ', Wood:' + str(self.wood) + ', Wool:' + str(self.wool) + ' )'

    def __to_object__(self):
        return {'cereal': str(self.cereal), 'mineral': str(self.mineral), 'clay': str(self.clay),
                'wood': str(self.wood), 'wool': str(self.wool)}

    def __repr__(self):
        return 'Materials()'
