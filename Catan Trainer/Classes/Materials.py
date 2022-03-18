class Materials:
    """
    Clase que representa los materiales. Se usa tanto en la mano de los jugadores como en las ofertas
    """
    # Variables
    cereal = 0
    mineral = 0
    clay = 0
    wood = 0
    wool = 0
    array_ids = [cereal, mineral, clay, wood, wool]

    def __init__(self, cereal=0, mineral=0, clay=0, wood=0, wool=0):
        self.cereal = cereal
        self.mineral = mineral
        self.clay = clay
        self.wood = wood
        self.wool = wool
        # self.array_ids = [cereal, mineral, clay, wood, wool]
        return

    def get_from_id(self, material_constant):
        self.array_ids = [self.cereal, self.mineral, self.clay, self.wood, self.wool]
        return self.array_ids[material_constant]

    ##### getters #####
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

    ##### setters #####
    def set_cereal(self, amount=0):
        self.cereal = amount
        return None

    def set_mineral(self, amount=0):
        self.mineral = amount
        return None

    def set_clay(self, amount=0):
        self.clay = amount
        return None

    def set_wood(self, amount=0):
        self.wood = amount
        return None

    def set_wool(self, amount=0):
        self.wool = amount
        return None

    ##### adders #####
    def add_cereal(self, amount=0):
        cereal = self.get_cereal() + amount
        self.set_cereal(cereal)
        return None

    def add_mineral(self, amount=0):
        mineral = self.get_mineral() + amount
        self.set_mineral(mineral)
        return None

    def add_clay(self, amount=0):
        clay = self.get_clay() + amount
        self.set_clay(clay)
        return None

    def add_wood(self, amount=0):
        wood = self.get_wood() + amount
        self.set_wood(wood)
        return None

    def add_wool(self, amount=0):
        wool = self.get_wool() + amount
        self.set_wool(wool)
        return None

    def has_this_more_materials(self, materials):
        """
        Le llega otra clase materiales y compara si esta clase tiene materiales suficientes
        :param materials:
        :return:
        """
        if self.wood < materials.wood:
            print('Menos madera de la que piden')
            return False
        if self.wool < materials.wool:
            print('Menos lana de la que piden')
            return False
        if self.clay < materials.clay:
            print('Menos arcilla de la que piden')
            return False
        if self.mineral < materials.mineral:
            print('Menos mineral del que piden')
            return False
        if self.cereal < materials.cereal:
            print('Menos cereal del que piden')
            return False
        return True

    def __str__(self):
        return 'Materials( Cereal: ' + str(self.cereal) + ', Mineral:' + str(self.mineral) + ', Clay:' + str(
            self.clay) + ', Wood:' + str(self.wood) + ', Wool:' + str(self.wool) + ' )'

    def __repr__(self):
        return 'Materials()'
